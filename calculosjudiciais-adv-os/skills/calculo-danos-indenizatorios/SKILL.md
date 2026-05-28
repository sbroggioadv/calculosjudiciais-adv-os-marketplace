---
name: calculo-danos-indenizatorios
description: >
  CALCULO-DANOS-INDENIZATORIOS — Estrutura memoria de calculo de
  indenizacao por danos (CC 944). Cobre 3 modalidades: (1) dano
  material (danos emergentes — despesas comprovadas — e lucros
  cessantes — CC 402-403), (2) dano moral (atualizado da data do
  arbitramento — Sumula 362 STJ — com juros conforme natureza
  contratual ou extracontratual), (3) lucros cessantes projetados
  (lucros razoavelmente esperados). Termo inicial dos juros: evento
  danoso para responsabilidade extracontratual (Sumula 54 STJ);
  citacao para responsabilidade contratual (CC 405). NUNCA gera
  indices hardcoded — sempre consulta scripts/data/indices/*.json.
  Use quando o advogado mencionar "calcular indenizacao", "atualizar
  dano moral", "lucros cessantes", "danos materiais", "atualizar
  condenacao por acidente", "Sumula 362", "Sumula 54", "CC 944" ou
  variacoes.
---

# CALCULO-DANOS-INDENIZATORIOS — Material + Moral + Lucros Cessantes

## 1. ESCOPO

Skill estrutura memoria de calculo de **condenacao indenizatoria** ja
fixada (sentenca, acordao, acordo) cobrindo:

- **Dano material — danos emergentes:** despesas comprovadas (CC 402)
- **Dano material — lucros cessantes:** o que razoavelmente deixou
  de ganhar (CC 402-403)
- **Dano moral:** quantificacao + atualizacao da data do arbitramento
  (Sumula 362 STJ)
- **Lucros cessantes projetados:** rendimentos futuros nao auferidos

NAO cobre: arbitramento do dano moral (skill conta valor ja fixado),
indenizacoes tarifadas (CDC 42 § unico — ver
`calculo-restituicao-dobro-cdc`), nem dano em saude (regimes
proprios — auxilio-acidente, etc.).

---

## 2. INPUT NECESSARIO

1. **Natureza da responsabilidade:** contratual (CC 389) ou
   extracontratual/aquiliana (CC 186)
2. **Modalidades de dano fixadas:** material (qual valor), moral
   (qual valor), lucros cessantes (qual valor + metodologia)
3. **Para dano MATERIAL — danos emergentes:**
   - Data de cada despesa (cada nota fiscal/recibo tem data propria)
   - Valor nominal de cada despesa
4. **Para dano MORAL:**
   - Valor arbitrado na sentenca
   - Data do arbitramento (Sumula 362 STJ — correcao a partir DAI)
5. **Para LUCROS CESSANTES:**
   - Periodo de incidencia
   - Valor mensal/anual estimado
   - Houve fixacao de pensionamento mensal? Termo final?
6. **Termo inicial dos juros:**
   - Extracontratual: data do evento danoso (Sumula 54 STJ)
   - Contratual: data da citacao (CC 405)
7. **Houve pagamento parcial?** Datas e valores
8. **Tabela de correcao monetaria aplicavel** (via
   `identificar-tj-aplicavel`)

---

## 3. PROCESSAMENTO — CHECKLIST

### 3.1 Segmentar por modalidade

Cada modalidade tem termo inicial proprio. NUNCA somar tudo e
atualizar de uma so data.

### 3.2 Dano material — danos emergentes (CC 402)

Para cada despesa:
```
valor_corrigido = valor_nominal × (acumulado_data_calculo / acumulado_data_despesa)
```

Termo inicial juros: ver 3.5.

### 3.3 Dano moral (Sumula 362 STJ)

- **Correcao:** a partir da **data do arbitramento** (sentenca ou
  acordao que fixou o valor). NAO da data do evento.
- **Juros:**
  - Extracontratual: desde data do evento (Sumula 54 STJ) — mesmo
    que correcao so a partir do arbitramento
  - Contratual: desde a citacao (CC 405)

```
valor_corrigido = valor_arbitrado × (acumulado_data_calculo / acumulado_data_arbitramento)
juros = valor_arbitrado × taxa × tempo_desde_termo_inicial
```

⚠️ Detalhe critico: juros incidem sobre o **valor NOMINAL** fixado
(nao corrigido) durante o periodo entre evento/citacao e
arbitramento, e sobre o valor corrigido apos. Existe divergencia
doutrinaria — alguns juizos calculam juros sobre valor corrigido
desde o inicio. **Conferir entendimento do TJ.**

### 3.4 Lucros cessantes

Se pensionamento mensal fixado:
- Cada parcela tem sua data de vencimento
- Cada parcela vencida = corrigida desde vencimento + juros desde vencimento
- Parcelas vincendas = nao integram calculo (cobra-se na execucao
  conforme vencem)

Se valor unico:
```
valor_corrigido = valor × (acumulado_data_calculo / acumulado_data_evento_ou_arbitramento)
```

### 3.5 Juros legais — taxa e marco

| Periodo | Taxa | Fundamento |
|---|---|---|
| Pre 11/01/2003 (CC/16) | 6% aa (0,5% am) | CC/16 art. 1.062 |
| 11/01/2003 ate 29/08/2024 | SELIC | CC 406 + EREsp 1.207.197 STJ |
| Pos 30/08/2024 | Taxa Legal (Selic-IPCA) | Lei 14.905/2024 |

### 3.6 Compor total

```
total = (material_corrigido + juros) + (moral_corrigido + juros) + (lucros_cessantes_corrigidos + juros) - pagamentos_parciais
```

---

## 4. OUTPUT — Memoria de Calculo

```markdown
## Memoria de Calculo — Indenizacao por Danos

**Processo:** [numero]
**Autor:** {{ADVOGADO_NOME}} (OAB/{{ADVOGADO_UF}} {{ADVOGADO_OAB}}) representando [parte]
**Reu:** [parte]
**Natureza:** [extracontratual / contratual]
**Juizo:** [vara/comarca/UF]

### Premissas

| Campo | Valor |
|---|---|
| Data do evento danoso | [data] |
| Data da citacao | [data] |
| Data do arbitramento (sentenca/acordao) | [data] |
| Modalidades fixadas | [material R$ X / moral R$ Y / lucros cessantes R$ Z] |
| Termo inicial juros (Sum. 54 ou CC 405) | [data] |
| Termo inicial correcao do dano moral (Sum. 362) | [data arbitramento] |
| Tabela correcao monetaria | [TJ-XX] — [URL] |

### Tabela 1 — Dano material (danos emergentes)

| Despesa | Data | Valor nominal | Indice acumulado | Valor corrigido |
|---|---|---|---|---|
| [descricao 1] | [data] | R$ ___ | _____ | R$ ___ |
| [descricao 2] | [data] | R$ ___ | _____ | R$ ___ |
| **Subtotal material corrigido** | | | | **R$ ___** |

**Juros sobre dano material:**
| Periodo | Taxa | Base | Juros |
|---|---|---|---|
| [termo inicial] -> [data calculo] | [SELIC/Taxa Legal] | [base] | R$ ___ |

### Tabela 2 — Dano moral (Sumula 362 STJ)

| Item | Valor |
|---|---|
| Valor arbitrado | R$ ___ em [data arbitramento] |
| Indice acumulado [data arb -> data calc] | _____ |
| **Valor corrigido** | **R$ ___** |

**Juros sobre dano moral:**
- Termo inicial: [data evento - Sum. 54 STJ se extracontratual / data citacao - CC 405 se contratual]
- Periodo: [N meses]
- Taxa segmentada: [SELIC pre 30/08/2024 + Taxa Legal pos]
- **Juros: R$ ___**

⚠️ Conferir entendimento do TJ sobre base dos juros (valor nominal
vs corrigido durante periodo evento->arbitramento). Skill apresenta
calculo padrao majoritario.

### Tabela 3 — Lucros cessantes

[Se pensionamento mensal:]
| Mes/Ano | Valor mensal corrigido | Juros desde vencimento | Subtotal |
|---|---|---|---|
| [mes] | R$ ___ | R$ ___ | R$ ___ |
| ... | ... | ... | ... |
| **Subtotal lucros cessantes vencidos** | | | **R$ ___** |

[Se valor unico:]
| Valor original | Indice acumulado | Valor corrigido | Juros | Total |
|---|---|---|---|---|
| R$ ___ em [data] | _____ | R$ ___ | R$ ___ | R$ ___ |

### Totalizacao

| Verba | Valor |
|---|---|
| Dano material corrigido + juros | R$ ___ |
| Dano moral corrigido + juros | R$ ___ |
| Lucros cessantes corrigidos + juros | R$ ___ |
| Honorarios sucumbenciais (sentenca) | R$ ___ |
| Pagamentos parciais (-) | -R$ ___ |
| **TOTAL EM [data]** | **R$ ___** |
```

---

## 5. FUNDAMENTACAO LEGAL

- **CC art. 186 e 927** — responsabilidade civil extracontratual
- **CC art. 389 e 395** — responsabilidade contratual
- **CC art. 402-403** — danos emergentes + lucros cessantes
- **CC art. 405** — juros desde a citacao (responsabilidade contratual)
- **CC art. 406** (Lei 14.905/2024) — Taxa Legal pos 30/08/2024
- **CC art. 944** — principio da reparacao integral
- **Sumula 54 STJ** — juros a partir do evento danoso (extracontratual)
- **Sumula 362 STJ** — correcao monetaria do dano moral desde
  arbitramento
- **Sumula 326 STJ** — sucumbencia recae sobre proveito economico
  efetivo (nao sobre o pedido reduzido)
- **REsp 1.207.197 (EREsp)** — SELIC como juros legais
- **Lei 14.905/2024** — em vigor desde 30/08/2024

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ CONFERIR INDICES CONTRA TABELA OFICIAL VIGENTE DO TJ APLICAVEL ANTES DE PROTOCOLAR

1. Tabela de correcao — conferir contra publicacao atual do TJ
   ([URL]). Esta skill consulta cache local com range definido em
   scripts/data/indices/*.json.

2. SELIC pre 30/08/2024 — conferir contra BCB. Taxa Legal pos
   30/08/2024 (Selic - IPCA, Lei 14.905/2024) — conferir contra
   apuracao BCB + IBGE.

3. Sumula 362 STJ: correcao do DANO MORAL e desde data do
   ARBITRAMENTO (sentenca/acordao que fixou o valor), NUNCA da
   data do evento.

4. Sumula 54 STJ: juros do dano EXTRACONTRATUAL incidem desde a
   data do evento danoso (mesmo que correcao so a partir do
   arbitramento — sao termos iniciais distintos).

5. Em responsabilidade CONTRATUAL, juros desde a CITACAO (CC 405).

6. Lucros cessantes exigem prova razoavel — "o que razoavelmente
   deixou de ganhar" (CC 402). NAO inclui ganhos hipoteticos ou
   especulativos.

7. Base dos juros sobre dano moral (valor nominal vs corrigido no
   periodo evento->arbitramento) tem divergencia. CONFERIR
   entendimento do TJ.

8. Atravessar 30/08/2024 (marco Lei 14.905/2024) exige SEGMENTAR
   o calculo de juros — pre = SELIC, pos = Taxa Legal.
```

---

## 7. INTEGRACAO

- **Upstream:** `identificar-tj-aplicavel`, `classificar-tipo-calculo`
- **Downstream:** `protocolo-p4-calculos` (auditoria obrigatoria pos-calculo final), `gestao-prazo-impugnacao` (15 dias CPC 525)
- **Cross-link:** `atualizador-indices-cache` (atualizacao monetaria padronizada)

---

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Peticionar cumprimento de sentenca indenizatoria | `/execucao cumprimento-sentenca` | `execucao-adv-os` (Kirvano) |
| Impugnar calculo do exequente | `/execucao embargos-execucao` | `execucao-adv-os` (Kirvano) |
| Auditar calculo com Suprema Corte R1-R4 | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |
| Buscar jurisprudencia Sumula 362/54 STJ | `/juris buscar Sumula 362 STJ` | `juris-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.

---

## 8. PROIBICOES

1. NUNCA atualizar dano moral desde data do evento (viola Sum. 362
   STJ — atualiza desde arbitramento)
2. NUNCA aplicar juros do dano extracontratual a partir da citacao
   (viola Sum. 54 STJ — desde o evento)
3. NUNCA somar todas as modalidades e atualizar de uma so data —
   cada modalidade tem termo inicial proprio
4. NUNCA incluir lucros cessantes meramente especulativos
5. NUNCA aplicar SELIC pos 30/08/2024 sem segmentar com Taxa Legal
6. NUNCA gerar indice de memoria — sempre consultar
   `scripts/data/indices/*.json`
7. NUNCA omitir aviso obrigatorio de validacao final
