---
name: classificar-tipo-calculo
description: >
  CLASSIFICAR-TIPO-CALCULO — Recebe contexto do caso (texto livre do
  advogado, fase processual, tipo de acao) e devolve: AREA (civel/
  trabalhista/tributario/previdenciario/familia/criminal/consumidor),
  SUBTIPO (cumprimento sentenca / liquidacao / RPV / verbas
  rescisorias / Selic federal / RMI / alimentos / etc), SKILL Tier 2
  a chamar, e contexto a propagar (marco intertemporal, natureza
  relacao). Use quando o orquestrador precisa rotear ou quando o
  advogado disser "que tipo de calculo e esse", "qual skill",
  "nao sei classificar", "me ajuda a identificar".
---

# CLASSIFICAR-TIPO-CALCULO — Decisao de Roteamento

## 1. ESCOPO

Skill de classificacao. Recebe input livre do advogado + estado
atual do yaml `calculo:` e devolve decisao estruturada de qual
skill Tier 2 acionar.

## 2. INPUT NECESSARIO

Minimo:
- **Texto livre** descrevendo o que precisa calcular (ou contexto
  do processo)

Opcional (melhora classificacao):
- Numero do processo (ajuda inferir tribunal/area)
- Tipo de acao em curso
- Fase processual atual (conhecimento / liquidacao / cumprimento /
  execucao)
- Polo do cliente (autor/reu/exequente/executado)
- Data de fatos relevantes (para marco intertemporal)

## 3. TABELA DE DECISAO (input → output)

### 3.1 CIVEL

| Sinais no input | Subtipo | Skill |
|---|---|---|
| "transito em julgado", "fase de cumprimento", "executar sentenca civel", "CPC 523" | cumprimento_sentenca | `calculo-cumprimento-sentenca-civel` |
| "RPV", "precatorio", "Fazenda Publica", "ente publico devedor", "Tema 810" | rpv_precatorio | `calculo-rpv-precatorio` |
| "dano material", "dano moral", "lucros cessantes", "indenizacao", "CC 944", "Sum 362" | danos | `calculo-danos-indenizatorios` |
| "condominio", "taxa condominial", "CC 1336", "convencao" | debito_condominial | `calculo-debito-condominial` |
| "aluguel atrasado", "locacao", "Lei 8245", "fiador" | debito_locaticio | `calculo-debito-locaticio` |
| "custas", "sucumbencia", "honorarios CPC 85", "contratuais", "Lei 8906" | custas_honorarios | `calculo-custas-honorarios` |
| "anatocismo", "Price vs SAC", "revisao bancaria", "CDC 51", "Sum 539", "expurgo juros" | revisao_bancaria | `calculo-revisao-bancaria` |

### 3.2 TRABALHISTA

| Sinais no input | Subtipo | Skill |
|---|---|---|
| "liquidacao trabalhista", "CLT 879", "sentenca trabalhista liquidanda", "ADC 58", "Lei 14.905" | liquidacao | `calculo-liquidacao-trabalhista` |
| "rescisao", "verbas rescisorias", "aviso previo", "13o proporcional", "FGTS 40", "Lei 12.506" | verbas_rescisorias | `calculo-verbas-rescisorias` |
| "hora extra", "horas extras", "DSR", "Sum 376", "OJ 394", "divisor 220" | horas_extras | `calculo-horas-extras-reflexos` |
| "insalubridade", "periculosidade", "noturno", "NR 15", "NR 16", "adicional 30%" | adicionais | `calculo-adicionais-trabalhistas` |
| "deposito recursal", "RO RR ED AIRR", "Ato SEGJUD TST" | deposito_recursal | `calculo-deposito-recursal` |

### 3.3 TRIBUTARIO

| Sinais no input | Subtipo | Skill |
|---|---|---|
| "IRPF atrasado", "IRPJ", "CSLL", "PIS", "COFINS", "Sicalc", "Selic tributo federal", "CTN 161" | tributo_federal | `calculo-tributo-federal-selic` |
| "REFIS", "PERT", "parcelamento tributario", "anistia multa" | refis | `calculo-refis-parcelamento` |
| "repeticao indebito", "restituicao tributo", "Sum 162 STJ", "Sum 188", "Sum 461" | repeticao_indebito | `calculo-repeticao-indebito` |

### 3.4 PREVIDENCIARIO

| Sinais no input | Subtipo | Skill |
|---|---|---|
| "RMI", "salario beneficio", "art 29 Lei 8213", "EC 103", "calculo INSS inicial" | rmi | `calculo-rmi-beneficio` |
| "atrasados INSS", "revisao beneficio", "Tema 905 STJ", "Tema 810", "Manual CJF" | atrasados_inss | `calculo-atrasados-inss` |
| "aposentadoria especial", "conversao tempo", "fator 1.40", "fator 1.20", "atividade insalubre 25 anos" | aposentadoria_especial | `calculo-aposentadoria-especial` |

### 3.5 FAMILIA / CRIMINAL / CONSUMIDOR

| Sinais no input | Subtipo | Skill |
|---|---|---|
| "alimentos atrasados", "pensao alimenticia", "Sum 309 STJ", "Tema 1137", "CNH passaporte" | alimentos | `calculo-alimentos-atrasados` |
| "partilha bens", "meacao", "tornas", "CC 1658", "comunhao parcial/universal" | partilha | `calculo-partilha-bens` |
| "pena multa", "dia-multa", "CP 49" | pena_multa | `calculo-pena-multa` |
| "restituicao dobro", "cobranca indevida CDC 42", "Tema 929 STJ", "engano justificavel" | restituicao_dobro | `calculo-restituicao-dobro-cdc` |

### 3.6 TRANSVERSAIS (auditoria — DIFERENCIAL)

| Sinais no input | Subtipo | Skill |
|---|---|---|
| "PDF PJE-CALC", "auditar PJE-CALC", "calculo do PJE-CALC errado", "Calculo nro" | auditoria_pjecalc | `parser-auditor-pjecalc` |
| "autor vs reu", "perito vs assistente", "2 calculos do mesmo caso", "qual a divergencia" | comparacao | `comparador-calculos` |
| "atualizar valor", "atualizar de X a Y", "Selic entre", "IPCA entre", "INPC entre" | atualizacao_pontual | `atualizador-indices-cache` |
| "laudo pericial contabil", "auditar laudo", "NBC PP 01", "perito oficial" | auditoria_laudo | `auditor-laudo-pericial-contabil` |
| "quesitos perito", "quesitos contabil", "impugnar nomeacao" | quesitos | `gerador-quesitos-perito-contabil` |
| "contra-laudo", "impugnar laudo perito" | contra_laudo | `contra-laudo-pericial` |

## 4. MARCO INTERTEMPORAL (sempre flaggar)

Ao classificar, AVALIE e PROPAGUE no output:

| Marco | Data corte | Impacta |
|---|---|---|
| **Lei 14.905/2024** (Taxa Legal CC 406) | vigencia 30/08/2024 | TODOS os calculos civeis pos-30/08/2024 usam Taxa Legal (Selic - IPCA) em vez de 1% am |
| **ADC 58/59 STF** | junho/2020 (acordao) + aplicacao retroativa | Trabalhistas: IPCA-E pre-ajuizamento + Selic pos-ajuizamento (sem 1% am cumulativo) |
| **EC 103/2019** (Reforma Previdenciaria) | 13/11/2019 | Calculos de RMI mudam regra de transicao |
| **Lei 13.467/2017** (Reforma Trabalhista) | 11/11/2017 | Intervalo intrajornada vira indenizatorio + so tempo suprimido |
| **Tema 810 STF** | 2018 | IPCA-E em condenacoes da Fazenda |
| **Tema 905 STJ** | 2018 | Juros poupanca em condenacoes da Fazenda ate 30/06/2009 → Selic depois |

Se data de fatos do caso atravessa qualquer marco → setar
`marco_intertemporal.<flag>: true` e ALERTAR a skill downstream.

## 5. NATUREZA DA RELACAO (sempre flaggar)

| Tipo | Sinais |
|---|---|
| `consumo` | banco, financeira, cartao, plano de saude, telefonia, varejo, ecommerce |
| `civil` | particular x particular sem CDC |
| `empresarial` | PJ x PJ, contratos B2B, franquia, distribuicao |
| `trabalhista` | reclamacao trabalhista, vinculo CLT, terceirizacao |
| `tributaria` | Fazenda Publica x contribuinte |
| `previdenciaria` | INSS, RGPS, RPPS, RPC |
| `locaticia` | locacao residencial/comercial Lei 8.245/91 |

Impacta: prazo prescricional, regime de juros, regra de inversao,
multas aplicaveis.

## 6. OUTPUT (formato estruturado)

```yaml
classificacao:
  area: civel
  subtipo: cumprimento_sentenca
  skill_alvo: calculo-cumprimento-sentenca-civel
  natureza_relacao: consumo
  marco_intertemporal:
    pre_lei_14905_2024: false
    pre_adc_58_59: false
    pre_ec_103: false
    notas: "fatos pos Lei 14.905/2024 — aplicar Taxa Legal CC 406"
  contexto_a_propagar:
    polo_cliente: exequente
    tipo_acao_origem: indenizatoria_dano_moral
    valor_principal: "R$ ..."
    data_transito_julgado: "YYYY-MM-DD"
    fonte_calculo: original
  pre_requisitos:
    - identificar-tj-aplicavel (UF: SP, comarca: Sao Paulo)
    - calculos-onboarding (verificar persona)
  observacoes_anti_halucinacao:
    - "Verificar tabela de correcao do TJSP em <url oficial>"
    - "Confirmar se ha multa 10% por nao pagto em 15d (CPC 523)"
```

E recomendacao em markdown:

```markdown
## Classificacao — classificar-tipo-calculo

**Area:** Civel
**Subtipo:** Cumprimento de sentenca
**Skill recomendada:** `calculo-cumprimento-sentenca-civel`

**Justificativa:** input mencionou "transito em julgado" + "executar
sentenca civel" + "CPC 523". Configura fase de cumprimento, nao
execucao de titulo extrajudicial.

**Marco intertemporal:** ⚠️ fatos pos 30/08/2024 — aplicar Taxa
Legal CC 406 (pos Lei 14.905/2024), nao 1% am tradicional.

**Pre-requisitos antes da skill principal:**
1. `calculos-onboarding` (se persona nao configurada)
2. `identificar-tj-aplicavel` (TJ {{UF}}, comarca {{CIDADE}})

Prosseguir para `calculo-cumprimento-sentenca-civel`?
```

## 7. CASOS LIMITROFES (perguntar UMA vez)

Se sinais conflitantes:

- "Cobrar honorarios" — `calculo-custas-honorarios` ou cumprimento?
  → perguntar: ja transitou em julgado a decisao que arbitrou?
- "Calculo de divida bancaria" — revisao ou cobranca simples?
  → perguntar: cliente quer impugnar contrato (revisao) ou aceita
  termos e so quer atualizar (cumprimento/cobranca)?
- "Trabalhista pre-Reforma" — aplicar regras antigas?
  → perguntar: contrato encerrou antes de 11/11/2017?

## 8. PROIBICOES

1. Nao classificar sem ler input — pelo menos 1 frase do advogado
2. Nao inferir marco intertemporal por padrao — checar data
3. Nao chutar skill — se duvida, pedir mais contexto (1 pergunta)
4. Nao perder info ja preenchida no yaml `calculo:`
5. Nao classificar como auditoria (Tier 3) se input nao mencionou
   PDF/laudo/comparativo explicitamente

## 💡 Proximos passos opcionais

Apos classificacao, a skill alvo Tier 2 dispara naturalmente. Em
seguida, considere:

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Peticionar com base no calculo | `/execucao <skill>` | `execucao-adv-os` |
| Liquidar e peticionar trabalhista | `/trabalhista liquidacao-execucao-trabalhista` | `trabalhista-adv-os` |
| Auditoria suprema R1-R4 | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` |

> Classificacao errada compromete TUDO — em duvida, perguntar uma
> vez ao usuario antes de prosseguir.
