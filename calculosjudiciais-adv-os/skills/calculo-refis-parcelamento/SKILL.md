---
name: calculo-refis-parcelamento
description: >
  CALCULO-REFIS-PARCELAMENTO — Simulador de parcelamento de debito
  federal em programas especiais (PERT, REFIS, PRR, parcelamento
  ordinario Lei 10.522/02) ou parcelamentos estaduais/municipais.
  Recebe debito atualizado + condicoes do programa (% desconto multa,
  % desconto juros, qtd parcelas, taxa de atualizacao das parcelas).
  Devolve: fluxo de pagamento mes a mes + total a pagar + total
  economizado vs pagamento integral. Cita lei do programa especifico
  (PERT = Lei 13.496/17; ordinario = Lei 10.522/02). Use quando o
  advogado precisar simular adesao a parcelamento, comparar regimes,
  avaliar custo-beneficio de programa especial ou orientar cliente
  sobre prestacao mensal.
---

# CALCULO-REFIS-PARCELAMENTO — Simulador de Parcelamento

## 1. ESCOPO

Simula adesao a **parcelamento** de debito tributario federal,
estadual ou municipal. Produz:

- Fluxo de pagamento mes a mes (parcela 1, 2, ..., N)
- Valor da parcela minima legal (se houver — ex: R$ 200 PJ / R$ 100 PF
  no ordinario federal)
- Total nominal a pagar (soma das parcelas)
- Total economizado vs pagamento integral (descontos de multa/juros)
- Aviso explicito sobre lei do programa + data limite de adesao

NAO calcula:
- Debito original — recebe ja **atualizado** (vindo de
  `calculo-tributo-federal-selic` ou similar)
- Atualizacao SELIC mes a mes das parcelas futuras — sinaliza apenas
  que parcelas sao atualizadas pela SELIC (regra geral)

---

## 2. INPUT NECESSARIO

Perguntar (ou extrair do contexto):

1. **Debito atualizado** (principal + multa + juros) — R$ [valor]
2. **Composicao detalhada do debito:**
   - Principal: R$ ___
   - Multa: R$ ___ (de mora ou de oficio)
   - Juros SELIC: R$ ___
3. **Programa de parcelamento:** PERT / REFIS / PRR / ordinario Lei
   10.522/02 / parcelamento estadual / municipal
4. **Lei do programa** (texto e versao vigente — programa especifico
   pode ter mudado)
5. **Numero de parcelas pretendido**
6. **Houve adesao a programa anterior?** (alguns programas vedam
   readesao — ex: PERT vedou para quem desistiu)
7. **Tipo de garantia** (se exigida — fianca, deposito, alienacao
   fiduciaria)
8. **Modalidade:** entrada + parcelas? Pagamento integral em parcela
   unica com desconto?

---

## 3. PROCESSAMENTO

### 3.1 Validacao do programa

```
SE programa = "PERT" (Lei 13.496/17):
  → atencao: programa ENCERRADO em 31/10/2017 para adesao geral
  → reabriu pontualmente para alguns debitos especificos
  → CONFIRMAR vigencia atual antes de seguir

SE programa = "ordinario" (Lei 10.522/02):
  → SEMPRE vigente
  → max 60 parcelas (regra geral)
  → parcela minima: R$ 200 PJ / R$ 100 PF
  → SEM descontos
  → garantia: ANTECIPAR 1 parcela = 1 mes

SE programa = "REFIS / PERT / outro especial":
  → REQUER consulta a lei vigente
  → descontos variam (PERT chegava a 90% multa + 50% juros + entrada 5%)
  → quase sempre ENCERRADO — confirmar
```

### 3.2 Aplicar descontos (se programa especial vigente)

```
multa_com_desconto = multa × (1 - desconto_multa%)
juros_com_desconto = juros × (1 - desconto_juros%)

debito_final = principal + multa_com_desconto + juros_com_desconto
```

### 3.3 Calcular parcela

```
valor_parcela = debito_final / N_parcelas

SE valor_parcela < parcela_minima_legal:
  → reduzir N_parcelas ate atingir parcela minima
  → alertar operador
```

### 3.4 Atualizacao das parcelas futuras

Regra geral: parcelas futuras sao **atualizadas pela SELIC** a partir
do mes seguinte ao parcelamento (cada parcela = valor_parcela ×
fator_SELIC_acumulado_ate_o_mes).

Esta skill NAO calcula a SELIC futura (impossivel — depende de
politica monetaria) — apenas sinaliza a regra.

### 3.5 Calculo do economizado

```
total_integral = principal + multa + juros
total_parcelado = debito_final (com descontos)
economia = total_integral - total_parcelado
percentual_economia = (economia / total_integral) × 100
```

---

## 4. OUTPUT — Simulacao de Parcelamento

```markdown
## Simulacao — parcelamento [PROGRAMA]

**Programa:** [PERT / ordinario / outro]
**Base legal:** [Lei XXX/AAAA art. XX]
**Vigencia confirmada:** [SIM — ate DD/MM/AAAA] | [⚠️ CONFIRMAR]
**Data simulacao:** [DD/MM/AAAA]

---

### Composicao do debito (situacao atual)

| Verba | Valor |
|-------|-------|
| Principal | R$ ___ |
| Multa | R$ ___ |
| Juros SELIC | R$ ___ |
| **Total integral (sem parcelamento)** | **R$ ___** |

---

### Descontos do programa

| Verba | Original | % Desconto | Com desconto |
|-------|----------|-----------|--------------|
| Principal | R$ ___ | 0% (nunca) | R$ ___ |
| Multa | R$ ___ | ___% | R$ ___ |
| Juros | R$ ___ | ___% | R$ ___ |
| **Debito final apos descontos** | | | **R$ ___** |

---

### Plano de parcelamento

| Item | Valor |
|------|-------|
| Numero de parcelas | [N] |
| Valor da parcela (1a) | R$ ___ |
| Parcela minima legal | R$ [200 PJ / 100 PF / variavel] |
| Atualizacao das parcelas | SELIC mensal acumulada |
| Garantia exigida? | [Sim — tipo / Nao] |

---

### Fluxo de pagamento (primeiras 6 parcelas — referencia)

| Mes | Parcela base | Atualizacao SELIC | Parcela final |
|-----|--------------|-------------------|---------------|
| 1 | R$ ___ | 0% (mes adesao) | R$ ___ |
| 2 | R$ ___ | _____% | R$ ___ |
| 3 | R$ ___ | _____% | R$ ___ |
| ... | ... | ... | ... |

*Parcelas atualizadas pela SELIC — valores reais flutuam.*

---

### Resumo economico

| Item | Valor |
|------|-------|
| Pagamento integral hoje | R$ ___ |
| Pagamento parcelado (total nominal) | R$ ___ |
| **Economia em valores nominais** | **R$ ___** |
| Percentual economizado | _____% |

*Atencao: economia nominal nao considera custo de oportunidade do
dinheiro. Comparar contra rentabilidade da aplicacao financeira
disponivel ao cliente (ex: Selic + 1% am do parcelamento vs 100% CDI
de uma aplicacao).*
```

---

## 5. FUNDAMENTACAO LEGAL

| Norma | Cobertura |
|-------|-----------|
| Lei 10.522/02 | Parcelamento ordinario federal (60 parcelas, sem descontos) |
| Lei 13.496/17 (PERT) | Programa Especial Regularizacao Tributaria — encerrado 31/10/2017 |
| Lei 13.043/14 | REFIS especifico (encerrado) |
| Lei 12.996/14 | REFIS da Copa (encerrado) |
| LC 123/06 art. 21 | Parcelamento Simples Nacional (60 parcelas) |
| MP 1.090/21 / Lei 14.375/22 | Transacao tributaria — alternativa a parcelamento |
| Portaria PGFN 14.402/20 | Transacao na divida ativa da Uniao |
| Sum. 437 STJ | Inclusao em parcelamento pressupoe pagamento de 1a parcela |
| Sum. 555 STJ | Quando ha defeito no titulo, parcelamento nao afasta nulidade |

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE ADERIR:

1. CONFIRMAR vigencia do programa na fonte oficial. Programas
   especiais (PERT, REFIS, PRR) sao temporarios e quase sempre
   ENCERRADOS — usar Sicalc / PGFN / Receita para confirmar.

2. Adesao = CONFISSAO DE DIVIDA (CTN art. 174 e legislacao do
   programa) → IMPOSSIVEL discutir o debito apos. Avaliar se ha
   chance real de exito em impugnacao antes de aderir.

3. Atrasos em parcelas (geralmente 3 consecutivas ou 6 alternadas)
   geram rescisao automatica do parcelamento + exigibilidade
   integral do saldo + inscricao em divida ativa.

4. Comparar custo do parcelamento (SELIC + 1% am) com:
   - Custo de oportunidade do capital
   - Custo de credito alternativo (CDC, financiamento)
   - Transacao tributaria (MP 1.090/21) — pode ter desconto maior

5. Simulacao gerada pode divergir de calculo oficial do programa
   (Sicalc / sistema da PGFN) — usar como referencia, NAO como
   fonte unica.

6. Em parcelamento de debito em discussao judicial → renuncia
   IMPLICITA a acao (art. 38 Lei 13.496/17 e similares). Avaliar
   antes de aderir.
```

---

## 7. INTEGRACAO

**Upstream:** `calculo-tributo-federal-selic` (gera debito atualizado
que vira input desta skill).

**Downstream:** `protocolo-p4-calculos` (auditoria R1-R4).

**Cross-link (sugestao soft, nao executa):**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Pedido de transacao tributaria PGFN | /tributario transacao-pgfn | tributario-societario-adv-os |
| Defesa de execucao fiscal | /execucao embargos-execucao | execucao-adv-os |
| Auditar legalidade do lancamento | /tributario impugnacao-administrativa | tributario-societario-adv-os |
```

---

## 8. PROIBICOES

1. **NUNCA** afirmar que PERT/REFIS/programa especial esta vigente
   sem CONFIRMACAO explicita do operador + fonte oficial.
2. **NUNCA** prometer economia que dependa de SELIC futura — SELIC
   flutua, parcelas atualizadas podem subir.
3. **NUNCA** omitir aviso de que adesao = confissao de divida.
4. **NUNCA** simular parcelamento abaixo da parcela minima legal sem
   reduzir o N.
5. **NUNCA** omitir comparacao com transacao tributaria (alternativa
   mais vantajosa em alguns casos).
6. **NUNCA** ignorar que parcelas atrasadas geram rescisao.
