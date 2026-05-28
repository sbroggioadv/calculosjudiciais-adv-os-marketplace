---
name: calculo-cumprimento-sentenca-civel
description: >
  CALCULO-CUMPRIMENTO-SENTENCA-CIVEL — Estrutura memoria de calculo
  para cumprimento de sentenca de quantia certa (CPC 523-538).
  Compoe: principal + correcao monetaria (tabela do TJ aplicavel via
  identificar-tj-aplicavel) + juros legais art. 406 CC pos Lei
  14.905/2024 (Taxa Legal = Selic - IPCA) + multa de 10% pelo nao
  pagamento em 15 dias (CPC 523 §1º) + honorarios de cumprimento de
  10% (mesmo dispositivo). NUNCA gera indices hardcoded — sempre
  consulta scripts/data/indices/*.json local. Use sempre que o
  advogado mencionar "cumprimento de sentenca", "executar sentenca
  civel", "intimar para pagar em 15 dias", "multa do art. 523",
  "honorarios de cumprimento", "iniciar a fase de cumprimento" ou
  variacoes.
---

# CALCULO-CUMPRIMENTO-SENTENCA-CIVEL — Quantia Certa (CPC 523-538)

## 1. ESCOPO

Skill estrutura a memoria de calculo da fase de **cumprimento
definitivo de sentenca que reconhece obrigacao de pagar quantia
certa** (CPC 523-527). Cobre:

- Atualizacao do valor da condenacao desde data fixada na sentenca
- Aplicacao da Taxa Legal pos Lei 14.905/2024 (CC 406)
- Multa de 10% pelo nao pagamento voluntario em 15 dias uteis
- Honorarios advocaticios de cumprimento (10%)

NAO cobre: execucao de titulo extrajudicial (ver `execucao-adv-os`),
cumprimento provisorio com peculiaridades (CPC 520-522), obrigacao
de fazer/nao fazer/entregar coisa.

---

## 2. INPUT NECESSARIO

Do contexto ou perguntar ao advogado:

1. **Numero do processo** e juizo (define TJ aplicavel)
2. **Valor da condenacao** + data-base fixada na sentenca (ex: "R$
   50.000 em 10/03/2023")
3. **Data do transito em julgado** (marco do CPC 523)
4. **Data da intimacao do devedor** (inicia prazo de 15 dias uteis)
5. **Data atual / data prevista do calculo final**
6. **Indice de correcao definido na sentenca** (se especificado) — caso
   contrario, aplicar tabela oficial do TJ via
   `identificar-tj-aplicavel`
7. **Houve pagamento parcial?** Datas e valores
8. **Existem honorarios sucumbenciais ja fixados na sentenca?**
   (compoem a base de calculo da multa do art. 523 §1º)

---

## 3. PROCESSAMENTO — CHECKLIST

### 3.1 Identificar TJ e tabela aplicavel
Disparar `identificar-tj-aplicavel` com UF + comarca para obter URL
oficial da tabela de correcao.

### 3.2 Atualizar valor principal (correcao monetaria)

```
valor_corrigido = valor_original × (acumulado_data_final / acumulado_data_inicial)
```

Consultar `scripts/data/indices/<indice>-mensal.json` conforme tabela
do TJ. Se data fora do `range_final` da tabela commitada → gerar
formula + link + placeholder (NUNCA inventar indice).

### 3.3 Aplicar juros legais (Taxa Legal CC 406 pos Lei 14.905/2024)

- **Pre 30/08/2024:** SELIC mensal acumulada (entendimento STJ pre
  Lei 14.905/2024 — EREsp 1.207.197)
- **Pos 30/08/2024:** Taxa Legal = Selic - IPCA (calculada via
  `scripts/data/indices/taxa-legal-cc406.json`)
- Termo inicial: transito em julgado ou termo fixado na sentenca

### 3.4 Calcular multa do art. 523 §1º

SE devedor intimado e NAO pagou em 15 dias uteis:
```
multa = (valor_corrigido + juros) × 10%
```

### 3.5 Calcular honorarios de cumprimento (CPC 523 §1º parte final)

```
honorarios_cumprimento = (valor_corrigido + juros) × 10%
```

Multa E honorarios sao cumulativos com sucumbenciais ja fixados.

### 3.6 Totalizar

```
total = valor_corrigido + juros + multa + honorarios_cumprimento + sucumbenciais_fixados - pagamentos_parciais
```

---

## 4. OUTPUT — Memoria de Calculo Estruturada

```markdown
## Memoria de Calculo — Cumprimento de Sentenca

**Processo:** [numero]
**Exequente:** {{ADVOGADO_NOME}} (OAB/{{ADVOGADO_UF}} {{ADVOGADO_OAB}}) representando [parte]
**Executado:** [parte]
**Juizo:** [vara/comarca/UF]

### Premissas

| Campo | Valor |
|---|---|
| Valor da condenacao | R$ [X] em [data-base] |
| Transito em julgado | [data] |
| Intimacao devedor (CPC 523) | [data] |
| Prazo 15 dias uteis findou em | [data calculada] |
| Pagamento voluntario? | [sim/nao/parcial] |
| Tabela de correcao | [TJ-XX] — [URL oficial] |
| Indice juros pre-30/08/2024 | SELIC (art. 406 CC redacao anterior) |
| Indice juros pos-30/08/2024 | Taxa Legal (Selic - IPCA, Lei 14.905/2024) |

### Tabela 1 — Atualizacao do valor principal

| Mes/Ano | Indice [TABELA] | Acumulado | Valor corrigido |
|---|---|---|---|
| [data inicial] | _____ | 1,000000 | R$ [valor original] |
| ... | _____ | _____ | _____ |
| [data final] | _____ | _____ | **R$ ___** |

**Formula:** principal_corrigido = principal × (acumulado_final / acumulado_inicial)
**Fonte obrigatoria:** [URL tabela oficial TJ]

### Tabela 2 — Juros legais (art. 406 CC)

| Periodo | Meses | Taxa aplicada | Juros |
|---|---|---|---|
| [transito] -> 29/08/2024 | [N] | SELIC mensal | R$ ___ |
| 30/08/2024 -> [data final] | [N] | Taxa Legal (Selic-IPCA) | R$ ___ |
| **Total juros** | | | **R$ ___** |

**Fonte:** scripts/data/indices/selic-mensal.json + taxa-legal-cc406.json

### Tabela 3 — Multa CPC 523 §1º (se nao pagto em 15d)

| Base de calculo | % | Valor |
|---|---|---|
| (Principal + Juros) | 10% | **R$ ___** |

### Tabela 4 — Honorarios de cumprimento (CPC 523 §1º)

| Base de calculo | % | Valor |
|---|---|---|
| (Principal + Juros) | 10% | **R$ ___** |

### Totalizacao

| Verba | Valor |
|---|---|
| Principal corrigido | R$ ___ |
| Juros legais | R$ ___ |
| Multa 10% (art. 523 §1º) | R$ ___ |
| Honorarios cumprimento (10%) | R$ ___ |
| Honorarios sucumbenciais (sentenca) | R$ ___ |
| Pagamentos parciais (-) | -R$ ___ |
| **TOTAL EM [data]** | **R$ ___** |

Valor sera atualizado ate a data do efetivo pagamento.
```

---

## 5. FUNDAMENTACAO LEGAL

- **CPC art. 513-538** — cumprimento de sentenca (regra geral)
- **CPC art. 523** — intimacao do devedor + prazo 15 dias uteis + multa 10% + honorarios 10%
- **CPC art. 524** — demonstrativo discriminado e atualizado
- **CPC art. 525** — impugnacao ao cumprimento (15 dias apos garantia)
- **CC art. 406** (redacao Lei 14.905/2024) — Taxa Legal = Selic - IPCA
- **Lei 14.905/2024** — em vigor desde 30/08/2024
- **REsp 1.207.197 (EREsp)** — SELIC como juros legais pre Lei 14.905/2024
- **Sumula 517 STJ** — multa do art. 523 incide tambem em cumprimento provisorio (com modulacoes)
- **Tema 677 STJ** — termo inicial da multa do art. 523

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ CONFERIR INDICES CONTRA TABELA OFICIAL VIGENTE DO TJ APLICAVEL ANTES DE PROTOCOLAR

1. Tabela de correcao monetaria — conferir contra publicacao
   atual do TJ ([URL]) — esta skill consulta cache local com
   range definido em scripts/data/indices/*.json.

2. Taxa Legal CC 406 (pos 30/08/2024) — conferir contra publicacao
   BCB + IBGE — taxa apurada mensalmente, pode haver revisao.

3. SELIC pre-Lei 14.905/2024 — conferir contra publicacao BCB.

4. Marco temporal Lei 14.905/2024 (30/08/2024) e CRITICO — se calculo
   atravessa essa data, segmentar em 2 periodos (item 3.3 acima).

5. Multa do art. 523 §1º exige INTIMACAO VALIDA do devedor — conferir
   data e modalidade da intimacao no processo.

6. Em caso de impugnacao por excesso de execucao (CPC 525 §1º V), o
   executado deve apontar valor que entende correto, sob pena de
   rejeicao (CPC 525 §4º).
```

---

## 7. INTEGRACAO

- **Upstream:** `identificar-tj-aplicavel` (define tabela), `classificar-tipo-calculo` (roteamento)
- **Downstream:** `protocolo-p4-calculos` (auditoria R1-R4 obrigatoria pos-calculo final), `gestao-prazo-impugnacao` (15 dias CPC 525)
- **Cross-link:** `atualizador-indices-cache` (sub-rotina pra atualizacao monetaria padronizada)

---

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Peticionar cumprimento de sentenca | `/execucao cumprimento-sentenca` | `execucao-adv-os` (Kirvano) |
| Defender o executado (impugnacao por excesso) | `/execucao embargos-execucao` | `execucao-adv-os` (Kirvano) |
| Auditar o calculo com Suprema Corte R1-R4 | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |
| Buscar jurisprudencia sobre multa do art. 523 | `/juris buscar Tema 677 STJ` | `juris-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.

---

## 8. PROIBICOES

1. NUNCA gerar indice numerico de memoria — sempre consultar
   `scripts/data/indices/*.json`
2. NUNCA aplicar SELIC pos 30/08/2024 sem segmentar com Taxa Legal
3. NUNCA aplicar multa do art. 523 sem confirmar intimacao valida
4. NUNCA usar indice INPC/IGP-M se a sentenca/TJ definiu outro
5. NUNCA omitir aviso obrigatorio de validacao final
6. NUNCA gerar valor final fora do range da tabela commitada — usar
   formula + placeholder
