---
name: calculo-deposito-recursal
description: >
  CALCULO-DEPOSITO-RECURSAL — Calcula o valor do deposito recursal
  trabalhista (RO + RR + ED + AIRR + recursos extraordinarios)
  consultando a tabela TST anual (Ato SEGJUD.GP do TST), publicada
  em scripts/data/indices/deposito-recursal-tst.json. NUNCA "lembra"
  o valor — sempre consulta a tabela. Aplica regras da Sumula 245
  TST + IN 03 TST sobre o limite ate a condenacao (valor menor) e
  sobre dispensa para entidades isentas (sindicato, MEI no JEC
  trab., MP/Defensoria/Fazenda Publica). Use quando o operador
  disser "deposito recursal", "valor do RO", "valor do RR",
  "deposito do recurso ordinario", "tabela TST anual", "isencao de
  deposito recursal", "Ato SEGJUD".
---

# CALCULO-DEPOSITO-RECURSAL — Deposito Recursal Trabalhista

## 1. ESCOPO

Skill Tier 2 do plugin `calculosjudiciais-adv-os`. Calcula o
**valor do deposito recursal** trabalhista — exigencia legal para
admissibilidade dos recursos trabalhistas da parte **vencida**
(condenada em valor pecuniario). Reflexo do art. 899 §1o CLT.

**Acionada quando o operador menciona:** deposito recursal, valor
do RO, valor do RR, deposito do recurso ordinario, recurso de
revista, embargos de declaracao trabalhista, agravo de instrumento
trabalhista, tabela TST, Ato SEGJUD.GP, isencao deposito recursal,
Sumula 245 TST, IN 03 TST.

## 2. SIDE-AWARENESS

| Polo | Postura |
|------|---------|
| **Reclamante** | Geralmente isento (beneficiario da justica gratuita). Quando vencido em pedido contraposto/RVT, sujeita-se ao deposito como qualquer parte. |
| **Reclamada (regra)** | Parte tipicamente sujeita ao deposito recursal — recurso da empregadora condenada exige garantia. **Estrategia**: conferir se a tabela vigente foi aplicada corretamente pelo juizo a quo; verificar se houve dobramento indevido entre as instancias. |

## 3. INPUT NECESSARIO

- **Recurso pretendido** (RO / RR / ED / AIRR / RE em RR / agravo
  de peticao etc.)
- **Data da interposicao do recurso** (define a tabela TST vigente
  no semestre)
- **Valor da condenacao** (deposito limitado pelo total da
  condenacao quando este for inferior — Sum. 245 TST)
- **Ja houve deposito em instancia anterior?** (se sim, valor
  acumulado conta para o limite)
- **Parte goza de isencao?** (justica gratuita / sindicato /
  MP / Fazenda Publica / massa falida / MEI ou ME no JEC trab. —
  Sum. 86 TST)
- **Reclamada e pessoa juridica de direito publico?** (Decreto-Lei
  779/69 — prerrogativas)

## 4. CONSULTA OBRIGATORIA A TABELA TST

**REGRA DURA**: NUNCA inventar valor de deposito recursal. Sempre
consultar:

```
scripts/data/indices/deposito-recursal-tst.json
```

Schema esperado:
```json
{
  "indice": "DEPOSITO_RECURSAL_TST",
  "fonte": "Ato SEGJUD.GP do TST (anual/semestral)",
  "url_oficial": "https://www.tst.jus.br/depositorecursal",
  "data_extracao": "AAAA-MM-DD",
  "release_plugin": "v0.1.0",
  "vigencias": {
    "2024-08-01": {
      "RO":     12665.85,
      "RR":     25331.71,
      "ED":      8443.91,
      "AIRR":   25331.71,
      "RE_em_RR": 38000.00,
      "fonte_ato": "Ato SEGJUD.GP n. XYZ/2024"
    },
    "2025-08-01": {
      "RO":     ...,
      "RR":     ...
    }
  },
  "aviso": "Valores atualizados semestralmente pelo TST. Apos data_extracao consultar url_oficial."
}
```

**Quando a data da interposicao do recurso esta DENTRO do range da
tabela** -> retornar valor direto.
**Quando esta FORA do range** -> retornar formula + URL oficial +
placeholder + aviso: *"valor nao cacheado neste release; consultar
[URL]"*.

## 5. RECURSOS QUE EXIGEM DEPOSITO

| Recurso | Codigo | Deposito? | Observacao |
|---------|--------|:---------:|------------|
| Recurso Ordinario (RO) | art. 895 CLT | ✅ | Valor da tabela RO |
| Recurso de Revista (RR) | art. 896 CLT | ✅ | Valor da tabela RR |
| Embargos de Declaracao (ED) | art. 897-A CLT | normalmente ✅ se cumulado com efeito modificativo / valor de ED da tabela quando exigido | `[VERIFICAR]` — depende da posicao do TRT/TST |
| Agravo de Instrumento (AI/AIRR) | art. 897 §5o CLT | ✅ | 50% do deposito do recurso ao qual visa destrancar (RO/RR) — Sum. 128 TST item III |
| Embargos a Execucao | art. 884 CLT | nao — exige **garantia integral do juizo** (deposito, penhora, fianca) | nao confundir com deposito recursal |
| Agravo de Peticao | art. 897 CLT | nao — depende de garantia do juizo previa | recurso da fase de execucao |
| Recurso Extraordinario (RE) em RR | art. 102 III CF | ✅ | Valor da tabela RE em RR (quando previsto) |

## 6. REGRAS CRITICAS

### Sumula 128 TST
- **Item I**: deposito devido **a cada recurso** — limitado, em
  cada um, ao **valor da condenacao** quando este for inferior ao
  valor da tabela.
- **Item II**: garantida a condenacao com depositos sucessivos
  ate o limite total, dispensam-se os depositos seguintes da mesma
  parte.
- **Item III**: deposito do **agravo de instrumento** = **50%** do
  valor do deposito do recurso que se quer destrancar.

### Sumula 245 TST
- Deposito recursal **NAO se confunde** com taxa judiciaria (custas
  processuais). E **garantia da execucao**, nao tributo.

### IN 03 TST (Instrucao Normativa)
- Regulamenta detalhes do deposito recursal.
- Atualizacao semestral por **Ato SEGJUD.GP do TST**.
- Reajuste segue indice oficial (historicamente TR).

### Isencoes
- **Empregado beneficiario da justica gratuita** (CLT art. 899 §10,
  com nuances pos-Reforma — `[VERIFICAR]` jurisprudencia)
- **Massa falida** (Sum. 86 TST)
- **Empresa em recuperacao judicial** — `[VERIFICAR]` posicionamento
- **Sindicato substituto processual** em acao coletiva
- **MEI e ME** (Reforma — CLT art. 899 §9o) — recolhimento
  **reduzido a 50%**
- **Beneficiarios da justica gratuita pessoa juridica** — Sum. 463
  TST item II + CPC 98 (depende de prova de insuficiencia)
- **Fazenda Publica, MP, Defensoria** — Decreto-Lei 779/69 +
  CPC 91 (dispensa de adiantamento)
- **Empregador domestico** — `[VERIFICAR]` posicionamento

## 7. PROCESSAMENTO — PASSO A PASSO

1. **Identificar o recurso** -> mapear na tabela do item 5
2. **Identificar a data da interposicao** -> definir vigencia
   aplicavel
3. **Consultar `scripts/data/indices/deposito-recursal-tst.json`**
   -> extrair valor exato do recurso
4. **Confrontar com o valor da condenacao** -> aplicar Sum. 128 I
   (limite menor prevalece)
5. **Verificar depositos ja feitos** -> aplicar Sum. 128 II
   (depositos sucessivos somam ate atingir condenacao)
6. **Aplicar isencoes** -> conferir item 6
7. **Para AI/AIRR**: aplicar 50% (Sum. 128 III)
8. **Output com aviso**: "valor extraido da tabela TST vigente em
   [data]; conferir Ato SEGJUD.GP n. [...] na URL oficial"

## 8. OUTPUT — MODELO

```markdown
# Deposito Recursal — [Reclamante x Reclamada]
**Recurso:** [RO / RR / AIRR / ED / RE em RR]
**Data da interposicao prevista:** [DD/MM/AAAA]
**Valor da condenacao:** R$ [valor]
**Depositos ja efetuados:** R$ [valor]

## Consulta a tabela TST

- Tabela vigente: **Ato SEGJUD.GP n. [...]/[AAAA]** (data inicial
  [DD/MM/AAAA])
- Fonte cacheada:
  `scripts/data/indices/deposito-recursal-tst.json` (data_extracao
  [AAAA-MM-DD])
- Valor tabelar do recurso: **R$ [valor]**

## Aplicacao das regras

| Regra | Aplicacao |
|-------|-----------|
| Sum. 128 I (limite condenacao) | [aplicada/nao] |
| Sum. 128 II (depositos sucessivos) | [aplicada/nao] |
| Sum. 128 III (50% para AI) | [aplicada/nao] |
| Isencoes | [nenhuma / ME 50% / etc.] |

## **VALOR DEVIDO: R$ [valor]**

## Comprovacao
- Guia GRU (codigo 18.806-9 — depositos judiciais trabalhistas) ou
  conta vinculada FGTS, conforme o caso.

## Avisos legais

> Valor extraido de tabela cacheada (data_extracao [...]). **Para
> recursos com interposicao apos [range_final da tabela], consultar
> obrigatoriamente:**
> https://www.tst.jus.br/depositorecursal
>
> Ato SEGJUD.GP do TST e publicado **semestralmente** (1o de agosto
> e 1o de fevereiro, em geral). Conferir vigencia do Ato no momento
> da interposicao.
```

## 9. FUNDAMENTACAO LEGAL

- **CLT art. 899** — deposito recursal (caput + §§)
- **CLT art. 899 §1o** — exigencia de garantia
- **CLT art. 899 §9o** — ME/EPP/MEI 50% (Reforma 13.467/2017)
- **CLT art. 899 §10** — justica gratuita pessoa fisica
- **CLT art. 895** — Recurso Ordinario
- **CLT art. 896** — Recurso de Revista
- **CLT art. 897** — Agravo de Peticao + Agravo de Instrumento
- **CLT art. 897-A** — Embargos de Declaracao
- **CLT art. 884** — embargos a execucao (garantia integral, nao
  deposito recursal)
- **Decreto-Lei 779/69** — prerrogativas Fazenda Publica
- **CPC 98** — gratuidade da justica
- **Sumula 86 TST** — massa falida isenta
- **Sumula 128 TST** — deposito por recurso, limite, AI 50%
- **Sumula 245 TST** — deposito nao se confunde com custas
- **Sumula 463 TST** — gratuidade pessoa juridica
- **IN 03 TST** — regulamenta o deposito recursal
- **Ato SEGJUD.GP do TST** — atualizacao semestral dos valores

## 10. PROIBICOES

1. **NUNCA** "lembrar" valor do deposito recursal — SEMPRE
   consultar `scripts/data/indices/deposito-recursal-tst.json`
2. **NUNCA** gerar valor final fora do `range_final` da tabela —
   apresentar formula + URL oficial + placeholder
3. **NUNCA** confundir deposito recursal com custas processuais
   (Sum. 245 TST)
4. **NUNCA** confundir deposito recursal com garantia do juizo
   (embargos a execucao / agravo de peticao)
5. **NUNCA** dobrar deposito em recursos sucessivos sem aplicar
   Sum. 128 II
6. **NUNCA** esquecer da regra dos 50% para Agravo de Instrumento
   (Sum. 128 III)
7. **NUNCA** omitir aviso de validacao contra Ato SEGJUD.GP
   vigente

## 11. INTEGRACAO

- **Acionada por:** `calculos-master`, `calculo-liquidacao-trabalhista`,
  `/calculo-trabalhista`
- **Apoio obrigatorio:** `atualizador-indices-cache` (le a tabela
  `deposito-recursal-tst.json`)
- **Encadeia:** `protocolo-p4-calculos`

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---------------|---------|-------------------|
| Calcular o valor da condenacao atualizado (base do deposito) | `/calculos calculo-liquidacao-trabalhista` | (este plugin) |
| Recurso ordinario trabalhista | `/trabalhista recurso-ordinario` | `trabalhista-adv-os` (Kirvano) |
| Recurso de revista | `/trabalhista recurso-revista` | `trabalhista-adv-os` (Kirvano) |
| Auditar PJE-CALC do escritorio contrario | `/calculos auditar-pjecalc` | (este plugin) |
| Suprema Corte R1-R4 do recurso | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar
> manualmente.
