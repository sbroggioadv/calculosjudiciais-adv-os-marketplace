---
name: gerador-quesitos-perito-contabil
description: >
  GERADOR-QUESITOS-PERITO-CONTABIL — Gera quesitos tecnicos para
  perito contador, calibrados por tipo de acao + parametros da
  sentenca + polo do cliente. Tres modos: (1) quesitos iniciais a
  formular ANTES da pericia (CPC 465 §1º), (2) quesitos
  complementares apos laudo evasivo (CPC 477 §2º), (3) contraditorio
  pontual aos quesitos da parte adversa. Cobre civel (dano material/
  moral, lucros cessantes, revisao bancaria, condominial, locaticio),
  trabalhista (revisao FGTS, horas extras, salario in natura,
  insalubridade, periculosidade), tributaria (apuracao IRPF/IRPJ,
  compensacao, exclusao ICMS na base PIS/COFINS), familia (partilha,
  alimentos, inventario), revisional. Use quando o usuario disser
  "quesitos pro perito", "formular quesitos", "quesitos complementares",
  "quesitos contabeis", "/auditar-laudo-pericial quesitos", "preparar
  pericia", "indicar assistente tecnico".
---

# GERADOR-QUESITOS-PERITO-CONTABIL — Engenharia Reversa de Pericia

## 1. ESCOPO

Skill complementar ao `auditor-laudo-pericial-contabil`. Em vez de
auditar laudo pronto, ANTECIPA: gera quesitos tecnicos especificos
para perito contador antes (ou depois) da pericia, calibrados pelo
tipo de acao + polo do cliente.

Mercado: o "quesitario padrao" copiado de modelo vira generico, perito
responde "prejudicado por falta de elementos", advogado perde a
oportunidade processual. Aqui geramos quesitos cirurgicos.

## 2. INPUT NECESSARIO

| Campo | Obrigatorio | Observacoes |
|---|---|---|
| `tipo_acao` | sim | civel/trabalhista/tributaria/familia/revisional/falimentar/inventario |
| `subtipo` | sim | ex: "horas extras + reflexos", "revisao bancaria SAC/Price", "exclusao ICMS PIS-COFINS", "partilha em comunhao parcial" |
| `polo_cliente` | sim | autor/reu/exequente/executado/inventariante/herdeiro/cobrador/cobrado |
| `modo` | sim | iniciais \| complementares \| contraditorio |
| `parametros_sentenca` ou `decisao_interlocutoria` | desejavel | Para quesitos complementares: comando judicial |
| `quesitos_adversario` | opcional | Para modo contraditorio |
| `laudo_pericial` | opcional | Para modo complementares — apos leitura do laudo |
| `area_normativa_critica` | opcional | Sumulas/Temas STJ/STF/TST a citar nos quesitos |

## 3. PROCESSAMENTO

### Modo 1 — Quesitos iniciais (CPC 465 §1º)

Antes da pericia (prazo: 15 dias da intimacao da nomeacao do perito).

Estrutura:

1. **Quesitos de identificacao** (sempre)
   - Qualificacao da pericia + objeto delimitado
2. **Quesitos de premissa** (verificar dados-base)
   - Documentos consultados, periodo, taxa, indice
3. **Quesitos de metodo** (forcar transparencia)
   - Formula aplicada, software utilizado, conferencia
4. **Quesitos de calculo** (questoes especificas do caso)
   - Numero e detalhe das verbas/operacoes
5. **Quesitos de resultado** (cruzar com tese)
   - Confirma/refuta a tese do polo cliente

### Modo 2 — Quesitos complementares (CPC 477 §2º)

Apos leitura do laudo. Foca nos pontos:
- Que o perito respondeu de forma evasiva
- Que o perito nao respondeu
- Que faltam dados/anexos
- Que ha contradicao entre planilha e laudo
- Que faltam fundamentar normativamente

### Modo 3 — Contraditorio aos quesitos do adversario

Recebe os quesitos da parte adversa e gera:
- Impugnacao a quesitos genericos / capciosos
- Reformulacao em forma neutra (sem direcionamento de
  resposta)
- Quesitos antagonicos que neutralizam direcionamento

## 4. OUTPUT

```markdown
## 📋 Quesitos Tecnicos — Pericia Contabil

**Processo:** {{numero}}
**Tipo de acao:** [civel/trabalhista/tributaria/...]
**Subtipo:** [revisao bancaria SAC/Price]
**Polo cliente:** [{{POLO}}]
**Modo:** [iniciais / complementares / contraditorio]

### Quesitos a formular

#### A) Quesitos de identificacao

1. Queira o(a) Sr.(a) Perito(a) identificar a integralidade
   dos contratos bancarios objeto da pericia (numero,
   modalidade, data, valor, prazo).

2. Indicar todos os documentos consultados (contratos,
   extratos, planilhas, taxas oficiais BCB, etc.) com
   respectivas datas e fontes.

#### B) Quesitos de premissa

3. Para cada operacao analisada, especificar:
   (a) modalidade do credito (CDC, financiamento de
       veiculo, leasing, etc.)
   (b) taxa efetiva mensal pactuada (CET)
   (c) sistema de amortizacao (SAC, Price, hibrido)
   (d) data de inicio e termino contratual
   (e) ocorrencia de aditivos / refinanciamentos

#### C) Quesitos de metodo

4. Esclarecer se foi adotado o sistema **Price** ou **SAC**
   no recalculo. Em caso de Price, indicar especificamente
   se ha capitalizacao mensal de juros e em qual ponto.

5. Indicar se a Sum. 539 STJ (capitalizacao so se pactuada
   expressamente) foi observada no recalculo.

6. Especificar o software ou planilha utilizado, anexando
   ao laudo (CPC 473 §3º).

#### D) Quesitos de calculo

7. Apurar:
   (a) saldo devedor inicial
   (b) saldo devedor segundo o contrato original
   (c) saldo devedor expurgado de anatocismo (caso
       indevida a capitalizacao)
   (d) diferenca a maior cobrada pela instituicao
       financeira no periodo
   (e) saldo devedor atualizado pela Selic ate
       {{data_referencia}}

8. Apresentar planilha mes a mes com (i) parcela paga,
   (ii) juros do mes, (iii) amortizacao do mes, (iv)
   saldo devedor remanescente — pelo contrato original
   E pelo recalculo expurgado.

#### E) Quesitos de resultado / tese

9. Caso constatada capitalizacao indevida, qual o valor
   total cobrado a maior do consumidor no periodo de
   {{data_inicio}} a {{data_fim}}?

10. Esse valor cobrado a maior corresponde a quantos
    pontos percentuais do CET pactuado?

11. Caracteriza-se enriquecimento sem causa da instituicao
    financeira nos termos do CC art. 884?

### ⚠️ Limites cruciais ao perito

- NAO substituir o juizo (so calcula, nao decide)
- NAO presumir documento ausente — declarar falta
- NAO usar indice sem fundamentar
- NAO omitir contradicao

### Modelo de peticao protocolando os quesitos

```
EXCELENTISSIMO SENHOR DOUTOR JUIZ ...

Processo: {{numero}}

[POLO], ja qualificado(a) nos autos, vem, dentro do prazo
de 15 (quinze) dias do art. 465 § 1º do CPC,
**APRESENTAR QUESITOS** ao perito contabil nomeado, alem
de **INDICAR ASSISTENTE TECNICO** [Nome — CRC __],
conforme abaixo:

[lista numerada dos quesitos acima]

Nestes termos, pede deferimento.

[Local], [Data].

{{ADVOGADO_NOME}} — OAB/{{ADVOGADO_UF}} {{ADVOGADO_OAB}}
```

> ⚠️ **Validar com a sentenca/decisao do processo antes de
> protocolar.** Esta lista e cardapio tecnico — adaptar ao
> caso concreto.
```

## 5. CATALOGOS POR AREA (referencia interna)

### Civel — Revisao bancaria (Price/SAC, anatocismo)

Foco: Sum. 539 STJ, Sum. 541 STJ (capitalizacao mensal
desde 31/03/2000 com previsao expressa), Sum. 530 STJ
(comissao de permanencia), Tema 246 STJ.

### Civel — Dano material + lucros cessantes

Foco: media historica + projecao futura + correcao desde
cada periodo nao auferido (CC 402 + Sum. 561 STJ).

### Civel — Condominial / locaticio

Foco: convencao + lei + reajuste + multa + juros legais.

### Trabalhista — Horas extras + reflexos

Foco: divisor jornada (220/200/180), DSR (Sum. 376 TST),
13º + ferias + aviso + FGTS, OJ 394 SDI-1 (vedacao dobra
DSR), Reforma 13.467/17 marcos.

### Trabalhista — Salario in natura / utilidades

Foco: art. 458 CLT, Sum. 367 TST (habitacao/alimentacao
nao integram se PAT/PCA), Sum. 247 TST (transporte).

### Trabalhista — Insalubridade / periculosidade

Foco: NR 15 + NR 16, base salarial (Sum. 228 STJ vs SV 4 STF).
Perito = engenheiro (nao contador); reflexo e contabil.

### Tributaria — Exclusao ICMS na base PIS/COFINS

Foco: RE 574.706/PR (Tema 69 STF), modulacao 15/03/2017,
nao incidencia tambem na propria base ICMS (RE 712.367
Tema 1.171 STF — pendente cunhamento definitivo).

### Tributaria — Compensacao / restituicao

Foco: Sum. 461 STJ, Sum. 162 STJ (correcao desde
recolhimento), Sum. 188 STJ (juros do transito).

### Familia — Partilha / inventario

Foco: avaliacao mercado na data da partilha, tornas, regime
de bens, sobrepartilha.

### Revisional — geral

Foco: contrato + taxa pactuada vs efetiva, CDC 51 IV, CET
(Res. BCB 3.517/2007).

## 6. FUNDAMENTACAO LEGAL

- **CPC 465 § 1º** — quesitos iniciais (15 dias)
- **CPC 477 § 2º** — quesitos complementares (15 dias)
- **CPC 473** — requisitos do laudo
- **CPC 466** — compromisso do perito
- **CPC 156 § 2º** — habilitacao do perito
- **NBC PP 01 / NBC TP 01 (CFC)** — pericia contabil
- **Resolucao CFC 1.243/2009** — procedimentos
- **Sumulas por area** — vide secao 5

## 7. AVISOS OBRIGATORIOS NO OUTPUT

1. ⚠️ Validar com a sentenca/decisao especifica antes de
   protocolar
2. ⚠️ Lista e cardapio tecnico — adaptar ao caso
3. ⚠️ Quesitos demais cansam o perito e diluem foco;
   priorizar os 10-15 mais cirurgicos
4. ⚠️ Prazo CPC 465 § 1º — 15 dias da intimacao da
   nomeacao do perito
5. ⚠️ Prazo CPC 477 § 2º — 15 dias do laudo (esclarecimentos
   e quesitos complementares)
6. ⚠️ Para pericia de engenharia (insalubridade,
   periculosidade), o perito e engenheiro de seguranca do
   trabalho — usar quesitos de NR 15/NR 16; calculo do
   reflexo, depois, e contabil

## 8. INTEGRACAO

- **Upstream:** `calculos-master`, `auditor-laudo-pericial-contabil`
  (modo complementares), `/auditar-laudo-pericial quesitos`
- **Downstream auto:** `protocolo-p4-calculos`,
  `gestao-prazo-impugnacao` (CPC 465/477)
- **Cross-link:** `civel-adv-os` / `trabalhista-adv-os` /
  `tributario-societario-adv-os` (peca), `juris-adv-os`,
  `ia-combativa-adv-os` (R1-R4)

## 9. PROIBICOES

1. **Nunca** gerar quesito capcioso (direcionar resposta) —
   pode ser indeferido pelo juiz
2. **Nunca** gerar quesito que substitua o juizo (ex:
   "o reu deve pagar?" — perito nao decide)
3. **Nunca** quesito puramente juridico (ex: "ha
   responsabilidade civil?") — perito e tecnico
4. **Nunca** quesito generico ("quanto deve o reu?") —
   sempre especifico ao calculo
5. **Nunca** mais de ~25 quesitos sem justificar (perito
   pede protelacao)
6. **Nunca** afirmar fato sem fundamentar (perito ignora)
7. **Nunca** apresentar lista sem aviso de adaptacao

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Auditar laudo apos pericia | `/auditar-laudo-pericial` | `calculosjudiciais-adv-os` (este) |
| Gerar contra-laudo se laudo divergir | `/auditar-laudo-pericial contra-laudo` | `calculosjudiciais-adv-os` (este) |
| Gerar peca formal apresentando quesitos | `/civel quesitos-pericia` ou `/trabalhista quesitos-pericia` | `civel-adv-os` ou `trabalhista-adv-os` |
| Validar Sumulas citadas | `/juris validar` | `juris-adv-os` |
| Auditoria Suprema R1-R4 | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` |

> Se plugin nao instalado, copiar lista de quesitos acima e
> usar manualmente.
