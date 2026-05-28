---
name: calculo-repeticao-indebito
description: >
  CALCULO-REPETICAO-INDEBITO — Calcula valor a repetir em acao de
  repeticao de indebito tributario (CTN art. 165-169) ou pedido
  administrativo de restituicao/compensacao. Aplica Sum. 162 STJ
  (correcao desde o recolhimento indevido), Sum. 188 STJ (juros a
  partir do transito em julgado — caso pre-1995) e Lei 9.250/95 art.
  39 §4º (SELIC engloba correcao + juros pos-1995 nos federais).
  Sum. 461 STJ: contribuinte escolhe compensacao OU restituicao.
  NUNCA gera SELIC numerica de cabeca — consulta
  scripts/data/indices/selic-mensal.json. Use quando o advogado
  precisar quantificar acao de repeticao, pedido PER-DCOMP,
  compensacao via DCOMP ou impugnar lancamento ja pago.
---

# CALCULO-REPETICAO-INDEBITO — Repeticao de Indebito Tributario

## 1. ESCOPO

Calcula valor a ser **repetido (restituicao em dinheiro)** ou
**compensado** em pedido de repeticao de indebito tributario federal.
Produz:

- Tabela de recolhimentos indevidos (data + valor + tributo)
- Atualizacao SELIC desde cada recolhimento (Lei 9.250/95 art. 39 §4º)
- Valor total a repetir (principal corrigido)
- Opcoes do contribuinte: restituicao em dinheiro OU compensacao
  (Sum. 461 STJ)
- Calculo do prazo prescricional (CTN art. 168) e decadencial (CTN
  art. 173)

Aplica-se a: tributos federais (IR, PIS, COFINS, CSLL, IPI, INSS,
contribuicoes). Para indebito estadual/municipal, regras de juros
podem divergir — sempre conferir lei local.

---

## 2. INPUT NECESSARIO

Perguntar (ou extrair):

1. **Tributo recolhido indevidamente** (nome + codigo receita)
2. **Causa do indebito:**
   - Pagamento a maior (erro de calculo)
   - Pagamento de tributo inexistente
   - Pagamento de tributo declarado inconstitucional (modulacao do
     STF? data efeitos?)
   - Erro na base de calculo / aliquota
   - Repeticao em razao de decisao judicial transitada
3. **Lista de DARFs / GPS / guias recolhidos:** data de pagamento +
   valor + codigo receita (ate 5 anos antes do pedido — CTN art. 168)
4. **Data prevista do pedido / acao** (DD/MM/AAAA)
5. **Modalidade desejada:**
   - Repeticao em dinheiro (precatorio se judicial)
   - Compensacao via PER-DCOMP (Lei 9.430/96 art. 74)
6. **Houve transito em julgado?** Se sim, data
7. **Tributo direto (IR, CSLL) ou indireto (ICMS, IPI, PIS, COFINS)?**
   - Indireto: deve provar nao-repasse OU autorizacao do contribuinte
     de fato (CTN art. 166 + Sum. 546 STF)

---

## 3. PROCESSAMENTO

### 3.1 Prescricao (CTN art. 168 + Lei 11.105/05 art. 3º + LC 118/05)

```
Prazo: 5 anos do pagamento indevido (LC 118/05 — vigencia 09/06/2005)

Tese dos 5+5 (REVOGADA pela LC 118 a partir de 09/06/2005 — Tema 4 STJ
+ ADI 4.071) ainda vale para fatos geradores ANTES de 09/06/2005
quando ja iniciada a discussao.

CHECAGEM: data ultimo pagamento + 5 anos > data prevista do pedido?
  SIM → tempestivo
  NAO → ⚠️ ALERTA prescricao
```

### 3.2 Correcao monetaria (Sum. 162 STJ)

> "Na repeticao de indebito tributario, a correcao monetaria incide
> a partir do **pagamento indevido**."

### 3.3 Juros — regime PRE/POS Lei 9.250/95

| Periodo | Regra |
|---------|-------|
| Pagamentos anteriores a 01/01/1996 | Correcao monetaria + juros 1% am a partir do transito em julgado (Sum. 188 STJ) |
| Pagamentos a partir de 01/01/1996 (federais) | **SELIC mensal** acumulada desde o pagamento indevido — Lei 9.250/95 art. 39 §4º (SELIC engloba correcao + juros, vedado cumular outro indice) |

### 3.4 Consulta SELIC

```
Consultar: scripts/data/indices/selic-mensal.json

Para CADA recolhimento indevido:
  acumulado_SELIC = soma(SELIC_mes_seguinte ate SELIC_mes_anterior_recebimento) + 1%
  valor_corrigido = valor_pago × (1 + acumulado_SELIC/100)

Dentro do range → calculo final
Fora do range → formula + link Sicalc/PGFN
```

### 3.5 Indireto — CTN art. 166

Se tributo INDIRETO (ICMS, IPI, ISS quando repassado, PIS/COFINS):
- Avisar que **contribuinte de direito** so pode pedir restituicao se:
  (a) provar que NAO repassou o onus financeiro, OU
  (b) tiver autorizacao expressa do **contribuinte de fato**
- Sum. 546 STF: "Cabe restituicao do tributo pago indevidamente,
  quando reconhecido por decisao, que o contribuinte de jure nao
  recuperou do contribuinte de facto o quantum respectivo."

### 3.6 Compensacao (Sum. 461 STJ)

> "O contribuinte pode optar por receber, por meio de precatorio ou
> por compensacao, o indebito tributario certificado por sentenca
> declaratoria transitada em julgado."

- Compensacao = via PER-DCOMP (Lei 9.430/96 art. 74)
- Restricoes: vedada compensacao com debitos previdenciarios em
  alguns periodos; verificar IN RFB vigente.

---

## 4. OUTPUT — Memoria de Calculo

```markdown
## Memoria de calculo — repeticao de indebito

**Tributo:** [nome] (codigo [XXXX])
**Causa do indebito:** [descricao]
**Modalidade:** [restituicao | compensacao]
**Data pedido:** [DD/MM/AAAA]

---

### Checagem de prescricao (CTN art. 168)

| Item | Resultado |
|------|-----------|
| Data ultimo pagamento | [DD/MM/AAAA] |
| Prazo 5 anos vence em | [DD/MM/AAAA] |
| Data prevista do pedido | [DD/MM/AAAA] |
| **Tempestivo?** | **[SIM | ⚠️ ALERTA]** |

---

### Tabela 1 — Recolhimentos indevidos atualizados

| Data DARF | Valor pago | SELIC acumulada + 1% | Valor corrigido |
|-----------|-----------|---------------------|-----------------|
| [DD/MM/AAAA] | R$ ___ | _____% | R$ ___ |
| [DD/MM/AAAA] | R$ ___ | _____% | R$ ___ |
| [DD/MM/AAAA] | R$ ___ | _____% | R$ ___ |
| **TOTAL** | **R$ ___** | | **R$ ___** |

**Formula:** valor_corrigido = valor_pago × (1 + SELIC_acumulada / 100)

**FONTE OBRIGATORIA:** https://sicalc.receita.fazenda.gov.br/

---

### Modalidade escolhida

**[SE restituicao em dinheiro]:**
- Via PER-DCOMP (administrativa) OU acao judicial
- Acao judicial: precatorio ou RPV apos transito em julgado
- Valor corrigido pela SELIC ate efetivo pagamento

**[SE compensacao — Sum. 461 STJ]:**
- Via PER-DCOMP eletronico (Receita Federal)
- Lei 9.430/96 art. 74 + IN RFB vigente
- Permite compensar com debitos PROPRIOS administrados pela RFB
- Vedada compensacao com debitos previdenciarios em alguns
  periodos — checar IN
- Habilita-se o credito apos transito em julgado da sentenca
  declaratoria (Sum. 461 STJ)

---

### Hipotese de tributo indireto (CTN art. 166)

[SE tributo for indireto — ICMS, IPI, ISS repassado, PIS/COFINS na
fase de revenda]

⚠️ Restituicao depende de provar:
- Que o contribuinte de direito NAO repassou o onus, OU
- Ter autorizacao expressa do contribuinte de fato

Sum. 546 STF aplicavel.
```

---

## 5. FUNDAMENTACAO LEGAL

| Norma | Cobertura |
|-------|-----------|
| CTN art. 165 | Direito a restituicao do pagamento indevido |
| CTN art. 166 | Restricao para tributos indiretos |
| CTN art. 167 | Restituicao em dobro (multa) |
| CTN art. 168 | Prazo prescricional 5 anos |
| CTN art. 169 | Acao anulatoria de decisao administrativa que negou restituicao |
| Lei 9.250/95 art. 39 §4º | SELIC aplicavel a indebito tributario federal |
| Lei 9.430/96 art. 74 | Compensacao via PER-DCOMP |
| LC 118/05 art. 3º | Redefine inicio do prazo prescricional (afasta tese dos 5+5) |
| Sum. 162 STJ | Correcao desde o pagamento indevido |
| Sum. 188 STJ | Juros desde o transito em julgado (regime pre-1995) |
| Sum. 461 STJ | Escolha entre restituicao ou compensacao |
| Sum. 546 STF | Restituicao de indireto exige nao-repasse |
| Tema 69 STF | ICMS fora da base PIS/COFINS — modulacao em 15/03/2017 |
| Tema 4 STJ | Tese 5+5 valida ate LC 118 (09/06/2005) |
| Sum. 213 STJ | Mandado de seguranca eh via adequada para compensacao |
| Sum. 460 STJ | Inviavel MS convalidando compensacao realizada |

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. CONFIRMAR prazo prescricional (CTN art. 168 — 5 anos do
   pagamento). Pagamento de mais de 5 anos atras = prescrito,
   nao incluir no calculo.

2. Conferir SELIC acumulada contra Sicalc / calculadora PGFN.
   Esta skill nao tem acesso a SELIC posterior a [range_final
   do scripts/data/indices/selic-mensal.json].

3. Se tributo indireto (ICMS, IPI, ISS repassado, PIS/COFINS):
   ANEXAR prova de nao-repasse OU autorizacao do contribuinte de
   fato (CTN art. 166 + Sum. 546 STF). Sem isso, pedido sera
   indeferido.

4. Para compensacao: usar PER-DCOMP eletronico apos transito em
   julgado (Sum. 461 STJ). Verificar IN RFB vigente — algumas
   compensacoes estao vedadas (previdenciario, debitos da PGFN
   inscritos, etc.).

5. Acao judicial = precatorio/RPV — prazo de pagamento varia por
   ente federativo. Compensacao = imediata, mas sujeita a
   homologacao (5 anos).

6. Modulacao temporal (ex: Tema 69 STF — ICMS fora da base PIS/COFINS
   so produz efeitos a partir de 15/03/2017) DEVE ser respeitada.
   Pedidos anteriores podem ser indeferidos por falta de direito
   liquido.
```

---

## 7. INTEGRACAO

**Upstream:** `classificar-tipo-calculo` → identifica "indebito
tributario" → chama esta skill.

**Downstream:** `protocolo-p4-calculos` (auditoria R1-R4).

**Cross-link (sugestao soft):**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Peticao de repeticao de indebito | /tributario peticao-repeticao-indebito | tributario-societario-adv-os |
| Pedido administrativo PER-DCOMP | /contabil per-dcomp | auditoria-contabil-os |
| Mandado de seguranca p/ compensacao | /tributario ms-compensacao | tributario-societario-adv-os |
```

---

## 8. PROIBICOES

1. **NUNCA** ignorar prazo prescricional CTN art. 168 (5 anos do
   pagamento) — calcular apenas valores nao prescritos.
2. **NUNCA** aplicar juros 1% am a indebito federal pos-01/01/1996
   (Lei 9.250/95 art. 39 §4º — SELIC engloba tudo).
3. **NUNCA** omitir CTN art. 166 para tributo indireto.
4. **NUNCA** prometer restituicao em dinheiro de tributo indireto
   sem prova de nao-repasse.
5. **NUNCA** ignorar modulacao temporal de decisoes STF (Tema 69 etc.).
6. **NUNCA** gerar SELIC numerica de cabeca — sempre consultar
   `scripts/data/indices/selic-mensal.json`.
