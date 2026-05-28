---
name: calculo-tributo-federal-selic
description: >
  CALCULO-TRIBUTO-FEDERAL-SELIC — Atualiza debito de tributo federal
  (IRPF, IRPJ, CSLL, PIS, COFINS, IPI, contribuicoes federais) pela
  SELIC acumulada (CTN art. 161 + Lei 9.430/96 art. 61). Aplica multa
  de mora 0,33%/dia limitada a 20% (art. 61 § 2º Lei 9.430/96) e
  juros SELIC mensal + 1% no mes do recolhimento. NUNCA gera SELIC
  numerica de cabeca — consulta scripts/data/indices/selic-mensal.json
  e devolve formula + link Sicalc se fora do range. Use quando o
  advogado precisar atualizar debito federal, simular DARF de
  parcelamento, conferir lancamento de auto de infracao federal ou
  preparar pedido de retificacao de pagamento (DCTF/PER-DCOMP).
---

# CALCULO-TRIBUTO-FEDERAL-SELIC — Atualizacao de Debito Federal

## 1. ESCOPO

Calcula atualizacao de **tributo federal em atraso** (CTN art. 161 +
Lei 9.430/96 art. 61), produzindo:

- Multa de mora (0,33%/dia × dias de atraso, **limitada a 20%**)
- Juros SELIC mensal acumulada (do mes seguinte ao vencimento ate o
  mes anterior ao pagamento)
- Juros 1% no mes do efetivo recolhimento (regra do art. 61 §3º)
- Valor total atualizado para DARF / parcelamento / impugnacao

Aplica-se a: **IRPF, IRPJ, CSLL, PIS, COFINS, IPI, IOF, ITR,
contribuicoes federais (INSS patronal/empregado, contribuicoes a
terceiros — Sistema S), CIDE.**

NAO aplica a: ICMS (estadual — Selic ou taxa propria por UF), ISS
(municipal), tributos com regime especial (ex: Simples — Lei
Complementar 123/06 tem regra propria).

---

## 2. INPUT NECESSARIO

Perguntar ao operador (ou extrair do contexto):

1. **Tributo** (IRPJ, PIS, COFINS, etc.) + **codigo da receita** (4
   digitos — ex: 2089 IRPJ Lucro Real, 8109 PIS, 2172 COFINS)
2. **Valor original do tributo** (R$ — base do debito, sem multa nem
   juros)
3. **Data de vencimento original** (DD/MM/AAAA)
4. **Data prevista do pagamento** (DD/MM/AAAA) — para calculo dos dias
   de mora
5. **Houve denuncia espontanea?** (CTN art. 138 — afasta multa de mora
   se pago antes de qualquer procedimento fiscal)
6. **Esta sob fiscalizacao / auto de infracao lavrado?** Se sim, qual
   multa (75% — passiva, 150% — qualificada, ou outra)
7. **Tipo de pagamento:** DARF avulso · parcelamento ordinario (Lei
   10.522/02) · parcelamento especial (PERT, REFIS, etc.)

---

## 3. PROCESSAMENTO

### 3.1 Composicao do debito (Lei 9.430/96 art. 61)

```
DEBITO TOTAL = PRINCIPAL + MULTA DE MORA + JUROS SELIC
```

### 3.2 Multa de mora (art. 61 caput)

```
multa = 0,33% × dias_atraso × principal
LIMITE: max 20% do principal
```

**Atencao:** se pago dentro do prazo (D+0), multa = 0. Conta-se a
partir do **primeiro dia util seguinte ao vencimento**.

### 3.3 Juros SELIC (art. 61 §3º)

```
juros = principal × (SOMA_SELIC_MENSAL + 1%)
```

Onde `SOMA_SELIC_MENSAL` = soma das SELIC mensais publicadas pelo BCB,
do **mes seguinte ao vencimento ate o mes ANTERIOR ao pagamento**.

O **1% adicional** corresponde ao mes do efetivo pagamento (regra
fixa, nao consulta tabela).

### 3.4 Consulta SELIC

```
Consultar: scripts/data/indices/selic-mensal.json

Dentro do range [range_inicial, range_final]:
  → valor final calculado com SELIC verificada

Fora do range:
  → formula + link Sicalc (https://sicalc.receita.fazenda.gov.br/)
  → placeholder _____ no campo SELIC
```

### 3.5 Denuncia espontanea (CTN art. 138)

Se operador respondeu **SIM**:
- ZERAR multa de mora (afastada por denuncia espontanea)
- Manter juros SELIC integralmente (Sum. 360 STJ: denuncia espontanea
  nao afasta juros)
- Avisar: "denuncia espontanea valida APENAS se pago ANTES de qualquer
  procedimento fiscal (notificacao, intimacao, inicio de fiscalizacao)"

### 3.6 Auto de infracao lavrado

Se operador informou **multa de oficio (75% ou 150%)**:
- NAO aplicar multa de mora (substituida pela multa de oficio)
- Calcular multa de oficio sobre o principal (75% — passiva; 150% —
  qualificada por sonegacao/fraude/conluio)
- Juros SELIC normal sobre principal
- Considerar reducoes do art. 6º Lei 8.218/91 (50% se pago em 30 dias,
  40% se parcelado em 30 dias, etc.)

---

## 4. OUTPUT — Memoria de Calculo

```markdown
## Memoria de calculo — atualizacao tributo federal

**Tributo:** [nome] (codigo receita [XXXX])
**Principal original:** R$ [valor]
**Vencimento original:** [DD/MM/AAAA]
**Data prevista pagamento:** [DD/MM/AAAA]
**Dias de atraso:** [N]

---

### Tabela 1 — Multa de mora (Lei 9.430/96 art. 61)

| Calculo | Valor |
|---------|-------|
| 0,33% × [N] dias × R$ [principal] | R$ ___ |
| Limite legal (20% do principal) | R$ ___ |
| **Multa devida (menor entre os dois)** | **R$ ___** |

---

### Tabela 2 — Juros SELIC (Lei 9.430/96 art. 61 §3º)

| Mes | SELIC mensal | Acumulado |
|-----|--------------|-----------|
| [mes vencimento + 1] | _____% | _____% |
| ... | _____% | _____% |
| [mes anterior pagamento] | _____% | _____% |
| **Mes do pagamento** | **1,00% (fixo)** | _____% |
| **TOTAL SELIC + 1%** | | **_____%** |

**Juros = R$ [principal] × _____%  =  R$ ___**

**FONTE OBRIGATORIA:** https://sicalc.receita.fazenda.gov.br/

---

### Totalizacao

| Verba | Valor |
|-------|-------|
| Principal | R$ ___ |
| Multa de mora (max 20%) | R$ ___ |
| Juros SELIC + 1% | R$ ___ |
| **TOTAL ATUALIZADO ATE [data]** | **R$ ___** |

---

### Codigo de receita para DARF

| Campo DARF | Valor |
|------------|-------|
| Codigo receita | [XXXX] |
| Periodo apuracao | [MM/AAAA] |
| Data vencimento | [DD/MM/AAAA] |
| Numero referencia | (preencher se houver) |
```

---

## 5. FUNDAMENTACAO LEGAL

| Norma | Cobertura |
|-------|-----------|
| CTN art. 161 | Juros de mora — taxa = 1% am salvo lei especial |
| Lei 9.430/96 art. 61 caput | Multa de mora 0,33%/dia, max 20% |
| Lei 9.430/96 art. 61 §3º | Juros SELIC mensal + 1% no mes do pagamento |
| Lei 8.218/91 art. 6º | Reducao de multa de oficio (50%/40%/30%) |
| CTN art. 138 | Denuncia espontanea — afasta multa, nao afasta juros |
| Sum. 360 STJ | Denuncia espontanea nao afasta juros |
| Sum. 436 STJ | DCTF/declaracao confessada nao precisa lancamento |
| Tema 444 STJ | Multa de oficio limita-se a 20% se ha falta de pagamento sem fraude |

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE GERAR DARF:

1. Conferir valor contra Sicalc da Receita Federal:
   https://sicalc.receita.fazenda.gov.br/sicalc/principal
   (calculadora oficial — gera DARF com codigo de barras valido).

2. SELIC mensal flutua — conferir mes a mes contra publicacao do
   BCB ou Sicalc. Esta skill nao tem acesso a SELIC posterior a
   [range_final do scripts/data/indices/selic-mensal.json].

3. Se ha auto de infracao: confirmar multa aplicada (75% / 150% /
   outra) e prazos de reducao (Lei 8.218/91 art. 6º).

4. Se denuncia espontanea: certificar que NAO ha procedimento
   fiscal iniciado (CTN art. 138 + Sum. 360 STJ).

5. Pagamento gera presuncao de quitacao apenas do principal — se
   houver duvida sobre composicao, abrir PER-DCOMP ou pedido
   administrativo de retificacao.
```

---

## 7. INTEGRACAO

**Upstream:** `classificar-tipo-calculo` (roteador) → identifica
"tributo federal" → chama esta skill.

**Downstream:** `protocolo-p4-calculos` (auditoria R1-R4 default-on).

**Cross-link (sugestao soft, nao executa):**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Impugnar lancamento administrativo | /tributario impugnacao-auto-infracao | tributario-societario-adv-os |
| Pedido de retificacao DCTF | /contabil retificar-dctf | auditoria-contabil-os |
| Defesa em execucao fiscal | /execucao embargos-execucao | execucao-adv-os |
```

---

## 8. PROIBICOES

1. **NUNCA** gerar SELIC numerica de cabeca — sempre consultar
   `scripts/data/indices/selic-mensal.json`.
2. **NUNCA** aplicar multa > 20% do principal (limite legal absoluto
   art. 61 caput).
3. **NUNCA** confundir multa de mora (atraso simples) com multa de
   oficio (auto de infracao 75/150%).
4. **NUNCA** zerar juros SELIC em denuncia espontanea (Sum. 360 STJ).
5. **NUNCA** aplicar SELIC a tributo estadual/municipal (cada UF/Mun
   tem regra propria — usar skill especifica ou contadoria local).
6. **NUNCA** omitir aviso de validacao via Sicalc.
