---
name: calculo-revisao-bancaria
description: >
  CALCULO-REVISAO-BANCARIA — Estrutura memoria de revisao de
  contrato bancario (cedula de credito, financiamento, leasing,
  cartao, cheque especial). Aplica CDC art. 51, IV (clausulas
  abusivas) + Sum. 539 STJ (capitalizacao mensal SO se
  expressamente pactuada e taxa anual > 12x mensal) + Sum. 596 STF
  (instituicoes financeiras nao se submetem ao teto de juros da
  Lei de Usura). Recalcula saldo expurgando anatocismo nao
  pactuado. Explica diferenca entre SAC (amortizacao constante)
  e Price (parcela constante) e impacto na revisao. Use quando o
  advogado mencionar: "revisao bancaria", "anatocismo",
  "capitalizacao de juros", "Tabela Price", "SAC vs Price",
  "expurgo de juros", "abusividade contratual", "limitacao de
  juros bancarios", "cheque especial abusivo", "cartao de
  credito rotativo", "financiamento de veiculo", "Sum. 539",
  "Sum. 596".
---

# CALCULO-REVISAO-BANCARIA — Memoria de Calculo Estruturada

## 1. ESCOPO

Revisao bancaria para expurgar:

- **Anatocismo** (Sum. 539 STJ)
- **Juros remuneratorios abusivos** (comparativo taxa media BCB)
- **Comissao de permanencia cumulada** com encargos moratorios (Sum. 472 STJ)
- **Tarifas indevidas** TAC/TEC/registro/avaliacao (Tema REsp 1.578.553 STJ)
- **Seguro com venda casada** (CDC 39 I)

Compara SAC × Price (cronograma e juros totais). Base: CDC 51 IV + Sum. 539/472/30 STJ + Sum. 596 STF.

---

## 2. INPUT NECESSARIO

Do contexto + perguntar:

1. **Tipo:** CCB, financiamento veiculo/imovel, leasing, cartao, cheque especial
2. **Contrato + aditivos** (juros, capitalizacao, tarifas)
3. **Valor financiado** + prazo + N parcelas
4. **Amortizacao:** SAC, Price, misto
5. **Taxa mensal e anual** contratada
6. **Clausula expressa de capitalizacao mensal?** (Sum. 539 STJ)
7. **Tarifas cobradas:** TAC, TEC, registro, avaliacao, seguro
8. **Comissao permanencia cumulada** com multa/moratorios/correcao? (Sum. 472)
9. **Inadimplencia atual:** valor cobrado pelo banco
10. **Polo cliente:** consumidor (CDC) ou empresarial (CC)

---

## 3. PROCESSAMENTO

1. Identificar natureza (CDC/CC)
2. Analisar juros: se `taxa_anual > 12 × taxa_mensal` ha capitalizacao mensal embutida → exige clausula expressa (Sum. 539); senao, recalcular juros simples
3. Identificar sistema (SAC/Price)
4. Reconstruir cronograma sem anatocismo (juros simples sobre saldo devedor)
5. Comparar com taxa media BCB (taxa muito acima = indicio de abusividade; Sum. 596 STF nao impede revisao de excesso)
6. Tarifas (Tema REsp 1.578.553): TAC licita se razoavel; TEC ABUSIVA; registro/avaliacao licitas se efetivamente prestados
7. Comissao de permanencia legitima SO se nao cumulada (Sum. 472)
8. Recalcular saldo expurgando abusos
9. Emitir aviso obrigatorio

---

## 4. OUTPUT — PLANILHA ESTRUTURADA

```markdown
## Memoria de calculo — Revisao bancaria

**Atencao:** este calculo apresenta ESTRUTURA + FORMULA. Taxas
medias do BCB devem ser consultadas no site oficial. Esta skill
NAO tem acesso a taxas BCB posteriores a Jan/2026.

### Premissas

| Campo | Valor |
|---|---|
| Tipo de contrato | [CCB/financiamento/leasing/etc] |
| Banco | [nome] |
| Valor financiado | R$ _____ |
| Data do contrato | [dd/mm/aaaa] |
| Prazo | [N parcelas] |
| Sistema de amortizacao | [SAC / Price / misto] |
| Taxa juros mensal contratada | [X%] |
| Taxa juros anual contratada | [Y%] |
| Capitalizacao mensal pactuada? | [sim/nao — clausula X] |
| Natureza | consumo (CDC) / empresarial (CC) |

---

### Parte 1 — Diagnostico de anatocismo (Sum. 539 STJ)

**Teste matematico:**
- Se taxa_anual ≈ 12 × taxa_mensal → SEM capitalizacao mensal
- Se taxa_anual > 12 × taxa_mensal → HA capitalizacao mensal

| Calculo | Valor |
|---|---|
| Taxa mensal contratada | [X%] |
| 12 × taxa mensal | [12X%] |
| Taxa anual contratada | [Y%] |
| Diferenca | [Y - 12X] |
| **Ha capitalizacao mensal?** | [sim/nao] |

**Validade:** capitalizacao mensal SO e LICITA se:
1. Contrato firmado APOS 31/03/2000 (MP 2.170-36/2001)
2. Clausula EXPRESSA prevendo (Sum. 539 STJ)

Se ausente clausula expressa OU contrato anterior a 31/03/2000 →
**recalcular com juros simples** (expurgo do anatocismo).

---

### Parte 2 — Comparativo SAC × Price

**SAC (Amortizacao Constante):** A = principal/N; J_n =
saldo × i; P_n = A + J_n. Parcelas decrescentes. Total juros
MENOR.

**Price (Frances):** P = principal × [i(1+i)^N] / [(1+i)^N - 1].
Parcelas constantes. Total juros MAIOR. STJ majoritario: Price NAO
e anatocismo automatico se clausula expressa + pos-31/03/2000
(Sum. 539). Comparativo formal com SAC pode revelar excesso.

---

### Parte 3 — Recalculo do saldo devedor (sem anatocismo)

**SE houve capitalizacao indevida** → reconstituir cronograma:

| Mes | Saldo inicial | Amortizacao | Juros simples | Parcela | Saldo final |
|---|---|---|---|---|---|
| 1 | R$ _____ | R$ _____ | R$ _____ | R$ _____ | R$ _____ |
| 2 | _____ | _____ | _____ | _____ | _____ |
| ... | _____ | _____ | _____ | _____ | _____ |
| N | _____ | _____ | _____ | _____ | R$ 0,00 |

**Formula juros simples:** J = principal × i × t (sem
capitalizacao do saldo devedor sobre os juros do mes anterior).

---

### Parte 4 — Tarifas analisadas (Tema REsp 1.578.553 STJ)

| Tarifa | Cobrada? | Valor | Status (jurisprudencia) | Expurgar? |
|---|---|---|---|---|
| TAC (Abertura Credito) | sim/nao | R$ _ | Licita se razoavel | nao/sim |
| TEC (Emissao Carne) | sim/nao | R$ _ | ABUSIVA | sim |
| Registro contrato | sim/nao | R$ _ | Licita se efetivamente prestada | depende |
| Avaliacao veiculo | sim/nao | R$ _ | Licita se efetivamente prestada | depende |
| Seguro vida/protecao | sim/nao | R$ _ | Abusiva se venda casada (CDC 39 I) | depende |
| **TOTAL TARIFAS A EXPURGAR** | | | | **R$ _____** |

---

### Parte 5 — Comissao de permanencia (Sum. 472 STJ)

| Verificacao | Resultado |
|---|---|
| Banco cobrou comissao de permanencia? | sim/nao |
| Cumulou com correcao monetaria? | sim/nao → abusiva |
| Cumulou com juros moratorios? | sim/nao → abusiva |
| Cumulou com multa contratual? | sim/nao → abusiva |
| **Comissao a expurgar (se cumulou)** | R$ _____ |

---

### Parte 6 — Comparativo de saldos

| Item | Valor cobrado pelo banco | Valor recalculado | Diferenca |
|---|---|---|---|
| Saldo devedor atual | R$ _____ | R$ _____ | R$ _____ |
| Total parcelas | _____ | _____ | _____ |
| Tarifas | _____ | (expurgadas) | _____ |
| Comissao permanencia | _____ | (expurgada se cumulada) | _____ |
| **TOTAL SALDO REVISADO** | | **R$ _____** | **R$ _____** |

---

### Anexos obrigatorios

1. Esta memoria (planilha) + cronograma mes a mes
2. Contrato bancario original + todos os aditivos
3. Demonstrativo do banco com saldo cobrado
4. Comprovantes de pagamento das parcelas pagas
5. Comparativo taxa contratada × taxa media BCB do periodo
   (consulta bcb.gov.br/estatisticas/historicodastaxasdejuros)
```

---

## 5. FUNDAMENTACAO LEGAL

- **CDC art. 6º V / 39 I / 51 IV / 52** — Modificacao de clausulas
  abusivas, venda casada vedada, nulidade de abusivas, liquidacao
  antecipada com reducao
- **CC art. 591** — Anatocismo vedado salvo lei especial
- **MP 2.170-36/2001 art. 5º** — Permite capitalizacao em contratos
  bancarios pos 31/03/2000
- **Sum. 30 STJ** — Capitalizacao semestral licita se expressa
- **Sum. 296 STJ** — Juros remuneratorios revisados se abusivos
- **Sum. 472 STJ** — Comissao permanencia nao cumula com encargos
  moratorios
- **Sum. 539 STJ** — Capitalizacao mensal licita: contrato pos
  31/03/2000 + clausula expressa
- **Sum. 596 STF** — Bancos nao sujeitos a Lei de Usura
- **Tema 247 STJ** — Pactuacao expressa pode ser comprovada por
  taxa anual > 12 × mensal
- **Tema REsp 1.578.553 STJ** — TAC/Registro licitas se pactuadas
  e razoaveis; TEC abusiva

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. Conferir TAXA MEDIA BCB para tipo/periodo:
   bcb.gov.br/estatisticas/historicodastaxasdejuros. Skill nao
   tem acesso a taxas pos Jan/2026.

2. Capitalizacao mensal licita SO se: contrato pos 31/03/2000 +
   clausula EXPRESSA (Sum. 539 STJ).

3. Sum. 596 STF: bancos nao sujeitos a Lei de Usura.
   Abusividade exige comparativo com taxa media BCB +
   circunstancias concretas (CDC 51).

4. TEC (Tarifa Emissao Carne) SEMPRE abusiva (Tema 1.578.553).
   TAC e Registro licitas se pactuadas e razoaveis.

5. Comissao de permanencia (Sum. 472): licita isolada, abusiva
   se cumulada com correcao + juros moratorios + multa.

6. Contratos APOS 30/06/2024 (Lei 14.905/2024): nova taxa legal
   CC 406 (Selic - IPCA) — verificar incidencia pos-inadimplencia.

7. Cliente PJ (nao consumidor): aplicar CC (boa-fe CC 421-422),
   revisao mais restrita que CDC 51.

8. Pode incluir repeticao de indebito em DOBRO (CDC 42) se
   indevida e sem engano justificavel (Tema 929 STJ).

9. Submeter a perito judicial — anexar laudo contabil se possivel.
```

---

## 7. INTEGRACAO

**Upstream:**
- `calculos-master` (orquestrador)
- `classificar-tipo-calculo` (identifica natureza bancaria)

**Downstream:**
- `protocolo-p4-calculos` (auditoria Suprema Corte — auto)
- `gestao-prazo-impugnacao` (se cumprimento ou impugnacao)
- `calculo-restituicao-dobro-cdc` (se houver indebito a restituir)

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Acao revisional de contrato bancario | `/execucao peticao-inicial-cobranca` | `execucao-adv-os` (Kirvano) |
| Embargos em execucao bancaria | `/execucao embargos-execucao` | `execucao-adv-os` (Kirvano) |
| Auditoria final com IA | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |
| Buscar julgado atualizado sobre tarifa X | `/juris buscar` | `juris-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.

---

## 8. PROIBICOES

1. **NUNCA pleitear expurgo de capitalizacao** se contrato pos
   31/03/2000 + clausula expressa (Sum. 539 STJ).
2. **NUNCA invocar Lei da Usura** contra banco (Sum. 596 STF).
3. **NUNCA recalcular** sem segregar consumidor (CDC) de PJ (CC).
4. **NUNCA citar taxa media BCB hardcoded.** Sempre placeholder +
   fonte oficial.
5. **NUNCA cumular** expurgo de comissao de permanencia + outros
   encargos sem provar a cumulacao no contrato (Sum. 472).
6. **NUNCA assumir Price = anatocismo automatico** — posicao do
   STJ e que Price e admissivel com clausula expressa.
7. **NUNCA omitir aviso de validacao final.**
