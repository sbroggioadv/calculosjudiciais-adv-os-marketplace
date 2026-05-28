---
name: calculo-rpv-precatorio
description: >
  CALCULO-RPV-PRECATORIO — Estrutura memoria de calculo de RPV
  (Requisicao de Pequeno Valor) e precatorio contra Fazenda Publica
  (CPC 534-535, CF 100, ADCT 97). Aplica IPCA-E como correcao monetaria
  (Tema 810 STF) + juros conforme natureza do credito (poupanca ate
  Lei 11.960/2009, depois remuneracao da caderneta de poupanca,
  conforme Tema 905 STJ — observar marcos da EC 113/2021). Define
  rito (RPV ate 60 SM federal, limites estaduais/municipais variam
  conforme lei local). NUNCA gera indices hardcoded — sempre consulta
  scripts/data/indices/*.json. Use quando o advogado mencionar
  "RPV", "precatorio", "execucao contra Fazenda", "cumprimento contra
  ente publico", "Uniao/Estado/Municipio", "expedir oficio
  requisitorio" ou variacoes.
---

# CALCULO-RPV-PRECATORIO — Cumprimento contra Fazenda Publica

## 1. ESCOPO

Skill estrutura memoria de calculo da fase de cumprimento de
sentenca contra **Fazenda Publica** (Uniao, Estados, DF, Municipios,
autarquias, fundacoes publicas) com expedicao de RPV ou Precatorio.

Cobre:
- Atualizacao monetaria pos-transito conforme Tema 810 STF (IPCA-E
  para debito nao tributario; SELIC para tributario)
- Juros moratorios conforme natureza + marcos legislativos (Lei
  11.960/2009, EC 113/2021, Lei 14.905/2024)
- Triagem RPV vs Precatorio conforme valor + ente
- Memoria pronta para expedicao do oficio requisitorio (CPC 535 §3º)

NAO cobre: requisicoes administrativas previas, FGTS, FUNRURAL,
verbas trabalhistas (essas podem ter regime proprio).

---

## 2. INPUT NECESSARIO

1. **Ente devedor** (Uniao / Estado-X / Municipio-Y / autarquia)
2. **Natureza do credito** (alimentar ou comum; tributario ou nao
   tributario) — define indices
3. **Valor da condenacao** + data-base + transito em julgado
4. **Houve impugnacao? Resultado?** (CPC 535)
5. **Lei estadual/municipal aplicavel para teto de RPV** (se nao
   federal)
6. **Quantidade de exequentes** (no caso de litisconsorcio, valor
   individual ≤ teto pode habilitar RPV individualizada)
7. **Houve fracionamento indevido?** (Sumula Vinculante 47 STF)

---

## 3. PROCESSAMENTO — CHECKLIST

### 3.1 Definir indice de correcao monetaria (Tema 810 STF)

| Natureza do credito | Indice aplicavel | Fonte |
|---|---|---|
| **Tributario** (repeticao indebito federal) | SELIC | scripts/data/indices/selic-mensal.json |
| **Nao tributario, alimentar** | IPCA-E | scripts/data/indices/ipca-e-mensal.json |
| **Nao tributario, comum** | IPCA-E (Tema 810) | scripts/data/indices/ipca-e-mensal.json |

### 3.2 Definir juros moratorios (Tema 905 STJ + marcos)

| Periodo | Juros aplicaveis |
|---|---|
| Ate 29/06/2009 | 1% am (Decreto-Lei 2.322/87) ou 6% aa (CC) conforme natureza |
| 30/06/2009 ate 08/12/2021 | Remuneracao da poupanca (Lei 11.960/2009 art. 1º-F) |
| 09/12/2021 (EC 113/2021) em diante para Fazenda | SELIC (englobando correcao + juros para Fazenda Publica) |
| Verbas alimentares federais (RE 870.947) | Juros equivalentes poupanca + IPCA-E ate EC 113/2021 |

⚠️ EC 113/2021 mudou regime: a partir de 09/12/2021, para
condenacoes da Fazenda Publica, **SELIC engloba correcao + juros**
(deixar de aplicar IPCA-E + poupanca em duplicidade).

### 3.3 Triagem RPV x Precatorio (CF 100 + leis especificas)

| Ente | Teto RPV padrao | Norma |
|---|---|---|
| Uniao | 60 SM (R$ depende ano-base) | Lei 10.259/2001 art. 17 §1º |
| Estados/DF | Lei estadual define (geralmente 40 SM, mas varia) | ADCT 97 + lei estadual |
| Municipios | Lei municipal define (geralmente 30 SM, mas varia) | ADCT 97 + lei municipal |

⚠️ Se nao houver lei estadual/municipal: aplica-se 40 SM (Estados) e
30 SM (Municipios) por forca do ADCT art. 87.

⚠️ **Sumula Vinculante 47 STF:** vedado fracionamento, repartido ou
quebra do valor da execucao para fins de enquadramento em RPV. Em
litisconsorcio, cada credor pode ter sua RPV se valor individual ≤
teto.

### 3.4 Atualizar valor e calcular juros

Segmentar em periodos conforme marcos da secao 3.2. Para cada
periodo:
```
valor_corrigido = valor_anterior × (acumulado_indice_periodo)
juros_periodo = base × taxa × tempo
```

### 3.5 Compor total

```
total_RPV_ou_precatorio = principal_corrigido + juros - pagamentos_parciais
```

---

## 4. OUTPUT — Memoria de Calculo

```markdown
## Memoria de Calculo — RPV / Precatorio

**Processo:** [numero]
**Exequente:** {{ADVOGADO_NOME}} (OAB/{{ADVOGADO_UF}} {{ADVOGADO_OAB}}) representando [parte]
**Executado:** [Uniao / Estado / Municipio / autarquia]
**Natureza:** [alimentar / comum] · [tributario / nao tributario]
**Juizo:** [vara/comarca/UF]

### Premissas

| Campo | Valor |
|---|---|
| Valor da condenacao | R$ [X] em [data-base] |
| Transito em julgado | [data] |
| Indice correcao monetaria | [IPCA-E / SELIC] (Tema 810 STF) |
| Marco EC 113/2021 atravessa? | [sim/nao] — segmentar se sim |
| Teto RPV aplicavel | [X SM] = R$ [valor] (lei [Lei 10.259/2001 art. 17 ou estadual/municipal X]) |
| Lei estadual/municipal | [link] |

### Tabela 1 — Atualizacao monetaria

| Mes/Ano | Indice [IPCA-E/SELIC] | Acumulado | Valor corrigido |
|---|---|---|---|
| [data-base] | _____ | 1,000000 | R$ [valor original] |
| ... | _____ | _____ | _____ |
| 08/12/2021 (marco EC 113) | _____ | _____ | R$ ___ |
| 09/12/2021 em diante | (SELIC engloba juros) | _____ | _____ |
| [data final] | _____ | _____ | **R$ ___** |

**Fonte:** scripts/data/indices/[ipca-e-mensal.json / selic-mensal.json]

### Tabela 2 — Juros moratorios

| Periodo | Taxa | Base | Juros |
|---|---|---|---|
| [transito] -> 29/06/2009 | 1% am / 6% aa (CC) | [base] | R$ ___ |
| 30/06/2009 -> 08/12/2021 | Poupanca | [base] | R$ ___ |
| 09/12/2021 -> [data final] | (englobado pela SELIC) | — | (zero — ja contado em correcao) |
| **Total juros separados** | | | **R$ ___** |

**Fonte:** Tema 905 STJ + RE 870.947 + EC 113/2021

### Triagem RPV vs Precatorio

| Calculo | Valor | Resultado |
|---|---|---|
| Valor final por exequente | R$ ___ | [< teto RPV / > teto = precatorio] |
| Salario minimo data-base | R$ ___ | [referencia] |
| Teto aplicavel | R$ ___ ([X SM]) | [norma] |

**CONCLUSAO:** [Expedir RPV / Expedir Precatorio]

Caminho: peticionar [CPC 535 §3º] requerendo expedicao do
[oficio requisitorio de RPV / precatorio] perante [orgao].

### Totalizacao

| Verba | Valor |
|---|---|
| Principal corrigido (IPCA-E ate EC 113 + SELIC depois) | R$ ___ |
| Juros separados (ate 08/12/2021) | R$ ___ |
| Pagamentos parciais (-) | -R$ ___ |
| **TOTAL EM [data]** | **R$ ___** |
```

---

## 5. FUNDAMENTACAO LEGAL

- **CF art. 100** + paragrafos — precatorios em geral
- **ADCT art. 87 e 97** — regime de RPV
- **CPC art. 534-535** — cumprimento de sentenca contra Fazenda
- **Lei 10.259/2001 art. 17** — RPV federal (60 SM)
- **Lei 12.153/2009** — juizado fazenda estadual/municipal
- **Lei 11.960/2009** — remuneracao da poupanca (vigente 30/06/2009 a 08/12/2021)
- **EC 113/2021** — SELIC engloba correcao + juros para Fazenda
- **Lei 14.905/2024** — Taxa Legal CC 406 (sem impacto direto na Fazenda, que segue EC 113)
- **Tema 810 STF** — IPCA-E para correcao de debitos nao tributarios da Fazenda
- **RE 870.947** — natureza alimentar / juros equivalentes a poupanca
- **Tema 905 STJ** — criterios de correcao + juros (ate vigencia EC 113)
- **Sumula Vinculante 47 STF** — vedacao fracionamento RPV/precatorio
- **Sumula Vinculante 17 STF** — juros entre expedicao e pagamento de precatorio (regime ate EC 113)

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ CONFERIR INDICES CONTRA TABELA OFICIAL VIGENTE ANTES DE PROTOCOLAR

1. IPCA-E — conferir contra IBGE
   (ibge.gov.br/estatisticas/economicas/precos-e-custos)
   — esta skill consulta cache local com range definido em
   scripts/data/indices/ipca-e-mensal.json.

2. SELIC — conferir contra BCB (bcb.gov.br/controleinflacao).

3. EC 113/2021 entrou em vigor em 09/12/2021. Se calculo
   atravessa essa data, SEGMENTAR em 2 periodos. NAO aplicar
   IPCA-E + poupanca em duplicidade apos essa data.

4. Lei estadual/municipal sobre teto de RPV: conferir publicacao
   oficial do ente. Padrao supletivo (ADCT 87): 40 SM Estados,
   30 SM Municipios.

5. Salario minimo de referencia: usar valor vigente na data da
   expedicao do oficio requisitorio (interpretacao majoritaria),
   nao o da data-base do calculo.

6. Sumula Vinculante 47: vedado fracionar o valor da execucao
   para enquadrar em RPV. Em litisconsorcio, cada credor pode ter
   sua RPV se valor individual ≤ teto.

7. CONFERIR LEI ESTADUAL/MUNICIPAL aplicavel — varia muito entre
   entes; alguns Estados ja superaram 40 SM.
```

---

## 7. INTEGRACAO

- **Upstream:** `identificar-tj-aplicavel` (JF vs Justica Comum vs Juizado Especial Fazendario), `classificar-tipo-calculo`
- **Downstream:** `protocolo-p4-calculos` (auditoria), `gestao-prazo-impugnacao` (Fazenda tem 30 dias uteis — CPC 535)
- **Cross-link:** `atualizador-indices-cache` para sub-rotinas de atualizacao

---

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Peticionar cumprimento contra Fazenda | `/execucao cumprimento-sentenca` | `execucao-adv-os` (Kirvano) |
| Defender Fazenda (impugnacao CPC 535) | `/execucao embargos-execucao` | `execucao-adv-os` (Kirvano) |
| Auditar com Suprema Corte R1-R4 | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |
| Buscar jurisprudencia Tema 810 / RE 870.947 | `/juris buscar Tema 810 STF` | `juris-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.

---

## 8. PROIBICOES

1. NUNCA aplicar IPCA-E + poupanca em duplicidade pos EC 113/2021
2. NUNCA usar SELIC para credito nao tributario pre EC 113/2021
   (contradiz Tema 810)
3. NUNCA fracionar valor da execucao para enquadrar RPV (SV 47 STF)
4. NUNCA inventar teto estadual/municipal sem consultar lei local
5. NUNCA gerar indice de memoria — sempre consultar
   `scripts/data/indices/*.json`
6. NUNCA omitir aviso obrigatorio de validacao final
