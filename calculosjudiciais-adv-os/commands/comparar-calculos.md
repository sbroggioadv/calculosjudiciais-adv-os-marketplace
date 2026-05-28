---
description: ⭐ Killer feature — posiciona 2-3 calculos do mesmo caso lado a lado (autor x reu x contadoria, ou perito x perito-assistente). Identifica divergencias verba a verba e quantifica o gap monetario.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [caminhos dos calculos a comparar (2 ou 3) + contexto do caso]
---

Voce foi acionado pelo comando `/comparar-calculos` do plugin Calculosjudiciais-Adv-OS.

Argumento recebido: `$ARGUMENTS`

**Objetivo:** posicionar 2-3 calculos do mesmo caso lado a lado e identificar onde divergem (verba × valor × indice × juros), quantificando o gap entre eles.

## PROTOCOLO

### 1. Validar o input

- O argumento deve conter 2 ou 3 caminhos de arquivos de calculo (PDF, texto, planilha ou ja parseados via PJE-Calc)
- Identificar quem produziu cada calculo:
  - Calculo do autor / exequente
  - Calculo do reu / executado
  - Calculo da contadoria judicial
  - Calculo do perito oficial
  - Calculo do perito-assistente
- Se algum dos calculos for PJE-Calc PDF: auto-acionar `parser-auditor-pjecalc` antes para extrair estrutura

### 2. Acionar a skill `comparador-calculos` imediatamente

Use `Skill(skill="comparador-calculos")` passando os caminhos + labels.

A skill ira:

1. Normalizar cada calculo em estrutura comum (verbas + valores + criterios)
2. Posicionar lado a lado em tabela markdown
3. Identificar divergencias em 4 dimensoes:
   - **Verba:** verba presente em um e ausente em outro
   - **Valor:** mesma verba, valores diferentes
   - **Indice:** indice de correcao diferente
   - **Juros:** criterio de juros diferente (pre/pos ADC 58/59)
4. Quantificar o gap monetario total + por divergencia
5. Apontar qual lado tem fundamentacao tecnica mais solida em cada ponto

### 3. Output estruturado

```
## 📊 CALCULOS COMPARADOS
[tabela lado a lado: verba | calc-A | calc-B | calc-C | diff]

## 🔍 DIVERGENCIAS IDENTIFICADAS
[lista numerada por dimensao]

## 💰 GAP MONETARIO
[total + por divergencia + percentual]

## ⚖️ ANALISE TECNICA
[qual lado tem razao em cada ponto + fundamentacao]

## 📝 ESTRATEGIA
[se cliente e autor: como atacar o calculo menor / se cliente e reu: como atacar o calculo maior]
```

### 4. Auto-chain

- Se algum calculo tem erro grave → sugerir `/auditar-pjecalc` ou `/auditar-laudo-pericial`
- Auto-disparar `protocolo-p4-calculos` (R1-R4) ao final
- Se ha prazo de impugnacao em curso → `gestao-prazo-impugnacao`

## REGRAS DURAS

1. **NUNCA escolher um lado** sem analise tecnica fundamentada.
2. **SEMPRE quantificar** o gap em R$ (valor absoluto + percentual).
3. **SEMPRE citar** o dispositivo legal/sumula que sustenta cada lado.
4. **NUNCA omitir** divergencia, mesmo que pequena (acumula em valor de causa alto).
5. **Aviso final obrigatorio:** "Comparativo tecnico — antes de impugnar, validar parametros da sentenca exequenda."

**Skill a acionar:** `comparador-calculos`.
