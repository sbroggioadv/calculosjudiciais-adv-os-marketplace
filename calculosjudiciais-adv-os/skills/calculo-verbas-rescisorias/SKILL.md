---
name: calculo-verbas-rescisorias
description: >
  CALCULO-VERBAS-RESCISORIAS — Calcula todas as verbas devidas na
  rescisao do contrato de trabalho: saldo de salario, aviso previo
  indenizado (Lei 12.506/2011 — +3 dias por ano), 13o proporcional,
  ferias proporcionais + 1/3, ferias vencidas + 1/3, FGTS 8% sobre
  remuneracao do periodo, multa 40% FGTS (dispensa sem justa causa).
  SIDE-AWARE (reclamante calcula a maior, reclamada confere). Use
  quando o operador disser "verbas rescisorias", "TRCT", "calcular
  rescisao", "aviso previo proporcional", "13o proporcional", "ferias
  proporcionais", "multa 40 FGTS", "saldo salario". Considera as 6
  modalidades de rescisao (sem justa causa / com justa causa / pedido
  demissao / distrato / rescisao indireta / culpa reciproca).
---

# CALCULO-VERBAS-RESCISORIAS — Verbas devidas na rescisao do contrato

## 1. ESCOPO

Skill Tier 2 do plugin `calculosjudiciais-adv-os`. Calcula o
**Termo de Rescisao do Contrato de Trabalho (TRCT)** ou as **verbas
postuladas em reclamatoria trabalhista** decorrentes do encerramento
do contrato de trabalho — em qualquer das 6 modalidades de rescisao
previstas na CLT.

**Acionada quando o operador menciona:** verbas rescisorias, TRCT,
calcular rescisao, aviso previo proporcional, 13o proporcional,
ferias proporcionais, ferias vencidas, multa 40% FGTS, saldo de
salario, recisao indireta calculo.

## 2. SIDE-AWARENESS

| Polo | Postura do calculo |
|------|--------------------|
| **Reclamante** | Calcular a maior — incluir todas as verbas devidas no tipo de rescisao postulado, com bases salariais maiores defensaveis (media de horas extras habituais, comissoes, gorjetas, adicionais habituais que integram remuneracao). |
| **Reclamada** | Conferir o TRCT pago — apontar correta apuracao + eventual compensacao de valores ja pagos + descontos legalmente cabiveis. |

## 3. INPUT NECESSARIO

- **Modalidade da rescisao** (lista no item 5)
- **Data de admissao** e **data de saida** (dia/mes/ano)
- **Salario-base** na data da rescisao
- **Dias trabalhados no mes da rescisao**
- **Mediana de variaveis** (horas extras, comissoes, premios,
  adicionais habituais — base de calculo das parcelas correlatas)
- **Periodos aquisitivos de ferias** (vencidas nao gozadas + em
  curso)
- **Saldo do FGTS na conta vinculada** (CEF — se nao informado,
  estimar 8% sobre a remuneracao do periodo)
- **Houve aviso previo trabalhado, indenizado ou nenhum?**
- **Reflexos de horas extras habituais em rescisorias?** (se sim,
  chamar `calculo-horas-extras-reflexos` antes)

## 4. MODALIDADES DE RESCISAO — O QUE E DEVIDO EM CADA

| Modalidade | Saldo salario | Aviso previo | 13o prop. | Ferias prop. + 1/3 | Ferias venc. + 1/3 | FGTS depositado | Multa 40% FGTS | Saque FGTS | Seguro-desemprego |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Sem justa causa (empregador) | ✅ | ✅ indenizado/trabalhado | ✅ | ✅ | ✅ | ✅ | ✅ 40% | ✅ | ✅ |
| Com justa causa (empregado) | ✅ | ❌ | ❌ | ❌ | ✅ | nao deposita | ❌ | ❌ | ❌ |
| Pedido de demissao | ✅ | ❌ (devido pelo empregado se nao trabalhar) | ✅ | ✅ | ✅ | nao deposita | ❌ | ❌ | ❌ |
| Distrato (art. 484-A CLT) | ✅ | 50% | 100% | ✅ | ✅ | ✅ | 20% (metade) | 80% | ❌ |
| Rescisao indireta (art. 483 CLT) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 40% | ✅ | ✅ |
| Culpa reciproca (Sum. 14 TST) | ✅ | 50% | 50% | 50% | ✅ | ✅ | 20% | ✅ | ❌ |

## 5. FORMULAS DE CADA VERBA

### Saldo de salario
```
saldo = (dias_trabalhados_no_mes / 30) * salario_base
```

### Aviso previo indenizado (Lei 12.506/2011)
```
dias_aviso = 30 + (3 * anos_completos_de_servico)
dias_aviso_max = 90
valor = (dias_aviso / 30) * salario_base
```
- Conta-se ano completo (12 meses ou fracao >= 6 meses pela
  jurisprudencia majoritaria — `[VERIFICAR]` posicao do TRT).
- Aviso indenizado projeta o contrato (anota CTPS, conta tempo para
  ferias/13o/FGTS).

### 13o proporcional
```
meses = numero_de_meses_trabalhados_no_ano (fracao >= 15 dias = mes)
valor = (meses / 12) * salario_base
```
- Se aviso indenizado projeta para o ano seguinte, integra meses
  adicionais.

### Ferias proporcionais + 1/3
```
meses = numero_de_meses_do_periodo_aquisitivo (fracao >= 15 dias = mes)
ferias = (meses / 12) * salario_base
um_terco = ferias / 3
total = ferias + um_terco
```

### Ferias vencidas + 1/3
- **Periodo aquisitivo completo** (12 meses) **nao gozadas** ate a
  rescisao -> direito a salario integral de ferias + 1/3.
- **Em dobro** se vencido o periodo concessivo (12 meses pos
  aquisitivo) sem concessao (art. 137 CLT).
```
valor = salario_base + (salario_base / 3)
```

### FGTS sobre remuneracao do periodo
```
fgts_devido = 0.08 * remuneracao_total_do_periodo_contratual
```
- Sob a CLT, ja deveria ter sido depositado mes a mes. Aqui
  calcula-se **a diferenca** entre o devido e o efetivamente
  depositado (extrato CEF).

### Multa 40% FGTS (dispensa sem justa causa)
```
multa = 0.40 * saldo_total_FGTS_da_conta_vinculada
```
- Saldo TOTAL — inclui depositos antigos + atualizacao + acrescimos.
- No distrato (484-A) e culpa reciproca, percentual cai para **20%**.

## 6. OBSERVACOES CRITICAS

1. **Remuneracao** != **salario-base**. Inclui medias de horas extras
   habituais, adicionais habituais, comissoes, gorjetas, premios
   (apos Reforma com restricoes), DSR — tudo o que integra a
   remuneracao para fins de rescisorias.

2. **Aviso indenizado projeta o contrato** — gera reflexos
   automaticos em 13o, ferias, FGTS, INSS (OJ 82 SDI-1 TST). Nao
   esquecer.

3. **Compensacoes legais**: vale-transporte adiantado, contribuicao
   sindical descontada, adiantamentos — abater apos calcular o bruto.

4. **Multa do art. 477 §8o CLT** (atraso > 10 dias no pagto das
   rescisorias) — 1 salario adicional, devida ainda que a
   reclamatoria seja apenas para impor o pagamento. Nao confundir
   com multa do FGTS.

5. **Sumula 14 TST** (culpa reciproca) — partes pela metade nas
   verbas indenizatorias (aviso, 13o, ferias proporcionais, multa
   FGTS).

## 7. OUTPUT — MODELO

```markdown
# Verbas Rescisorias — [Reclamante x Reclamada]
**Modalidade:** [sem justa causa / etc.]
**Periodo contratual:** [DD/MM/AAAA] a [DD/MM/AAAA]
**Salario na rescisao:** R$ [valor]

## Calculo verba a verba

| Verba | Base | Calculo | Valor |
|-------|------|---------|-------|
| Saldo salario ([N] dias) | R$ [salario] | N/30 * salario | R$ [valor] |
| Aviso previo indenizado ([N] dias) | R$ [salario] | N/30 * salario | R$ [valor] |
| 13o proporcional ([N]/12) | R$ [salario] | N/12 * salario | R$ [valor] |
| Ferias proporcionais + 1/3 | R$ [salario] | (N/12 * sal) + 1/3 | R$ [valor] |
| Ferias vencidas + 1/3 | R$ [salario] | salario + 1/3 | R$ [valor] |
| FGTS do periodo | R$ [remun. total] | 8% sobre remun. | R$ [valor] |
| Multa 40% FGTS | R$ [saldo conta] | 40% sobre saldo | R$ [valor] |

**TOTAL BRUTO RESCISORIO: R$ [valor]**

## Avisos legais

> Calculo gerado por skill automatizada. Conferir contra TRCT
> oficial (extrato CEF para FGTS) antes de protocolar.
> Modalidade pressuposta: [...]. Caso o juizo reconheca modalidade
> diversa, recalcular conforme tabela do item 4.
```

## 8. FUNDAMENTACAO LEGAL

- **CLT art. 477** — TRCT, prazo de pagamento (10 dias), multa §8o
- **CLT art. 478-484-A** — modalidades de rescisao
- **CLT art. 482** — justa causa do empregado
- **CLT art. 483** — rescisao indireta (justa causa do empregador)
- **CLT art. 484-A** — distrato (Reforma 13.467/2017)
- **Lei 12.506/2011** — aviso previo proporcional (+3 dias/ano)
- **CF art. 7o III** — FGTS; XVII — 1/3 ferias
- **Sumula 14 TST** — culpa reciproca (50%)
- **Sumula 305 TST** — multa 40% FGTS inclui o saldo TOTAL
- **OJ 82 SDI-1 TST** — aviso indenizado projeta contrato
- **Sumula 7 TST** — ferias indenizadas: base = salario do periodo

## 9. PROIBICOES

1. NUNCA usar salario-base quando deve usar remuneracao
2. NUNCA esquecer projecao do aviso indenizado em 13o/ferias/FGTS
3. NUNCA calcular multa 40% so sobre depositos do contrato — e sobre
   saldo TOTAL da conta vinculada
4. NUNCA aplicar tabela da Lei 12.506 a contratos anteriores a sua
   vigencia (10/10/2011) sem segmentacao
5. NUNCA omitir aviso de validacao contra TRCT/extrato CEF

## 10. INTEGRACAO

- **Acionada por:** `calculos-master`, `calculo-liquidacao-trabalhista`,
  `/calculo-trabalhista`
- **Aciona em sequencia:** `calculo-horas-extras-reflexos` (para
  apurar reflexos habituais em rescisorias, se houver)
- **Encadeia:** `protocolo-p4-calculos`

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---------------|---------|-------------------|
| Apurar horas extras habituais com reflexos em rescisorias | `/calculos calculo-horas-extras-reflexos` | (este plugin) |
| Auditar PJE-CALC do reclamado/reclamante | `/calculos auditar-pjecalc` | (este plugin) |
| Petição inicial trabalhista | `/trabalhista peticao-inicial-trabalhista` | `trabalhista-adv-os` (Kirvano) |
| Suprema Corte R1-R4 do calculo | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar
> manualmente.
