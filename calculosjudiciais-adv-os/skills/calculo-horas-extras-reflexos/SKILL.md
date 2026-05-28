---
name: calculo-horas-extras-reflexos
description: >
  CALCULO-HORAS-EXTRAS-REFLEXOS — Calcula horas extras (adicional
  minimo 50% CF 7o XVI, ou superior por CCT) + reflexos habituais em
  DSR (Sum. 376 TST), 13o, ferias + 1/3, aviso previo e FGTS. Aplica
  divisor de jornada correto (220/200/180), tolerancia 5min/10min
  (Sum. 366 TST), regra do intervalo intrajornada suprimido (Sum. 437
  TST + Reforma 13.467/2017 art. 71 §4o CLT) e OJ 394 SDI-1 TST
  (vedacao da dobra do DSR). SIDE-AWARE. Use quando o operador
  disser "horas extras", "calcular HE", "reflexos de horas extras",
  "DSR", "divisor 220", "intervalo intrajornada suprimido",
  "Sumula 376 TST", "OJ 394 SDI-1".
---

# CALCULO-HORAS-EXTRAS-REFLEXOS — Horas Extras e Reflexos Habituais

## 1. ESCOPO

Skill Tier 2 do plugin `calculosjudiciais-adv-os`. Apura **horas
extras** e seus **reflexos habituais** nas demais verbas trabalhistas
(DSR, 13o, ferias + 1/3, aviso previo, FGTS).

**Acionada quando o operador menciona:** horas extras, calcular HE,
divisor de jornada, reflexos em DSR, intervalo intrajornada
suprimido, Sumula 376 TST, OJ 394 SDI-1, banco de horas, tolerancia
de marcacao.

## 2. SIDE-AWARENESS

| Polo | Postura do calculo |
|------|--------------------|
| **Reclamante** | Calcular **a maior** — divisor menor defensavel (e.g., 180 se jornada 6h diarias), adicional maximo defensavel (CCT > CF), aplicar todos os reflexos habituais nas verbas correlatas, pleitear intervalo intrajornada como hora extra integral se contrato pre-Reforma. |
| **Reclamada** | Conferir o calculo do reclamante — apontar divisor correto, restringir reflexos aos efetivamente habituais (Protocolo 1 — sem habitualidade, sem reflexo), aplicar regra pos-Reforma para contratos posteriores a 11/11/2017 (intervalo: so o tempo suprimido, indenizatorio). |

## 3. INPUT NECESSARIO

- **Jornada contratual** (horas diarias e semanais — 8h/44, 8h/40,
  6h/36, etc.)
- **Salario-base** (e evolucao se houver)
- **Periodo** (com **marco intertemporal 11/11/2017** — Reforma)
- **Horas extras semanais/mensais** trabalhadas (cartao de ponto ou
  alegacao)
- **Adicional aplicavel** (CF 7o XVI = minimo 50%; CCT pode majorar
  para 60/70/100%)
- **Habitualidade** (sim/nao — sem habitualidade nao ha reflexo)
- **Intervalo intrajornada** foi respeitado? Suprimido total ou
  parcial?
- **CCT/ACT da categoria** (pode prever adicional/divisor/regras
  especificas)
- **Banco de horas** vigente? (suspende a remuneracao das HE ate o
  acerto)

## 4. DIVISOR DE JORNADA

| Jornada contratual | Divisor mensal |
|--------------------|---------------:|
| 8h diarias / 44h semanais (regra geral) | **220** |
| 8h diarias / 40h semanais (sem reflexo sabado) | **200** |
| 6h diarias / 36h semanais | **180** |
| 6h diarias / 30h semanais (escala 5x2) | **150** |
| 12x36 (Reforma art. 59-A) | regra propria |

**Calculo do valor da hora normal:**
```
valor_hora = salario_base / divisor
```

## 5. CALCULO DA HORA EXTRA

```
valor_HE = valor_hora * (1 + adicional)
adicional minimo = 0.50 (CF 7o XVI)
adicional CCT = se houver, prevalece se superior
```

**Para apuracao mensal:**
```
HE_mensal = quantidade_HE_no_mes * valor_HE
```

## 6. REFLEXOS HABITUAIS — REGRA E LIMITES

### Tese central (Sumula 376 TST)
A integracao das horas extras prestadas com habitualidade na
remuneracao gera **reflexo no DSR** (descanso semanal remunerado) e,
em seguida, nas demais verbas:
- **DSR** (Lei 605/49 art. 7o §2o)
- **13o salario** (Lei 4.090/62)
- **Ferias + 1/3** (CLT art. 142)
- **Aviso previo** (Sum. 305 TST analoga)
- **FGTS** (8% sobre tudo)

### VEDACAO CRITICA — OJ 394 SDI-1 TST
A repercussao do DSR ja integrado **NAO** volta a integrar 13o,
ferias e aviso. Isto e: o DSR e calculado uma vez sobre as HE; nas
demais verbas, a base de calculo e a HE pura (sem o DSR ja
integrado) — sob pena de **bis in idem**.

**Exemplo numerico:**
- HE mensal = R$ 1.000,00
- DSR sobre HE = R$ 1.000 x (dias_descanso / dias_uteis) = R$ 200,00
- Base para 13o/ferias/aviso/FGTS = **R$ 1.000,00** (HE pura), NAO
  R$ 1.200,00 (com DSR).

### Sumula 366 TST — tolerancia de marcacao
- Ate **5 minutos por marcacao** (entrada ou saida) — sem hora
  extra
- Ate **10 minutos por dia** (somando todas as marcacoes) — sem
  hora extra
- Excedido o limite, **todo o tempo** e considerado a disposicao
  (nao so o excesso) — ou seja, e devida a integral.

## 7. INTERVALO INTRAJORNADA SUPRIMIDO

### Pre-Reforma (ate 10/11/2017)
- **Sumula 437 TST** — supressao total ou parcial gera direito ao
  pagamento **integral** do periodo correspondente, com **adicional
  de 50%**, **com reflexos** em todas as verbas (natureza salarial).

### Pos-Reforma (a partir de 11/11/2017 — Lei 13.467/2017)
- CLT art. 71 §4o (nova redacao) — supressao do intervalo gera
  pagamento **apenas do periodo suprimido**, com adicional de 50%, e
  com natureza **indenizatoria** (SEM reflexos).

### Contrato "a cavalo" (iniciou antes, persistiu apos 11/11/2017)
- **Segmentar**: aplicar regra antiga ate 10/11/2017 (com reflexos) +
  regra nova de 11/11/2017 em diante (sem reflexos). Protocolo
  intertemporal aplicavel ate o STF/TST consolidar tese diversa.

## 8. PROCESSAMENTO — PASSO A PASSO

1. **Mapear jornada** -> definir divisor
2. **Calcular valor_hora** = salario / divisor
3. **Calcular HE mes a mes** = quantidade * valor_hora * (1 + adicional)
4. **Confirmar habitualidade** -> se habituais, aplicar reflexos
5. **Calcular DSR sobre HE** (sumula 376 TST):
   - DSR = HE x (dias_descanso_no_mes / dias_uteis_no_mes)
6. **Calcular reflexos nas demais verbas** com base nas HE puras (OJ
   394 SDI-1):
   - 13o = HE_media_ano / 12 (a cada mes acumulado)
   - Ferias = HE_media_periodo + 1/3
   - Aviso = HE_media_ultimos_12_meses
   - FGTS = 8% sobre (HE + DSR + reflexos)
7. **Verificar intervalo intrajornada** -> apurar conforme marco
8. **Atualizar** com IPCA-E + Selic / Lei 14.905 (chamar
   `atualizador-indices-cache`)

## 9. OUTPUT — MODELO

```markdown
# Horas Extras + Reflexos — [Reclamante]
**Jornada:** [Xh diarias / Y h semanais]   **Divisor:** [N]
**Adicional:** [50% CF / X% CCT]
**Periodo:** [MM/AAAA] a [MM/AAAA]
**Marco intertemporal:** [contrato pre/pos/a cavalo Reforma]

## Apuracao mensal das HE

| Mes | Salario | Valor hora | Qte HE | Adicional | Valor HE | DSR | Total |
|-----|---------|------------|--------|-----------|----------|-----|-------|
| MM/AAAA | R$ | R$ | N | 50% | R$ | R$ | R$ |
| ... | | | | | | | |

**Subtotal HE + DSR:** R$ [valor]

## Reflexos habituais (Sum. 376 TST, observada OJ 394 SDI-1)

| Reflexo | Base | Calculo | Valor |
|---------|------|---------|-------|
| 13o | HE pura media | media/12 acumulado | R$ |
| Ferias + 1/3 | HE pura media periodo aquisitivo | media + 1/3 | R$ |
| Aviso previo | HE pura media ultimos 12 meses | media | R$ |
| FGTS 8% | HE + DSR + reflexos | 8% sobre total | R$ |
| Multa 40% FGTS (se cabivel) | saldo FGTS | 40% | R$ |

## Intervalo intrajornada
[se aplicavel — segmentar marco intertemporal]

**TOTAL: R$ [valor]**

## Avisos legais

> Calculo gerado por skill automatizada. **Validar contra cartao de
> ponto** e contracheques. Habitualidade depende de prova dos autos.
> OJ 394 SDI-1 TST aplicada para evitar bis in idem (DSR ja
> integrado nao volta a integrar demais reflexos).
```

## 10. FUNDAMENTACAO LEGAL

- **CF art. 7o XVI** — adicional minimo 50% das HE
- **CF art. 7o XV** — DSR
- **Lei 605/49 art. 7o §2o** — DSR sobre HE habituais
- **CLT art. 58** — duracao normal de trabalho
- **CLT art. 59** — banco de horas
- **CLT art. 59-A** — escala 12x36 (Reforma)
- **CLT art. 71 §4o** — intervalo intrajornada suprimido
  (pos-Reforma — indenizatorio)
- **CLT art. 142** — base de calculo das ferias
- **Sumula 376 TST** — reflexo das HE habituais em DSR e demais
- **Sumula 366 TST** — tolerancia de marcacao (5min/10min)
- **Sumula 437 TST** — intervalo intrajornada pre-Reforma (integral
  + reflexos)
- **OJ 394 SDI-1 TST** — vedacao da dobra do DSR nas demais verbas

## 11. PROIBICOES

1. NUNCA aplicar a "dobra do DSR" — violacao da OJ 394 SDI-1 TST
2. NUNCA usar divisor errado para a jornada efetiva
3. NUNCA aplicar reflexos sem confirmar habitualidade (Protocolo 1)
4. NUNCA aplicar regra pre-Reforma do intervalo intrajornada a
   contrato integralmente pos-11/11/2017
5. NUNCA esquecer de segmentar contrato "a cavalo"
6. NUNCA omitir adicional da CCT quando superior ao constitucional

## 12. INTEGRACAO

- **Acionada por:** `calculos-master`, `calculo-liquidacao-trabalhista`,
  `calculo-verbas-rescisorias` (para reflexos habituais em
  rescisorias), `/calculo-trabalhista`
- **Apoio:** `atualizador-indices-cache` (Selic/IPCA-E),
  `calculo-adicionais-trabalhistas` (insalub./pericul./noturno
  podem integrar base de HE)
- **Encadeia:** `protocolo-p4-calculos`

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---------------|---------|-------------------|
| Calcular adicionais (insalub./pericul./noturno) que podem integrar base | `/calculos calculo-adicionais-trabalhistas` | (este plugin) |
| Liquidacao completa da sentenca | `/calculos calculo-liquidacao-trabalhista` | (este plugin) |
| Auditar PJE-CALC do escritorio contrario | `/calculos auditar-pjecalc` | (este plugin) |
| Pericia contabil de jornada | `/trabalhista pericia-trabalhista` | `trabalhista-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar
> manualmente.
