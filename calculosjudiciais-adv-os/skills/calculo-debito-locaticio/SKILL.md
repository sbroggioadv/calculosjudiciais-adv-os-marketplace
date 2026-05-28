---
name: calculo-debito-locaticio
description: >
  CALCULO-DEBITO-LOCATICIO — Estrutura memoria de calculo de
  debito de aluguel inadimplente (Lei 8.245/91 — Inquilinato).
  Compoe aluguel vencido + encargos (IPTU, condominio, agua, luz
  rateada conforme contrato) + multa contratual + juros 1% am +
  correcao monetaria (indice contratual). Considera multa
  rescisoria proporcional (art. 4º — denuncia antecipada do
  locatario; art. 9º — hipoteses de rescisao). NUNCA gera valor
  final com indice hardcoded (anti-halucinacao). Produz memoria
  mes a mes. Use quando o advogado mencionar: "aluguel atrasado",
  "debito locaticio", "acao de despejo por falta de pagamento",
  "execucao de aluguel", "cobranca de inquilino", "multa
  rescisoria locacao", "purga da mora", "encargos locaticios".
---

# CALCULO-DEBITO-LOCATICIO — Memoria de Calculo Estruturada

## 1. ESCOPO

Estrutura calculo de divida locaticia (Lei 8.245/91). Cobre:

- Alugueis vencidos (mes a mes)
- Encargos contratualmente atribuidos ao locatario (IPTU,
  condominio, agua, luz, taxas)
- Multa contratual moratoria (clausula penal — usualmente 10%)
- Juros de mora (1% am — default codigo civil)
- Correcao monetaria (indice contratual — IGP-M, IPCA, INPC)
- Multa rescisoria proporcional (art. 4º — denuncia antecipada
  pelo locatario)
- Possibilidade de purga da mora (art. 62, II)

Base legal: **Lei 8.245/91 (Lei do Inquilinato)** + **CC art. 406**
+ **CPC art. 784, VIII** (contrato escrito de locacao = titulo
executivo extrajudicial dos alugueis vencidos).

---

## 2. INPUT NECESSARIO

Do contexto + perguntar:

1. **Identificacao** das partes (locador + locatario + fiador, se
   houver) + imovel locado
2. **Contrato de locacao:** prazo, valor do aluguel, indice de
   correcao, data-base do reajuste anual
3. **Lista de alugueis vencidos:** mes/ano + valor + data
   vencimento
4. **Encargos atribuidos ao locatario** (clausula contratual):
   IPTU, condominio, agua, luz, taxas — listar por mes
5. **Multa contratual moratoria:** percentual (usualmente 10%)
6. **Multa rescisoria** (clausula penal compensatoria): valor
   total (geralmente 3 alugueis) — verificar se aplicavel
   (denuncia antecipada do locatario — art. 4º)
7. **Indice de correcao contratual:** IGP-M, IPCA, INPC
8. **Data ate quando atualizar**
9. **Tipo de garantia** (caucao, fianca, seguro-fianca, cessao
   fiduciaria) — pode impactar legitimidade
10. **Possibilidade de purga da mora?** (art. 62, II — uma vez a
    cada 24 meses)

---

## 3. PROCESSAMENTO — PASSOS

1. Validar titulo executivo: contrato escrito (CPC 784, VIII)
2. Listar alugueis vencidos mes a mes
3. Listar encargos vencidos mes a mes (separado do aluguel)
4. Aplicar correcao monetaria de cada parcela desde o vencimento
5. Aplicar multa contratual moratoria sobre cada parcela
   inadimplente
6. Aplicar juros de mora 1% am desde cada vencimento
7. Se denuncia antecipada do locatario (art. 4º): calcular multa
   rescisoria PROPORCIONAL ao tempo restante do contrato
8. Somar verbas: alugueis + encargos + multa contratual + juros
   + (eventual) multa rescisoria
9. Emitir aviso obrigatorio: validacao final + alertar sobre
   direito de purga (art. 62, II)

---

## 4. OUTPUT — PLANILHA ESTRUTURADA

```markdown
## Memoria de calculo — Debito locaticio

**Atencao:** este calculo apresenta ESTRUTURA + FORMULA. Os indices
numericos devem ser preenchidos a partir da fonte oficial (IBGE/FGV
conforme indice contratual). Esta skill NAO tem acesso a indices
posteriores a Jan/2026.

### Premissas

| Campo | Valor |
|---|---|
| Locador | [nome] |
| Locatario | [nome] |
| Fiador (se houver) | [nome] |
| Imovel | [endereco] |
| Contrato | [data inicio - data fim] |
| Aluguel base | R$ [X] |
| Indice de correcao contratual | [IGP-M / IPCA / INPC] |
| Multa contratual moratoria | [X% — usualmente 10%] |
| Multa rescisoria (se aplicavel) | [valor total — geralmente 3 alugueis] |
| Juros de mora | 1% am (CC 406) |
| Termo final do calculo | [data] |
| Titulo executivo (CPC 784, VIII) | sim |

### Tabela 1 — Alugueis vencidos

| Mes/Ano | Vencimento | Valor nominal |
|---|---|---|
| [mes] | [dd/mm/aaaa] | R$ _____ |
| ... | ... | ... |
| **TOTAL ALUGUEIS NOMINAIS** | | **R$ _____** |

### Tabela 2 — Encargos vencidos (clausula contratual)

| Mes/Ano | IPTU | Condominio | Agua | Luz | Outros | Total |
|---|---|---|---|---|---|---|
| [mes] | R$ _ | R$ _ | R$ _ | R$ _ | R$ _ | R$ _ |
| ... | | | | | | |
| **TOTAL ENCARGOS** | | | | | | **R$ _** |

### Tabela 3 — Correcao monetaria por parcela

Para CADA parcela (aluguel + encargos):

| Parcela (mes/ano) | Indice inicial | Indice final | Coef. | Valor corrigido |
|---|---|---|---|---|
| [mes] | _____ | _____ | _____ | R$ _____ |

**Formula:** valor_corrigido = valor_nominal × (indice_final / indice_inicial)

**FONTE OBRIGATORIA:**
- IGP-M: portalibre.fgv.br
- IPCA / INPC: ibge.gov.br/estatisticas/economicas/precos-e-custos

### Tabela 4 — Multa contratual moratoria

Para CADA parcela inadimplente:
multa = valor_corrigido × [percentual_contratual] / 100

| Parcela | Valor corrigido | Multa (%) | Valor multa |
|---|---|---|---|
| [mes] | R$ _____ | [X%] | R$ _____ |

### Tabela 5 — Juros de mora (1% am, simples)

| Parcela | Vencimento | Meses ate termo | Juros |
|---|---|---|---|
| [mes] | [dd/mm/aaaa] | [N] | R$ _____ |

**Formula:** juros = valor_corrigido × 0,01 × N_meses

### Tabela 6 — Multa rescisoria proporcional (art. 4º Lei 8.245)

**SO se denuncia antecipada do locatario.** Calcular pela formula:

multa_proporcional = multa_total × (meses_restantes / meses_totais)

| Campo | Valor |
|---|---|
| Multa total contratada | R$ _____ |
| Meses totais do contrato | [X] |
| Meses ja cumpridos | [Y] |
| Meses restantes | [X - Y] |
| **Multa proporcional devida** | **R$ _____** |

### Totalizacao

| Verba | Valor |
|---|---|
| Alugueis corrigidos (Tabela 3) | R$ _____ |
| Encargos corrigidos (Tabela 3) | R$ _____ |
| Multa contratual moratoria (Tabela 4) | R$ _____ |
| Juros de mora (Tabela 5) | R$ _____ |
| Multa rescisoria proporcional (Tabela 6, se aplicavel) | R$ _____ |
| **TOTAL ATE [data]** | **R$ _____** |

Valor sera atualizado ate o efetivo pagamento ou desocupacao.

### Anexos obrigatorios

1. Esta memoria (planilha)
2. Contrato de locacao escrito
3. Comprovantes de cobranca + notificacao
4. Boletos/recibos de IPTU/condominio/agua/luz dos meses cobrados
5. Demonstrativo do indice oficial usado
```

---

## 5. FUNDAMENTACAO LEGAL

- **Lei 8.245/91 art. 4º** — Multa proporcional na denuncia antecipada
  pelo locatario
- **Lei 8.245/91 art. 9º** — Hipoteses de rescisao da locacao
- **Lei 8.245/91 art. 22, VIII** — Locador deve pagar IPTU (salvo
  pactuacao em contrario)
- **Lei 8.245/91 art. 23, XII** — Locatario deve pagar despesas ordinarias
- **Lei 8.245/91 art. 62, II** — Direito de purga da mora (uma vez
  cada 24 meses)
- **Lei 8.245/91 art. 63 a 66** — Procedimento da acao de despejo
- **CC art. 406** — Juros legais 1% am
- **CC art. 408** — Multa contratual nao excedente da obrigacao
- **CC art. 413** — Possibilidade de reducao judicial da clausula
  penal manifestamente excessiva
- **CPC art. 784, VIII** — Contrato escrito de locacao = titulo
  executivo extrajudicial

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. Conferir indices contra a FONTE OFICIAL (IGP-M = FGV, IPCA/INPC =
   IBGE). Esta skill NAO tem acesso a indices posteriores a
   Janeiro/2026.

2. Verificar se contrato esta ESCRITO (CPC 784, VIII) — locacao
   verbal nao gera titulo executivo extrajudicial.

3. Confirmar se locatario tem direito de PURGAR a mora (art. 62, II
   Lei 8.245) — usado uma vez a cada 24 meses. Se aplicavel, calculo
   deve permitir quitacao em 15 dias.

4. Multa rescisoria proporcional (art. 4º) SO se denuncia antecipada
   foi do LOCATARIO — se foi do locador sem culpa do locatario, NAO
   incide.

5. Encargos como agua/luz so sao devidos se houver clausula
   contratual expressa OU se locatario for o consumidor direto.

6. Se clausula penal for manifestamente excessiva, juiz pode
   reduzir (CC 413). Multa moratoria habitual: 10%.

7. Acao de despejo por falta de pagamento exige nominal de alugueis +
   encargos + multa + juros + custas + honorarios advocaticios
   (Lei 8.245 art. 62).

8. O calculo final tem efeito vinculante na execucao. Excesso gera
   embargos (CPC 525 §1º V).
```

---

## 7. INTEGRACAO

**Upstream:**
- `calculos-master` (orquestrador)
- `classificar-tipo-calculo` (identifica natureza locaticia)

**Downstream:**
- `protocolo-p4-calculos` (auditoria Suprema Corte — auto)
- `gestao-prazo-impugnacao` (se cumprimento de sentenca)

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Acao de despejo por falta de pagamento | `/execucao peticao-inicial-cobranca` | `execucao-adv-os` (Kirvano) |
| Notificacao extrajudicial de purga | `/execucao notificacao-extrajudicial-mora` | `execucao-adv-os` (Kirvano) |
| Contestacao a despejo (defesa do locatario) | `/execucao contestacao-cobranca` | `execucao-adv-os` (Kirvano) |
| Auditoria final com IA | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.

---

## 8. PROIBICOES

1. **NUNCA gerar valor final com indice hardcoded.** So formula + fonte.
2. **NUNCA citar indice especifico numerico.** Sempre placeholder `_____`.
3. **NUNCA aplicar multa rescisoria integral** quando contrato ja
   foi parcialmente cumprido — sempre proporcional (art. 4º).
4. **NUNCA assumir encargos** sem clausula contratual expressa
   atribuindo-os ao locatario.
5. **NUNCA omitir o direito de purga da mora** (art. 62, II) no
   aviso final.
6. **NUNCA omitir o aviso de validacao final.**
