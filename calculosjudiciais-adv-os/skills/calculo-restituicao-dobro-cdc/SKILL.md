---
name: calculo-restituicao-dobro-cdc
description: >
  CALCULO-RESTITUICAO-DOBRO-CDC — Estrutura memoria de calculo de
  restituicao em dobro do valor cobrado indevidamente em relacao de
  consumo (CDC art. 42 paragrafo unico). Identifica cobranca indevida
  (paga ou exigida), aplica multiplicador 2× sobre o valor pago em
  excesso, atualiza pela correcao monetaria do TJ desde a DATA DO
  PAGAMENTO INDEVIDO + juros 1% am desde a CITACAO. Aplica tese
  vinculante do Tema 929 STJ (engano justificavel afasta a dobra) e
  Tema 953 STJ (a dobra independe de demonstracao de ma-fe — basta
  cobranca indevida em consumo, exceto erro justificavel). Identifica
  hipoteses do superendividamento (Lei 14.181/2021) e do art. 940 CC
  (analogo civil). NUNCA aplica dobra automatica sem checar engano
  justificavel (anti-halucinacao). Use sempre que o advogado
  mencionar repeticao de indebito em consumo, cobranca indevida,
  restituicao em dobro, art. 42 CDC, Tema 929 STJ, Tema 953 STJ,
  ou cobranca abusiva de fornecedor.
---

# CALCULO-RESTITUICAO-DOBRO-CDC — Repeticao do Indebito Consumerista

## 1. ESCOPO

Memoria de calculo em 3 outputs:

1. **Classificacao da cobranca:** indevida+paga (dobra) / indevida+nao paga (so cessacao) / engano justificavel (sem dobra)
2. **Calculo da dobra:** 2× valor pago + correcao + juros
3. **Alternativa CC 940** quando nao for CDC

NAO substitui acao — gera planilha auditavel.

---

## 2. INPUT NECESSARIO

Perguntar ou propagar:

1. **Natureza:** consumo (CDC) / civil (CC) / outras
2. **Tipo cobranca indevida:** tarifa bancaria sem previsao, mensalidade pos-cancelamento, aluguel pos-rescisao, servico publico duplicado, negativacao indevida (a dobra incide sobre valor pago pra retirar, nao sobre dano moral)
3. **Valor cobrado** (cada parcela com data)
4. **Pago ou exigido?** (CDC 42 so aplica dobra ao PAGO)
5. **Data de cada pagamento** (CRUCIAL — termo inicial correcao)
6. **Data da citacao** (termo inicial juros — Sum. 54 STJ)
7. **Engano justificavel alegado?** (Tema 929 STJ)
8. **Indice de correcao** (tabela do TJ)

---

## 3. PROCESSAMENTO

### Passo 1 — Aplicar Tema 953 STJ (paradigma atual)

**Tema 953 STJ (2025, atualizado):**
> "A repeticao em dobro do indebito (art. 42, paragrafo unico, do
> CDC) e cabivel quando a cobranca indevida consubstanciar conduta
> contraria a boa-fe objetiva, sendo INDEPENDENTE de demonstracao de
> ma-fe subjetiva."

Mudanca de paradigma vs entendimento anterior (que exigia ma-fe). Hoje
basta cobranca indevida em consumo + nao se enquadrar em engano
justificavel.

### Passo 2 — Verificar engano justificavel (Tema 929 STJ)

**Tema 929 STJ:** AFASTA a dobra quando ha "engano justificavel".

Exemplos jurisprudenciais de engano justificavel (afasta dobra):
- Falha pontual de sistema sem reincidencia
- Erro do consumidor que induziu a cobranca
- Interpretacao razoavel de clausula ambigua

NAO sao engano justificavel:
- Repeticao da cobranca apos protocolo de reclamacao
- Cobranca em duplicidade
- Cobranca apos cancelamento formal

### Passo 3 — Calcular a dobra

```
para cada cobranca_indevida_paga:
  valor_dobrado = valor_pago × 2
  correcao = valor_dobrado × (idx_final / idx_pagamento - 1)
  juros = (valor_dobrado + correcao) × 0,01 × meses_desde_citacao
  total_parcela = valor_dobrado + correcao + juros

total_devolucao = soma de total_parcela de todas as cobrancas
```

### Passo 4 — Alternativa CC art. 940 (se NAO for consumo)

CC art. 940:
> "Aquele que demandar por divida ja paga, no todo ou em parte, sem
> ressalvar as quantias recebidas ou pedir mais do que for devido,
> ficara obrigado a pagar ao devedor, no primeiro caso, o DOBRO do
> que houver cobrado e, no segundo, o EQUIVALENTE do que dele exigir,
> salvo se houver prescricao."

Diferencas vs CDC 42:
- CC 940 exige DEMANDA JUDICIAL (cobrar em juizo o ja pago) — nao
  basta cobranca extrajudicial
- CC 940 exige MA-FE (Sum. 159 STF firme)
- CDC 42 nao exige ma-fe (Tema 953 STJ)

### Passo 5 — Superendividamento (Lei 14.181/2021)

Lei 14.181/2021 incluiu CDC 54-A a 54-G — superendividamento.
Aplicacao especifica para consumidores pessoas fisicas em situacao
de incapacidade de honrar dividas sem comprometer o minimo
existencial. Nao gera dobra automatica, mas pode gerar repactuacao
+ devolucao de juros abusivos.

---

## 4. OUTPUT — PLANILHA ESTRUTURADA

```markdown
## Memoria de Calculo — Restituicao em Dobro (CDC art. 42 §u)

**Atencao:** indices de correcao devem ser preenchidos pela tabela
oficial do TJ aplicavel. Esta skill NAO arbitra "engano justificavel"
— sinaliza quando o argumento aparece e deixa a tese para o advogado.

### Premissas

| Campo | Valor |
|-------|-------|
| Natureza | [consumo CDC / civil CC 940] |
| Fornecedor | [identificacao] |
| Tipo cobranca indevida | [descricao] |
| Pago ou exigido? | [pago / exigido] |
| Data da citacao | [DD/MM/AAAA] |
| Engano justificavel alegado? | [sim — descrever / nao] |
| Tabela correcao | [TJ-X — link] |

---

### Tabela 1 — Cobrancas indevidas pagas

| # | Descricao | Data pagamento | Valor pago | Dobra (×2) |
|---|-----------|----------------|------------|------------|
| 1 | Tarifa bancaria indevida out/2024 | 10/10/2024 | R$ 50,00 | R$ 100,00 |
| 2 | Mensalidade pos-cancelamento nov/2024 | 10/11/2024 | R$ 89,90 | R$ 179,80 |
| ... | ... | ... | ... | ... |

---

### Tabela 2 — Atualizacao parcela a parcela

| # | Dobra base | Correcao [TABELA] desde pagamento | Juros 1% am desde citacao | Total |
|---|------------|------------------------------------|---------------------------|-------|
| 1 | R$ 100,00 | _____ | _____ | R$ ___ |
| 2 | R$ 179,80 | _____ | _____ | R$ ___ |
| ... | ... | ... | ... | ... |

**Formula correcao:** valor_corrigido = dobra × (idx_atual / idx_pagamento)
**Formula juros:** juros = valor_corrigido × 0,01 × meses_desde_citacao

---

### Totalizacao

| Item | Valor |
|------|-------|
| Soma das dobras nominais | R$ ___ |
| Correcao monetaria total | R$ ___ |
| Juros 1% am desde citacao | R$ ___ |
| **TOTAL A RESTITUIR ATE [data]** | **R$ ___** |
| Eventual dano moral (a arbitrar) | a definir |

---

### Tese de defesa antecipada — engano justificavel (Tema 929 STJ)

Caso o fornecedor alegue engano justificavel, sinalizar contra-argumentos
para a peticao:
- [ ] Houve reclamacao previa? Quando? Houve resposta?
- [ ] Cobranca foi REPETIDA apos a reclamacao? (afasta engano)
- [ ] Falha sistemica ja documentada em outros casos? (Procon/ADC/etc.)
- [ ] Clausula contratual e clara? (se sim, nao cabe interpretacao)
```

---

## 5. AVISOS OBRIGATORIOS NO OUTPUT FINAL

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. CDC 42 §u SO SE APLICA AO VALOR PAGO — nao cabe dobra sobre valor
   apenas cobrado/exigido (se nao pagou, pede so cessacao + dano moral
   eventual).

2. TEMA 929 STJ — engano justificavel AFASTA a dobra. Identificar e
   refutar antecipadamente na peticao (cobranca repetida apos
   reclamacao = nao e engano).

3. TEMA 953 STJ — a dobra INDEPENDE de demonstracao de ma-fe (basta
   cobranca contraria a boa-fe objetiva). Mudou paradigma anterior —
   citar e ressaltar.

4. RELACAO DE CONSUMO — confirmar antes (CDC art. 2º e 3º). Se for
   civil pura, aplicar CC 940 (que exige ma-fe + demanda judicial,
   nao basta cobranca extrajudicial).

5. PRESCRICAO — CDC 27 (5 anos para acoes consumeristas) ou CC 206
   §3º IV (3 anos pra repeticao de indebito civil). Verificar termo
   inicial.

6. NEGATIVACAO INDEVIDA — em si NAO gera dobra de valor (a dobra e do
   valor cobrado, nao do dano moral). Se o consumidor PAGOU para tirar
   o nome, ai cabe dobra do valor pago.

7. CORRECAO da data do PAGAMENTO INDEVIDO (Sum. 43 STJ) + juros da
   CITACAO (responsabilidade contratual, Sum. 54 STJ a contrario
   senso — relacao contratual). Em casos de negocio juridico
   inexistente: juros da efetivacao do dano.

8. SUPERENDIVIDAMENTO (Lei 14.181/2021) — abre hipoteses adicionais
   de repactuacao e devolucao de juros abusivos, mas NAO substitui
   o CDC 42 §u.
```

---

## 6. FUNDAMENTACAO LEGAL

- **CDC art. 42 §u** — "o consumidor cobrado em quantia indevida tem
  direito a repeticao do indebito, por valor IGUAL AO DOBRO do que
  pagou em excesso, acrescido de correcao monetaria e juros legais,
  salvo hipotese de engano justificavel"
- **CDC art. 51 IV** — clausulas abusivas (limita cobranca)
- **CDC art. 2º, 3º** — definicao de consumidor e fornecedor
- **CDC art. 27** — prescricao quinquenal em consumo
- **CDC art. 54-A a 54-G** (Lei 14.181/2021) — superendividamento
- **CC art. 940** — dobra civil (exige ma-fe + demanda judicial)
- **CC art. 206 §3º IV** — prescricao trienal repeticao civil
- **Sumula 43 STJ** — correcao desde o efetivo prejuizo
- **Sumula 54 STJ** — juros da citacao em responsabilidade contratual
  / do evento danoso em extracontratual
- **Sumula 159 STF** — CC 940 exige ma-fe
- **Tema 929 STJ** — engano justificavel afasta dobra
- **Tema 953 STJ** — dobra independe de demonstracao de ma-fe
  subjetiva (mudanca de paradigma vs entendimento anterior)

---

## 7. INTEGRACAO

- **Upstream:** `calculos-master`, `classificar-tipo-calculo`,
  `identificar-tj-aplicavel`, `atualizador-indices-cache`
- **Downstream:** auto-dispara `protocolo-p4-calculos`
- **Sugestao de plugin-irmao:**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Acao de repeticao de indebito + dano moral | /ia-combativa peticao-consumidor | ia-combativa-adv-os |
| Defesa do fornecedor — engano justificavel | /ia-combativa contestacao-cdc | ia-combativa-adv-os |
| Acao de superendividamento (Lei 14.181) | /direito-familia superendividamento | direito-familia-adv-os |
| Calcular dano moral compativel com Tema 929 | /calculos calculo-danos-indenizatorios | (interno) |
| Auditar calculo (R1-R4) antes do protocolo | /calculos protocolo-p4 | (interno) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.
```

---

## 8. PROIBICOES

1. **NUNCA aplicar dobra sobre valor apenas exigido** — so sobre o
   efetivamente pago (CDC 42 §u literal).
2. **NUNCA confundir CDC 42 com CC 940** — CDC nao exige ma-fe (Tema
   953 STJ); CC exige (Sum. 159 STF).
3. **NUNCA omitir verificacao de engano justificavel** (Tema 929) —
   defesa standard.
4. **NUNCA aplicar dobra em relacao civil pura** sem analisar CC 940
   (regimes distintos).
5. **NUNCA usar correcao desde a citacao** — e desde a DATA DO
   PAGAMENTO INDEVIDO (Sum. 43 STJ).
6. **NUNCA pedir dobra sobre dano moral** — a dobra e do VALOR
   cobrado/pago, nao do dano. Dano moral tem calculo proprio
   (`calculo-danos-indenizatorios`).
