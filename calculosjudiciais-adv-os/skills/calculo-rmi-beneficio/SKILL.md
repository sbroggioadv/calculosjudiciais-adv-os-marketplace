---
name: calculo-rmi-beneficio
description: >
  CALCULO-RMI-BENEFICIO — Calcula a Renda Mensal Inicial (RMI) de
  beneficio previdenciario do RGPS. Aplica Lei 8.213/91 art. 29 +
  EC 103/2019. Pre-EC: media aritmetica dos 80% MAIORES salarios de
  contribuicao desde julho/94 atualizados pelo INPC. Pos-EC (a partir
  de 13/11/2019): media de TODOS (100%) os salarios. RMI =
  salario_de_beneficio × percentual_do_tipo. Cobre aposentadoria
  programada (EC 103), por idade, especial, por incapacidade
  permanente (antiga invalidez), pensao por morte e auxilios. NUNCA
  gera INPC numerico de cabeca — consulta
  scripts/data/indices/inpc-mensal.json. Use quando o advogado
  precisar quantificar RMI de cliente, conferir calculo do INSS,
  preparar acao de revisao ou simular cenarios pre/pos-Reforma.
---

# CALCULO-RMI-BENEFICIO — Renda Mensal Inicial Previdenciaria

## 1. ESCOPO

Calcula **Renda Mensal Inicial (RMI)** de beneficio previdenciario do
RGPS (INSS), produzindo:

- Salario de Beneficio (SB) — media dos salarios de contribuicao
  atualizados pelo INPC desde 07/1994
- Percentual aplicavel ao tipo de beneficio
- RMI = SB × percentual
- Tabela de salarios de contribuicao mes a mes
- Comparacao pre-Reforma (Lei 8.213 original) vs pos-Reforma
  (EC 103/2019) quando o cliente tem direito adquirido ou regra de
  transicao

NAO calcula:
- Atrasados em juizo (vide `calculo-atrasados-inss`)
- Atualizacao do beneficio em manutencao (reajuste anual — outra
  regra)
- Beneficios assistenciais (BPC/LOAS — nao tem RMI, e 1 SM)
- Beneficios do RPPS (servidor publico — regra propria)

---

## 2. INPUT NECESSARIO

Perguntar (ou extrair):

1. **Tipo de beneficio:**
   - Aposentadoria por tempo de contribuicao (EXTINTA pela EC 103/2019
     — so direito adquirido ate 13/11/2019 ou regra de transicao)
   - Aposentadoria por idade (homem 65 / mulher 62 pos-EC)
   - Aposentadoria especial (atividade insalubre/perigosa — 15/20/25
     anos)
   - Aposentadoria programada (nova — pos-EC, regra geral)
   - Aposentadoria por incapacidade permanente (antiga invalidez)
   - Auxilio por incapacidade temporaria (antigo auxilio-doenca)
   - Auxilio-acidente
   - Pensao por morte
   - Salario-maternidade
2. **DIB pretendida** (Data de Inicio do Beneficio — DD/MM/AAAA)
3. **Sexo** do segurado (homem/mulher — define regras pos-EC)
4. **Data de filiacao ao RGPS** (1a contribuicao) — define se ha
   regra de transicao
5. **Lista de salarios de contribuicao** desde 07/1994 (ou desde a
   filiacao, se posterior) — mes a mes ou CNIS completo
6. **Houve atividade especial?** Periodos e fatores de conversao
7. **Tempo total de contribuicao** ate a DIB (anos/meses/dias)
8. **Houve uso da regra dos 80% maiores OU 100%?**
   - Se DIB **ate 12/11/2019** → regra dos **80% maiores** (Lei 8.213
     original art. 29)
   - Se DIB **a partir de 13/11/2019** → regra dos **100%** (todos os
     salarios — EC 103 art. 26)
   - Cliente com direito adquirido pode optar (acao judicial)

---

## 3. PROCESSAMENTO

### 3.1 Atualizar salarios de contribuicao pelo INPC

```
Para CADA salario de contribuicao:
  Consultar: scripts/data/indices/inpc-mensal.json

  fator_correcao = (INPC_mes_DIB / INPC_mes_salario)
  salario_atualizado = salario_original × fator_correcao
```

Salario de contribuicao = limitado ao **teto do INSS** vigente em cada
mes (consultar tabela INSS anual).

### 3.2 Aplicar regra do 80% (pre-EC) ou 100% (pos-EC)

```
SE DIB <= 12/11/2019:
  ordenar salarios atualizados em ordem decrescente
  pegar 80% MAIORES (descartar 20% menores)
  SB = media aritmetica dos 80% maiores

SE DIB >= 13/11/2019:
  SB = media aritmetica de TODOS os salarios atualizados (100%)
```

### 3.3 Aplicar percentual do tipo de beneficio

**Tabela pre-EC 103 (DIB ate 12/11/2019):**

| Beneficio | Percentual sobre SB |
|-----------|---------------------|
| Aposentadoria por tempo de contribuicao | 100% × fator previdenciario (Lei 9.876/99) ou 100% se 85/95 (Lei 13.183/15) |
| Aposentadoria por idade | 70% + 1% por grupo de 12 contribuicoes mensais, max 100% |
| Aposentadoria especial | 100% (sem fator previdenciario) |
| Aposentadoria por invalidez | 100% (acidente trabalho ou doenca profissional) ou 100% (geral) |
| Auxilio-doenca | 91% |
| Auxilio-acidente | 50% (em adicao ao salario) |
| Pensao por morte | 100% (pre-Lei 13.135/15) ou cota familiar + cota individual (pos) |

**Tabela pos-EC 103 (DIB a partir de 13/11/2019):**

| Beneficio | Percentual sobre SB |
|-----------|---------------------|
| Aposentadoria programada (idade + tempo) | 60% + 2% por ano de contribuicao acima de 20 anos (homem) ou 15 anos (mulher) |
| Aposentadoria por idade | 60% + 2% por ano acima de 20 (H) / 15 (M) — mesma regra |
| Aposentadoria especial (15/20/25 anos) | 60% + 2% por ano acima de 20 (H) / 15 (M) |
| Aposentadoria por incapacidade permanente | 60% + 2% por ano acima de 20 (H) / 15 (M); 100% se decorrente de acidente do trabalho |
| Auxilio por incapacidade temporaria | 91% do SB |
| Pensao por morte | 50% + 10% por dependente, max 100% (EC 103 art. 23) |

### 3.4 Regras de transicao (EC 103 art. 15-20)

Aplicaveis para quem ja contribuia em 13/11/2019:

| Regra | Sintese |
|-------|---------|
| Pontos (15) | 86/96 em 2019, +1 ponto/ano ate 100/105 |
| Idade minima progressiva (16) | 56/61 em 2019, +6 meses/ano ate 62/65 |
| Pedagio 50% (17) | Tempo faltante × 1,5 + 50% tempo faltante |
| Pedagio 100% (20) | Idade minima 57/60 + tempo + 100% tempo faltante |
| Idade transicao (18) | Idade minima escalonada 60/61/62/63 + 30/35 anos contrib |

### 3.5 Limites

- **Piso:** 1 salario minimo vigente
- **Teto:** teto do RGPS vigente (consultar tabela INSS ano)

---

## 4. OUTPUT — Memoria de Calculo

```markdown
## Memoria de calculo — RMI

**Segurado:** [nome cliente — preencher em runtime]
**Beneficio:** [tipo]
**DIB pretendida:** [DD/MM/AAAA]
**Sexo:** [H/M]
**Regra aplicavel:** [pre-EC 80% | pos-EC 100% | transicao tipo X]

---

### Tabela 1 — Salarios de contribuicao atualizados (INPC)

| Mes/Ano | SC original | INPC mes | INPC DIB | Fator | SC atualizado |
|---------|-------------|----------|----------|-------|---------------|
| 07/1994 | R$ ___ | _____ | _____ | _____ | R$ ___ |
| ... | ... | ... | ... | ... | ... |
| [mes anterior DIB] | R$ ___ | _____ | _____ | _____ | R$ ___ |

**Total de competencias:** [N]
**FONTE INPC:** https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9258-inpc.html

---

### Tabela 2 — Salario de Beneficio (SB)

| Calculo | Valor |
|---------|-------|
| Total salarios atualizados | R$ ___ |
| Competencias consideradas | [N pre-EC: 80% maiores | N pos-EC: 100%] |
| **Salario de Beneficio (SB)** | **R$ ___** |

---

### Tabela 3 — RMI

| Calculo | Valor |
|---------|-------|
| SB | R$ ___ |
| Percentual aplicavel ([tipo beneficio]) | _____% |
| **RMI antes de limites** | **R$ ___** |
| Piso (1 SM = R$ ___) | R$ ___ |
| Teto RGPS ([ano DIB]) | R$ ___ |
| **RMI FINAL** | **R$ ___** |

---

### Comparativo pre-EC vs pos-EC (se aplicavel direito adquirido)

| Item | Pre-EC (80% maiores) | Pos-EC (100%) |
|------|----------------------|---------------|
| SB | R$ ___ | R$ ___ |
| Percentual | _____% | _____% |
| RMI | R$ ___ | R$ ___ |

**Mais vantajoso:** [pre | pos]
**Ja-segurado em 13/11/2019:** [sim — direito de escolher | nao]
```

---

## 5. FUNDAMENTACAO LEGAL

| Norma | Cobertura |
|-------|-----------|
| Lei 8.213/91 art. 29 | Calculo do salario de beneficio |
| Lei 8.213/91 art. 41 | Reajuste do beneficio (manutencao) |
| Lei 9.876/99 | Fator previdenciario (revogado pos-EC) |
| Lei 13.183/15 | Regra 85/95 e 86/96 (formula alternativa) |
| EC 103/2019 art. 17-20 | Regras de transicao |
| EC 103/2019 art. 23-26 | Novas formulas pos-Reforma |
| Decreto 3.048/99 | Regulamento da Previdencia |
| Sum. 76 TNU | INPC e o indice correto desde 07/1994 |
| Tema 1124 STJ | Revisao da vida toda — VEDADA (definicao 2024) |
| Tema 999 STJ | Revisao de tempo especial — viavel |
| Tema 1102 STJ | Pensao por morte — calculo |

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR ACAO:

1. CONFERIR salarios de contribuicao contra CNIS atualizado
   (consulta MEU INSS — https://meu.inss.gov.br/). Divergencias
   geram impugnacao da autarquia.

2. INPC e o indice CORRETO (Sum. 76 TNU). Esta skill nao tem
   acesso a INPC posterior a [range_final do
   scripts/data/indices/inpc-mensal.json]. Conferir contra IBGE.

3. Direito adquirido em 13/11/2019: cliente com tempo + idade
   completos ANTES dessa data pode optar pela regra mais vantajosa.
   Calcular AMBOS os cenarios.

4. Tema 1124 STJ (2024): revisao da vida toda VEDADA — calculo de
   SB com salarios pre-07/1994 nao e mais possivel via judicial.

5. Tipo de beneficio define percentual. Confirmar:
   - Aposentadoria programada (pos-EC) ≠ por idade ≠ especial
   - Pensao pos-Lei 13.135/15 tem cota familiar + individual
   - Aposentadoria por incapacidade decorrente de acidente do
     trabalho = 100% sempre

6. Limites: PISO = 1 SM vigente na DIB; TETO = teto RGPS do ano
   da DIB. SB calculado pode ser maior, mas RMI fica limitada.

7. Tempo especial: precisa PPP + LTCAT — vide skill especifica
   `calculo-aposentadoria-especial`.
```

---

## 7. INTEGRACAO

**Upstream:** `classificar-tipo-calculo` (roteador) → identifica
"previdenciario / RMI" → chama esta skill.

**Downstream:**
- `calculo-atrasados-inss` (se acao judicial de revisao com atrasados)
- `protocolo-p4-calculos` (auditoria R1-R4)

**Cross-link (sugestao soft):**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Acao de concessao/revisao | /previdenciario peticao-concessao-revisao | previdenciario-adv-os |
| Calcular atrasados (DIB ate hoje) | /calculos atrasados-inss | calculosjudiciais-adv-os |
| Conversao especial → comum | /calculos aposentadoria-especial | calculosjudiciais-adv-os |
```

---

## 8. PROIBICOES

1. **NUNCA** usar INPC numerico de cabeca — sempre consultar
   `scripts/data/indices/inpc-mensal.json`.
2. **NUNCA** aplicar regra dos 80% maiores em DIB >= 13/11/2019
   (extinta pela EC 103) — exceto direito adquirido comprovado.
3. **NUNCA** aplicar fator previdenciario em DIB >= 13/11/2019
   (extinto pela EC).
4. **NUNCA** prometer revisao da vida toda — Tema 1124 STJ (2024)
   vedou.
5. **NUNCA** ignorar TETO do RGPS — RMI nao pode ultrapassar.
6. **NUNCA** confundir RGPS (INSS) com RPPS (servidor publico) —
   regras diferentes.
