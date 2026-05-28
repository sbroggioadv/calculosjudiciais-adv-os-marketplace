---
name: contra-laudo-pericial
description: >
  CONTRA-LAUDO-PERICIAL — Gera memoria de contra-laudo (impugnacao
  tecnica formal) ao laudo do perito oficial, baseada em NBC PP 01
  CFC + CPC 477 + Sumulas/Temas STJ/STF/TST aplicaveis ao caso.
  Recebe o laudo oficial + parametros do polo cliente (tese,
  documentos, calculo alternativo) e produz contra-laudo estruturado:
  (1) qualificacao do assistente tecnico, (2) ponto-a-ponto de
  impugnacao tecnica do laudo oficial, (3) calculo alternativo
  proprio, (4) conclusao tecnica autonoma, (5) sugestao de quesitos
  complementares ou nova pericia (CPC 480). Use SEMPRE que o usuario
  disser "contra-laudo", "impugnar laudo do perito", "parecer do
  assistente tecnico", "rebater pericia", "laudo divergente",
  "/auditar-laudo-pericial contra-laudo", "preciso de assistente
  tecnico".
---

# CONTRA-LAUDO-PERICIAL — Impugnacao Tecnica do Laudo Oficial

## 1. ESCOPO

Skill final do trio (audita → quesita → contra-lauda) de pericia
contabil. Quando `auditor-laudo-pericial-contabil` detecta vermelho
estrutural OU quando o polo cliente decide impugnar formalmente o
laudo, esta skill gera o **PARECER TECNICO DO ASSISTENTE** — peca
de assinatura conjunta advogado + assistente tecnico (CPC 466 § 1º).

E o documento tecnico que ataca o laudo oficial e oferece calculo
alternativo, no qual o juiz vai se basear (junto com o laudo) pra
decidir CPC 479.

## 2. INPUT NECESSARIO

| Campo | Obrigatorio | Observacoes |
|---|---|---|
| `laudo_oficial_path` ou `laudo_texto` | sim | Laudo do perito oficial |
| `parametros_polo_cliente` | sim | Tese, documentos, premissas |
| `calculo_alternativo` | sim | Memoria de calculo do assistente tecnico (pode ser gerada via skills Tier 2) |
| `assistente_tecnico` | sim | Nome, CRC, especialidade (apresentado nos autos) |
| `polo_cliente` | sim | autor/reu/exequente/executado |
| `area_pericia` | sim | civel/trab/trib/familia/revisional |
| `sentenca_decisao` | desejavel | Para argumentar com base no comando judicial |
| `auditoria_anterior` | opcional | Output do `auditor-laudo-pericial-contabil` (auto-pull) |

## 3. PROCESSAMENTO

### Estrutura canonica do contra-laudo (NBC PP 01 + CPC 477)

#### Secao I — Qualificacao e habilitacao
- Identificacao do assistente tecnico
- CRC ativo e regular
- Indicacao nos autos
- Termo de compromisso (e ele assina o parecer)

#### Secao II — Objeto da impugnacao
- Numero CNJ + vara + partes
- Pedido formal de impugnacao do laudo oficial (CPC 477)
- Indicacao dos pontos especificos impugnados

#### Secao III — Sintese do laudo oficial (resumo executivo)
- 2-3 paragrafos do que o perito oficial concluiu
- Identifica claramente os pontos a serem rebatidos

#### Secao IV — Pontos de impugnacao tecnica (ponto a ponto)

Para cada ponto:
1. **Ponto impugnado** (transcricao literal do laudo)
2. **Fundamento da impugnacao** (norma violada — NBC PP 01,
   CPC 473, Sumula, Tema)
3. **Argumentacao tecnica** (porque esta errado)
4. **Impacto quantificado** (gap em R$ se aplicavel)
5. **Solucao tecnica proposta**

#### Secao V — Calculo alternativo (memoria propria)
- Premissas declaradas
- Metodologia explicita (Sumula 539 STJ, Tema X STF, etc.)
- Memoria mes a mes (ou operacao a operacao)
- Resultado final
- Anexos (planilha + documentos)

#### Secao VI — Conclusao tecnica autonoma
- Sintese final do assistente
- Resposta direta aos quesitos do polo cliente
- Recomendacao processual:
  - Adesao ao laudo oficial (se nada substancial divergir)
  - Esclarecimentos (CPC 477 § 2º)
  - Substituicao parcial do laudo oficial pelo contra-laudo
  - Nova pericia (CPC 480)

#### Secao VII — Pedido
- Acolhimento do contra-laudo
- Determinacao de esclarecimentos ao perito oficial
- Subsidiariamente: nova pericia
- Assinatura conjunta advogado + assistente tecnico

## 4. OUTPUT

```markdown
## ⚖️ Contra-Laudo Tecnico — Processo {{numero}}

**Polo cliente:** [{{POLO}}]
**Perito oficial:** [Nome — CRC ___]
**Assistente tecnico:** [Nome — CRC ___]

### I — Qualificacao

[Nome do assistente] CRC [XX/000.000-O/X], regular e
adimplente, ja indicado nos autos (fls. ___), apresenta
PARECER TECNICO DO ASSISTENTE em impugnacao parcial ao
laudo oficial (fls. ___), nos termos do art. 477 do CPC.

### II — Objeto

Impugnam-se especificamente os seguintes pontos do laudo
oficial:

(a) [ponto 1 — sintese]
(b) [ponto 2 — sintese]
(c) [ponto 3 — sintese]

### III — Sintese do laudo oficial

O laudo oficial concluiu que [...]. Adotou as seguintes
premissas: [...]. Aplicou a seguinte metodologia: [...].

### IV — Pontos de impugnacao tecnica

#### Ponto 1 — [titulo]

**Trecho impugnado:** "[transcricao literal do laudo]"

**Fundamento da impugnacao:**
- NBC PP 01 item ___
- CPC art. 473, II
- Sumula ___ do STJ
- [outras normas aplicaveis]

**Argumentacao tecnica:**
[parágrafos tecnicos explicando o erro]

**Impacto quantificado:** o ponto impugnado infla o valor
final em R$ ___ (___% do total), conforme demonstrado no
calculo alternativo abaixo (Secao V).

**Solucao tecnica proposta:**
[o que o laudo deveria ter feito]

---

#### Ponto 2 — [titulo]
[mesma estrutura]

#### Ponto 3 — [titulo]
[mesma estrutura]

### V — Calculo alternativo

**Premissas adotadas (declaradas):**
1. [premissa 1 — fundamento]
2. [premissa 2 — fundamento]
3. [premissa 3 — fundamento]

**Metodologia:**
- Indice correcao: [IPCA-E / Selic / Tema 810 / ADC 58]
- Indice juros: [Taxa Legal CC406 / Selic / 1% am]
- Marco temporal: [data X — fundamento]
- Sumulas aplicadas: [Sum. 539 STJ; Sum. 368 TST; etc.]

**Memoria de calculo (resumo):**

| Verba/Operacao | Calculo oficial (R$) | Calculo do assistente (R$) | Gap (R$) |
|---|---:|---:|---:|
| [verba 1] | ___ | ___ | ___ |
| [verba 2] | ___ | ___ | ___ |
| **TOTAL** | **___** | **___** | **___** |

**Planilha detalhada:** anexa (Anexo A)

### VI — Conclusao tecnica

O laudo oficial, embora atendendo parcialmente aos comandos
do juizo, contem incorrecoes tecnicas estruturais que
conduzem a resultado divergente em R$ ___ (___%) do que
seria correto pela metodologia adequada.

Recomenda-se: [esclarecimentos / substituicao parcial /
nova pericia, conforme gravidade].

### VII — Pedido

Requer-se a V. Exa.:

(a) acolhimento do presente parecer em impugnacao parcial;
(b) intimacao do perito oficial para esclarecimentos sobre
    os pontos 1-3 (CPC 477 § 2º);
(c) subsidiariamente, designacao de nova pericia (CPC 480),
    com perito especializado em [area];
(d) na manutencao do laudo, que este contra-laudo seja
    considerado elemento de conviccao (CPC 479).

[Local, Data]

{{ADVOGADO_NOME}} — OAB/{{ADVOGADO_UF}} {{ADVOGADO_OAB}}

[Assinatura conjunta — Assistente Tecnico]
CRC ___

### Anexos

- Anexo A — Planilha detalhada do calculo alternativo
- Anexo B — Documentos consultados
- Anexo C — [outros]

> ⚠️ **Validar contra fonte oficial antes de protocolar.**
> Este contra-laudo e modelo tecnico — adaptar ao caso
> concreto e revisar conjuntamente com o assistente tecnico
> indicado.
```

## 5. FUNDAMENTACAO LEGAL

- **CPC 466 § 1º** — atuacao do assistente tecnico
- **CPC 473** — requisitos do laudo
- **CPC 477** — esclarecimentos + impugnacao (15 dias)
- **CPC 479** — laudo nao vincula o juiz
- **CPC 480** — nova pericia
- **NBC PP 01 / NBC TP 01 (CFC)** — pericia contabil
- **Resolucao CFC 1.243/2009** — procedimentos
- **Sumulas por area:** civel revisional Sum. 539/541/530 STJ; trabalhista Sum. 368/381 TST; tributaria Sum. 461/162/188 STJ + Tema 69 STF
- **REsp 1.214.794/SP** — limites de impugnacao
- **Tema 905 STJ** — juros/correcao Fazenda
- **ADC 58/59 STF + Lei 14.905/2024** — atualizacao

## 6. AVISOS OBRIGATORIOS NO OUTPUT

1. ⚠️ Validar contra fonte oficial antes de protocolar
2. ⚠️ Contra-laudo deve ter assinatura CONJUNTA com
   assistente tecnico (CRC ativo) — sem isso vale como
   manifestacao do advogado mas nao como parecer pericial
3. ⚠️ Prazo CPC 477 — 15 dias comuns para impugnar +
   apresentar contra-laudo
4. ⚠️ Se assistente tecnico nao foi indicado dentro do
   prazo do CPC 465 § 1º (15 dias da nomeacao do perito),
   ainda assim pode-se apresentar parecer juntando peca
   tecnica do assistente (ele apenas nao acompanha
   diligencias)
5. ⚠️ Contra-laudo nao gera vinculacao automatica do
   juiz — o juiz decide pelo elemento de conviccao
   (CPC 479)
6. ⚠️ Se ha 3+ vermelhos estruturais, mais eficaz pedir
   nova pericia (CPC 480) do que impugnar ponto a ponto

## 7. INTEGRACAO

- **Upstream:** `calculos-master`,
  `auditor-laudo-pericial-contabil` (auto se alertas vermelhos),
  `/auditar-laudo-pericial contra-laudo`
- **Encadeamento recomendado:** (1) auditor diagnostica → (2)
  skill Tier 2 da area gera memoria alternativa → (3)
  `comparador-calculos` side-by-side → (4) esta skill empacota
- **Downstream auto:** `gestao-prazo-impugnacao`,
  `protocolo-p4-calculos`
- **Cross-link:** `civel-adv-os` / `trabalhista-adv-os` /
  `tributario-societario-adv-os` (peca), `execucao-adv-os`
  (embargos), `ia-combativa-adv-os` (R1-R4), `juris-adv-os`

## 8. PROIBICOES

1. **Nunca** apresentar contra-laudo sem assinatura do
   assistente tecnico (CRC ativo)
2. **Nunca** afirmar que o perito oficial agiu de ma-fe
   (so impugnar tecnicamente)
3. **Nunca** importar dados de outros plugins em runtime
4. **Nunca** apresentar calculo alternativo sem memoria
   detalhada anexa
5. **Nunca** ocultar premissa adotada — sempre declarar
6. **Nunca** usar indice sem fundamentar via Sumula/Tema/Lei
7. **Nunca** apresentar valor final sem aviso obrigatorio
8. **Nunca** confundir contra-laudo (PARECER TECNICO do
   assistente) com impugnacao puramente juridica do
   advogado (PETICAO de manifestacao) — sao pecas distintas
   que podem conviver

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Auditar laudo oficial ponto a ponto | `/auditar-laudo-pericial` | `calculosjudiciais-adv-os` (este) |
| Comparar side-by-side laudo vs contra-laudo | `/comparar-calculos` | `calculosjudiciais-adv-os` (este) |
| Gerar quesitos complementares | `/auditar-laudo-pericial quesitos` | `calculosjudiciais-adv-os` (este) |
| Peca formal de impugnacao | `/civel impugnacao-laudo` ou `/trabalhista impugnacao-laudo` | `civel-adv-os` ou `trabalhista-adv-os` |
| Embargos a execucao | `/execucao embargos-execucao` | `execucao-adv-os` |
| Auditoria Suprema R1-R4 da peca | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` |
| Validar Sumulas/Temas | `/juris validar` | `juris-adv-os` |

> Se plugin nao instalado, copiar memoria do contra-laudo
> acima e usar manualmente (com assinatura conjunta do
> assistente tecnico).
