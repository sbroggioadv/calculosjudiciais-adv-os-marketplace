---
description: Atalho para calculos civeis — cumprimento de sentenca, RPV/precatorio, dano material/moral, debito condominial/locaticio, custas/honorarios, revisao bancaria. Roteia o orquestrador direto pro Tier 2 civel.
allowed-tools: Read, Write, Edit, WebFetch, WebSearch, Bash, Glob, Grep
argument-hint: [tipo de calculo civel + dados do caso]
---

Voce foi acionado pelo comando `/calculo-civel` do plugin Calculosjudiciais-Adv-OS.

Argumento recebido: `$ARGUMENTS`

**Objetivo:** atalho direto para calculos civeis — pular a classificacao automatica e ir direto pro Tier 2 civel.

## PROTOCOLO

### 1. Acionar a skill `calculos-master` com area pre-fixada

Use `Skill(skill="calculos-master")` passando o argumento + flag `area=civel`.

O orquestrador ja sabe que e civel — vai direto pra:

- `identificar-tj-aplicavel` (precisa de UF + comarca + valor da causa)
- Roteamento pra skill Tier 2 civel correta conforme palavras-chave no argumento:

| Palavra-chave no input | Skill acionada |
|---|---|
| "cumprimento", "sentenca transitada", "art. 523 CPC" | `calculo-cumprimento-sentenca-civel` |
| "RPV", "precatorio", "Fazenda Publica" | `calculo-rpv-precatorio` |
| "dano moral", "dano material", "lucros cessantes" | `calculo-danos-indenizatorios` |
| "condominio", "taxa condominial", "art. 1336 CC" | `calculo-debito-condominial` |
| "aluguel", "locacao", "Lei 8245" | `calculo-debito-locaticio` |
| "custas", "honorarios sucumbenciais", "art. 85 CPC" | `calculo-custas-honorarios` |
| "anatocismo", "Price", "SAC", "revisao bancaria" | `calculo-revisao-bancaria` |

### 2. Auto-chain obrigatorio

Toda saida final:

- Dispara `atualizador-indices-cache` se o calculo precisa atualizar valores
- Dispara `protocolo-p4-calculos` (R1-R4) ao final
- Se houver intimacao com prazo: dispara `gestao-prazo-impugnacao`

### 3. Anti-halucinacao

- NUNCA "lembrar" indice de tabela TJ. Identificar TJ → consultar tabela JSON local → se fora do range, fornecer formula + URL oficial.
- ADC 58/59 STF + Lei 14.905/2024 obrigatorias em juros pos 2024-08.
- Sumula 362 STJ obrigatoria em dano moral (correcao da data do arbitramento).

**Skill a acionar:** `calculos-master` (area=civel).
