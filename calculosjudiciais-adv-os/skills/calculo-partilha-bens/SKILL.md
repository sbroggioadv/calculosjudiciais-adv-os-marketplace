---
name: calculo-partilha-bens
description: >
  CALCULO-PARTILHA-BENS — Estrutura memoria de calculo de partilha de
  bens em divorcio, dissolucao de uniao estavel ou inventario.
  Identifica regime de bens aplicavel (comunhao parcial default,
  comunhao universal, separacao convencional/obrigatoria, participacao
  final aquestos), classifica cada bem em comunicavel/incomunicavel/
  particular, calcula valor de mercado na data da partilha (perícia
  pode ser necessaria), calcula diferencas de meacao atualizadas
  (correcao TJ + juros 1% am) e tornas devidas fundamentadas. NUNCA
  gera avaliacao de mercado por estimativa propria (anti-halucinacao —
  exige laudo ou referencia objetiva). Use sempre que o advogado
  mencionar partilha de bens, divisao do patrimonio do casal,
  dissolucao patrimonial, meacao, comunhao parcial/universal,
  separacao de bens, participacao final nos aquestos ou inventario
  com mais de um herdeiro.
---

# CALCULO-PARTILHA-BENS — Divisao Patrimonial

## 1. ESCOPO

Memoria de calculo de partilha em 4 outputs auditaveis:

1. **Regime de bens** (data casamento + pacto antenupcial)
2. **Classificacao de bens** (comunicavel / incomunicavel / particular)
3. **Meacao** (50% sobre comunicavel) + diferencas atualizadas
4. **Tornas** (compensacao em dinheiro quando partilha desigual)

NAO substitui peticao de divorcio/inventario nem laudo. Gera planilha.

---

## 2. INPUT NECESSARIO

Perguntar ou propagar do `calculos-master`:

1. **Tipo:** divorcio / dissolucao UE / inventario
2. **Data fato gerador:** celebracao (casamento) / inicio UE / obito (CC 1.784 saisine)
3. **Pacto antenupcial?** (sim/nao + regime)
4. **Data separacao de fato** (CC 1.642 V — exclui bens posteriores)
5. **Lista de bens:** descricao, data aquisicao, forma (esforco comum/heranca/doacao/sub-rogacao/pre-existente), valor atual (FIPE/ITBI/CRECI/laudo)
6. **Dividas comuns** (CC 1.659 V — comunicaveis se em proveito do casal)
7. **Data da partilha** (sentenca/acordo)
8. **Indice de correcao** (tabela do TJ)

---

## 3. PROCESSAMENTO

### Passo 1 — Identificar regime de bens

| Regime | Quando | Comunica |
|--------|--------|----------|
| **Comunhao parcial** (default Lei 6.515/77) | Sem pacto | ADQUIRIDOS NA CONSTANCIA (CC 1.658-1.666) |
| **Comunhao universal** | Pacto expresso | TUDO, exceto CC 1.668 |
| **Separacao convencional** | Pacto expresso | NADA |
| **Separacao obrigatoria** | CC 1.641 (> 70 anos, suprimento) | NADA. Sum. 377 STF: esforco comum partilhavel (controverso) |
| **Participacao aquestos** | Pacto expresso (raro) | Diferenca patrimonial CC 1.672-1.686 |

**Sum. 377 STF:** em separacao obrigatoria, bens com esforco comum
AINDA partilhaveis. STJ divergente — citar e deixar advogado decidir.

### Passo 2 — Classificar cada bem

Para CADA bem listado:

| Status | Criterio (regime comunhao parcial) |
|--------|-------------------------------------|
| **Comunicavel** | Adquirido NA CONSTANCIA, por esforco comum ou presumido (default) |
| **Incomunicavel** | Recebido por heranca/doacao a UM dos conjuges (CC 1.659 I) |
| **Sub-rogacao** | Comprado com produto de bem incomunicavel (CC 1.659 II) — mas a VALORIZACAO durante o casamento pode ser comunicavel (controversia STJ — REsp 1.295.991/RS) |
| **Pre-existente** | Adquirido ANTES do casamento/UE (CC 1.659 I) |
| **Personalissimo** | Bens de uso pessoal, livros, instrumentos profissionais (CC 1.659 V/VI) |
| **Adquirido apos separacao de fato** | CC 1.642 V — excluido se prova separacao + nao colaboracao |

### Passo 3 — Avaliacao a valor de mercado

⚠️ **REGRA DURA:** NAO inventar valor. Para cada bem:
- **Imovel:** laudo corretor CRECI / venal ITBI / avaliacao judicial
  (CPC 870)
- **Veiculo:** Tabela FIPE da data da partilha
- **Empresa/quotas:** balanco + perito contabil
- **Aplicacoes:** extrato da data da partilha
- **Joias/arte:** laudo especializado

Faltou valor objetivo → marcar `[exige laudo]`.

### Passo 4 — Calcular meacao + diferencas

```
Total comunicavel = soma dos valores de mercado dos bens comunicaveis
                   - dividas comuns (CC 1.659 V)
Meacao de cada conjuge = Total comunicavel / 2
```

Se um conjuge ficou com bens de valor > sua meacao → deve TORNA ao
outro pelo excesso.

### Passo 5 — Atualizar diferencas/tornas

Se ja se passou tempo desde a data da partilha "no papel" ate o efetivo
pagamento da torna:
- Correcao monetaria pela tabela do TJ
- Juros 1% am desde a fixacao judicial (ou desde a constituicao em mora)

---

## 4. OUTPUT — PLANILHA ESTRUTURADA

```markdown
## Memoria de Partilha de Bens

**Atencao:** valores de mercado dependem de avaliacao objetiva (laudo,
FIPE, ITBI). Esta skill NAO arbitra valor — usa o que o advogado
informou ou marca `[exige laudo]`. Indices de correcao devem ser
preenchidos pela tabela oficial do TJ aplicavel.

### Premissas

| Campo | Valor |
|-------|-------|
| Tipo | [divorcio / dissolucao UE / inventario] |
| Regime de bens | [comunhao parcial / universal / separacao / aquestos] |
| Data inicio comunicacao | [DD/MM/AAAA] |
| Data separacao de fato | [DD/MM/AAAA ou "nao aplica"] |
| Data da partilha | [DD/MM/AAAA] |
| Tabela correcao | [TJ-X — link] |

---

### Tabela 1 — Classificacao dos bens

| # | Bem | Aquisicao (data + forma) | Valor mercado | Status | Comunicavel? |
|---|-----|--------------------------|---------------|--------|--------------|
| 1 | Apto Vila Nova | 03/2018, compra c/ renda comum | R$ ___ | constancia | SIM |
| 2 | Carro Civic | 06/2020, compra | R$ ___ (FIPE) | constancia | SIM |
| 3 | Quotas X Ltda | 2010, antes UE | [exige laudo] | pre-existente | NAO |
| ... | ... | ... | ... | ... | ... |

---

### Tabela 2 — Dividas comuns (CC 1.659 V)

| # | Divida | Origem | Saldo atual | Comunicavel? |
|---|--------|--------|-------------|--------------|
| 1 | Financiamento imovel | proveito casal | R$ ___ | SIM |
| 2 | Cartao A (uso pessoal) | proveito unico | R$ ___ | NAO |

---

### Tabela 3 — Calculo da meacao

| Item | Valor |
|------|-------|
| Total bens comunicaveis | R$ ___ |
| (-) Dividas comuns | (R$ ___) |
| **Patrimonio liquido comunicavel** | **R$ ___** |
| Meacao de cada conjuge (50%) | R$ ___ |

---

### Tabela 4 — Atribuicao de bens + tornas

| Conjuge | Bens atribuidos | Valor recebido | Meacao devida | Torna |
|---------|-----------------|----------------|---------------|-------|
| A | [lista] | R$ ___ | R$ ___ | +/- R$ ___ |
| B | [lista] | R$ ___ | R$ ___ | +/- R$ ___ |

Se torna > 0: conjuge devedor paga a torna ao outro em dinheiro.

---

### Tabela 5 — Atualizacao da torna (se nao paga a vista)

| Periodo | Correcao [TABELA] | Juros 1% am | Total |
|---------|-------------------|-------------|-------|
| [data fixacao] a [data pagamento] | _____ | _____ | R$ ___ |
```

---

## 5. AVISOS OBRIGATORIOS NO OUTPUT FINAL

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. AVALIACAO A VALOR DE MERCADO exige fonte objetiva — laudo,
   FIPE, ITBI, balanco. NUNCA aceitar "estimativa" sem documento.
   Em caso de divergencia: requerer avaliacao judicial (CPC 870).

2. REGIME DE SEPARACAO OBRIGATORIA (CC 1.641): apesar de "separacao",
   a SUMULA 377 STF permite partilha de bens adquiridos COM ESFORCO
   COMUM na constancia — controverso no STJ, citar tese e deixar o
   advogado decidir.

3. SUB-ROGACAO (CC 1.659 II): a coisa recebida em substituicao a bem
   incomunicavel mantem o status de incomunicavel, MAS a VALORIZACAO
   ocorrida durante o casamento pode ser objeto de partilha (STJ
   REsp 1.295.991/RS — analise caso a caso).

4. UNIAO ESTAVEL — Sum. 380 STF e CC 1.725: regime supletivo e
   comunhao parcial. Pacto entre os companheiros pode dispor diferente.
   PROVAR data inicial da UE e essencial (declaracao judicial ou
   escritura publica).

5. INVENTARIO — partilha sucessoria tem regras proprias (legitima,
   meacao do conjuge supérstite, colacao de bens — CC 2.002-2.012).
   ITCMD incide sobre transmissao (aliquota varia por UF, atualizada
   pela LC 227/2026).

6. INDICES de correcao da torna devem ser preenchidos pela TABELA
   OFICIAL do TJ aplicavel — esta skill NAO tem acesso a indices
   posteriores a Janeiro/2026.

7. Se ha bens NO EXTERIOR: aplicacao do CC 1.785 + Lei 10.406/02 +
   competencia exclusiva da justica brasileira para bens situados no
   Brasil (CPC 23 II); bens no exterior podem exigir homologacao no
   pais de origem.
```

---

## 6. FUNDAMENTACAO LEGAL

- **CC art. 1.658-1.688** — regimes (comunhao parcial/universal/
  separacao/aquestos)
- **CC art. 1.639-1.657** — pacto antenupcial
- **CC art. 1.642 V** — bens pos separacao de fato excluiveis
- **CC art. 1.659** — exclusoes comunhao parcial
- **CC art. 1.668** — exclusoes comunhao universal
- **CC art. 1.725** — UE = comunhao parcial salvo contrato
- **CC art. 1.784** — saisine
- **Sumula 377 STF** — esforco comum em separacao obrigatoria
- **Sumula 380 STF** — UE e esforco comum
- **REsp 1.295.991/RS** — valorizacao de bem sub-rogado
- **REsp 2.124.424/2025** — inventariante digital + criptoativos
- **LC 227/2026** — ITCMD vigente desde 13/01/2026
- **CPC art. 870** — avaliacao judicial
- **CPC art. 610-673** — inventario judicial

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
| Peticionar divorcio litigioso com partilha | /direito-familia divorcio-litigioso | direito-familia-adv-os |
| Inventario judicial completo | /direito-familia inventario-itcmd | direito-familia-adv-os |
| Calcular ITCMD da partilha | /tributario itcmd-uf | tributario-societario-adv-os |
| Auditar partilha (R1-R4) antes do protocolo | /calculos protocolo-p4 | (interno) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.
```

---

## 8. PROIBICOES

1. **NUNCA arbitrar valor de mercado** sem fonte objetiva (laudo, FIPE,
   ITBI, balanco). Se faltar, marcar `[exige laudo]`.
2. **NUNCA assumir 50/50 cego** — sempre validar regime e
   classificacao por bem.
3. **NUNCA misturar partilha sucessoria com partilha conjugal** —
   sao dois calculos distintos (meacao do supérstite + legitima dos
   herdeiros).
4. **NUNCA omitir Sumula 377 STF** em separacao obrigatoria — tese
   relevante.
5. **NUNCA aplicar comunhao parcial em casamento celebrado antes de
   1977** sem checar regra de transicao (Lei 6.515/77 art. 50).
6. **NUNCA omitir aviso sobre necessidade de laudo** em bens de
   avaliacao tecnica (empresa, obra de arte, criptoativo).
