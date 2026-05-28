---
name: comparador-calculos
description: >
  COMPARADOR-CALCULOS — Recebe 2 ou 3 calculos do MESMO caso (autor x
  reu, autor x contadoria, perito oficial x perito assistente, calculo
  original x calculo atualizado), posiciona-os lado a lado em tabela
  markdown comparativa, identifica divergencias verba a verba, e
  quantifica o gap em R$ por linha + agregado. Para cada divergencia,
  sugere causa provavel (indice diferente, base diferente, periodo
  diferente, juros pos-deducao vs pre-deducao, IRPF mes-a-mes vs
  acumulado, contribuicao previdenciaria omitida, etc.). Use SEMPRE
  que o usuario disser "comparar calculos", "lado a lado", "autor vs
  reu", "perito vs assistente", "calculo do exequente esta diferente",
  "/comparar-calculos" ou passar 2+ memorias de calculo.
---

# COMPARADOR-CALCULOS — Comparacao Side-by-Side de Calculos

## 1. ESCOPO

Diferencial competitivo do plugin. Posiciona 2 ou 3 calculos do mesmo
caso lado a lado, evidencia divergencias com cores semaforo e
quantifica o gap em R$. Casos tipicos de uso:

| Cenario | Quem fornece os calculos |
|---|---|
| Cumprimento de sentenca civel — autor cobra, reu impugna | Autor (memoria propria) + reu (peticao de impugnacao) |
| Liquidacao trabalhista — calculo do reclamante vs contadoria | Reclamante + PJE-Calc da contadoria |
| Pericia — perito oficial vs perito assistente | Laudo oficial + laudo assistente |
| Revisao bancaria — banco vs revisional | Banco (extrato) + recalculo expurgado |
| Repeticao indebito — Fazenda vs contribuinte | Sicalc + memoria do contribuinte |
| Conferencia interna — original vs atualizado | Versao N + versao N+1 |

Output anexavel direto em peca processual ou parecer.

## 2. INPUT NECESSARIO

| Campo | Obrigatorio | Observacoes |
|---|---|---|
| `calculo_a` | sim | Estrutura: nome_fonte, autor, data, verbas[] (nome, valor_corrigido, juros, total), total_geral |
| `calculo_b` | sim | Mesma estrutura |
| `calculo_c` | opcional | Mesma estrutura — quando ha 3 versoes (ex: perito A x perito B x contadoria) |
| `parametros_sentenca` | desejavel | Para indicar qual calculo segue a sentenca |
| `polo_cliente` | desejavel | Molda framing (favor / contra) |

Os calculos podem vir de:
- `parser-auditor-pjecalc` (auto-disparo apos parse)
- Memoria gerada por skill Tier 2 deste plugin
- Texto colado pelo advogado (memoria de calculo)
- Texto extraido de outro PDF/peticao

## 3. PROCESSAMENTO

### Passo 1 — Normalizar verbas

Verbas com nomes diferentes que se referem a mesma coisa
devem ser pareadas:

| Sinonimos comuns | Pareado como |
|---|---|
| "Adicional insalubridade 20%" / "Ad. insalubre 20%" / "Insal 20%" | adicional_insalubridade |
| "13o proporcional" / "Decimo terceiro" / "Gratificacao natalina" | decimo_terceiro |
| "Ferias + 1/3" / "Ferias com terco" / "Ferias indenizadas" | ferias_indenizadas |
| "FGTS 8% + 40%" / "FGTS rescisorio" | fgts_multa_40 |
| "Honorarios 10%" / "Sucumbenciais" / "CPC 85" | honorarios_sucumbenciais |

Se ha verba so em A e nao em B → marcar **OMITIDA EM B** com
peso especifico no diagnostico.

### Passo 2 — Comparar linha a linha

Para cada verba pareada:
- `gap = valor_a - valor_b` (positivo = A maior)
- Classificar tamanho do gap:
  - `< 1%` do total: 🟢 OK (arredondamento)
  - `1% a 5%`: 🟡 atencao
  - `> 5%`: 🔴 alerta

### Passo 3 — Diagnosticar causa provavel de cada divergencia

Heuristicas:

| Sintoma | Causa provavel |
|---|---|
| Valor corrigido diverge mas juros iguais | Indice de correcao diferente |
| Valor corrigido igual mas juros divergem | Marco temporal de juros diferente OU taxa diferente |
| Verba aparece em A e nao em B | Sentenca interpretada diferentemente (parametros) |
| Total geral diverge muito mais que verbas individuais | Verba significativa omitida ou somada errado |
| IRPF muito diferente | Regime de competencia vs caixa (Lei 7.713 art 12-A) |
| INSS muito diferente | Aliquota diferente OU omissao da deducao |
| Honorarios divergem | Base de calculo diferente (proveito vs causa) |

### Passo 4 — Calcular gap agregado e ponderado

- `gap_absoluto = |total_a - total_b|`
- `gap_percentual = gap_absoluto / max(total_a, total_b)`
- `verbas_divergentes_significativas = count(gap_percentual > 5%)`

### Passo 5 — Indicar qual calculo segue a sentenca

Se `parametros_sentenca` foi fornecido:
- Cruzar indices, marcos, verbas deferidas
- Marcar com ✅ CORRESPONDE A SENTENCA o calculo certo
- Marcar com 🔴 DIVERGE DA SENTENCA o errado

Se nao fornecido: deixar campo "verificar contra sentenca" e
listar pontos a conferir.

### Passo 6 — Recomendacao de proxima acao

| Cenario | Recomendacao |
|---|---|
| Gap percentual < 1% | Aceitar — diferenca de arredondamento |
| Gap percentual 1-5% + verbas todas presentes | Negociar topicos especificos |
| Gap percentual > 5% OU verba omitida | Impugnar formalmente + pedir nova conta |
| Sentenca claramente nao seguida por um lado | Embargos a execucao ou agravo |

## 4. OUTPUT

```markdown
## 🔎 Comparativo de Calculos — Processo {{numero}}

**Calculos comparados:**
- **A:** [nome_fonte_a] — autor: [...] — data: [...]
- **B:** [nome_fonte_b] — autor: [...] — data: [...]
- **C:** [opcional]

**Polo cliente:** [{{POLO}}]

### Tabela Comparativa Side-by-Side

| Verba | Calculo A | Calculo B | Gap R$ | Gap % | Status |
|---|---:|---:|---:|---:|:---:|
| Adicional insalubridade 20% | R$ 7.037,07 | R$ 6.890,12 | +146,95 | +2,1% | 🟡 |
| 13o proporcional | R$ 3.450,00 | R$ 0,00 | +3.450,00 | — | 🔴 OMITIDA EM B |
| Ferias + 1/3 | R$ 4.200,00 | R$ 4.150,00 | +50,00 | +1,2% | 🟢 |
| FGTS + 40% | R$ 8.900,00 | R$ 7.200,00 | +1.700,00 | +19,1% | 🔴 |
| Juros (total) | R$ 359,35 | R$ 1.207,80 | -848,45 | -70% | 🔴 |
| **TOTAL GERAL** | **R$ 23.946,42** | **R$ 19.447,92** | **+4.498,50** | **+18,8%** | 🔴 |

### 🔴 Divergencias Significativas Diagnosticadas

#### 1. 13o proporcional — OMITIDA EM B
- **Gap:** R$ 3.450,00 (15% do total)
- **Causa provavel:** sentenca interpretada diferentemente
  OU omissao deliberada
- **Acao:** verificar parametro da sentenca; se deferido,
  impugnar omissao

#### 2. FGTS + 40% — divergencia 19,1%
- **Gap:** R$ 1.700,00
- **Causa provavel:** base salarial diferente OU periodo
  de incidencia diferente (verificar se contemplou
  reflexos de horas extras)
- **Acao:** pedir memoria detalhada de FGTS de B

#### 3. Juros (total) — divergencia 70%
- **Gap:** R$ 848,45 (B aplicou juros maiores)
- **Causa provavel:** marco temporal diferente — possivel
  juros sobre BRUTO (pre-deducao INSS) em B
- **Fundamento:** Sum. 368 TST item IV — juros incidem
  sobre o valor liquido apos deducao da contribuicao
  previdenciaria
- **Acao:** se polo cliente = reclamado, IMPUGNAR (B
  prejudica reclamado)

### ✅ Verificacao contra Sentenca

[ se parametros fornecidos: marcar qual calculo confere; senao:
"Conferir: indice de correcao (sentenca diz X, A usa Y, B usa Z),
marco de juros (...), verbas deferidas (...)" ]

### 💰 Impacto Financeiro Total

- **Calculo A > Calculo B em R$ {{gap_absoluto}} ({{gap_percentual}}%)**
- Se polo cliente = autor, A favorece em R$ {{gap}}
- Se polo cliente = reu, B favorece em R$ {{gap}}

### 📝 Recomendacao

[com base no gap_percentual e verbas omitidas]

### Modelo de manifestacao (esqueleto)

```
EXCELENTISSIMO SENHOR DOUTOR JUIZ ...

[descricao do processo]

A divergencia entre os calculos apresentados monta em
R$ {{gap_absoluto}}, decorrente principalmente de:

1. [divergencia 1] — [fundamento]
2. [divergencia 2] — [fundamento]
3. [divergencia 3] — [fundamento]

Diante do exposto, requer-se a retificacao do calculo
{{erronoeo}}, adotando-se o calculo {{correto}}, ou
subsidiariamente a remessa dos autos a contadoria
oficial.
```

> ⚠️ **Validar contra fonte oficial antes de protocolar.**
```

## 5. FUNDAMENTACAO LEGAL

- **CPC 525** — impugnacao do executado (15 dias uteis)
- **CLT 879 § 2º** — prazo 8 dias para manifestacao sobre
  calculos
- **CPC 1.022** — embargos de declaracao se divergencia for
  obscuridade/contradicao
- **CPC 535-536** — embargos a execucao
- **ADC 58/59 STF** — IPCA-E + Selic em trabalhista
- **Lei 14.905/2024** — Taxa Legal CC 406 par. unico
- **Sumula 368 TST** itens II, IV, V — INSS + IRPF
- **Sumula 362 STJ** — atualizacao dano moral da data do
  arbitramento
- **Tema 905 STJ** — juros e correcao em condenacoes da
  Fazenda Publica
- **NBC PP 01 CFC** — base de auditoria contabil

## 6. AVISOS OBRIGATORIOS NO OUTPUT

1. ⚠️ Validar contra fonte oficial antes de protocolar
2. ⚠️ Comparativo automatizado — confirmacao via memoria
   detalhada de cada calculo e indispensavel
3. ⚠️ Se ha 3 calculos (A, B, C), comparativo e par a par
   (A vs B, A vs C, B vs C) — atencao a redundancia
4. ⚠️ Pareamento de verbas por sinonimo pode falhar em
   nomenclatura nao usual — revisar manualmente verbas
   marcadas "OMITIDA"

## 7. INTEGRACAO

### Upstream (quem dispara)
- `calculos-master` (orquestrador)
- `parser-auditor-pjecalc` (auto-disparo se ha 2º calculo)
- `auditor-laudo-pericial-contabil` (auto-disparo se ha
  laudo assistente)

### Downstream auto-disparado
- `gestao-prazo-impugnacao` — sempre apos comparativo
- `protocolo-p4-calculos` — auditoria R1-R4 antes do output

### Cross-link (plugins-irmaos)
- `trabalhista-adv-os` — gerar peca
- `execucao-adv-os` — embargos
- `ia-combativa-adv-os` — Suprema Corte R1-R4
- `juris-adv-os` — validar Sumulas

## 8. PROIBICOES

1. **Nunca** comparar calculos de PROCESSOS DIFERENTES (sem
   sentido juridico)
2. **Nunca** ocultar verba presente so em um dos calculos —
   marcar OMITIDA com destaque
3. **Nunca** afirmar qual esta "correto" sem cruzar contra
   sentenca
4. **Nunca** apresentar valor final sem aviso de validacao
5. **Nunca** apagar a memoria original de cada calculo —
   sempre preservar pra rastreabilidade
6. **Nunca** comparar calculos com **datas-base** muito
   diferentes sem atualizar para a mesma data primeiro
   (auto-disparar `atualizador-indices-cache`)
7. **Nunca** importar calculo de outro plugin — sempre via
   memoria interna ou input do advogado

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Atualizar ambos para mesma data | `/atualizar-valor` | `calculosjudiciais-adv-os` (este) |
| Auditar individualmente cada calculo | `/auditar-pjecalc` ou `/auditar-laudo-pericial` | `calculosjudiciais-adv-os` (este) |
| Gerar peca de impugnacao | `/trabalhista impugnacao-calculos` | `trabalhista-adv-os` |
| Embargar execucao | `/execucao embargos-execucao` | `execucao-adv-os` |
| Auditoria Suprema R1-R4 da peca | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` |

> Se plugin nao instalado, copiar memoria comparativa acima e
> usar manualmente.
