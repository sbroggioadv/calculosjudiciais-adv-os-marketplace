---
description: Atualiza um valor unico entre duas datas pelo indice indicado (Selic, IPCA, IPCA-E, INPC, TR, Taxa Legal CC 406). Anti-halucinacao — consulta tabela JSON local; fora do range, retorna formula + URL oficial.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [valor + data inicial + data final + indice]
---

Voce foi acionado pelo comando `/atualizar-valor` do plugin Calculosjudiciais-Adv-OS.

Argumento recebido: `$ARGUMENTS`

**Objetivo:** atualizar um valor monetario unico entre duas datas, com indice oficial cacheado localmente — operacao basica usada em peticoes simples sem necessidade de orquestrador completo.

## PROTOCOLO

### 1. Parsing do argumento

Identificar 4 campos no argumento:

- **valor** — R$ XXX,XX (aceitar formatos: "1.500,00", "1500", "1500.00", "R$ 1500", etc.)
- **data inicial** — DD/MM/AAAA ou AAAA-MM-DD
- **data final** — DD/MM/AAAA ou AAAA-MM-DD (default: hoje)
- **indice** — selic / ipca / ipca-e / inpc / tr / taxa-legal-cc406

Se faltar campo: perguntar ao operador qual falta (NAO inventar).

### 2. Acionar a skill `atualizador-indices-cache` imediatamente

Use `Skill(skill="atualizador-indices-cache")` passando os 4 campos.

A skill ira:

1. Identificar o arquivo de tabela: `scripts/data/indices/<indice>-mensal.json`
2. Validar que o intervalo [data_inicial, data_final] cabe em [range_inicial, range_final] da tabela
3. **Dentro do range:** aplicar fator acumulado mes a mes → valor final
4. **Fora do range:** gerar formula + link oficial + placeholder (NAO valor final)

### 3. Output estruturado

```
## 💰 ATUALIZACAO DE VALOR

| Campo | Valor |
|---|---|
| Valor original | R$ X.XXX,XX |
| Data inicial | DD/MM/AAAA |
| Data final | DD/MM/AAAA |
| Indice | NOME do indice |
| Fonte | URL oficial |

## 📊 CALCULO

[ou: valor final R$ Y.YYY,YY (fator X,YYYYY)]
[ou: formula + link oficial + placeholder]

## ✅ FONTE CONSULTADA

- Arquivo cacheado: scripts/data/indices/<indice>-mensal.json
- Range coberto: [AAAA-MM] a [AAAA-MM]
- Data de extracao: AAAA-MM-DD
- Release do plugin: vX.Y.Z

## ⚠️ AVISO LEGAL

Indice cacheado de release passada do plugin. Para protocolar, validar contra
fonte oficial: <URL_OFICIAL>
```

### 4. Anti-halucinacao (regra dura)

- NUNCA "lembrar" valor de indice — sempre consultar tabela JSON local.
- NUNCA gerar valor final se o intervalo cai fora do `range_final` da tabela.
- Fora do range = formula + URL oficial + placeholder, e operador completa manualmente.
- Aviso de release vigente OBRIGATORIO no rodape.

### 5. Selecao de indice por contexto

Se o operador nao especificou o indice, sugerir conforme natureza:

| Natureza | Indice sugerido |
|---|---|
| Tributo federal | Selic |
| Atrasados INSS (pre 09/2009) | Poupanca → SELIC |
| Atrasados INSS (pos 09/2009) | IPCA-E (Tema 810 STF) |
| Tabela TJ civel | Indice da tabela TJ (varia por UF) |
| RPV/Precatorio (Fazenda) | IPCA-E (Tema 810 STF) |
| Liquidacao trabalhista pos 2024-08 | Selic (CC 406 §u, Lei 14.905/2024) |
| Liquidacao trabalhista pre 2024-08 | IPCA-E (ADC 58 STF) |
| Reajuste contratual generico | IGP-M, IPCA ou INPC (conforme contrato) |

**Skill a acionar:** `atualizador-indices-cache`.
