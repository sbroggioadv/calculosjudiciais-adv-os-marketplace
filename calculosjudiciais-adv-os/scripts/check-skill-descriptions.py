#!/usr/bin/env python3
"""
check-skill-descriptions.py — Validacao pre-release para Claude Cowork.

Verifica DOIS limites hard descobertos via decompile do app.asar do Cowork:

1. **Description <= 1024 chars** (validacao client-side + schema do banco):
   if (description.length > 1024) throw new Error("Description too long (max 1024)");
   description: ht("description", { length: 1024 }).notNull()

2. **NAO colidir nomes de skill** com plugin pai (constraint UNIQUE no banco):
   uniqUserName: unique(userId + name)
   Se duas skills tiverem o mesmo `name` no mesmo userId, a SEGUNDA e
   silenciosamente rejeitada pelo backend do Cowork.

USO:
  python3 scripts/check-skill-descriptions.py

EXIT:
  0 = todos os checks passam
  1 = alguma falha (build/release deve falhar)
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

LIMIT_HARD = 1024  # limite real do Cowork (description)
LIMIT_WARN = 1000  # margem de seguranca recomendada (description)

# Limite empirico do tamanho do arquivo SKILL.md observado nos testes:
# - bissect-B (max 10.557 bytes) PASSOU
# - alpha.1/2/3 (master 17.856 / onboarding 12.410) FALHARAM
# Limite real fica entre ~10.6 KB e ~12 KB.
# Margem de seguranca operacional: 11.000 bytes (~10.7 KB)
SKILL_FILE_SIZE_HARD = 11_000
SKILL_FILE_SIZE_WARN = 10_500

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"

# Skills de outros plugins da familia Adv-OS ja publicados pelo mesmo operador
# no Cowork — colidir com qualquer uma faz o backend rejeitar silenciosamente o
# upload (constraint UNIQUE userId+name). Todas as skills do plugin trabalhista
# usam sufixo de dominio (-trabalhista/-trabalhistas) para nao colidir.
PLUGIN_PAI_SKILLS = {
    # Plugin pai (Mentoria) — nomes neutros
    "analise-trilateral", "calculo-juridico", "compliance-lgpd",
    "comunicacao-cliente", "contrarrazoes-recursais",
    "contrato-social-holding", "contratos-societarios",
    "cowork-onboarding", "cowork-sync", "documentos-extrajudiciais",
    "due-diligence", "escritorio-advocacia", "estrategia-de-caso",
    "financeiro-juridico", "firm-master", "jurisprudencia-estrategica",
    "marketing-juridico", "memory-evolver", "minutas-contratuais",
    "parecer-juridico", "pecas-processuais", "peticao-universal",
    "replica-estrategica", "resumo-audiencia", "suprema-corte-r1-coleta",
    "suprema-corte-r2-base-juridica", "suprema-corte-r3-tese",
    "suprema-corte-r4-completude", "visual-law",
    # Plugin previdenciario irmao
    "previdenciario-master", "previdenciario-onboarding",
    "suprema-corte-previdenciaria",
}


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"ERRO: pasta skills nao encontrada em {SKILLS_DIR}", file=sys.stderr)
        return 2

    bad: list[tuple[str, int]] = []
    warn: list[tuple[str, int]] = []
    ok_count = 0
    collisions: list[str] = []
    file_too_big: list[tuple[str, int]] = []
    file_warn: list[tuple[str, int]] = []

    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        # Ignorar pasta _archived (skills consolidadas e fora do plugin ativo)
        if "_archived" in str(skill_md):
            continue

        text = skill_md.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not m:
            print(f"WARN: SKILL.md sem frontmatter: {skill_md}", file=sys.stderr)
            continue

        fm = m.group(1)
        # Captura description (formato folded `>` ou block `|` ou inline)
        df = re.search(r"^description:\s*[>|]?\s*\n((?:[ \t].*\n?)+)", fm, re.MULTILINE)
        if not df:
            # Tentar inline: description: "..."
            inline = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
            if inline:
                desc = inline.group(1).strip().strip('"\'')
            else:
                continue
        else:
            desc = re.sub(r"\n[ \t]+", " ", df.group(1)).strip()

        n = len(desc)
        skill_name = skill_md.parent.name

        # Check 1: description <= 1024 chars
        if n > LIMIT_HARD:
            bad.append((skill_name, n))
        elif n > LIMIT_WARN:
            warn.append((skill_name, n))
        else:
            ok_count += 1

        # Check 2: nao colidir com skills do plugin pai
        if skill_name in PLUGIN_PAI_SKILLS:
            collisions.append(skill_name)

        # Check 3: tamanho do SKILL.md
        file_size = skill_md.stat().st_size
        if file_size > SKILL_FILE_SIZE_HARD:
            file_too_big.append((skill_name, file_size))
        elif file_size > SKILL_FILE_SIZE_WARN:
            file_warn.append((skill_name, file_size))

    print(f"[OK <{LIMIT_WARN}]:  {ok_count} skills")
    print(f"[WARN {LIMIT_WARN}-{LIMIT_HARD}]: {len(warn)} skills")
    for s, n in warn:
        print(f"  - {s}: {n} chars (margem apertada — considere reduzir)")

    print(f"[FAIL >{LIMIT_HARD}]: {len(bad)} skills")
    for s, n in bad:
        print(f"  - {s}: {n} chars (ESTOURA limite hard do Cowork)")

    print()
    print(f"[COLISAO com plugin pai]: {len(collisions)} skills")
    for s in collisions:
        print(f"  - {s} (rename obrigatorio — backend rejeita silenciosamente)")

    print()
    print(f"[FILE SIZE WARN {SKILL_FILE_SIZE_WARN}-{SKILL_FILE_SIZE_HARD}]: {len(file_warn)}")
    for s, n in file_warn:
        print(f"  - {s}: {n} bytes (margem apertada para Cowork)")
    print(f"[FILE SIZE FAIL >{SKILL_FILE_SIZE_HARD}]: {len(file_too_big)}")
    for s, n in file_too_big:
        print(f"  - {s}: {n} bytes (Cowork rejeita silenciosamente)")

    failed = False
    if bad:
        print()
        print(f"FALHA: descriptions estouram o limite hard do Cowork ({LIMIT_HARD} chars).")
        failed = True

    if collisions:
        print()
        print(f"FALHA: {len(collisions)} skill(s) colidem com nomes do plugin pai.")
        print("O backend do Cowork rejeita silenciosamente uploads com colisao UNIQUE.")
        print("Renomeie cada skill colidente (sugestao: adicionar sufixo do dominio).")
        failed = True

    if file_too_big:
        print()
        print(f"FALHA: {len(file_too_big)} skill(s) excedem {SKILL_FILE_SIZE_HARD} bytes.")
        print("Cowork rejeita silenciosamente SKILL.md acima de ~11KB.")
        print("Comprima a skill ou divida em multiplas skills menores.")
        failed = True

    if failed:
        return 1

    print()
    print(f"APROVADO: descriptions OK + sem colisoes + tamanhos OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
