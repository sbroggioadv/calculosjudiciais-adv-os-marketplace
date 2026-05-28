---
name: protocolo-p4-calculos
description: >
  PROTOCOLO-P4-CALCULOS — Auditoria Suprema Corte R1-R4 aplicada a
  qualquer calculo judicial gerado pelo plugin antes do protocolo.
  Quatro gates sequenciais: R1 BRIEF (premissas conferem com a
  sentenca/titulo executivo?), R2 CALCULO (matematica correta,
  formulas aplicadas, indices dentro do range?), R3 COMPLIANCE
  (fundamentacao legal completa, sumulas/temas STJ/STF, ADC 58/59
  + Lei 14.905/2024 quando aplicavel?), R4 PERFORMANCE (memoria
  clara, auditavel por terceiro). Veredito: APROVADA / REVISAR /
  BLOQUEADA. Auto-disparada apos qualquer calculo final do plugin.
  Especializada em pegadinhas de calculo (formula, termo inicial,
  juros compostos sem clausula, indice hardcoded). Use quando pedir
  auditoria de calculo, validar antes de protocolar, R1 R2 R3 R4,
  ou apos memoria de calculo gerada.
---

# PROTOCOLO-P4-CALCULOS — Auditoria R1-R4 Especializada em Calculo

## 1. ESCOPO

Quatro gates sequenciais de auditoria que rodam DEPOIS da geracao do
calculo, ANTES do protocolo. Cada gate emite veredito:
- ✅ **OK** (passa pro proximo)
- ⚠️ **REVISAR** (ajustar antes de prosseguir — recomendacao especifica)
- 🛑 **BLOQUEADO** (impede protocolo — exige correcao)

Veredito final consolidado:
- **APROVADA** — todos os 4 gates OK
- **REVISAR** — pelo menos 1 gate REVISAR (mas nenhum BLOQUEADO)
- **BLOQUEADA** — pelo menos 1 gate BLOQUEADO

---

## 2. INPUT NECESSARIO

Receber via auto-chain (skill upstream passa contexto):
1. **Memoria de calculo** completa gerada pela skill especifica
2. **Sentenca/contrato/titulo** que originou o calculo (texto ou
   referencia)
3. **Tipo de calculo** (qual skill gerou — civel/trabalhista/etc.)
4. **Indices usados** (preenchidos ou em placeholder)
5. **Data de protocolo prevista**

---

## 3. PROCESSAMENTO — OS 4 GATES

### R1 — BRIEF (Premissas conferem com a fonte?)

Auditar contra sentenca/contrato/titulo:

- [ ] **Verbas** — todas calculadas, nenhuma inventada/omitida
- [ ] **Termo correcao** — bate com sentenca/lei (dano moral = arbitramento Sum. 362; indebito = pagamento Sum. 43)
- [ ] **Termo juros** — citacao (contratual) / evento (extracontratual) — Sum. 54 STJ
- [ ] **Indice correcao** — determinado pela sentenca/TJ/lei especial
- [ ] **Taxa juros** — pactuada / legal / CC 406 pos-14.905/2024 / ADC 58/59 trabalhista
- [ ] **Periodo** — datas inicial/final coerentes com pedido
- [ ] **Partes** — nomes, CPF/CNPJ, processo conferem

**Pegadinha R1:** termo inicial errado (citacao quando sentenca fixou evento) → matematica certa mas REJEITADA.

### R2 — CALCULO (Matematica esta certa?)

- [ ] **Indices dentro do range** da tabela JSON; se fora, formula explicita + link oficial
- [ ] **Formulas corretas** (simples vs composta — Sum. 539 STJ exige clausula expressa em bancario)
- [ ] **Sequencia** — primeiro corrige depois juros simples sobre principal corrigido
- [ ] **Pagamentos parciais imputados** (CC 354 — juros antes de principal)
- [ ] **Honorarios** sobre base correta (CPC 85 §2º — condenacao/proveito/valor causa)
- [ ] **Multa** incide sobre principal corrigido, NAO sobre juros
- [ ] **Arredondamento** consistente (2 casas decimais, nao truncar)

**Pegadinha R2:** capitalizar juros sem clausula expressa (Sum. 539 STJ) → embargos por excesso.

### R3 — COMPLIANCE (Fundamentacao legal completa?)

- [ ] **Artigos atuais** (CC 406 pos Lei 14.905/2024 — Taxa Legal substituiu SELIC para juros civis desde 30/08/2024)
- [ ] **Sumulas aplicaveis** citadas
- [ ] **Temas vinculantes** STJ/STF (ADC 58/59 trabalhista, Tema 810 STF precatorios, Tema 905 STJ previdenciario)
- [ ] **Marco intertemporal** (trabalhista pre/pos ADC 58; civil pre/pos 30/08/2024)
- [ ] **Tabela do TJ** correta para o foro (alimentos = domicilio alimentando; condominial = imovel; etc.)
- [ ] **Aviso de validacao final** presente

**Pegadinha R3:** ignorar Lei 14.905/2024 em calculos civis pos 30/08/2024 — usar SELIC quando deveria usar Taxa Legal (SELIC - IPCA, ver `taxa-legal-cc406.json`).

### R4 — PERFORMANCE (Auditavel por terceiro?)

- [ ] **Memoria refazivel** por contador judicial
- [ ] **Tabela parcela-a-parcela** (quando aplicavel)
- [ ] **Formulas explicitas** em cada bloco
- [ ] **Fontes citadas** (link TJ/BCB/CJF)
- [ ] **Formato BR** — datas DD/MM/AAAA; R$ com 2 casas, separador 1.234,56
- [ ] **Aviso de cutoff** presente
- [ ] **Sugestao plugins-irmaos** (sinaliza, nao executa)

**Pegadinha R4:** so o valor final sem memoria → impugnacao por falta de demonstrativo (CPC 524 II/IV).

---

## 4. OUTPUT — RELATORIO CONSOLIDADO

```markdown
## Auditoria R1-R4 — Protocolo P4 Calculos

**Calculo auditado:** [tipo + data + valor total]
**Skill geradora:** [nome da skill upstream]

---

### R1 — BRIEF (Premissas)

| Item | Status | Observacao |
|------|--------|------------|
| Verbas completas | ✅/⚠️/🛑 | [observacao] |
| Termo inicial correcao | ✅/⚠️/🛑 | [observacao] |
| Termo inicial juros | ✅/⚠️/🛑 | [observacao] |
| Indice aplicavel | ✅/⚠️/🛑 | [observacao] |
| Taxa juros aplicavel | ✅/⚠️/🛑 | [observacao] |
| Periodo coerente | ✅/⚠️/🛑 | [observacao] |
| Partes identificadas | ✅/⚠️/🛑 | [observacao] |

**Veredito R1:** ✅ OK / ⚠️ REVISAR / 🛑 BLOQUEADO

---

### R2 — CALCULO (Matematica)

| Item | Status | Observacao |
|------|--------|------------|
| Indices dentro do range | ✅/⚠️/🛑 | [observacao] |
| Formulas corretas | ✅/⚠️/🛑 | [observacao] |
| Sequencia matematica | ✅/⚠️/🛑 | [observacao] |
| Pagamentos parciais imputados | ✅/⚠️/🛑 | [observacao] |
| Honorarios sobre base correta | ✅/⚠️/🛑 | [observacao] |
| Multa em base correta | ✅/⚠️/🛑 | [observacao] |
| Arredondamento consistente | ✅/⚠️/🛑 | [observacao] |

**Veredito R2:** ✅ OK / ⚠️ REVISAR / 🛑 BLOQUEADO

---

### R3 — COMPLIANCE (Fundamentacao)

| Item | Status | Observacao |
|------|--------|------------|
| Artigos atuais (Lei 14.905/2024) | ✅/⚠️/🛑 | [observacao] |
| Sumulas aplicaveis | ✅/⚠️/🛑 | [lista das principais] |
| Temas STJ/STF | ✅/⚠️/🛑 | [lista] |
| Marco intertemporal | ✅/⚠️/🛑 | [observacao] |
| Tabela TJ correta | ✅/⚠️/🛑 | [observacao] |
| Aviso de validacao | ✅/⚠️/🛑 | [observacao] |

**Veredito R3:** ✅ OK / ⚠️ REVISAR / 🛑 BLOQUEADO

---

### R4 — PERFORMANCE (Apresentacao)

| Item | Status | Observacao |
|------|--------|------------|
| Memoria refazivel | ✅/⚠️/🛑 | [observacao] |
| Tabela parcela-a-parcela | ✅/⚠️/🛑 | [observacao] |
| Formulas explicitas | ✅/⚠️/🛑 | [observacao] |
| Fontes citadas | ✅/⚠️/🛑 | [observacao] |
| Formato brasileiro datas/R$ | ✅/⚠️/🛑 | [observacao] |
| Aviso de cutoff | ✅/⚠️/🛑 | [observacao] |
| Sugestao plugins-irmaos | ✅/⚠️/🛑 | [observacao] |

**Veredito R4:** ✅ OK / ⚠️ REVISAR / 🛑 BLOQUEADO

---

## VEREDITO CONSOLIDADO

✅ APROVADA — pode protocolar
⚠️ REVISAR — corrigir [N] itens marcados acima antes do protocolo
🛑 BLOQUEADA — corrigir os itens 🛑 antes de prosseguir; calculo
            atual nao pode ser protocolado

### Recomendacoes especificas

1. [se houver]
2. [se houver]
3. [se houver]

### Proximos passos

[Se APROVADA] → protocolar com a planilha + memoria
[Se REVISAR] → ajustar e auto-disparar nova rodada R1-R4
[Se BLOQUEADA] → corrigir, regerar via skill geradora, nova rodada R1-R4
```

---

## 5. AVISOS OBRIGATORIOS NO OUTPUT FINAL

```
⚠️ APOS AUDITORIA R1-R4:

1. APROVADA NAO substitui revisao humana final — o advogado e o
   responsavel ultimo pelo conteudo do protocolo.

2. R1-R4 e auditoria de COERENCIA INTERNA + LEGAL FORMAL. Nao
   substitui parecer de contador especializado em casos complexos
   (perícia, divergencia, controversia).

3. Se R3 marcou pendencia em "Tabela TJ correta": confirmar foro
   da execucao antes do protocolo — competencia errada gera
   redistribuicao + perda de prazo.

4. Se R2 marcou pendencia em "Indices dentro do range": indices apos
   range_final da tabela JSON DEVEM ser preenchidos manualmente da
   fonte oficial — esta skill nao "atualiza" indices em runtime.
```

---

## 6. FUNDAMENTACAO LEGAL

- **CPC art. 524** — demonstrativo discriminado da divida atualizada
- **CPC art. 525 §1º V** — embargos por excesso de execucao
- **CPC art. 853-854** — perícia para liquidacao de sentenca
- **Sumula 362 STJ** — termo correcao dano moral
- **Sumula 43 STJ** — termo correcao indebito
- **Sumula 54 STJ** — termo juros contratual/extracontratual
- **Sumula 539 STJ** — capitalizacao bancaria exige clausula expressa
- **ADC 58/59 STF (2020)** — IPCA-E + Selic em trabalhista
- **Lei 14.905/2024** — Taxa Legal substituiu SELIC para CC 406
  (vigente 30/08/2024)
- **Tema 810 STF** — IPCA-E em precatorios
- **Tema 905 STJ** — correcao e juros pos-EC 113/2021 em Fazenda
- **CC art. 406** (com Lei 14.905/2024) — Taxa Legal = SELIC - IPCA
- **CC art. 354** — imputacao de pagamento

---

## 7. INTEGRACAO

- **Upstream:** TODAS as skills de calculo do plugin (auto-disparada)
- **Downstream:** se APROVADA, libera output final; se REVISAR/BLOQUEADA,
  retorna a skill geradora para correcao

**Auto-chain critica:** TODA skill de calculo final do plugin
(`calculo-*`) DEVE disparar `protocolo-p4-calculos` antes de marcar
output como final.

---

## 8. PROIBICOES

1. **NUNCA marcar APROVADA** com pelo menos 1 gate em 🛑.
2. **NUNCA pular auditoria** mesmo a pedido — regra dura.
3. **NUNCA "consertar" calculo automaticamente** — sinalizar e
   retornar a skill geradora; correcao e deliberada.
4. **NUNCA omitir alerta** quando indices fora do range estao em uso.
5. **NUNCA marcar R3 OK** se Lei 14.905/2024 nao foi considerada em
   calculo civil pos 30/08/2024.
6. **NUNCA aprovar calculo trabalhista** sem ADC 58/59 STF aplicada.
