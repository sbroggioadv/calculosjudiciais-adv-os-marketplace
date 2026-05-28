---
name: calculo-atrasados-inss
description: >
  CALCULO-ATRASADOS-INSS — Calcula atrasados de beneficio
  previdenciario (concessao retroativa, revisao, restabelecimento)
  conforme Manual de Calculos da Justica Federal (CJF). Aplica
  correcao IPCA-E (Tema 810 STF — natureza alimentar dos beneficios)
  e juros: 1% am ate 30/06/2009 (Lei 8.213 art. 41 §2º redacao
  antiga), depois taxa poupanca (Lei 11.960/2009 — TR + 0,5% am ou
  0,5% am ate 5% poupanca, conforme periodo) e SELIC pos-Tema 905 STJ
  / Lei 14.905/2024 para periodos recentes. Sum. 148 STJ: juros
  desde a citacao. NUNCA gera IPCA-E nem SELIC numerica de cabeca —
  consulta scripts/data/indices/. Use quando o advogado precisar
  quantificar atrasados em acao previdenciaria, conferir conta de
  liquidacao do INSS ou preparar cumprimento de sentenca/RPV.
---

# CALCULO-ATRASADOS-INSS — Atrasados Previdenciarios em Juizo

## 1. ESCOPO

Calcula **atrasados de beneficio previdenciario** apos sentenca
concessiva, revisao ou restabelecimento. Aplica o **Manual de
Calculos da Justica Federal (CJF)** — fonte oficial vinculante na JF.

Produz:

- Parcelas mensais devidas (DIB → data calculo)
- Correcao monetaria parcela a parcela (IPCA-E — Tema 810 STF)
- Juros conforme regime temporal (1% / poupanca / SELIC)
- Total devido para RPV ou precatorio
- Honorarios sucumbenciais sobre os atrasados (regra: ate a sentenca)

NAO calcula:
- RMI (vide `calculo-rmi-beneficio`)
- Atualizacao de beneficio em manutencao (reajuste anual)
- Atrasados de servidor publico — RPPS tem regra propria

---

## 2. INPUT NECESSARIO

Perguntar (ou extrair):

1. **Tipo de acao:**
   - Concessao de beneficio (DIB judicial)
   - Revisao de beneficio (parcelas a maior)
   - Restabelecimento (cessacao indevida)
   - Implantacao de tutela antecipada
2. **DIB judicial** (Data de Inicio do Beneficio fixada na sentenca)
3. **DCB** (Data de Cessacao do Beneficio — se restabelecimento)
4. **RMI ja calculada** (vide `calculo-rmi-beneficio`)
5. **Reajustes anuais aplicaveis** (INPC do periodo — Lei 11.430/06)
6. **Data da citacao** (define termo inicial dos juros — Sum. 148 STJ)
7. **Data prevista do calculo / liquidacao** (DD/MM/AAAA)
8. **Tipo de pagamento previsto:** RPV (ate 60 SM) ou precatorio

---

## 3. PROCESSAMENTO

### 3.1 Gerar parcelas mes a mes

```
Para cada mes entre DIB e data_calculo:
  parcela_mensal = RMI × (reajustes_acumulados_INPC ate o mes)
  registrar (mes/ano, valor_devido)
```

**Reajuste anual**: 1º de janeiro de cada ano pelo INPC do INSS (Lei
11.430/06 + Decreto regulamentar). 13o salario integral em dezembro.

### 3.2 Correcao monetaria parcela a parcela (IPCA-E)

```
Para CADA parcela:
  Consultar: scripts/data/indices/ipca-e-mensal.json

  fator = IPCA-E_acumulado_do_mes_parcela_ate_mes_calculo
  parcela_corrigida = parcela_mensal × fator
```

**Base legal:** Tema 810 STF (RE 870.947) — IPCA-E e o indice correto
para beneficios previdenciarios (natureza alimentar) desde 30/06/2009,
em substituicao a TR.

### 3.3 Juros — regime temporal

| Periodo | Regra de juros |
|---------|----------------|
| Ate 30/06/2009 | 1% ao mes (Lei 8.213/91 art. 41 §2º — redacao original) |
| 01/07/2009 a 25/03/2015 | TR + 0,5% ao mes (Lei 11.960/09 art. 5º — declarada inconstitucional p/ atualizacao mas valida p/ juros — Tema 810 STF parcial) |
| 26/03/2015 ate Tema 905 STJ | Mantida regra Lei 11.960 ate decisao judicial |
| Pos-Tema 905 STJ / pos-Lei 14.905/2024 | Taxa Legal (Selic - IPCA, conforme novo CC art. 406) ou SELIC integral conforme natureza |

**Sum. 148 STJ:** "Os juros moratorios, na repeticao do indebito
tributario, sao contados a partir do transito em julgado da
sentenca." → para previdenciario, juros desde a **CITACAO** (regra
geral CPC art. 240 + Sum. 204 STJ adaptada para beneficios).

### 3.4 Calculo dos juros

```
Para CADA parcela:
  meses_atraso = (data_calculo - data_inicio_juros)

  SE periodo da parcela ate 30/06/2009:
    juros = parcela_corrigida × 1% × meses_atraso (simples)

  SE periodo 01/07/2009 ate Tema 905:
    juros = parcela_corrigida × (TR_acumulada + 0,5% × meses)
    OU 0,5% am ate 5% poupanca (regra do menor)

  SE periodo pos-Tema 905 / pos-Lei 14.905:
    juros = parcela_corrigida × SELIC_acumulada (engloba correcao)
    → atencao: se SELIC ja engloba correcao, NAO aplicar IPCA-E nesse periodo
```

### 3.5 Honorarios sucumbenciais

- Regra geral CPC art. 85 §3º incisos: 10-20% sobre o valor da
  condenacao
- **Sum. 111 STJ:** "Os honorarios advocaticios, nas acoes
  previdenciarias, nao incidem sobre as prestacoes vencidas apos a
  sentenca."
  → calculo dos honorarios = atrasados ATE A SENTENCA (nao do
  calculo)

### 3.6 RPV ou precatorio

- **RPV federal:** ate 60 salarios minimos vigentes (CF art. 100 §3º
  + Lei 10.259/01 art. 17)
- **Precatorio:** acima do limite RPV
- Cada beneficiario tem seu proprio RPV (regra do "pagamento por
  pessoa" — cliente ou cliente + sucessores)

---

## 4. OUTPUT — Memoria de Calculo

```markdown
## Memoria de calculo — atrasados INSS

**Beneficio:** [tipo + RMI R$ ___]
**DIB judicial:** [DD/MM/AAAA]
**Data citacao:** [DD/MM/AAAA] (termo inicial juros)
**Data calculo:** [DD/MM/AAAA]
**Periodo:** [N] meses + 13o salario × [N anos]

---

### Tabela 1 — Parcelas mensais (sem correcao/juros)

| Mes/Ano | RMI base | Reajuste acum (INPC) | Parcela devida |
|---------|----------|----------------------|----------------|
| [mes 1] | R$ ___ | 1,0000 | R$ ___ |
| ... | ... | ... | ... |
| Dezembro [ano] | R$ ___ | _____ | R$ ___ + 13o R$ ___ |
| ... | ... | ... | ... |
| **TOTAL nominal** | | | **R$ ___** |

---

### Tabela 2 — Correcao monetaria (IPCA-E — Tema 810 STF)

| Parcela | Valor nominal | IPCA-E acumulado | Valor corrigido |
|---------|---------------|------------------|-----------------|
| [mes 1] | R$ ___ | _____ | R$ ___ |
| ... | ... | ... | ... |
| **TOTAL corrigido** | **R$ ___** | | **R$ ___** |

**FONTE OBRIGATORIA:** Manual de Calculos da Justica Federal — CJF
https://www.cjf.jus.br/

---

### Tabela 3 — Juros (regime temporal)

| Parcela | Regime | Taxa | Meses | Juros |
|---------|--------|------|-------|-------|
| [parcela ate 30/06/2009] | 1% am simples | 1% | _____ | R$ ___ |
| [parcela 07/2009 - Tema 905] | TR+0,5%/poupanca | _____ | _____ | R$ ___ |
| [parcela pos-Tema 905/Lei 14.905] | SELIC ou Taxa Legal CC406 | _____ | _____ | R$ ___ |
| **TOTAL juros** | | | | **R$ ___** |

**Termo inicial juros:** citacao [DD/MM/AAAA] (CPC 240 + Sum. 148 STJ
adaptada)

---

### Totalizacao

| Verba | Valor |
|-------|-------|
| Atrasados corrigidos | R$ ___ |
| Juros de mora | R$ ___ |
| **TOTAL DEVIDO** | **R$ ___** |
| Honorarios 10-20% (Sum. 111 STJ — ate sentenca) | R$ ___ |
| Custas | R$ ___ |

---

### Forma de pagamento

| Cenario | Modalidade |
|---------|-----------|
| Total <= 60 SM federal | RPV |
| Total > 60 SM federal | Precatorio |

**Limite RPV [ano]:** R$ ___ (60 × SM vigente)
**Total calculado:** R$ ___
**Modalidade:** [RPV | PRECATORIO]
```

---

## 5. FUNDAMENTACAO LEGAL

| Norma | Cobertura |
|-------|-----------|
| Lei 8.213/91 art. 41 | Reajuste de beneficio em manutencao |
| Lei 8.213/91 art. 41-A | Pagamento de atrasados |
| Lei 11.430/06 | INPC como indice de reajuste anual |
| Lei 11.960/09 art. 5º | TR + 0,5% am — declarada parcialmente inconstitucional |
| Tema 810 STF (RE 870.947) | IPCA-E para beneficios desde 30/06/2009 |
| Tema 905 STJ | Juros: detalhamento por periodo |
| Sum. 111 STJ | Honorarios sobre atrasados ate a sentenca |
| Sum. 148 STJ | Juros desde citacao (adaptado p/ previdenciario) |
| Sum. 204 STJ | Juros previdenciarios desde citacao |
| CF art. 100 | RPV e precatorio |
| Lei 10.259/01 art. 17 | RPV federal — limite 60 SM |
| CPC art. 525 | Cumprimento de sentenca contra Fazenda |
| Lei 14.905/2024 | Taxa Legal CC art. 406 — Selic - IPCA |
| Manual CJF | Procedimentos vinculantes na JF para liquidacao |

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. Manual de Calculos do CJF e a fonte VINCULANTE na Justica
   Federal. Conferir versao vigente em:
   https://www.cjf.jus.br/cjf/corregedoria-da-justica-federal/
   centro-de-estudos-judiciarios/manual-de-calculos

2. IPCA-E e SELIC flutuam — esta skill nao tem acesso a indices
   posteriores a [range_final do scripts/data/indices/].
   Conferir mensalmente contra IBGE (IPCA-E) e BCB (SELIC).

3. Regime de juros e SEGMENTADO por periodo (1% / TR-poupanca /
   SELIC). Errar a divisao temporal gera impugnacao do INSS.

4. Sum. 111 STJ: honorarios incidem APENAS ate a sentenca. Calculo
   posterior NAO entra na base.

5. Reajustes anuais aplicam-se em 1º de janeiro pelo INPC do INSS
   (NAO IPCA, NAO IGP-M). Lei 11.430/06.

6. 13o salario: 1/12 por mes de fato impeditivo a partir do mes em
   que beneficio era devido. Integral em dezembro.

7. RPV vs precatorio: dividir por beneficiario (cada um tem seu
   limite de 60 SM). Sucessores hereditarios contam separadamente.

8. Verificar TUTELA ANTECIPADA: parcelas pagas administrativamente
   por forca de tutela NAO sao atrasados (ja foram pagas). Calcular
   apenas o GAP.
```

---

## 7. INTEGRACAO

**Upstream:**
- `calculo-rmi-beneficio` (fornece RMI base)
- `classificar-tipo-calculo` (roteador) → identifica
  "previdenciario / atrasados" → chama esta skill

**Downstream:** `protocolo-p4-calculos` (auditoria R1-R4)

**Cross-link (sugestao soft):**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Cumprimento de sentenca contra INSS | /execucao cumprimento-sentenca | execucao-adv-os |
| Peticao de RPV / Precatorio | /previdenciario peticao-rpv-precatorio | previdenciario-adv-os |
| Pedido de tutela de urgencia para implantacao | /execucao pedido-tutela-urgencia | execucao-adv-os |
```

---

## 8. PROIBICOES

1. **NUNCA** gerar IPCA-E nem SELIC numerica de cabeca — sempre
   consultar `scripts/data/indices/`.
2. **NUNCA** aplicar juros uniformes — separar por periodo
   (1% / poupanca / SELIC).
3. **NUNCA** aplicar TR como correcao monetaria pos-Tema 810 STF
   (declarada inconstitucional para beneficios).
4. **NUNCA** calcular honorarios sobre parcelas posteriores a
   sentenca (Sum. 111 STJ).
5. **NUNCA** ignorar tutela antecipada — parcelas ja pagas
   administrativamente nao sao atrasados.
6. **NUNCA** usar IGP-M ou IPCA "cheio" — para previdenciario e
   IPCA-E (Tema 810 STF).
7. **NUNCA** somar atrasados de varios beneficiarios para definir
   RPV/precatorio — cada beneficiario tem seu limite.
