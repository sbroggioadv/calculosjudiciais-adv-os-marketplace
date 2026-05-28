---
name: calculo-alimentos-atrasados
description: >
  CALCULO-ALIMENTOS-ATRASADOS — Estrutura memoria de calculo de
  alimentos vencidos e nao pagos (rito CPC 528 prisao OU CPC 530
  expropriacao). Identifica parcelas vencidas mes a mes + correcao
  monetaria pela tabela do TJ aplicavel + juros 1% am desde cada
  vencimento + multa contratual se houver. Marca a janela da
  Sumula 309 STJ (3 ultimas vencidas + as que vencerem no curso da
  execucao = autorizam prisao civil; demais = rito expropriacao).
  Sinaliza Tema 1.137 STJ (2026) sobre suspensao de CNH/passaporte.
  Distingue alimentos preteritos (cobranca comum, sem prisao) de
  proximos. NUNCA gera valor final com indices hardcoded (anti-
  halucinacao). Use sempre que o advogado mencionar alimentos
  atrasados, execucao de alimentos, prisao civil, Sumula 309,
  pensao alimenticia em atraso, cumprimento de sentenca alimentar
  ou rito CPC 528/530.
---

# CALCULO-ALIMENTOS-ATRASADOS — Execucao de Alimentos

## 1. ESCOPO

Estrutura memoria de calculo para execucao de alimentos com 3 outputs
auditaveis:

1. **Tabela de parcelas** (vencidas mes a mes — principal, correcao,
   juros, total por parcela)
2. **Segmentacao da Sumula 309 STJ** (janela de prisao vs janela de
   expropriacao)
3. **Memoria final consolidada** para anexar a peticao de cumprimento
   ou execucao (CPC 528 / 530)

NAO substitui a peticao — gera a planilha. Para a peticao, sugerir
plugin-irmao `direito-familia-adv-os` ou `execucao-adv-os`.

---

## 2. INPUT NECESSARIO

Perguntar ou propagar do `calculos-master`:

1. **Tipo do titulo** — judicial (sentenca/decisao homologatoria) ou
   extrajudicial (escritura publica de divorcio com clausula alimentar)
2. **Valor da pensao mensal fixada** (em SM, percentual de rendimentos,
   ou valor fixo em reais)
3. **Data inicial da inadimplencia** (1a parcela nao paga)
4. **Data final do calculo** (geralmente data prevista de protocolo)
5. **Pagamentos parciais ja feitos** (data + valor) — se houver
6. **Indice de correcao** (geralmente tabela do TJ do foro da execucao
   — vem do `identificar-tj-aplicavel`)
7. **Juros pactuados?** (raro em alimentos — default 1% am, CC art. 406
   + CPC 528 §7º)
8. **Existe clausula de reajuste?** (anual pelo INPC ou outro indice —
   se sim, recalcular base anual)

---

## 3. PROCESSAMENTO

### Passo 1 — Calcular janela da Sumula 309 STJ

```
hoje = data_final_calculo
janela_prisao = ultimas 3 parcelas vencidas (anteriores ao protocolo)
              + todas que vencerem no curso da execucao
janela_expropriacao = parcelas anteriores a janela_prisao
```

A Sumula 309 STJ atualizada (firme desde HC 53.068/MS) diz:
> "O debito alimentar que autoriza a prisao civil do alimentante e o
> que compreende as **3 prestacoes anteriores ao ajuizamento da
> execucao e as que se vencerem no curso do processo**."

### Passo 2 — Gerar tabela parcela-a-parcela

Para CADA parcela vencida (do `data_inicial_inadimplencia` ate
`data_final_calculo`):

| Coluna | Calculo |
|--------|---------|
| Mes/Ano | sequencial |
| Valor nominal | valor fixado (ou reajustado se ano > 1) |
| Indice correcao [TABELA] | placeholder (advogado preenche) |
| Valor corrigido | placeholder formula |
| Juros 1% am desde vencimento | placeholder formula |
| **Total parcela** | placeholder soma |
| Rito (Sum. 309) | "PRISAO (CPC 528)" ou "EXPROPRIACAO (CPC 530)" |

### Passo 3 — Aplicar pagamentos parciais (se houver)

Imputar pagamentos na ordem cronologica (CC art. 354 — primeiro juros,
depois principal). Quitar parcelas das mais antigas para as mais novas
(salvo indicacao expressa do alimentante).

### Passo 4 — Marcar medidas atipicas (Tema 1.137 STJ)

Tema 1.137 STJ (julgado em 2026, fixacao em sede repetitiva) admite
medidas atipicas em alimentos:
- Suspensao de CNH
- Suspensao de passaporte
- Inscricao em cadastros de inadimplentes (SPC/Serasa)
- Protesto da decisao (CPC 528 §1º — ja era expresso)

So aplicaveis APOS esgotamento das medidas tipicas (penhora, prisao
quando cabivel) e mediante fundamentacao especifica. Sinalizar no
output como "opcao do exequente, NAO automatico".

---

## 4. OUTPUT — PLANILHA ESTRUTURADA

```markdown
## Memoria de Calculo — Execucao de Alimentos

**Atencao:** este calculo apresenta ESTRUTURA + FORMULA. Os indices
de correcao devem ser preenchidos pelo advogado a partir da **tabela
oficial vigente do TJ do foro da execucao** (geralmente TJ do
domicilio do alimentando — CC 1.700 / CPC 53 II).

### Premissas

| Campo | Valor |
|-------|-------|
| Titulo executivo | [judicial / extrajudicial] |
| Valor da pensao mensal | [R$ X ou X% rendimentos ou X SM] |
| Data inicial inadimplencia | [DD/MM/AAAA] |
| Data final calculo | [DD/MM/AAAA] |
| Tabela correcao aplicavel | [TJSP/TJPR/TJ-X — link] |
| Juros | 1% ao mes desde cada vencimento (CC 406 + CPC 528 §7º) |
| Pagamentos parciais | [lista ou "nenhum"] |

---

### Tabela 1 — Parcelas vencidas (parcela a parcela)

| # | Vencimento | Nominal | Indice | Corrigido | Juros 1% am | Total | Rito Sum.309 |
|---|------------|---------|--------|-----------|-------------|-------|--------------|
| 1 | [data] | R$ ___ | _____ | R$ ___ | R$ ___ | R$ ___ | EXPROPRIACAO |
| ... | ... | ... | ... | ... | ... | ... | ... |
| N-2 | [data] | R$ ___ | _____ | R$ ___ | R$ ___ | R$ ___ | **PRISAO** |
| N-1 | [data] | R$ ___ | _____ | R$ ___ | R$ ___ | R$ ___ | **PRISAO** |
| N | [data] | R$ ___ | _____ | R$ ___ | R$ ___ | R$ ___ | **PRISAO** |

**Formula correcao:** valor_corrigido = nominal × (idx_final / idx_vencimento)
**Formula juros:** juros = corrigido × 0,01 × meses_desde_vencimento

---

### Tabela 2 — Segmentacao por rito (Sum. 309 STJ)

| Bloco | Periodo | Parcelas | Total | Rito |
|-------|---------|----------|-------|------|
| Antigo | [data inicial] a [N-3] | [qtd] | R$ ___ | EXPROPRIACAO (CPC 530) |
| Recente (3 ultimas) | [N-2] a [N] | 3 | R$ ___ | **PRISAO CIVIL (CPC 528)** |
| Vincendas no curso | apos protocolo | conforme | R$ ___ | **PRISAO CIVIL (CPC 528)** |

---

### Totalizacao

| Verba | Valor |
|-------|-------|
| Principal corrigido | R$ ___ |
| Juros de mora 1% am | R$ ___ |
| Pagamentos parciais imputados (CC 354) | (R$ ___) |
| **TOTAL DEVIDO ATE [data]** | **R$ ___** |
| Honorarios sucumbenciais (a fixar) | a definir |
```

---

## 5. AVISOS OBRIGATORIOS NO OUTPUT FINAL

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. Conferir indices de correcao contra a TABELA OFICIAL ATUAL do
   TJ competente — esta skill NAO tem acesso a indices posteriores
   a Janeiro/2026.

2. SUMULA 309 STJ — a 3ª parcela "anterior ao ajuizamento" e contada
   da DATA DO PROTOCOLO da execucao, NAO da data atual. Recalcular
   se houver delay entre geracao da planilha e protocolo.

3. RITO CPC 528 (PRISAO): aplicavel APENAS as 3 ultimas + vincendas.
   Misturar com parcelas antigas e nulidade absoluta (HC 92.100/SP STJ).

4. RITO CPC 530 (EXPROPRIACAO): para parcelas alem das 3 ultimas. NAO
   admite prisao civil. Penhora, leilao, desconto em folha (CPC 529).

5. TEMA 1.137 STJ (2026) — medidas atipicas (CNH/passaporte) sao
   admitidas mas exigem esgotamento das tipicas + fundamentacao
   especifica. Nao pedir genericamente.

6. ALIMENTOS PRETERITOS (alem de ~2 anos sem cobranca): risco de
   serem reclassificados como "indenizacao" sem rito especial de
   prisao (REsp 1.354.963/SP). Cobrar por procedimento comum.

7. Conferir formula de juros: simples (1% × meses) NAO capitalizado,
   salvo clausula expressa.
```

---

## 6. FUNDAMENTACAO LEGAL

- **CC art. 1.694-1.710** — obrigacao alimentar (criterios, revisao,
  exoneracao, transmissibilidade)
- **CC art. 354 e 406** — imputacao de pagamento + juros legais
- **CPC art. 528-533** — cumprimento de sentenca que reconhece
  obrigacao alimentar (528 = prisao; 530 = expropriacao)
- **CF art. 5º LXVII** — unica hipotese de prisao civil por divida no
  Brasil ("inadimplente voluntario e inescusavel de obrigacao
  alimenticia")
- **Sumula 309 STJ** — janela de 3 ultimas + vincendas para prisao
- **Sumula 358 STJ** — extincao da obrigacao alimentar pela maioridade
  exige contraditorio (NAO automatica)
- **Tema 1.137 STJ (2026)** — admissibilidade de medidas atipicas
  (CNH/passaporte) em alimentos
- **HC 92.100/SP STJ** — nulidade da prisao com base em parcelas
  antigas misturadas
- **REsp 1.354.963/SP** — alimentos preteritos cobrados tardiamente
  perdem natureza alimentar para fins de prisao

---

## 7. INTEGRACAO

- **Upstream:** `calculos-master`, `classificar-tipo-calculo`,
  `identificar-tj-aplicavel`, `atualizador-indices-cache`
- **Downstream:** auto-dispara `protocolo-p4-calculos` (auditoria R1-R4)
- **Sugestao de plugin-irmao (NAO executa):**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Peticionar cumprimento de sentenca alimentar | /direito-familia cumprimento-alimentos | direito-familia-adv-os |
| Executar pelo rito CPC 528 (prisao) | /execucao alimentos-prisao | execucao-adv-os |
| Executar pelo rito CPC 530 (expropriacao) | /execucao alimentos-expropriacao | execucao-adv-os |
| Auditar calculo (R1-R4) antes do protocolo | /calculos protocolo-p4 | (interno) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.
```

---

## 8. PROIBICOES

1. **NUNCA misturar parcelas antigas na janela de prisao** — nulidade.
2. **NUNCA gerar valor final com indice hardcoded** — so formula.
3. **NUNCA presumir juros compostos** em alimentos — sempre simples.
4. **NUNCA pedir medida atipica (Tema 1.137) sem esgotar tipica.**
5. **NUNCA aplicar correcao retroativa a data anterior a vencimento**
   de cada parcela.
6. **NUNCA omitir aviso sobre recontagem das 3 ultimas na data do
   protocolo** (parcela que e "ultima" hoje pode nao ser no protocolo
   se ha delay).
