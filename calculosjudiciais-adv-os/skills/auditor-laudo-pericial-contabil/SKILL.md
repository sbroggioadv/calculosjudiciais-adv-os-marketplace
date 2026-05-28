---
name: auditor-laudo-pericial-contabil
description: >
  AUDITOR-LAUDO-PERICIAL-CONTABIL — Diferencial competitivo. Recebe
  laudo de perito contador (PDF, DOCX ou texto colado) e audita por
  checklist canonico baseado em NBC PP 01 do CFC + Resolucao CFC
  1.243/2009 + CPC art. 473. Verifica: (1) base normativa explicita,
  (2) coerencia interna premissa-calculo-resultado, (3) indices
  aplicados batem com a sentenca/decisao, (4) cumprimento dos
  quesitos formulados, (5) anexos completos (planilha + memoria),
  (6) ausencia de erro grosseiro ou omissao. Devolve checklist
  estruturado com OK / ALERTA por item + sugestao de impugnacao ou
  concordancia. Use SEMPRE que o usuario disser "auditar laudo",
  "laudo do perito", "perito contabil", "NBC PP 01", "laudo pericial
  esta certo", "impugnar laudo", "/auditar-laudo-pericial" ou anexar
  laudo pericial.
---

# AUDITOR-LAUDO-PERICIAL-CONTABIL — Auditoria de Laudo Pericial

## 1. ESCOPO

Diferencial competitivo. Mercado GERA calculos (PJE-Calc, Calculo
Juridico, Debit, Doc9) — ninguem AUDITA laudo de perito contador
antes do advogado se manifestar.

Esta skill:
1. Recebe laudo de perito contador (qualquer area)
2. Audita contra checklist baseado em **NBC PP 01 (CFC)** + **CPC
   464-480**
3. Devolve diagnostico estruturado com cada item OK / ALERTA
4. Sugere impugnacao (CPC 477) ou concordancia
5. Auto-dispara `contra-laudo-pericial` e
   `gerador-quesitos-perito-contabil` quando aplicavel

## 2. INPUT NECESSARIO

| Campo | Obrigatorio | Observacoes |
|---|---|---|
| `laudo_path` ou `laudo_texto` | sim | PDF / DOCX / texto colado |
| `quesitos_originais` | desejavel | Quesitos formulados pelo juizo + pelas partes |
| `parametros_sentenca` ou `decisao_interlocutoria` | desejavel | Para auditar se laudo seguiu o comando judicial |
| `polo_cliente` | desejavel | Molda framing (impugnar / aderir) |
| `area_pericia` | desejavel | trabalhista \| civel \| tributaria \| falimentar \| inventario \| revisional |

Se o laudo vier em PDF, primeiro extrair texto via
`pdftotext` (poppler), `pdfplumber` ou `PyPDF2`. Se extracao
falhar, instruir advogado a colar conteudo manualmente.

## 3. PROCESSAMENTO

### Checklist canonico (10 itens)

#### Check 1 — Identificacao formal do perito (NBC PP 01 item 14)
- Nome completo
- CRC ativo e regular
- Especialidade (se for o caso — pericia tributaria, falimentar,
  trabalhista)
- Endereco profissional
- Assinatura digital com certificado ICP-Brasil OU assinatura
  fisica + reconhecimento
- Status: 🟢 OK / 🔴 falta(m) campo(s)

#### Check 2 — Identificacao do processo
- Numero CNJ completo
- Vara/Juizo
- Partes
- Objeto da pericia (claramente delimitado)
- Status: 🟢 / 🔴

#### Check 3 — Base normativa explicita (NBC PP 01 item 17)
- Mencao a NBC PP 01 (Norma Brasileira de Contabilidade —
  Pericia)
- Mencao a NBC TP 01 (Normas Tecnicas de Pericia Contabil)
- Mencao a Resolucao CFC 1.243/2009 (e atualizacoes)
- Mencao a CPC art. 473 (requisitos do laudo)
- Status: 🟢 / 🟡 (parcial) / 🔴 (ausente)

#### Check 4 — Coerencia interna (premissas → calculo → resultado)
- Premissas declaradas no inicio
- Cada premissa usada no calculo
- Resultados decorrem das premissas (sem salto logico)
- Anexos (planilha) confirmam o resultado do laudo
- Status: 🟢 / 🟡 / 🔴

#### Check 5 — Indices aplicados conferem com decisao
- Indice de correcao usado bate com sentenca/decisao
- Indice de juros bate com sentenca/decisao
- Marco temporal (data-base, ajuizamento, vencimento) bate
- Se sentenca silente → indice usado e defensivel (ex:
  ADC 58/59 STF, Tema 905 STJ)
- Status: 🟢 / 🟡 / 🔴

#### Check 6 — Cumprimento dos quesitos
- Cada quesito do juizo respondido
- Cada quesito da parte autora respondido
- Cada quesito da parte re respondida
- Respostas tecnicas (nao evasivas)
- Status: por quesito → 🟢 respondido / 🟡 evasivo / 🔴 omisso

#### Check 7 — Anexos completos
- Planilha de calculo (Excel/CSV/PDF) anexada
- Memoria de calculo passo a passo
- Documentos consultados listados
- Diligencias declaradas (data, local, pessoas)
- Status: 🟢 / 🟡 / 🔴

#### Check 8 — Erro grosseiro ou omissao detectavel
- Aritmetica basica conferida (sample 3-5 verbas)
- Indice acumulado bate com cache local do plugin
- Verbas omitidas vs sentenca/decisao
- Valores que destoam de ordem de grandeza esperada
- Status: 🟢 sem erro detectado / 🟡 ponto a esclarecer /
  🔴 erro grosseiro

#### Check 9 — Honorarios periciais (CPC 95 + Resolucao CNJ 305)
- Valor compativel com complexidade
- Fundamentacao do valor (horas, hierarquia da pericia)
- Pedido de complementacao justificado se for o caso
- Status: 🟢 / 🟡 / 🔴

#### Check 10 — Conclusao tecnica clara
- Sintese final inequivoca
- Sem expressoes evasivas ("aparentemente", "ao que parece")
- Posicao tecnica firmada
- Status: 🟢 / 🟡 / 🔴

### Resumo final

- `total_ok`: contagem de 🟢
- `total_alerta`: contagem de 🟡
- `total_erro`: contagem de 🔴

### Diagnostico de risco

| Combinacao | Diagnostico |
|---|---|
| 10 verde | Aderir ao laudo |
| 7-9 verde + 1-3 amarelo | Pedir esclarecimentos (CPC 477) |
| 1+ vermelho estrutural (checks 4-8) | Impugnar (CPC 477) + contra-laudo |
| 3+ vermelho | Pedir nova pericia (CPC 480) |

## 4. OUTPUT

```markdown
## 🔬 Auditoria de Laudo Pericial — Processo {{numero}}

**Perito:** [Nome] — CRC: [XX/000.000-O/X]
**Area:** [trabalhista/civel/tributaria/...]
**Data do laudo:** [DD/MM/AAAA]
**Polo cliente:** [{{POLO}}]

### Sintese do Laudo (resumo executivo)

[3-5 paragrafos do que o perito concluiu]

### ✅ Checklist Canonico

| # | Item | Status | Observacao |
|---|---|:---:|---|
| 1 | Identificacao do perito (NBC PP 01 §14) | 🟢 | CRC ativo, ICP-Brasil OK |
| 2 | Identificacao do processo | 🟢 | |
| 3 | Base normativa explicita | 🟡 | Cita NBC PP 01 mas omite Resolucao CFC 1.243/2009 |
| 4 | Coerencia interna | 🟢 | Premissas → calculos → resultado consistentes |
| 5 | Indices conferem com decisao | 🔴 | Decisao manda IPCA-E; perito usou IGP-M |
| 6 | Cumprimento dos quesitos | 🟡 | Quesito 4 do reu respondido de forma evasiva |
| 7 | Anexos completos | 🟢 | Planilha + memoria + diligencias |
| 8 | Sem erro grosseiro | 🟢 | Aritmetica conferida em 5 verbas |
| 9 | Honorarios periciais (CPC 95) | 🟢 | Fundamentados em horas trabalhadas |
| 10 | Conclusao tecnica clara | 🟢 | Sintese final inequivoca |

**Resumo:** 7 🟢 / 2 🟡 / 1 🔴

### 🔴 Alertas Vermelhos Detectados

#### Check 5 — Indice errado
- **Decisao judicial:** "atualizacao monetaria pelo IPCA-E"
- **Aplicado no laudo:** IGP-M
- **Impacto:** o IGP-M acumulado no periodo foi superior ao
  IPCA-E em ~ 8 pontos percentuais → laudo SUPERESTIMA valor
  em ~ R$ ___ (a verificar contra cache `ipca-e-mensal.json`
  e `igp-m`)
- **Acao:** IMPUGNAR (se polo cliente = reu) ou ACEITAR
  beneficio mas sinalizar risco de reforma em recurso (se
  polo cliente = autor)

### 🟡 Pontos a Esclarecer

#### Check 3 — Base normativa parcial
- Pedir esclarecimento (CPC 477 § 2º) sobre adesao a
  Resolucao CFC 1.243/2009

#### Check 6 — Quesito 4 evasivo
- Reformular quesito complementar exigindo resposta tecnica
  objetiva

### 📝 Recomendacao Tecnico-Processual

[com base no diagnostico de risco — pedir esclarecimentos /
impugnar / requerer nova pericia / aceitar]

### Modelo de manifestacao (esqueleto — CPC 477)

```
EXMO. SR. DR. JUIZ ...

[POLO], ja qualificado(a), vem no prazo comum de 15 dias
(CPC 477) MANIFESTAR-SE SOBRE O LAUDO PERICIAL, requerendo:

1. ESCLARECIMENTOS SOBRE [pontos 🟡]: ...
2. IMPUGNACAO DOS PONTOS [pontos 🔴]:
   - O laudo aplicou IGP-M em violacao a decisao deste juizo
     que determinou IPCA-E (fls. ___), superestimando o valor
     em ~R$ ___ (NBC PP 01 item ___; CPC 473, II).
3. Subsidiariamente, [pedido subsidiario].
```

> ⚠️ **Validar contra fonte oficial antes de protocolar.**
> Auditoria automatizada nao substitui revisao do advogado.
```

## 5. FUNDAMENTACAO LEGAL

- **CPC 156** — perito como auxiliar
- **CPC 464-480** — pericia (geral)
- **CPC 473** — requisitos do laudo
- **CPC 477** — esclarecimentos + impugnacao (15 dias)
- **CPC 480** — nova pericia
- **CPC 95** — honorarios periciais
- **NBC PP 01 / NBC TP 01 (CFC)** — pericia contabil
- **Resolucao CFC 1.243/2009** — procedimentos
- **Res. CNJ 305/2019** — honorarios
- **REsp 1.214.794/SP** — limites de impugnacao

## 6. AVISOS OBRIGATORIOS NO OUTPUT

1. ⚠️ Validar contra fonte oficial antes de protocolar
2. ⚠️ Auditoria automatizada NAO substitui revisao do
   advogado responsavel
3. ⚠️ Prazo CPC 477 — 15 dias comuns
4. ⚠️ Se perito tem CRC inativo/suspenso, requerer
   substituicao imediata
5. ⚠️ Se laudo vem com erro grosseiro estrutural (check 5
   ou 8), avaliar pedido de nova pericia (CPC 480)

## 7. INTEGRACAO

- **Upstream:** `calculos-master`, advogado direto via
  `/auditar-laudo-pericial`
- **Downstream auto:** `gerador-quesitos-perito-contabil` (quesitos
  evasivos), `contra-laudo-pericial` (vermelho estrutural),
  `comparador-calculos` (se ha assistente), `gestao-prazo-impugnacao`
  (CPC 477 — 15 dias), `protocolo-p4-calculos`
- **Cross-link:** `trabalhista-adv-os` / `tributario-societario-adv-os`
  / `licitacoes-adv-os` (peca), `execucao-adv-os` (embargos),
  `ia-combativa-adv-os` (R1-R4)

## 8. PROIBICOES

1. **Nunca** afirmar que perito agiu de ma-fe (so impugnar
   tecnicamente o laudo)
2. **Nunca** pedir desconsideracao do laudo sem fundamentar
   item por item
3. **Nunca** apresentar diagnostico sem rodar TODOS os 10
   checks
4. **Nunca** apresentar valor final sem aviso obrigatorio
5. **Nunca** ignorar quesito do polo cliente nao respondido
   pelo perito (e impugnacao certa)
6. **Nunca** confundir esclarecimento (CPC 477 § 2º) com
   impugnacao (CPC 477 caput)
7. **Nunca** importar dados de outros plugins

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Gerar contra-laudo tecnico | `/auditar-laudo-pericial contra-laudo` | `calculosjudiciais-adv-os` (este — skill `contra-laudo-pericial`) |
| Gerar quesitos complementares | `/auditar-laudo-pericial quesitos` | `calculosjudiciais-adv-os` (este — skill `gerador-quesitos-perito-contabil`) |
| Comparar com laudo de assistente | `/comparar-calculos` | `calculosjudiciais-adv-os` (este) |
| Gerar peca de impugnacao | `/civel impugnacao-laudo` ou `/trabalhista impugnacao-laudo` | `civel-adv-os` ou `trabalhista-adv-os` |
| Embargos a execucao | `/execucao embargos-execucao` | `execucao-adv-os` |
| Auditoria Suprema R1-R4 da peca | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` |

> Se plugin nao instalado, copiar memoria de auditoria acima
> e usar manualmente.
