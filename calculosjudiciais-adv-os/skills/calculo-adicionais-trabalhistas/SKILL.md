---
name: calculo-adicionais-trabalhistas
description: >
  CALCULO-ADICIONAIS-TRABALHISTAS — Calcula adicionais legais:
  insalubridade (10/20/40% NR 15, com debate Sumula Vinculante 4 STF
  vs OJ 415 SDI-1 TST sobre base de calculo), periculosidade (30%
  sobre salario base — CLT 193 §1o + NR 16), noturno urbano (>=20%,
  hora reduzida 52'30'' — CLT 73) e noturno rural (Lei 5.889/73).
  Inclui intervalo intrajornada suprimido com segmentacao
  pre/pos-Reforma 13.467/2017. SIDE-AWARE. Sinaliza necessidade de
  pericia (CLT 195) para insalub./pericul. Use quando o operador
  disser "adicional de insalubridade", "periculosidade", "noturno",
  "NR 15", "NR 16", "Sumula Vinculante 4", "OJ 415 SDI-1".
---

# CALCULO-ADICIONAIS-TRABALHISTAS — Insalubridade, Periculosidade, Noturno

## 1. ESCOPO

Skill Tier 2 do plugin `calculosjudiciais-adv-os`. Calcula os
**adicionais legais** previstos na CLT e na CF para condicoes
especiais de trabalho: **insalubridade**, **periculosidade**,
**noturno (urbano e rural)** e **intervalo intrajornada suprimido**.

**Acionada quando o operador menciona:** adicional de insalubridade,
periculosidade, adicional noturno, hora noturna reduzida, NR 15, NR
16, Sumula Vinculante 4, OJ 415 SDI-1, intervalo intrajornada,
agente insalubre, atividade perigosa.

## 2. SIDE-AWARENESS

| Polo | Postura do calculo |
|------|--------------------|
| **Reclamante** | Calcular **a maior** — defender grau maximo do agente (insalubridade 40% se enquadravel, periculosidade integral 30%), defender base de calculo mais favoravel (OJ 415 SDI-1 TST = salario base ou da norma coletiva; SV 4 STF = salario minimo so na ausencia de regra), reflexos plenos em DSR/13o/ferias/aviso/FGTS. |
| **Reclamada** | Conferir o grau pleiteado contra laudo pericial, defender base salario minimo (SV 4 STF) quando o titulo nao fixou outra, restringir reflexos a habitualidade comprovada, conferir CCT (pode definir base distinta). |

## 3. INPUT NECESSARIO

- **Tipo do adicional postulado** (insalub. / pericul. / noturno /
  intrajornada)
- **Grau** (insalub. mínimo/médio/máximo) ou **percentual** (CCT
  pode majorar)
- **Salario-base**
- **Periodo** (com marco intertemporal 11/11/2017 — Reforma —
  relevante para intervalo intrajornada)
- **Laudo pericial existe?** (se sim, qual o agente caracterizado e
  qual a base de calculo determinada)
- **Houve uso/fornecimento de EPI eficaz?** (afasta insalub. — Sum.
  80 TST; nao afasta pericul.)
- **Sentenca/CCT fixou base de calculo distinta?**

## 4. INSALUBRIDADE — CLT art. 192 + NR 15 do MTb

### Percentuais
| Grau | Percentual |
|------|------------|
| Minimo | 10% |
| Medio | 20% |
| Maximo | 40% |

### Base de calculo — DEBATE CONSOLIDADO
- **Sumula Vinculante 4 STF**: vedacao do uso do salario minimo
  como indexador. Porem, o STF declarou que **enquanto nao houver
  regra legal/coletiva expressa**, o **salario minimo permanece**
  como base — **provisoriamente** — para evitar vacuo (modulacao
  por seguranca juridica).
- **OJ 415 SDI-1 TST** (ressalvada apos SV 4): se houver **salario
  basico** definido em norma coletiva, em lei especial ou na
  propria sentenca, este prevalece sobre o salario minimo.
- **Pratica**: na duvida, calcular **dois cenarios** (sobre SM e
  sobre salario base) e apresentar ambos com fundamentacao.

```
adicional_insalub = base_de_calculo * grau_percentual
```

### EPI eficaz (Sumula 80 TST)
Fornecimento e uso comprovado de EPI eficaz **elimina** o direito
ao adicional de insalubridade. Verificar fichas de EPI e CAT.

### Pericia obrigatoria (CLT art. 195)
A caracterizacao da insalubridade **depende de pericia tecnica**
(engenheiro/medico do trabalho). Sem pericia, **nao se condena**.

## 5. PERICULOSIDADE — CLT art. 193 + NR 16 do MTb

### Percentual
- **30%** sobre **salario base** (CLT 193 §1o — base e taxativa, NAO
  inclui adicionais nem gratificacoes).

### Atividades caracterizadas (NR 16)
Explosivos, inflamaveis, energia eletrica, radiacoes ionizantes,
seguranca patrimonial (vigilantes), motociclistas (Lei 12.997/2014
incluiu).

### EPI nao afasta
Diferente da insalub., o uso de EPI **NAO afasta** o adicional de
periculosidade — o risco e potencial e nao se elimina.

### Tempo de exposicao
Exposicao **intermitente** com habitualidade gera direito ao
adicional integral (Sum. 364 TST). So afasta se for **eventual**
ou por **tempo extremamente reduzido**.

### Pericia obrigatoria (CLT art. 195)
Igual a insalubridade — sem laudo, sem condenacao.

## 6. NOTURNO URBANO — CLT art. 73

- **Periodo noturno**: 22h00 as 05h00 (urbano)
- **Adicional minimo**: **20%** sobre a hora diurna (CCT pode
  majorar)
- **Hora noturna reduzida**: **52 minutos e 30 segundos** (so para
  fins de **contagem** — a cada 52'30'' computa-se 1h)

### Calculo
```
hora_noturna_reduzida = hora_diurna * (60 / 52.5)  # fator 1.1428...
valor_hora_noturna_normal = valor_hora_diurna * (60/52.5)
valor_hora_noturna_com_adicional = valor_hora_noturna_normal * 1.20
adicional_noturno_total = valor_hora * 1.20 (ou %CCT) * horas_efetivas
```

### Prorrogacao do horario noturno (Sum. 60 TST)
Quando a jornada **inicia no periodo noturno e se prolonga apos
05h00**, o **adicional noturno persiste** sobre as horas
prorrogadas — nao se desliga ao raiar do dia.

## 7. NOTURNO RURAL — Lei 5.889/73 art. 7o

- **Lavoura**: 21h00 as 05h00
- **Pecuaria**: 20h00 as 04h00
- **Adicional**: **25%** sobre a hora diurna
- **Hora NAO** e reduzida (sem fator 52'30'') — diferenca chave

## 8. INTERVALO INTRAJORNADA SUPRIMIDO

Ver detalhamento na skill `calculo-horas-extras-reflexos` item 7.
Resumo do marco intertemporal:
- **Pre-Reforma (ate 10/11/2017)**: integral + adicional 50% + com
  reflexos (Sum. 437 TST)
- **Pos-Reforma (a partir de 11/11/2017)**: so o tempo suprimido +
  adicional 50% + **indenizatorio** sem reflexos (CLT 71 §4o nova
  redacao)

## 9. CUMULACAO E REFLEXOS

### Cumulacao insalub. + pericul. (Tema vigente)
A regra geral e a **opcao** (CLT 193 §2o) — empregado escolhe o
mais favoravel. Ha decisoes que admitem cumulacao com base em
convencoes da OIT (155 e 161) — `[VERIFICAR]` jurisprudencia
atualizada do TST/STF. Por seguranca, calcular ambos e indicar o
mais vantajoso.

### Habitualidade e reflexos
Adicional pago com habitualidade tem natureza salarial — reflete em
DSR, 13o, ferias + 1/3, aviso previo, FGTS. Aplicar com observancia
da **OJ 394 SDI-1 TST** (nao dobrar DSR).

## 10. OUTPUT — MODELO

```markdown
# Adicionais Trabalhistas — [Reclamante]
**Adicional postulado:** [tipo]
**Grau/percentual:** [N%]
**Base de calculo defendida:** [salario minimo / salario base / CCT]
**Periodo:** [MM/AAAA] a [MM/AAAA]
**Laudo pericial:** [sim/nao + sintese]

## Apuracao

| Item | Base | Percentual | Periodo | Valor |
|------|------|------------|---------|-------|
| Adicional principal | R$ [base] | N% | [meses] | R$ [valor] |
| Reflexo DSR (Sum. 376) | R$ [adic] | dias_desc/dias_uteis | | R$ |
| Reflexo 13o | R$ [adic puro — OJ 394] | media/12 | | R$ |
| Reflexo ferias + 1/3 | R$ [adic puro] | media + 1/3 | | R$ |
| Reflexo aviso previo | R$ [adic puro] | media 12 meses | | R$ |
| Reflexo FGTS 8% | R$ [adic + reflexos] | 8% | | R$ |
| Multa 40% FGTS (se cabivel) | R$ [saldo] | 40% | | R$ |

**TOTAL: R$ [valor]**

## Avisos legais

> Calculo gerado por skill automatizada. **Adicionais de insalub. e
> pericul. dependem de PERICIA (CLT 195) — sem laudo, nao se
> condena.** EPI eficaz afasta insalub. (Sum. 80 TST); NAO afasta
> pericul.
>
> Debate SV 4 STF x OJ 415 SDI-1 TST — base de calculo: na ausencia
> de regra legal/coletiva, salario minimo permanece provisoriamente.
> Verificar entendimento do TRT/TST no momento.
```

## 11. FUNDAMENTACAO LEGAL

- **CLT art. 192** — insalubridade (10/20/40%)
- **CLT art. 193** — periculosidade (30% sobre salario base)
- **CLT art. 193 §2o** — opcao (cumulacao vedada na regra geral)
- **CLT art. 195** — pericia obrigatoria
- **CLT art. 73** — noturno urbano (20%, hora reduzida 52'30'')
- **CLT art. 71 §4o** — intervalo intrajornada pos-Reforma
- **Lei 5.889/73 art. 7o** — noturno rural (25%, sem reducao)
- **Lei 12.997/2014** — incluiu motociclista na pericul.
- **NR 15** — agentes insalubres e graus
- **NR 16** — atividades perigosas
- **Sumula Vinculante 4 STF** — vedacao salario minimo como
  indexador (com modulacao)
- **OJ 415 SDI-1 TST** — base salario basico se previsto
- **Sumula 80 TST** — EPI eficaz afasta insalub.
- **Sumula 364 TST** — exposicao intermitente integra pericul.
- **Sumula 60 TST** — prorrogacao do noturno mantem adicional
- **Sumula 437 TST** — intervalo intrajornada pre-Reforma
- **Sumula 139 TST** — adicional de insalub. integra remuneracao

## 12. PROIBICOES

1. NUNCA calcular insalub./pericul. **sem aviso de necessidade de
   pericia** (CLT 195)
2. NUNCA cumular insalub. + pericul. sem flag `[VERIFICAR]`
3. NUNCA usar EPI eficaz para afastar **periculosidade** (so
   insalub.)
4. NUNCA aplicar hora reduzida 52'30'' a noturno **rural**
5. NUNCA omitir o debate SV 4 STF vs OJ 415 SDI-1 quando a base e
   controversa
6. NUNCA aplicar regra pos-Reforma de intervalo intrajornada a
   contrato pre-11/11/2017

## 13. INTEGRACAO

- **Acionada por:** `calculos-master`, `calculo-liquidacao-trabalhista`,
  `calculo-horas-extras-reflexos` (adicional integra base de HE),
  `/calculo-trabalhista`
- **Apoio:** `atualizador-indices-cache`
- **Encadeia:** `protocolo-p4-calculos`

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---------------|---------|-------------------|
| Apurar HE com base que integra adicional habitual | `/calculos calculo-horas-extras-reflexos` | (este plugin) |
| Quesitos tecnicos para o perito do trabalho | `/calculos gerador-quesitos-perito-contabil` | (este plugin — adaptar para insalub./pericul.) |
| Pericia trabalhista completa | `/trabalhista pericia-trabalhista` | `trabalhista-adv-os` (Kirvano) |
| Auditar PJE-CALC do escritorio contrario | `/calculos auditar-pjecalc` | (este plugin) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar
> manualmente.
