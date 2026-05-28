---
name: calculo-debito-condominial
description: >
  CALCULO-DEBITO-CONDOMINIAL — Estrutura memoria de calculo de
  cotas condominiais vencidas (CC art. 1.336 §1º + CPC art. 784,
  X — titulo executivo extrajudicial). Compoe principal (cotas
  vencidas) + multa convencional ate 2% + juros 1% am (default
  convencao) + correcao monetaria (indice da convencao — IGP-M,
  IPCA ou outro). NUNCA gera valor final com indice hardcoded
  (anti-halucinacao por design). Produz memoria mes a mes com
  formula pronta. Use quando o advogado mencionar: "cota
  condominial", "debito condominio", "execucao condominial",
  "cobranca condominial", "taxa condominial atrasada", "fundo de
  reserva nao pago", "rateio extraordinario inadimplente",
  "morador inadimplente", "cobranca de condomino".
---

# CALCULO-DEBITO-CONDOMINIAL — Memoria de Calculo Estruturada

## 1. ESCOPO

Estrutura calculo de divida condominial executavel. Cobre:

- Cotas condominiais vencidas (ordinarias + extraordinarias)
- Fundo de reserva inadimplido
- Rateios extraordinarios (obra, indenizacao)
- Multa convencional (CC art. 1.336 §1º — teto 2%)
- Juros de mora (default 1% am — se convencao silencia)
- Correcao monetaria (indice fixado na convencao — IGP-M, IPCA, INPC)

Base legal: **CC art. 1.336 §1º** (multa nao superior a 2%) +
**CPC art. 784, X** (credito de condominio referente a despesas
condominiais ordinarias ou extraordinarias — titulo executivo
extrajudicial, desde que comprovado por documento idoneo).

---

## 2. INPUT NECESSARIO

Do contexto + perguntar:

1. **Identificacao do condominio** + unidade autonoma + condomino
   inadimplente
2. **Lista de cotas vencidas:** mes/ano + valor nominal + data
   vencimento
3. **Tipo de cota:** ordinaria, extraordinaria (rateio), fundo de
   reserva
4. **Convencao condominial:** anexar trecho que disciplina
   multa, juros e indice de correcao (perguntar ao advogado o
   texto literal)
5. **Multa convencional:** percentual previsto na convencao
   (limite legal: ≤ 2% — CC 1.336 §1º)
6. **Juros pactuados na convencao:** percentual e momento de
   incidencia (se silente → juros legais 1% am pela jurisprudencia
   dominante)
7. **Indice de correcao da convencao:** IGP-M, IPCA, INPC ou
   outro
8. **Data ate quando atualizar:** geralmente data prevista de
   ajuizamento da execucao ou data atual
9. **Tribunal de destino:** UF + comarca (importante pra tabela
   pratica do TJ se convencao silente sobre indice)

---

## 3. PROCESSAMENTO — PASSOS

1. Validar titulo executivo: convencao registrada + ata de
   assembleia que aprovou orcamento + boleto/aviso de cobranca
2. Listar cotas vencidas mes a mes (1 linha por cota)
3. Aplicar multa convencional sobre cada cota inadimplente
   (limite 2%)
4. Aplicar correcao monetaria de cada cota desde o vencimento
   ate o termo final (planilha mes a mes)
5. Aplicar juros de mora de cada cota desde o vencimento (juros
   simples, default — capitalizacao mensal so se convencao
   expressamente previr)
6. Somar verbas: cotas atualizadas + multa + juros
7. Emitir aviso obrigatorio: validacao final contra tabela do TJ
   ou indice oficial

---

## 4. OUTPUT — PLANILHA ESTRUTURADA

```markdown
## Memoria de calculo — Debito condominial

**Atencao:** este calculo apresenta ESTRUTURA + FORMULA. Os indices
numericos devem ser preenchidos a partir da fonte oficial (tabela do
TJ, IBGE-IPCA, FGV-IGP-M conforme indice da convencao). Esta skill
NAO tem acesso a indices posteriores a Jan/2026.

### Premissas

| Campo | Valor |
|---|---|
| Condominio | [nome / CNPJ] |
| Unidade autonoma | [bloco/apto] |
| Condomino inadimplente | [nome] |
| Convencao registrada em | [data + cartorio] |
| Indice de correcao (convencao) | [IGP-M / IPCA / INPC / outro] |
| Multa convencional | [X%] (≤ 2% CC 1.336 §1º) |
| Juros de mora | [X% am — default 1%] |
| Termo final do calculo | [data] |
| Titulo executivo (CPC 784, X) | sim |

### Tabela 1 — Cotas vencidas (principal nominal)

| Mes/Ano | Tipo | Vencimento | Valor nominal | Data inadimplencia |
|---|---|---|---|---|
| [mes] | ordinaria/extra/FR | [dd/mm/aaaa] | R$ [X] | [dd/mm/aaaa] |
| ... | ... | ... | ... | ... |
| **TOTAL NOMINAL** | | | **R$ [X]** | |

### Tabela 2 — Correcao monetaria por cota

Para CADA cota da Tabela 1:

| Cota (mes/ano) | Indice inicial | Indice final | Coef. | Valor corrigido |
|---|---|---|---|---|
| [mes] | _____ | _____ | _____ | R$ _____ |

**Formula:** valor_corrigido = valor_nominal × (indice_final / indice_inicial)

**FONTE OBRIGATORIA (escolher conforme convencao):**
- IGP-M: portalibre.fgv.br
- IPCA: ibge.gov.br/estatisticas/economicas/precos-e-custos
- INPC: ibge.gov.br/estatisticas/economicas/precos-e-custos
- Tabela do TJ ({{UF}}): site oficial do tribunal

### Tabela 3 — Multa convencional

Para CADA cota inadimplente:
multa = valor_corrigido × [percentual_convencao] / 100

**Limite legal (CC 1.336 §1º):** percentual ≤ 2,00%. Multa acima de
2% e nula no excesso.

| Cota | Valor corrigido | Multa (max 2%) |
|---|---|---|
| [mes] | R$ _____ | R$ _____ |

### Tabela 4 — Juros de mora (simples, 1% am default)

| Cota | Vencimento | Meses ate termo | Taxa | Juros |
|---|---|---|---|---|
| [mes] | [dd/mm/aaaa] | [N] | 1% am | R$ _____ |

**Formula (juros simples):**
juros = valor_corrigido × 0,01 × N_meses

**Capitalizacao mensal:** SO se convencao expressamente prever
(jurisprudencia exige clausula clara). Default e juros simples.

### Totalizacao

| Verba | Valor |
|---|---|
| Principal corrigido (Tabela 2 — total) | R$ _____ |
| Multa convencional (Tabela 3 — total) | R$ _____ |
| Juros de mora (Tabela 4 — total) | R$ _____ |
| **TOTAL ATE [data]** | **R$ _____** |

Valor sera atualizado ate o efetivo pagamento.

### Anexos obrigatorios

1. Esta memoria (planilha)
2. Convencao condominial registrada
3. Ata de assembleia que aprovou orcamento + cotas
4. Boletos/avisos de cobranca das cotas vencidas
5. Demonstrativo do indice oficial usado (impressao IGP-M/IPCA)
```

---

## 5. FUNDAMENTACAO LEGAL

- **CC art. 1.336, §1º** — Multa por inadimplencia ≤ 2%
- **CC art. 1.345** — Adquirente responde por debitos anteriores
- **CPC art. 784, X** — Credito condominial e titulo executivo
  extrajudicial
- **CPC art. 798, I, c** — Demonstrativo do debito atualizado obrigatorio
- **Tema 522 STJ** — Multa convencional para o adimplemento da
  obrigacao condominial nao se confunde com multa moratoria
- Jurisprudencia firme: juros de mora 1% am quando convencao
  silente (regra geral codigo civil — natureza condominial)

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. Conferir indices contra a FONTE OFICIAL do indice escolhido
   pela convencao (IGP-M = FGV, IPCA/INPC = IBGE). Esta skill NAO
   tem acesso a indices posteriores a Janeiro/2026.

2. Verificar se convencao foi devidamente REGISTRADA em cartorio
   de Registro de Imoveis — sem registro, eficacia restrita aos
   participantes da assembleia.

3. Confirmar que ATA que fixou as cotas tem quorum minimo
   (CC 1.341).

4. Multa convencional NAO PODE exceder 2% (CC 1.336 §1º) —
   excesso e nulo de pleno direito.

5. Capitalizacao mensal de juros so se convencao expressamente
   pactuar — caso contrario, juros simples.

6. Se convencao silente sobre indice, usar tabela pratica do
   TJ {{UF}} (consulta obrigatoria ao site do tribunal).

7. O calculo final tem efeito vinculante na execucao (CPC 524).
   Excesso gera embargos por excesso de execucao (CPC 525 §1º V).
```

---

## 7. INTEGRACAO

**Upstream (skills que podem chamar esta):**
- `calculos-master` (orquestrador, roteia por classificacao)
- `classificar-tipo-calculo` (identifica natureza condominial)

**Downstream (skills disparadas apos esta):**
- `protocolo-p4-calculos` (auditoria Suprema Corte R1-R4 — auto)
- `gestao-prazo-impugnacao` (se for em fase de cumprimento)

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Peticao inicial de execucao condominial | `/execucao peticao-inicial-execucao` | `execucao-adv-os` (Kirvano) |
| Embargos a execucao (defesa do condomino) | `/execucao embargos-execucao` | `execucao-adv-os` (Kirvano) |
| Notificacao extrajudicial previa | `/execucao notificacao-extrajudicial-mora` | `execucao-adv-os` (Kirvano) |
| Auditoria final com IA | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.

---

## 8. PROIBICOES

1. **NUNCA gerar valor final com indice hardcoded.** So formula + fonte.
2. **NUNCA citar indice especifico numerico** (ex: "IPCA de jul/2025 =
   0,28%"). Sempre placeholder `_____`.
3. **NUNCA aplicar multa > 2%** (CC 1.336 §1º — nulidade).
4. **NUNCA assumir capitalizacao composta** sem clausula expressa na
   convencao.
5. **NUNCA omitir aviso de validacao final.**
6. **NUNCA assumir titulo executivo sem convencao registrada** +
   ata de assembleia + comprovante de cobranca.
