---
name: parser-auditor-pjecalc
description: >
  PARSER-AUDITOR-PJECALC — Killer feature do plugin. Le PDF do PJE-Calc
  Cidadao (qualquer versao 2.x.x) via script Python local
  (scripts/parsers/pjecalc_pdf_parser.py) e devolve dois blocos: (1)
  resumo estruturado do calculo (metadata, verbas, totais, criterios) e
  (2) auditoria automatica com checks de conformidade legal — ADC 58/59
  STF, Lei 14.905/2024, Sumula 368 TST itens IV/V, IRPF Lei 7.713/88 art
  12-A, deducao de contribuicao social antes dos juros, conferencia de
  indices contra o cache local. Use SEMPRE que o usuario disser
  "auditar PJE-CALC", "PDF do PJE", "calculo do PJE-CALC esta certo",
  "PJE-CALC errado", "/auditar-pjecalc", anexar PDF do PJE-Calc ou
  passar caminho de arquivo PJE-Calc.
---

# PARSER-AUDITOR-PJECALC — Auditor Automatico do PJE-Calc Cidadao

## 1. ESCOPO

Killer feature. PJE-Calc Cidadao e gerador oficial CSJT/CNJ pra
liquidacao trabalhista — seus PDFs chegam da contadoria ou da parte
adversa. Esta skill:

1. **Le** o PDF (caminho local) via parser Python local
2. **Estrutura** metadata + resumo de verbas + criterios aplicados
3. **Audita** matematica e fundamentacao contra checklist canonico
4. **Quantifica** divergencias (R$ a mais / a menos)
5. **Entrega** memoria pronta pra impugnacao (CLT 879 § 2º — 8 dias)

NAO substitui contadoria — substitui o tempo do advogado conferindo
planilha pagina por pagina.

## 2. INPUT NECESSARIO

| Campo | Obrigatorio | Observacoes |
|---|---|---|
| `pdf_path` | sim | Caminho absoluto do PDF (PJE-Calc Cidadao 2.x.x) |
| `parametros_sentenca` | desejavel | Para auditoria comparativa: indice de correcao, marco juros, periodo, verbas deferidas |
| `polo_cliente` | desejavel | reclamante \| reclamado — molda o framing do output |
| `calculo_referencia_path` | opcional | Outro PDF/texto pra auto-disparar `comparador-calculos` |

Se faltar `parametros_sentenca`, ainda assim audita os checks
estruturais (ADC 58/59, Sum. 368 TST, IRPF, juros pos-deducao
INSS) — sao independentes da sentenca.

## 3. PROCESSAMENTO

### Passo 1 — Execucao do parser Python

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parsers/pjecalc_pdf_parser.py <pdf_path>
```

O parser:
- Tenta `pdfplumber` (mais robusto pra tabelas)
- Fallback `PyPDF2`
- Fallback final `pdftotext` (poppler CLI)
- Se nenhuma das tres disponivel → instrui usuario a `pip install pdfplumber`
- Retorna dict Python (a skill consome via stdout/print do JSON dumpado)

### Passo 2 — Validacao do parse

- Se `metadata.processo` ausente → layout nao reconhecido,
  exibe texto bruto + aviso
- Se `resumo.verbas` vazia → tabela "Resumo do Calculo" nao
  encontrada, exibe pagina 3-5 pra checagem manual
- Se `criterios` vazio → suspeita versao antiga do PJE-Calc;
  prossegue com auditoria parcial

### Passo 3 — Auditoria automatica (checklist canonico)

#### Check 1 — ADC 58/59 STF + Lei 14.905/2024 (correcao + juros)
- Se `criterios.indice_correcao_pre` mencionar **IPCA-E ate
  ajuizamento** → OK
- Se `criterios.indice_correcao_pos` mencionar **Selic a partir
  do ajuizamento** ATE 29/08/2024 → OK
- Se ha verba com periodo posterior a 30/08/2024 e `criterios.
  fundamento_juros_pos_2024` NAO menciona CC 406 paragrafo unico
  (Lei 14.905/2024) → 🔴 ALERTA
- Se calculo aplicar TR ou taxa antiga → 🔴 ALERTA grave

#### Check 2 — Sumula 368 TST itens IV/V (contribuicao social)
- Contribuicao previdenciaria deduzida ANTES dos juros → OK
- Contribuicao deduzida DEPOIS dos juros → 🔴 ALERTA
  (sobrevaloriza juros, prejudica reclamado)
- Sem deducao de previdenciaria do empregado → 🔴 ALERTA

#### Check 3 — IRPF (Lei 7.713/88 art. 12-A + IN RFB 1500)
- IRPF aplicado pela **tabela progressiva acumulada** (regime
  de competencia) e nao mes a mes → OK
- IRPF aplicado mes-a-mes (regime de caixa) sobre verbas em
  atraso → 🔴 ALERTA (Sum. 368 TST item II + REsp 1118429
  rito repetitivo)

#### Check 4 — Juros pos-deducao de contribuicao social
- Base de juros calculada APOS deducao da contribuicao
  previdenciaria do empregado → OK
- Juros sobre valor BRUTO antes da deducao → 🔴 ALERTA

#### Check 5 — Indices conferem com cache local
- Pegar todos os indices de correcao mencionados no calculo
- Cruzar com `scripts/data/indices/<indice>-mensal.json`
- Se valor utilizado fora do range_final da tabela → 🟡 AVISO
  (precisa validar via url_oficial)
- Se valor utilizado divergir em mais de 0.05 percentual do
  cache → 🔴 ALERTA (provavel digitacao errada)

#### Check 6 — Marco intertemporal de juros (se aplicavel)
- Verbas pre-Reforma Trabalhista (anterior a 11/11/2017) →
  juros 1% am simples (CLT 39 §1º) ate 10/11/2017, depois
  Selic
- Verbas pos-Reforma → Selic desde sempre

#### Check 7 — Aliquota INSS empresarial
- Confirmar `criterios.aliquota_inss_empresa` = 0.20 (default)
- Se especial (entidade beneficente, MEI, etc) → exigir
  fundamentacao

#### Check 8 — Total bruto vs Total geral
- Conferencia aritmetica: `sum(verbas.valor_corrigido) +
  sum(verbas.juros)` == `resumo.total_geral` (tolerancia
  R$ 1,00 por arredondamento)

### Passo 4 — Quantificar divergencias

Para cada 🔴 ALERTA, estimar **gap em R$** comparado ao calculo
correto. Ex: "Juros calculados sobre bruto invez de pos-INSS
infla resultado em ~ R$ 1.247,33 a maior contra o reclamado."

### Passo 5 — Sugestao de proximos passos

- Se 0 alertas → 🟢 calculo aceitavel, prazo de impugnacao
  apenas formal
- Se 1-2 alertas pontuais → 🟡 impugnar topicos especificos
- Se 3+ alertas estruturais → 🔴 impugnacao completa + pedido
  de novos calculos

## 4. OUTPUT

```markdown
## 📊 Auditoria PJE-Calc — Processo {{numero}}

**Calculo nº:** [786]
**Versao PJE-Calc detectada:** [2.13.2]
**Reclamante:** [...]
**Reclamado:** [...]
**Periodo:** [06/01/2020 a 28/07/2022]
**Data liquidacao:** [31/05/2025]
**Polo cliente:** [{{POLO}}]

### Resumo do Calculo

| Verba | Valor Corrigido | Juros | Total |
|---|---:|---:|---:|
| ADICIONAL DE INSALUBRIDADE 20% | R$ 6.757,70 | R$ 279,37 | R$ 7.037,07 |
| ... | ... | ... | ... |
| **TOTAL GERAL** | **R$ ...** | **R$ ...** | **R$ ...** |

### Criterios Aplicados

| Item | Valor |
|---|---|
| Indice correcao pre-ajuizamento | IPCA-E ate 29/01/2024 |
| Indice correcao pos-ajuizamento | Selic a partir de 30/01/2024 |
| Sumula aplicada | Sumula 381 TST |
| Aliquota INSS empresa | 20% |
| Marco juros pos Lei 14.905 | 30/01/2024 |
| Fundamento juros pos-2024 | CC 406 paragrafo unico (Lei 14.905/2024) |

### ✅ Checklist de Auditoria

| # | Check | Status | Observacao |
|---|---|---|---|
| 1 | ADC 58/59 STF aplicada corretamente | 🟢 OK | IPCA-E + Selic pos ajuizamento |
| 2 | Sumula 368 TST itens IV/V (INSS) | 🟢 OK | Deducao antes dos juros |
| 3 | IRPF tabela progressiva acumulada | 🟢 OK | Lei 7.713/88 art 12-A |
| 4 | Juros sobre base pos-deducao INSS | 🟢 OK | |
| 5 | Indices conferem com cache local | 🟢 OK | Cruzado com selic-mensal.json |
| 6 | Marco intertemporal pre/pos-Reforma | 🟢 OK | |
| 7 | Aliquota INSS empresarial | 🟢 OK | 20% padrao |
| 8 | Aritmetica total bruto vs geral | 🟢 OK | Tolerancia respeitada |

### 🔴 Alertas Detectados

[lista de alertas, ou "Nenhum alerta — calculo aceitavel."]

### 💰 Impacto Financeiro Estimado das Divergencias

[ se ha alertas: tabela quantificando R$ a mais/a menos por alerta ]

### 📝 Sugestao de Proximo Passo

[🟢 aceitar / 🟡 impugnar topicos / 🔴 impugnar completo + novos calculos]

### Modelo de manifestacao (esqueleto)

```
EXMO. SR. DR. JUIZ DA ___ VARA DO TRABALHO DE [CIDADE/UF]

Processo: {{numero}}

[{{POLO}}], ja qualificado(a), vem, no prazo do art. 879 § 2º
da CLT (8 dias), MANIFESTAR-SE SOBRE OS CALCULOS DE LIQUIDACAO:

[premissas + alertas detectados acima + pedido de retificacao]
```

> ⚠️ **Validar contra fonte oficial antes de protocolar.** Esta
> auditoria automatizada nao substitui contadoria judicial nem
> revisao do advogado responsavel.
```

## 5. FUNDAMENTACAO LEGAL

- **CLT 879 e § 2º** — liquidacao + prazo 8 dias
- **CLT 39 § 1º** — juros legais 1% am (pre-Reforma)
- **CF 100** — precatorios
- **ADC 58 e 59 STF** (DJe 07/04/2020) — IPCA-E ate ajuizamento + Selic apos
- **Lei 14.905/2024** — Taxa Legal CC 406 (vigencia 30/08/2024)
- **Sumula 368 TST** itens II, IV e V — INSS + IRPF
- **Lei 7.713/88 art. 12-A** — IRPF acumulado em RRA
- **REsp 1.118.429/SP** (repetitivo) — competencia IRPF
- **CC 406 par. unico** (Lei 14.905) — Taxa Legal = Selic - IPCA
- **NBC PP 01 (CFC)** — base pericia contabil

## 6. AVISOS OBRIGATORIOS NO OUTPUT

1. ⚠️ Validar contra fonte oficial antes de protocolar
2. ⚠️ Auditoria automatizada nao substitui contadoria
3. ⚠️ Prazo CLT 879 § 2º — 8 dias corridos
4. ⚠️ Se polo cliente = reclamado, dobrar atencao em alertas
   que favorecem o reclamante (omissao de INSS, IRPF mes a mes)
5. ⚠️ Se polo cliente = reclamante, dobrar atencao em alertas
   que favorecem o reclamado (verbas faltantes, indice errado)

## 7. INTEGRACAO

- **Upstream:** `calculos-master`, `calculos-onboarding`
- **Downstream auto:** `comparador-calculos` (se ha 2º calculo),
  `gestao-prazo-impugnacao` (8 dias CLT), `protocolo-p4-calculos`
- **Cross-link:** `trabalhista-adv-os` (peca), `execucao-adv-os`
  (embargos), `ia-combativa-adv-os` (R1-R4), `juris-adv-os`

## 8. PROIBICOES

1. **Nunca** chamar API externa do PJE-CALC oficial em runtime
2. **Nunca** "lembrar" indice — sempre cruzar com cache local
3. **Nunca** apresentar valor final sem aviso de validacao
4. **Nunca** afirmar que calculo esta correto sem rodar TODOS
   os 8 checks
5. **Nunca** ignorar alerta porque parece pequeno — sempre
   quantificar gap em R$
6. **Nunca** modificar o PDF original
7. **Nunca** assumir versao do PJE-Calc sem confirmar
   `metadata.versao_pjecalc`
8. **Nunca** rodar parser sem `${CLAUDE_PLUGIN_ROOT}/scripts/
   parsers/pjecalc_pdf_parser.py` existente — abortar se faltar

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Comparar com calculo do reclamado/autor | `/comparar-calculos` | `calculosjudiciais-adv-os` (este) |
| Gerar peca de manifestacao | `/trabalhista manifestacao-calculos` | `trabalhista-adv-os` |
| Embargar execucao trabalhista | `/execucao embargos-execucao-trabalhista` | `execucao-adv-os` |
| Auditoria Suprema Corte R1-R4 da peca | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` |
| Validar Sumula 368 TST citada | `/juris validar "Sumula 368 TST"` | `juris-adv-os` |

> Se plugin nao instalado, copiar memoria de auditoria acima e
> usar manualmente.
