#!/usr/bin/env python3
"""
pjecalc_pdf_parser.py — Parser do PDF do PJE-Calc Cidadao (CSJT/CNJ).

Le PDF gerado pelo PJE-Calc Cidadao (qualquer versao 2.x.x) e retorna
dict Python estruturado com:

- metadata: numero do processo, calculo, partes, periodo, versao
- resumo: lista de verbas + totais (bruto, juros, geral)
- criterios: indices aplicados + sumulas + aliquotas + marco juros
- auditoria: checks automaticos (ADC 58/59, Sum. 368 TST, IRPF, etc)

USO MANUAL:
    python3 pjecalc_pdf_parser.py <pdf_path>

INTEGRACAO:
    A skill `parser-auditor-pjecalc` aciona este script via subprocess
    e consome o stdout (JSON dumpado).

DEPENDENCIAS (em ordem de preferencia):
    1. pdfplumber (pip install pdfplumber) — mais robusto pra tabelas
    2. PyPDF2 (pip install PyPDF2) — fallback
    3. pdftotext (poppler-utils — CLI) — fallback final

Se nenhuma das tres estiver disponivel, instrui o usuario a instalar
pdfplumber.

PROIBICOES:
- Nao chama API externa em runtime
- Nao modifica o PDF original
- Nao assume layout — sempre confere antes de extrair
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# EXTRACAO DE TEXTO — 3 estrategias com fallback
# ---------------------------------------------------------------------------


def _extract_text_pdfplumber(pdf_path: str) -> str | None:
    """Tenta extrair texto via pdfplumber (preferido pra tabelas)."""
    try:
        import pdfplumber  # type: ignore
    except ImportError:
        return None
    try:
        paginas: list[str] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                txt = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
                paginas.append(txt)
        return "\n\n--- PAGINA ---\n\n".join(paginas)
    except Exception as exc:  # pragma: no cover
        print(f"[parser] pdfplumber falhou: {exc}", file=sys.stderr)
        return None


def _extract_text_pypdf2(pdf_path: str) -> str | None:
    """Fallback via PyPDF2."""
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except ImportError:
        try:
            from pypdf import PdfReader  # type: ignore
        except ImportError:
            return None
    try:
        reader = PdfReader(pdf_path)
        paginas = [page.extract_text() or "" for page in reader.pages]
        return "\n\n--- PAGINA ---\n\n".join(paginas)
    except Exception as exc:  # pragma: no cover
        print(f"[parser] PyPDF2 falhou: {exc}", file=sys.stderr)
        return None


def _extract_text_pdftotext_cli(pdf_path: str) -> str | None:
    """Fallback final via CLI pdftotext (poppler-utils)."""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:  # pragma: no cover
        print(f"[parser] pdftotext CLI falhou: {exc}", file=sys.stderr)
    return None


def extract_text(pdf_path: str) -> tuple[str, str]:
    """
    Tenta extrair texto do PDF usando 3 estrategias em ordem.

    Retorna: (texto_extraido, metodo_utilizado).
    Levanta RuntimeError se nenhuma das 3 funcionar.
    """
    pdf = Path(pdf_path)
    if not pdf.exists():
        raise FileNotFoundError(f"PDF nao encontrado: {pdf_path}")

    for metodo, fn in (
        ("pdfplumber", _extract_text_pdfplumber),
        ("PyPDF2/pypdf", _extract_text_pypdf2),
        ("pdftotext-cli", _extract_text_pdftotext_cli),
    ):
        txt = fn(pdf_path)
        if txt and len(txt.strip()) > 50:
            return txt, metodo

    raise RuntimeError(
        "Nenhuma estrategia de extracao funcionou. Instale uma das opcoes:\n"
        "  - pip install pdfplumber (RECOMENDADO)\n"
        "  - pip install pypdf\n"
        "  - brew install poppler  (ou apt install poppler-utils)"
    )


# ---------------------------------------------------------------------------
# REGEX — captura metadata + criterios
# ---------------------------------------------------------------------------


RE_PROCESSO = re.compile(
    r"Processo\s*[:n°ºNn]*\s*([\d.\-]+(?:[.\-]\d+){2,})", re.IGNORECASE
)
RE_CALCULO_NRO = re.compile(r"C[aá]lculo\s*[:nN°º]*\s*(\d+)", re.IGNORECASE)
RE_RECLAMANTE = re.compile(r"Reclamante[:\s]+(.+?)(?:\n|Reclamado)", re.IGNORECASE | re.DOTALL)
RE_RECLAMADO = re.compile(r"Reclamado[:\s]+(.+?)(?:\n|Per[ií]odo|Data)", re.IGNORECASE | re.DOTALL)
RE_PERIODO = re.compile(
    r"Per[ií]odo[^:]*:?\s*(\d{2}/\d{2}/\d{4})\s*(?:a|at[eé]|-)\s*(\d{2}/\d{2}/\d{4})",
    re.IGNORECASE,
)
RE_DATA_AJUIZ = re.compile(
    r"(?:Data\s+(?:do\s+)?ajuizamento|Ajuizamento)[:\s]+(\d{2}/\d{2}/\d{4})",
    re.IGNORECASE,
)
RE_DATA_LIQ = re.compile(
    r"(?:Data\s+(?:da\s+)?liquida[cç][aã]o|Liquida[cç][aã]o)[:\s]+(\d{2}/\d{2}/\d{4})",
    re.IGNORECASE,
)
RE_VERSAO_PJE = re.compile(r"vers[aã]o\s*(?:do\s+)?PJE[\s-]?Calc[:\s]*(\d+\.\d+\.\d+)", re.IGNORECASE)

# Verbas e valores — captura linha tipo "ADICIONAL DE INSALUBRIDADE 20%   6.757,70   279,37   7.037,07"
RE_VERBA_LINHA = re.compile(
    r"^([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9 \-/%º°ª.]+?)\s+"
    r"([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s*$",
    re.MULTILINE,
)

# Total geral
RE_TOTAL = re.compile(
    r"TOTAL\s*(?:GERAL|DA\s+LIQUIDA[CÇ][AÃ]O)?[:\s]+(?:R\$\s*)?([\d.,]+)",
    re.IGNORECASE,
)

# Criterios — indices e marcos
RE_IPCA_E = re.compile(r"IPCA[\s\-]?E\s+at[eé]\s+(\d{2}/\d{2}/\d{4})", re.IGNORECASE)
RE_SELIC_APOS = re.compile(
    r"Selic\s+a\s+partir\s+de\s+(\d{2}/\d{2}/\d{4})", re.IGNORECASE
)
RE_SUMULA = re.compile(r"S[uú]mula\s+(\d+)\s+(?:do\s+)?(TST|STJ|STF)", re.IGNORECASE)
RE_ALIQ_INSS = re.compile(
    r"al[ií]quota\s+INSS\s+(?:empresa)?[:\s]+(\d+(?:[,.]\d+)?)\s*%", re.IGNORECASE
)
RE_LEI_14905 = re.compile(r"Lei\s+14\.905\s*/?\s*2024", re.IGNORECASE)
RE_CC_406 = re.compile(r"(?:CC|C[oó]digo\s+Civil)\s+406", re.IGNORECASE)


# ---------------------------------------------------------------------------
# PARSE PRINCIPAL
# ---------------------------------------------------------------------------


def _br_to_float(valor_str: str) -> float:
    """Converte '6.757,70' (BR) em 6757.70 (float)."""
    clean = valor_str.strip().replace(".", "").replace(",", ".")
    try:
        return float(clean)
    except ValueError:
        return 0.0


def parse_metadata(texto: str) -> dict[str, Any]:
    """Extrai metadata do PDF."""

    def _grupo_seguro(regex: re.Pattern[str], default: str = "") -> str:
        m = regex.search(texto)
        return m.group(1).strip() if m else default

    processo = _grupo_seguro(RE_PROCESSO)
    calculo_nro = _grupo_seguro(RE_CALCULO_NRO)

    reclamante_match = RE_RECLAMANTE.search(texto)
    reclamante = reclamante_match.group(1).strip()[:200] if reclamante_match else ""

    reclamado_match = RE_RECLAMADO.search(texto)
    reclamado = reclamado_match.group(1).strip()[:200] if reclamado_match else ""

    periodo_match = RE_PERIODO.search(texto)
    periodo_calculo = (
        f"{periodo_match.group(1)} a {periodo_match.group(2)}" if periodo_match else ""
    )

    return {
        "processo": processo,
        "calculo_nro": calculo_nro,
        "reclamante": reclamante,
        "reclamado": reclamado,
        "periodo_calculo": periodo_calculo,
        "data_ajuizamento": _grupo_seguro(RE_DATA_AJUIZ),
        "data_liquidacao": _grupo_seguro(RE_DATA_LIQ),
        "versao_pjecalc": _grupo_seguro(RE_VERSAO_PJE),
    }


def parse_resumo(texto: str) -> dict[str, Any]:
    """Extrai verbas e totais."""
    verbas: list[dict[str, Any]] = []
    seen_keys: set[str] = set()

    # Procurar bloco "Resumo do Calculo" para limitar contexto
    bloco_resumo = texto
    idx_resumo = re.search(r"Resumo\s+do\s+C[aá]lculo", texto, re.IGNORECASE)
    if idx_resumo:
        bloco_resumo = texto[idx_resumo.start() :]

    for match in RE_VERBA_LINHA.finditer(bloco_resumo):
        nome = match.group(1).strip()
        valor_corr = _br_to_float(match.group(2))
        juros = _br_to_float(match.group(3))
        total = _br_to_float(match.group(4))

        # Filtros para reduzir falso positivo
        if len(nome) < 3 or "PAGINA" in nome:
            continue
        # Skip linha "TOTAL"
        if re.match(r"^TOTAL\b", nome, re.IGNORECASE):
            continue
        # Dedupe por chave nome+valor
        key = f"{nome}|{valor_corr}"
        if key in seen_keys:
            continue
        seen_keys.add(key)

        verbas.append(
            {
                "nome": nome,
                "valor_corrigido": valor_corr,
                "juros": juros,
                "total": total,
            }
        )

    total_bruto = sum(v["valor_corrigido"] for v in verbas)
    total_juros = sum(v["juros"] for v in verbas)

    # Tentar pegar TOTAL GERAL do texto
    total_geral_explicito = 0.0
    m = RE_TOTAL.search(texto)
    if m:
        total_geral_explicito = _br_to_float(m.group(1))

    return {
        "verbas": verbas,
        "total_bruto": round(total_bruto, 2),
        "total_juros": round(total_juros, 2),
        "total_geral": total_geral_explicito or round(total_bruto + total_juros, 2),
    }


def parse_criterios(texto: str) -> dict[str, Any]:
    """Extrai criterios do calculo."""
    criterios: dict[str, Any] = {}

    m_ipca = RE_IPCA_E.search(texto)
    if m_ipca:
        criterios["indice_correcao_pre"] = f"IPCA-E ate {m_ipca.group(1)}"

    m_selic = RE_SELIC_APOS.search(texto)
    if m_selic:
        criterios["indice_correcao_pos"] = f"Selic a partir de {m_selic.group(1)}"
        criterios["juros_taxa_legal_inicio"] = m_selic.group(1)

    sumulas_encontradas = RE_SUMULA.findall(texto)
    if sumulas_encontradas:
        criterios["sumula_aplicada"] = ", ".join(
            f"Sumula {num} {trib.upper()}" for num, trib in sumulas_encontradas[:5]
        )

    m_aliq = RE_ALIQ_INSS.search(texto)
    if m_aliq:
        criterios["aliquota_inss_empresa"] = _br_to_float(m_aliq.group(1)) / 100

    if RE_LEI_14905.search(texto) and RE_CC_406.search(texto):
        criterios["fundamento_juros_pos_2024"] = (
            "CC 406 paragrafo unico (Lei 14.905/2024)"
        )

    return criterios


def auditar(
    metadata: dict[str, Any],
    resumo: dict[str, Any],
    criterios: dict[str, Any],
    texto: str,
) -> dict[str, Any]:
    """Aplica checks de auditoria automatica."""
    checks: list[dict[str, str]] = []
    alertas: list[dict[str, str]] = []

    # Check 1 — ADC 58/59 STF aplicada
    if criterios.get("indice_correcao_pre") and criterios.get("indice_correcao_pos"):
        checks.append(
            {
                "item": "ADC 58/59 STF aplicada (IPCA-E ate ajuizamento + Selic apos)",
                "status": "OK",
            }
        )
    else:
        alertas.append(
            {
                "item": "ADC 58/59 STF — indices pre/pos NAO foram detectados explicitamente",
                "status": "ALERTA",
                "recomendacao": "Confirmar manualmente no laudo do calculo",
            }
        )

    # Check 2 — Sumula 368 TST
    if "368" in (criterios.get("sumula_aplicada") or ""):
        checks.append(
            {
                "item": "Sumula 368 TST itens IV/V (contribuicao social)",
                "status": "OK",
            }
        )
    else:
        alertas.append(
            {
                "item": "Sumula 368 TST itens IV/V NAO mencionada explicitamente",
                "status": "ALERTA",
                "recomendacao": "Confirmar se INSS empregado deduzido antes dos juros",
            }
        )

    # Check 3 — IRPF tabela progressiva acumulada
    irpf_acum_padroes = [
        r"IRPF.*tabela\s+progressiva\s+acumulada",
        r"Lei\s+7\.?713",
        r"art\.?\s*12-A",
    ]
    if any(re.search(p, texto, re.IGNORECASE) for p in irpf_acum_padroes):
        checks.append(
            {
                "item": "IRPF tabela progressiva acumulada (Lei 7.713/88 art. 12-A)",
                "status": "OK",
            }
        )
    else:
        alertas.append(
            {
                "item": "IRPF — nao foi detectada aplicacao explicita do regime de competencia (Lei 7.713/88 art. 12-A)",
                "status": "ALERTA",
                "recomendacao": "Confirmar se IRPF aplicado pela tabela acumulada e nao mes a mes",
            }
        )

    # Check 4 — Juros apos deducao INSS
    if criterios.get("fundamento_juros_pos_2024"):
        checks.append(
            {
                "item": "Fundamento dos juros pos 2024-08-30 (Lei 14.905/CC 406 par. unico)",
                "status": "OK",
            }
        )

    # Check 5 — Aliquota INSS empresarial
    aliq = criterios.get("aliquota_inss_empresa")
    if aliq is not None:
        if abs(aliq - 0.20) < 0.001:
            checks.append(
                {
                    "item": "Aliquota INSS empresa (20% padrao)",
                    "status": "OK",
                }
            )
        else:
            alertas.append(
                {
                    "item": f"Aliquota INSS divergente do padrao (lida: {aliq * 100:.2f}%)",
                    "status": "ALERTA",
                    "recomendacao": "Confirmar fundamentacao (entidade beneficente, MEI, etc)",
                }
            )

    # Check 6 — Aritmetica
    if resumo["verbas"]:
        soma_calc = round(resumo["total_bruto"] + resumo["total_juros"], 2)
        diff = abs(soma_calc - resumo["total_geral"])
        if diff < 1.0:
            checks.append(
                {
                    "item": "Aritmetica total bruto+juros == total geral (tolerancia R$ 1,00)",
                    "status": "OK",
                }
            )
        else:
            alertas.append(
                {
                    "item": f"Aritmetica divergente: soma das verbas R$ {soma_calc:.2f} vs total geral lido R$ {resumo['total_geral']:.2f} (diff R$ {diff:.2f})",
                    "status": "ALERTA",
                    "recomendacao": "Conferir manualmente — possivel verba nao parseada ou linha de total mal lida",
                }
            )

    return {
        "checks": checks,
        "alertas": alertas,
        "total_checks_ok": len(checks),
        "total_alertas": len(alertas),
    }


def parse_pjecalc_pdf(pdf_path: str) -> dict[str, Any]:
    """
    Le PDF gerado pelo PJE-Calc Cidadao (versao 2.x.x).

    Retorna dict estruturado com metadata, resumo, criterios e auditoria.
    Em caso de layout nao reconhecido, devolve dump de texto bruto +
    aviso para validacao manual.
    """
    try:
        texto, metodo = extract_text(pdf_path)
    except (FileNotFoundError, RuntimeError) as exc:
        return {
            "ok": False,
            "erro": str(exc),
            "metadata": {},
            "resumo": {"verbas": [], "total_geral": 0},
            "criterios": {},
            "auditoria": {"checks": [], "alertas": [{"item": str(exc)}]},
        }

    metadata = parse_metadata(texto)
    resumo = parse_resumo(texto)
    criterios = parse_criterios(texto)

    # Fallback gracioso: layout nao reconhecido
    layout_ok = bool(metadata.get("processo") or resumo.get("verbas"))
    if not layout_ok:
        return {
            "ok": False,
            "metodo_extracao": metodo,
            "aviso": (
                "Layout do PDF nao reconhecido — pode ser versao do PJE-Calc "
                "diferente da esperada (2.x.x), ou PDF escaneado sem OCR. "
                "Veja texto bruto abaixo para validacao manual."
            ),
            "metadata": metadata,
            "resumo": resumo,
            "criterios": criterios,
            "auditoria": {"checks": [], "alertas": []},
            "texto_bruto_amostra": texto[:3000],
        }

    auditoria = auditar(metadata, resumo, criterios, texto)

    return {
        "ok": True,
        "metodo_extracao": metodo,
        "metadata": metadata,
        "resumo": resumo,
        "criterios": criterios,
        "auditoria": auditoria,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _main() -> int:
    if len(sys.argv) < 2:
        print(
            "USO: python3 pjecalc_pdf_parser.py <pdf_path>\n\n"
            "Exemplo: python3 pjecalc_pdf_parser.py ~/Desktop/calculo-pjecalc.pdf",
            file=sys.stderr,
        )
        return 2

    pdf_path = sys.argv[1]
    resultado = parse_pjecalc_pdf(pdf_path)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0 if resultado.get("ok") else 1


if __name__ == "__main__":
    sys.exit(_main())
