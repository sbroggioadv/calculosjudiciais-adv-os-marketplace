---
description: ⭐ Killer feature — audita PDF do PJE-Calc Cidadao da parte contraria/contadoria/perito. Identifica erros de indice, aliquota, ADC 58/59, Sumula 368 TST, IRPF acumulado. NUNCA gera so audita.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [caminho do PDF PJE-Calc + opcional: lado do cliente (autor/reu)]
---

Voce foi acionado pelo comando `/auditar-pjecalc` do plugin Calculosjudiciais-Adv-OS.

Argumento recebido: `$ARGUMENTS`

**Objetivo:** auditar um calculo gerado pelo PJE-Calc Cidadao (apresentado pela parte contraria, contadoria judicial ou perito) e identificar erros tecnicos que sustentam impugnacao.

## PROTOCOLO

### 1. Validar o input

- Verificar que o argumento contem caminho de PDF local valido
- Se nao houver caminho: pedir ao operador "Cole o caminho do PDF do PJE-Calc no argumento, ou anexe o arquivo via Read"
- Se PDF nao for legivel: avisar e oferecer fallback (operador cola texto manualmente)

### 2. Acionar a skill `parser-auditor-pjecalc` imediatamente

Use `Skill(skill="parser-auditor-pjecalc")` passando o caminho do PDF.

A skill ira:

1. Acionar `scripts/parsers/pjecalc_pdf_parser.py` (Python — `pdfplumber` primario, `PyPDF2`/`pdftotext` fallback)
2. Extrair metadata (processo, calculo nº, reclamante, reclamado, periodo, data ajuizamento, versao PJE-Calc)
3. Extrair resumo (verbas, valores corrigidos, juros, total)
4. Extrair criterios (indice de correcao pre/pos ajuizamento, sumula aplicada, aliquota INSS)
5. **Auditar** contra checklist:
   - ADC 58/59 STF aplicada corretamente? (IPCA-E ate ajuizamento + Selic apos)
   - Sumula 368 TST itens IV/V aplicada? (contribuicao social sobre verbas)
   - IRPF tabela progressiva acumulada (Lei 7.713/88 art. 12-A)?
   - Juros incidem APOS deducao da contribuicao social?
   - Indices conferem com tabela oficial (`scripts/data/indices/*.json`)?
   - Marco temporal Lei 14.905/2024 respeitado?

### 3. Output estruturado

Devolver markdown com 4 blocos:

```
## 📄 RESUMO DO CALCULO PJE-CALC
[metadata + total + verbas principais]

## 🔍 AUDITORIA TECNICA
[checklist com ✅ / ❌ / ⚠️ por item]

## 🚨 ERROS IDENTIFICADOS
[lista numerada com fundamentacao + impacto monetario estimado]

## 📝 BASE PARA IMPUGNACAO
[texto pronto para servir de minuta de impugnacao a contadoria]
```

### 4. Fallback gracioso

Se layout do PDF for diferente (PJE-Calc lancou versao nova):

- Avisar operador
- Dumpar texto bruto extraido
- Pedir que cole manualmente as verbas em formato yaml estruturado

### 5. Auto-chain

- Se o operador ja tem calculo proprio do mesmo caso: sugerir `/comparar-calculos`
- Apos auditoria: auto-disparar `protocolo-p4-calculos` (R1-R4)

## REGRAS DURAS

1. **NUNCA gerar** calculo proprio nesta skill — auditoria apenas.
2. **SEMPRE citar** a fonte legal de cada erro identificado (artigo, sumula, tema).
3. **NUNCA omitir** a versao do PJE-Calc no output (layout muda entre versoes).
4. **Aviso final obrigatorio:** "Auditoria tecnica — validar conclusoes contra autos do processo e tabela oficial do TRT antes de impugnar."

**Skill a acionar:** `parser-auditor-pjecalc`.
