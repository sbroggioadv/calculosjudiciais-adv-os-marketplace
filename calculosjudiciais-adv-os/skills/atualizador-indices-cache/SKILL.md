---
name: atualizador-indices-cache
description: >
  ATUALIZADOR-INDICES-CACHE — Atualiza um valor unico (R$) entre duas
  datas usando o cache local de indices oficiais. Aceita Selic, IPCA,
  IPCA-E, INPC, TR e Taxa Legal CC406 (pos Lei 14.905/2024). Consulta
  scripts/data/indices/<indice>-mensal.json. Se as datas estao
  DENTRO do range da tabela, devolve valor atualizado final + memoria
  de calculo. Se estao FORA, devolve formula explicita, link oficial
  da fonte (BCB/IBGE) e placeholder. NUNCA "lembra" indice — sempre
  consulta a tabela commitada. Use SEMPRE que o usuario disser
  "atualizar valor", "atualizar de X a Y", "quanto vale hoje",
  "indice acumulado", "Selic acumulada", "IPCA do periodo",
  "/atualizar-valor", "trazer a valor presente".
---

# ATUALIZADOR-INDICES-CACHE — Atualizacao por Indice Oficial

## 1. ESCOPO

Skill atomica de atualizacao monetaria. Recebe um VALOR + DATA INICIAL
+ DATA FINAL + INDICE e devolve o valor corrigido + memoria de calculo
+ rastreabilidade da fonte (data de extracao do indice, range valido,
url oficial).

E o cerne da filosofia ANTI-HALUCINACAO do plugin: indices vivem em
JSON commitado em `scripts/data/indices/`, e a skill NUNCA "lembra"
de memoria — sempre le do arquivo.

## 2. INPUT NECESSARIO

| Campo | Obrigatorio | Observacoes |
|---|---|---|
| `valor` | sim | Em R$, formato decimal (ex: 12500.00) |
| `data_inicial` | sim | YYYY-MM-DD ou YYYY-MM (mes/ano) |
| `data_final` | sim | YYYY-MM-DD ou YYYY-MM ou "hoje" |
| `indice` | sim | SELIC \| IPCA \| IPCA-E \| INPC \| TR \| TAXA_LEGAL_CC406 |
| `juros_complementar` | opcional | Se houver juros a adicionar (ex: 1% am, taxa contratual) |
| `pro_rata_die` | opcional | true = aplica fracao do mes; false = mes cheio |

## 3. PROCESSAMENTO

### Passo 1 — Validar indice e carregar tabela

```python
indice_map = {
    "SELIC": "scripts/data/indices/selic-mensal.json",
    "IPCA": "scripts/data/indices/ipca-mensal.json",
    "IPCA-E": "scripts/data/indices/ipca-e-mensal.json",
    "INPC": "scripts/data/indices/inpc-mensal.json",
    "TR": "scripts/data/indices/tr-mensal.json",
    "TAXA_LEGAL_CC406": "scripts/data/indices/taxa-legal-cc406.json",
}
```

Se indice nao mapeado → erro com lista de validos.

Carregar JSON. Validar `range_inicial` <= `data_inicial`
e `data_final` <= `range_final`.

### Passo 2 — Classificar cenario

| Cenario | Acao |
|---|---|
| Datas DENTRO do range | Calcular valor final |
| Datas PARCIALMENTE fora (final > range_final) | Calcular ate range_final + aviso de extensao manual |
| Datas TOTALMENTE fora | Formula + placeholder + url_oficial |
| Indice mensal em data com dia (ex: 2024-03-15) | Decisao: usar mes cheio do mes inicial OU pro_rata_die |

### Passo 3 — Aplicar formula do indice

#### SELIC (composta mensal)
```
fator_acumulado = produto((1 + selic_mes/100) for mes in periodo)
valor_atualizado = valor * fator_acumulado
```

#### IPCA / IPCA-E / INPC (variacao percentual composta)
```
fator_acumulado = produto((1 + indice_mes/100) for mes in periodo)
valor_atualizado = valor * fator_acumulado
```

#### TR (taxa referencial — geralmente baixa, composta)
```
fator_acumulado = produto((1 + tr_mes/100) for mes in periodo)
valor_atualizado = valor * fator_acumulado
```

#### TAXA_LEGAL_CC406 (pos Lei 14.905/2024)
```
# Selic acumulada menos IPCA acumulado do mesmo periodo (piso zero)
taxa_legal_mes = max(0, selic_mes - ipca_mes)
fator_acumulado = produto((1 + taxa_legal_mes/100) for mes in periodo)
```

Se `juros_complementar` informado:
```
juros_total = valor * taxa_juros_am * num_meses  # simples
# ou composto se especificado
valor_atualizado_final = valor_atualizado + juros_total
```

### Passo 4 — Montar memoria de calculo

Tabela mes a mes com valor de inicio, indice aplicado, valor de fim.

### Passo 5 — Rastreabilidade

Sempre incluir:
- `fonte`: do JSON
- `url_oficial`: do JSON
- `data_extracao`: do JSON (ex: "2026-05-28")
- `release_plugin`: do JSON (ex: "v0.1.0")
- `range_valido`: range_inicial / range_final do JSON
- ⚠️ Aviso: "Validar contra fonte oficial antes de protocolar"

## 4. OUTPUT

### Cenario A — Dentro do range

```markdown
## 💰 Atualizacao por Indice — {{INDICE}}

**Valor original:** R$ 12.500,00
**Data inicial:** 2024-03-15
**Data final:** 2026-04-30
**Indice aplicado:** SELIC mensal composta
**Periodo:** 25 meses + fracao

### Memoria de Calculo

| Mes | Valor inicio (R$) | Indice (%) | Valor fim (R$) |
|---|---:|---:|---:|
| 2024-03 (15 dias) | 12.500,00 | 0,44 (pro-rata) | 12.555,00 |
| 2024-04 | 12.555,00 | 0,89 | 12.666,74 |
| 2024-05 | 12.666,74 | 0,80 | 12.768,07 |
| ... | ... | ... | ... |
| 2026-04 | ... | 1,02 | **R$ 14.927,12** |

### Resultado Final

| Item | Valor |
|---|---:|
| Valor original | R$ 12.500,00 |
| Indice acumulado periodo | + 19,42% |
| Valor atualizado | **R$ 14.927,12** |

### Rastreabilidade

- **Indice:** SELIC mensal
- **Fonte:** Banco Central do Brasil
- **URL oficial:** https://www.bcb.gov.br/controleinflacao/historicotaxasjuros
- **Data extracao do cache:** 2026-05-28
- **Release plugin:** v0.1.0
- **Range valido do cache:** 2024-01 a 2026-04

> ⚠️ Validar contra fonte oficial antes de protocolar.
> Para datas posteriores a 2026-04 atualizar via release nova
> do plugin OU consultar diretamente a URL acima.
```

### Cenario B — Parcialmente fora do range

```markdown
## 💰 Atualizacao por Indice — {{INDICE}} (PARCIAL)

**Valor original:** R$ 12.500,00
**Data inicial:** 2024-03-15
**Data final solicitada:** 2026-08-31
**Data final calculada:** 2026-04-30 (limite do cache)

⚠️ **ATENCAO:** o cache local cobre ate 2026-04. Os 4 meses
restantes (2026-05 a 2026-08) precisam ser preenchidos
manualmente via URL oficial.

### Calculo parcial ate 2026-04
[memoria igual ao Cenario A]

### Periodo nao calculado (2026-05 a 2026-08)

| Mes | Indice (%) | Fonte |
|---|---|---|
| 2026-05 | __% | https://... (preencher) |
| 2026-06 | __% | https://... (preencher) |
| 2026-07 | __% | https://... (preencher) |
| 2026-08 | __% | https://... (preencher) |

**Formula a aplicar:** valor_em_2026-04 * (1 + indice_2026-05/100)
* (1 + indice_2026-06/100) * ... = valor_atualizado_final

> ⚠️ Validar contra fonte oficial antes de protocolar.
```

### Cenario C — Totalmente fora do range

```markdown
## ⚠️ Atualizacao por Indice — {{INDICE}} (FORA DO CACHE)

**Valor original:** R$ 12.500,00
**Data inicial:** 2019-05-20
**Data final:** 2023-11-15
**Range do cache:** 2024-01 a 2026-04 (NAO COBRE o periodo solicitado)

### Formula a aplicar

```
fator_acumulado = produto((1 + indice_mes/100) for mes in periodo)
valor_atualizado = valor_original * fator_acumulado
```

### Fonte oficial a consultar manualmente

- **Indice:** SELIC mensal
- **URL oficial:** https://www.bcb.gov.br/controleinflacao/historicotaxasjuros
- **Periodo a coletar:** 2019-05 a 2023-11 (55 meses)

### Sugestao operacional

Solicitar release nova do plugin com extensao historica do
cache OU usar calculadora oficial do BCB/IBGE para o periodo
historico.

> ⚠️ Validar contra fonte oficial antes de protocolar.
```

## 5. FUNDAMENTACAO LEGAL

- **CC art. 406 paragrafo unico** (red. Lei 14.905/2024) —
  Taxa Legal = Selic - IPCA, piso zero
- **CTN art. 161** — Selic aplicavel em tributos federais
- **Lei 9.430/96** — Selic acumulada + 1% mes do recolhimento
- **Tema 810 STF** — IPCA-E em condenacoes da Fazenda
- **Tema 905 STJ** — juros e correcao Fazenda Publica
- **ADC 58/59 STF** — IPCA-E + Selic em trabalhista (ate
  29/08/2024)
- **Lei 8.245/91** — locacao, indice contratual
- **Manual de Calculos CJF** — atualizacao em benefico
  previdenciario

## 6. AVISOS OBRIGATORIOS NO OUTPUT

1. ⚠️ Validar contra fonte oficial antes de protocolar
2. ⚠️ Cache local tem range explicito — fora dele, formula +
   link
3. ⚠️ Para juros complementares, conferir se o titulo prevê
   (contrato, sentenca, lei)
4. ⚠️ Para Taxa Legal CC406, lembrar que e vigente APENAS a
   partir de 30/08/2024 — antes disso, juros de 1% am simples
5. ⚠️ Indice mensal nao captura variacao intra-mes —
   pro_rata_die e aproximacao

## 7. INTEGRACAO

### Upstream (quem dispara)
- `calculos-master` (orquestrador)
- Praticamente TODAS as skills Tier 2 (sempre que precisa
  atualizar um valor)
- `parser-auditor-pjecalc` (validar indice usado pelo PJE)
- `comparador-calculos` (normalizar datas)

### Downstream auto-disparado
- `protocolo-p4-calculos` — apos atualizacao para selo de
  qualidade

### Cross-link (plugins-irmaos)
- Nao precisa — skill standalone, encerra ciclo do calculo

## 8. PROIBICOES

1. **Nunca** "lembrar" indice de memoria — sempre ler JSON
2. **Nunca** calcular valor final fora do range do cache
   (so devolver formula + link)
3. **Nunca** apresentar valor sem rastreabilidade (fonte,
   url, data_extracao, range_valido)
4. **Nunca** misturar indices (ex: usar IPCA ate X e Selic
   apos) sem que skill upstream tenha mandado fazer
5. **Nunca** aplicar Taxa Legal CC406 a periodo anterior a
   30/08/2024
6. **Nunca** aplicar SELIC mensal como se fosse anual (erro
   classico — Selic do BCB e mensal capitalizada)
7. **Nunca** chamar API externa do BCB/IBGE em runtime
8. **Nunca** apresentar valor final sem aviso obrigatorio

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Auditar calculo do PJE-CALC do mesmo caso | `/auditar-pjecalc` | `calculosjudiciais-adv-os` (este) |
| Comparar com outro calculo | `/comparar-calculos` | `calculosjudiciais-adv-os` (este) |
| Gerar peca de cumprimento ou execucao | `/execucao cumprimento-sentenca` | `execucao-adv-os` |
| Validar jurisprudencia citada | `/juris validar "Tema 810 STF"` | `juris-adv-os` |

> Se plugin nao instalado, copiar memoria de atualizacao
> acima e usar manualmente.
