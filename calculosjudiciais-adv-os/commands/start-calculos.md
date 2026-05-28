---
description: Inicia o wizard de configuracao do plugin calculosjudiciais — cria a pasta calculos/ com identidade do advogado, OAB, UF, tribunais que atua, areas de calculo e tom de voz.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [--update para reconfigurar]
---

Voce foi acionado pelo comando `/start-calculos` do plugin Calculosjudiciais-Adv-OS.

Argumento recebido: `$ARGUMENTS`

**Objetivo:** configurar o plugin de calculos no ambiente do operador.

## PROTOCOLO

1. **Acionar a skill `calculos-onboarding`** imediatamente — ela conduz o wizard completo.
2. O wizard cria `<cwd>/calculos/` com:
   - `persona.md` — identidade do advogado (nome, OAB, UF, escritorio, tom de voz)
   - `config.md` — tribunais que atua, areas de calculo (civel/trab/trib/prev/fam/crim/cons), modo de fluxo
   - `cowork-state.json` — estado canonico do workspace
   - `<cwd>/.claude/settings.local.json` — aponta `CALCULOS_PERSONA` para o arquivo gerado
3. Se ja existir `calculos/cowork-state.json`, a skill oferece **continuar / atualizar / recriar** (idempotencia).
4. Se o argumento for `--update`, ir direto para o fluxo de atualizacao (sem perguntar tudo de novo).

**Atencao LGPD:** a skill avisa se o diretorio estiver em pasta sincronizada (iCloud/OneDrive/Dropbox/Drive) — dados de calculos contem valores e CPF/CNPJ; pasta sincronizada e risco de vazamento.

**Skill a acionar:** `calculos-onboarding`.
