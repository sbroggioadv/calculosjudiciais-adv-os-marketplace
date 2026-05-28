---
description: ⭐ Killer feature — audita laudo pericial contabil (PDF/texto). Confere base normativa NBC PP 01 CFC, coerencia interna, indices aplicados e cumprimento dos quesitos. Diferencial brutal de mercado.
allowed-tools: Read, Write, Edit, WebFetch, WebSearch, Bash, Glob, Grep
argument-hint: [caminho do laudo (PDF ou texto) + opcional: parametros da sentenca]
---

Voce foi acionado pelo comando `/auditar-laudo-pericial` do plugin Calculosjudiciais-Adv-OS.

Argumento recebido: `$ARGUMENTS`

**Objetivo:** auditar laudo pericial contabil produzido por perito oficial (ou perito-assistente da parte contraria) e identificar fragilidades tecnicas que sustentam impugnacao ou contra-laudo.

## PROTOCOLO

### 1. Validar o input

- Verificar que o argumento contem caminho de PDF ou texto do laudo
- Se possivel, identificar tambem os parametros da sentenca (so eles validam quais indices o perito DEVERIA ter usado)
- Sem parametros da sentenca: prosseguir mas avisar que auditoria fica parcial (so coerencia interna + base normativa, nao confronto com sentenca)

### 2. Acionar a skill `auditor-laudo-pericial-contabil` imediatamente

Use `Skill(skill="auditor-laudo-pericial-contabil")` passando o caminho + parametros.

A skill ira auditar 4 dimensoes:

#### a) Base normativa (NBC PP 01 CFC)

- Laudo identifica perito + numero CRC + ART?
- Estrutura segue NBC PP 01 (introducao + quesitos + metodologia + calculo + conclusao)?
- Indices aplicados estao fundamentados (citacao da fonte oficial)?

#### b) Coerencia interna

- Premissas declaradas → calculo executado bate?
- Resultado final = soma das parcelas detalhadas?
- Memoria de calculo permite refazer a conta?
- Anexos (planilhas, decisoes, citacoes) presentes e referenciados?

#### c) Indices aplicados

- Indices conferem com tabela oficial (`scripts/data/indices/*.json`)?
- Indices estao em conformidade com a sentenca?
- ADC 58/59 STF + Lei 14.905/2024 respeitados (calculos pos 2024-08)?
- Sumula aplicavel ao caso (362 STJ dano moral / 368 TST contrib. social / 539 STJ anatocismo) observada?

#### d) Cumprimento dos quesitos

- Todos os quesitos formulados pelas partes foram respondidos?
- Respostas tecnicas ou apenas evasivas?
- Quesito complementar pendente?

### 3. Output estruturado

```
## 📄 RESUMO DO LAUDO
[perito + CRC + objeto + total]

## 🔍 AUDITORIA NBC PP 01 CFC
[checklist por dimensao]

## ⚠️ FRAGILIDADES IDENTIFICADAS
[lista numerada com fundamentacao + impacto]

## 📝 BASE PARA IMPUGNACAO / CONTRA-LAUDO
[texto pronto + sugestao de auto-chain]
```

### 4. Auto-chain (Tier 3 transversais)

Apos auditoria, sugerir downstream:

- Se ha quesitos para perito → `/calculos gerador-quesitos-perito-contabil`
- Se cliente precisa de contra-laudo → `Skill(skill="contra-laudo-pericial")`
- Auto-disparar `protocolo-p4-calculos` (R1-R4)

### 5. Sugestao de plugin-irmao

```
| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Auditar com Suprema Corte R1-R4 | /ia-combativa suprema-corte | ia-combativa-adv-os |
| Buscar jurisprudencia sobre impugnacao | /juris buscar | juris-adv-os |
```

## REGRAS DURAS

1. **NUNCA "lembrar" valor de indice** — sempre consultar tabela cacheada local.
2. **SEMPRE citar** NBC PP 01 CFC + dispositivo legal + sumula/tema quando aplicavel.
3. **NUNCA acusar** o perito de erro sem citar o dispositivo descumprido.
4. **Aviso final obrigatorio:** "Auditoria tecnica preliminar — recomenda-se contra-laudo formal por perito-assistente registrado no CRC antes de impugnacao judicial."

**Skill a acionar:** `auditor-laudo-pericial-contabil`.
