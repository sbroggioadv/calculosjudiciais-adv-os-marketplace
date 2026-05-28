---
name: calculo-liquidacao-trabalhista
description: >
  CALCULO-LIQUIDACAO-TRABALHISTA — Liquidacao de sentenca trabalhista (CLT
  879). Aplica parametros da sentenca em verbas + reflexos + INSS + IRRF +
  correcao monetaria (ADC 58/59 STF + Lei 14.905/2024) + juros. SIDE-AWARE
  (reclamante calcula a maior, reclamada impugna). Use quando o operador
  disser "liquidacao trabalhista", "liquidar sentenca CLT", "memoria de
  calculo trabalhista", "impugnar conta de liquidacao", "art. 879 CLT",
  "executar sentenca trabalhista". Anti-halucinacao: indice consultado em
  scripts/data/indices/*.json, nunca lembrado.
---

# CALCULO-LIQUIDACAO-TRABALHISTA — Liquidacao de Sentenca (CLT art. 879)

## 1. ESCOPO

Skill Tier 2 do plugin `calculosjudiciais-adv-os`. Executa a **liquidacao
de sentenca trabalhista** — fase posterior ao transito em julgado da
sentenca de merito, em que se apura o **quantum debeatur** aplicando os
parametros fixados no titulo executivo.

**Acionada quando o operador menciona:** liquidacao de sentenca,
liquidar trabalhista, art. 879 CLT, memoria de calculo da execucao,
impugnacao a conta, conta de liquidacao, calcular verbas da sentenca.

## 2. SIDE-AWARENESS

Pergunte **sempre** antes de iniciar: qual o polo do cliente?

| Polo | Postura do calculo |
|------|--------------------|
| **Reclamante (exequente)** | Calcular **a maior** — incluir todas as verbas reconhecidas, com reflexos plenos, juros e correcao maximos legalmente admissiveis. Memoria detalhada para apresentar como conta inicial. |
| **Reclamada (executada)** | Calcular **a minima** — conferir cada verba da conta do exequente, identificar excessos (verbas nao deferidas na sentenca, reflexos vedados, indices incorretos, juros em duplicidade), produzir conta-contraposta para impugnacao em **8 dias** (art. 879 §2o CLT). |

O calculo matematico e neutro; o **uso estrategico** segue o polo.

## 3. INPUT NECESSARIO

Pedir ao operador (e parar com Ponto de Omissao se faltar):

- **Sentenca** (ou dispositivo): quais verbas foram deferidas, qual o
  marco temporal, quais reflexos foram expressamente acolhidos
- **Periodo contratual** (admissao, saida, modalidade de rescisao)
- **Salario-base** (e evolucao salarial se houver)
- **Jornada** (divisor 220, 200, 180)
- **Data do ajuizamento** (marco para Selic — fase judicial)
- **Data do vencimento de cada verba** (marco para correcao pre-judicial)
- **CCT/ACT aplicavel** (se houver — pode alterar adicional, base de calculo)
- **Modalidade da rescisao** (com/sem justa causa, pedido demissao,
  rescisao indireta, distrato, culpa reciproca)
- **Existe calculo da parte contraria?** (se sim, oferecer
  `comparador-calculos` em seguida)

## 4. MODALIDADES DE LIQUIDACAO (CLT art. 879)

| Modalidade | Quando aplicar |
|------------|----------------|
| **Por calculos** (regra) | Sentenca fixou todos os parametros — basta aplicar a memoria de calculo. |
| **Por arbitramento** | Depende de avaliacao tecnica (ex.: valor de bem, percentual de insalubridade pendente de pericia). |
| **Por artigos** | Necessario provar **fato novo** indispensavel a apuracao do valor. |

A esmagadora maioria das liquidacoes trabalhistas e **por calculos**.

## 5. PROCESSAMENTO — 7 PASSOS

### Passo 1 — Mapear parametros da sentenca
Listar **cada verba deferida** com: percentual, base de calculo, periodo,
reflexos expressamente reconhecidos, indices determinados.

### Passo 2 — Apurar cada verba (valor principal)
Aplicar a formula correta segundo o tipo da verba:
- Verbas rescisorias -> chamar `calculo-verbas-rescisorias`
- Horas extras + reflexos -> chamar `calculo-horas-extras-reflexos`
- Adicionais (insalubridade/periculosidade/noturno) -> chamar
  `calculo-adicionais-trabalhistas`
- Outras verbas (multa 477, diferencas salariais, FGTS nao depositado,
  PLR, etc.) -> aplicar diretamente.

### Passo 3 — Aplicar reflexos
Confirmar quais reflexos a sentenca acolheu **expressamente**. Aplicar
nas verbas correlatas (DSR, 13o, ferias+1/3, aviso, FGTS+40%). Observar
**OJ 394 SDI-1 TST** — vedacao da "dobra do DSR" (DSR ja integrado nao
volta a integrar 13o, ferias, etc.).

### Passo 4 — Correcao monetaria — **ADC 58/59 STF + Lei 14.905/2024**

**Periodo PRE-judicial (do vencimento ate o ajuizamento):**
- **IPCA-E** (sumula 381 TST: correcao desde o **mes subsequente** ao
  vencimento da obrigacao trabalhista)
- Consultar `scripts/data/indices/ipca-e-mensal.json` — **NUNCA**
  inventar indice.

**Periodo POS-judicial (do ajuizamento em diante):**
- **Selic** (engloba juros + correcao monetaria — sem cumulacao)
- Consultar `scripts/data/indices/selic-mensal.json`.

**Periodo POS Lei 14.905/2024 (vigencia 30/08/2024):**
- Nova metodologia legal do CC art. 406 paragrafo unico: **IPCA**
  (correcao) + **Selic deduzido IPCA** (juros). Aplica-se
  subsidiariamente ao processo do trabalho — sempre **`[VERIFICAR]`**
  doutrina/jurisprudencia trabalhista do momento do calculo.

### Passo 5 — Juros
- **Ate 30/08/2024** (entrada em vigor da Lei 14.905) — segue ADC 58/59
  STF: Selic absorve juros na fase pos-ajuizamento.
- **Apos 30/08/2024** — taxa legal CC 406 paragrafo unico: Selic - IPCA.
  Consultar `scripts/data/indices/taxa-legal-cc406.json`.

### Passo 6 — Contribuicao previdenciaria + IRRF
- **Sumula 368 TST**:
  - Item **IV** — INSS calculado **mes a mes** (regime de competencia),
    aplicando o teto vigente em cada competencia.
  - Item **V** — IRPF retido na fonte: **tabela progressiva acumulada**
    (Lei 7.713/88 art. 12-A) — pagamento acumulado tributa-se com tabela
    do mes do pagamento mas com base na quantidade de meses a que se
    refere o credito.
- **Sumula 381 TST** — correcao desde o **mes subsequente** ao
  vencimento (criterio de incidencia da correcao).
- **Importante**: juros NAO integram base de calculo de INSS/IRRF.

### Passo 7 — Memoria de calculo auditavel
Output em markdown estruturado: cada verba com fundamento, base,
periodo, indice aplicado, percentual, valor principal, atualizacao,
juros, total. Subtotais por grupo + total geral. Qualquer terceiro
deve conseguir refazer.

## 6. OUTPUT — MODELO

```markdown
# Memoria de Calculo — Liquidacao Trabalhista
**Processo:** [numero]   **Reclamante:** [nome]
**Polo do cliente:** [reclamante/reclamada]
**Data-base do calculo:** [DD/MM/AAAA]

## Parametros da sentenca
[lista das verbas deferidas + reflexos expressos + indices]

## Apuracao por verba

### 1. [Nome da verba]
- Fundamento: [artigo/sumula]
- Base de calculo: R$ [valor]
- Periodo: [mm/aaaa - mm/aaaa]
- Indice aplicado (pre-ajuizamento): IPCA-E (fonte:
  scripts/data/indices/ipca-e-mensal.json, data_extracao: AAAA-MM-DD)
- Indice aplicado (pos-ajuizamento): Selic (fonte:
  scripts/data/indices/selic-mensal.json, data_extracao: AAAA-MM-DD)
- Valor principal: R$ [valor]
- Correcao: R$ [valor]
- Juros: R$ [valor]
- **Subtotal: R$ [valor]**

[repetir para cada verba]

## Resumo

| Grupo | Bruto | Correcao | Juros | INSS | IRRF | Liquido |
|-------|-------|----------|-------|------|------|---------|
| Rescisorias | | | | | | |
| Horas extras + reflexos | | | | | | |
| Adicionais | | | | | | |
| **TOTAL** | | | | | | |

## Avisos legais

> Este calculo foi gerado por skill automatizada. **Validar contra fonte
> oficial** antes de protocolar. Indices consultados em cache local —
> `range_final` da tabela: [AAAA-MM]. Para meses posteriores, conferir
> [URL oficial].
>
> Lei 14.905/2024 — aplicacao subsidiaria ao processo do trabalho
> permanece em discussao doutrinaria. Verificar entendimento do TRT/TST.
```

## 7. FUNDAMENTACAO LEGAL

- **CLT art. 879** — liquidacao de sentenca (por calculos/arbitramento/artigos)
- **CLT art. 879 §2o** — prazo comum de **8 dias** para impugnacao
- **Sumula 368 TST**:
  - Item IV — INSS mes a mes
  - Item V — IRPF tabela progressiva acumulada (Lei 7.713/88 art. 12-A)
- **Sumula 381 TST** — correcao desde o mes subsequente ao vencimento
- **OJ 394 SDI-1 TST** — vedacao da dobra do DSR nos demais reflexos
- **ADC 58/59 STF** — IPCA-E pre-ajuizamento + Selic pos-ajuizamento
- **Lei 14.905/2024** — nova metodologia CC art. 406 paragrafo unico
  (IPCA + Selic-IPCA) — `[VERIFICAR]` aplicacao trabalhista
- **Lei 7.713/88 art. 12-A** — IRPF tabela progressiva acumulada (RRA)

## 8. PROIBICOES

1. NUNCA "lembrar" valor de indice — sempre consultar
   `scripts/data/indices/*.json`
2. NUNCA gerar valor final fora do `range_final` da tabela — usar
   formula + link oficial + placeholder
3. NUNCA incluir verba que a sentenca nao deferiu (PA-05 do polo)
4. NUNCA aplicar reflexo que a OJ 394 SDI-1 veda
5. NUNCA misturar juros no calculo base de INSS/IRRF
6. NUNCA ignorar marco intertemporal (pre-Reforma 11/11/2017 vs pos)
7. NUNCA omitir aviso de validacao no rodape

## 9. INTEGRACAO

- **Acionada por:** `calculos-master`, `/calculo-trabalhista`,
  `/calculos liquidacao-trabalhista`
- **Aciona em sequencia:** `calculo-verbas-rescisorias`,
  `calculo-horas-extras-reflexos`, `calculo-adicionais-trabalhistas`
  (conforme as verbas da sentenca)
- **Apoio:** `atualizador-indices-cache` (consulta tabelas JSON),
  `comparador-calculos` (se houver conta da parte contraria)
- **Encadeia:** `protocolo-p4-calculos` (auditoria R1-R4 obrigatoria)

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---------------|---------|-------------------|
| Impugnar conta do exequente (8 dias) | `/trabalhista liquidacao-execucao-trabalhista` | `trabalhista-adv-os` (Kirvano) |
| Auditar calculo de PJE-CALC do escritorio contrario | `/calculos auditar-pjecalc` | (este plugin) |
| Comparar 2-3 calculos lado a lado | `/calculos comparar-calculos` | (este plugin) |
| Pericia contabil | `/trabalhista pericia-trabalhista` | `trabalhista-adv-os` (Kirvano) |
| Suprema Corte R1-R4 da conta | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar
> manualmente.
