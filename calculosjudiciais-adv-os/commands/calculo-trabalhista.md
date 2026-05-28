---
description: Atalho para calculos trabalhistas — liquidacao, verbas rescisorias, horas extras+reflexos, adicionais (insalubridade/periculosidade/noturno), deposito recursal. Roteia o orquestrador direto pro Tier 2 trabalhista.
allowed-tools: Read, Write, Edit, WebFetch, WebSearch, Bash, Glob, Grep
argument-hint: [tipo de calculo trabalhista + dados do caso]
---

Voce foi acionado pelo comando `/calculo-trabalhista` do plugin Calculosjudiciais-Adv-OS.

Argumento recebido: `$ARGUMENTS`

**Objetivo:** atalho direto para calculos trabalhistas — pular a classificacao automatica e ir direto pro Tier 2 trabalhista.

## PROTOCOLO

### 1. Acionar a skill `calculos-master` com area pre-fixada

Use `Skill(skill="calculos-master")` passando o argumento + flag `area=trabalhista`.

O orquestrador ja sabe que e trabalhista — vai direto pra:

| Palavra-chave no input | Skill acionada |
|---|---|
| "liquidacao", "art. 879 CLT", "parametros da sentenca" | `calculo-liquidacao-trabalhista` |
| "rescisao", "verbas rescisorias", "aviso previo", "FGTS+40%" | `calculo-verbas-rescisorias` |
| "horas extras", "HE", "DSR", "reflexos" | `calculo-horas-extras-reflexos` |
| "insalubridade", "periculosidade", "adicional noturno", "intervalo intrajornada" | `calculo-adicionais-trabalhistas` |
| "deposito recursal", "RO", "RR", "AIRR", "tabela TST" | `calculo-deposito-recursal` |

### 2. Pre-requisitos especificos

Antes de calcular, garantir que estao disponiveis:

- **Marco intertemporal** (pre/pos Reforma 13.467/2017) — afeta intervalo, intermitente, autonomo
- **CCT/ACT da categoria** (se aplicavel) — adicionais convencionais > legais
- **Sumula 368 TST itens IV/V** — contribuicao social sobre verbas trabalhistas
- **IRPF tabela progressiva acumulada** (Lei 7.713/88 art. 12-A) — calculo mes a mes, nao no total

### 3. Auto-chain obrigatorio

- Liquidacao → `atualizador-indices-cache` (IPCA-E pre-2024 + Selic pos-2024 conforme ADC 58/59)
- Toda saida final → `protocolo-p4-calculos` (R1-R4)
- Intimacao com prazo de impugnacao → `gestao-prazo-impugnacao` (CLT 879 §2º — 8 dias)

### 4. Sugestao de plugin-irmao (soft)

Se operador quiser peticionar a liquidacao apos o calculo:

```
| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Peticao de liquidacao completa | /trabalhista liquidacao | trabalhista-adv-os (Kirvano) |
```

NAO chamar, NAO importar. Apenas sugerir.

**Skill a acionar:** `calculos-master` (area=trabalhista).
