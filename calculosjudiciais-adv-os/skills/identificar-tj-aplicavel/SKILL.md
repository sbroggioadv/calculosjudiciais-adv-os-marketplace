---
name: identificar-tj-aplicavel
description: >
  IDENTIFICAR-TJ-APLICAVEL — Recebe UF + comarca + valor da causa
  (e opcionalmente parte demandada: pessoa fisica, juridica, ente
  publico federal/estadual/municipal, INSS, Uniao). Devolve: TJ
  aplicavel (1 dos 27 estaduais + DF) ou Justica Federal (TRF1-6) ou
  Justica do Trabalho (TRT1-24) + URL da tabela oficial de correcao
  monetaria + observacao de competencia (JEC ate 40 SM / Vara Comum /
  JEF ate 60 SM / Vara Federal / Vara da Fazenda / JECrim). Use
  quando o orquestrador precisa de tabela de correcao oficial OU
  quando o usuario disser "qual TJ", "qual tabela usar", "competencia
  foro", "onde corre", "JEC ou comum", "JEF ou vara federal".
---

# IDENTIFICAR-TJ-APLICAVEL — Tabela de Correcao Oficial

## 1. ESCOPO

Skill de mapeamento. Recebe localizacao + parte + valor e devolve:
- Tribunal aplicavel (TJ-UF / TRF / TRT)
- URL oficial da tabela de correcao monetaria daquele tribunal
- Competencia funcional (JEC / Vara Comum / JEF / Vara Federal /
  Vara Fazenda / JECrim) baseada em valor

**Critica para anti-halucinacao:** sem URL oficial da tabela do TJ
correto, a skill Tier 2 nao pode aplicar indice de correcao.

## 2. INPUT NECESSARIO

Minimo:
- **UF** (sigla)
- **Comarca/cidade**

Opcional (refina classificacao):
- **Valor da causa** (define JEC vs Comum, JEF vs Federal)
- **Parte demandada** (PF, PJ, Uniao, Estado, Municipio, INSS,
  autarquia, fundacao publica)
- **Natureza** (civel / trabalhista / penal / tributario federal /
  previdenciario)

## 3. TABELAS — 27 JUSTICAS ESTADUAIS + DF

### Sul

| UF | Tribunal | URL tabela correcao |
|---|---|---|
| RS | TJRS | https://www.tjrs.jus.br/ — buscar "Indices de Correcao Monetaria" |
| SC | TJSC | https://www.tjsc.jus.br/ — Servicos → Calculo Judicial |
| PR | TJPR | https://www.tjpr.jus.br/ — Servicos → Indices economicos |

### Sudeste

| UF | Tribunal | URL tabela correcao |
|---|---|---|
| SP | TJSP | https://www.tjsp.jus.br/IndicesConversaoDebitosJudiciais |
| RJ | TJRJ | https://www.tjrj.jus.br/ — Servicos → Conversao Monetaria |
| MG | TJMG | https://www.tjmg.jus.br/ — Servicos → Calculo Judicial |
| ES | TJES | https://www.tjes.jus.br/ — Servicos → Calculo Judicial |

### Centro-Oeste

| UF | Tribunal | URL tabela correcao |
|---|---|---|
| DF | TJDFT | https://www.tjdft.jus.br/ — Cidadao → Calculo Judicial |
| GO | TJGO | https://www.tjgo.jus.br/ — Servicos → Calculadora Judicial |
| MT | TJMT | https://www.tjmt.jus.br/ — Servicos → Calculo Judicial |
| MS | TJMS | https://www.tjms.jus.br/ — Servicos → Calculadora Judicial |

### Nordeste

| UF | Tribunal | URL tabela correcao |
|---|---|---|
| BA | TJBA | https://www.tjba.jus.br/ — Servicos → Calculo Judicial |
| PE | TJPE | https://www.tjpe.jus.br/ — Servicos → Calculo Judicial |
| CE | TJCE | https://www.tjce.jus.br/ — Servicos → Calculo Judicial |
| MA | TJMA | https://www.tjma.jus.br/ — Servicos → Calculadora |
| PB | TJPB | https://www.tjpb.jus.br/ — Servicos → Calculo Judicial |
| RN | TJRN | https://www.tjrn.jus.br/ — Servicos → Calculo Judicial |
| AL | TJAL | https://www.tjal.jus.br/ — Servicos → Calculadora |
| SE | TJSE | https://www.tjse.jus.br/ — Servicos → Calculadora |
| PI | TJPI | https://www.tjpi.jus.br/ — Servicos → Calculo Judicial |

### Norte

| UF | Tribunal | URL tabela correcao |
|---|---|---|
| PA | TJPA | https://www.tjpa.jus.br/ — Servicos → Calculadora |
| AM | TJAM | https://www.tjam.jus.br/ — Servicos → Calculadora |
| AC | TJAC | https://www.tjac.jus.br/ — Servicos → Calculadora |
| RO | TJRO | https://www.tjro.jus.br/ — Servicos → Calculadora |
| RR | TJRR | https://www.tjrr.jus.br/ — Servicos → Calculadora |
| AP | TJAP | https://www.tjap.jus.br/ — Servicos → Calculadora |
| TO | TJTO | https://www.tjto.jus.br/ — Servicos → Calculadora |

> **Aviso anti-halucinacao:** os caminhos especificos podem mudar.
> Sempre confirmar o URL definitivo navegando ao portal do TJ —
> aviso obrigatorio no output.

## 4. JUSTICA FEDERAL — 6 TRFs

Competencia: Uniao, autarquias federais (INSS, IBAMA, ANATEL),
empresas publicas federais (CEF, Correios), causas previdenciarias,
tributos federais (IR/PIS/COFINS/CSLL).

| TRF | Estados | URL tabela |
|---|---|---|
| TRF1 | DF, AC, AM, AP, BA, GO, MA, MT, MG, PA, PI, RO, RR, TO | https://www.trf1.jus.br/ — Servicos → Calculo Judicial |
| TRF2 | RJ, ES | https://www.trf2.jus.br/ — Servicos → Calculo Judicial |
| TRF3 | SP, MS | https://www.trf3.jus.br/ — Servicos → Calculo Judicial |
| TRF4 | RS, SC, PR | https://www.trf4.jus.br/ — Servicos → Calculo Judicial |
| TRF5 | PE, CE, AL, SE, PB, RN | https://www.trf5.jus.br/ — Servicos → Calculo Judicial |
| TRF6 | MG (desmembrado do TRF1 em 2022) | https://www.trf6.jus.br/ — Servicos → Calculo Judicial |

**Fonte preferida CJF:** Manual de Calculos da Justica Federal —
https://www.cjf.jus.br/cjf/corregedoria-da-justica-federal/centro-de-estudos-judiciarios-1/manual-de-orientacao-de-procedimentos-para-os-calculos-na-justica-federal

## 5. JUSTICA DO TRABALHO — 24 TRTs

| TRT | UF |
|---|---|
| TRT1 | RJ |
| TRT2 | SP capital + grande SP + Santos |
| TRT3 | MG |
| TRT4 | RS |
| TRT5 | BA |
| TRT6 | PE |
| TRT7 | CE |
| TRT8 | PA, AP |
| TRT9 | PR |
| TRT10 | DF, TO |
| TRT11 | AM, RR |
| TRT12 | SC |
| TRT13 | PB |
| TRT14 | RO, AC |
| TRT15 | SP interior (Campinas) |
| TRT16 | MA |
| TRT17 | ES |
| TRT18 | GO |
| TRT19 | AL |
| TRT20 | SE |
| TRT21 | RN |
| TRT22 | PI |
| TRT23 | MT |
| TRT24 | MS |

**Tabela unificada TST:** ADC 58/59 STF + Lei 14.905/2024 — pre
ajuizamento: IPCA-E + juros TR; pos ajuizamento: SELIC. Tabela
unica recomendada: https://www.tst.jus.br/web/corregedoria/calculo

## 6. COMPETENCIA POR VALOR

### Civel Estadual

| Valor | Competencia |
|---|---|
| Ate 20 SM (Lei 9.099/95) | JEC — Juizado Especial Civel (facultativo) |
| 20-40 SM | JEC com obrigatoriedade de advogado (Lei 9.099/95 art. 9o) |
| Acima 40 SM | Vara Civel comum |
| Causas envolvendo Fazenda Publica estadual/municipal | Vara da Fazenda Publica (ou JEC Fazenda ate 60 SM — Lei 12.153/2009) |

### Federal

| Valor | Competencia |
|---|---|
| Ate 60 SM (Lei 10.259/2001) | JEF — Juizado Especial Federal |
| Acima 60 SM | Vara Federal |
| Causas previdenciarias | JEF prioritario ate 60 SM |

### Trabalhista

Sem limite de valor — toda Vara do Trabalho (CLT 651).

### Criminal

JECrim ate pena maxima 2 anos (Lei 9.099/95 art. 61) — infracoes
de menor potencial ofensivo.

## 7. LOGICA DE DECISAO

```
1. Receber UF + comarca + (opcional) valor + parte
2. SE parte = Uniao/INSS/autarquia federal/tributo federal:
     → Justica Federal (mapear UF → TRF)
     → SE valor ≤ 60 SM (previdenciario/causas comuns):
         juizo = JEF
       SENAO:
         juizo = Vara Federal
3. SENAO SE natureza = trabalhista:
     → Justica do Trabalho (mapear UF → TRT)
     → juizo = Vara do Trabalho (sem JEC trabalhista)
4. SENAO SE parte = Fazenda Estadual/Municipal:
     → TJ-UF
     → SE valor ≤ 60 SM:
         juizo = JEC Fazenda
       SENAO:
         juizo = Vara da Fazenda Publica
5. SENAO (civel comum):
     → TJ-UF
     → SE valor ≤ 20 SM:
         juizo = JEC (facultativo dispensa advogado)
       SENAO SE valor ≤ 40 SM:
         juizo = JEC com advogado
       SENAO:
         juizo = Vara Civel
6. Consultar persona.tribunais — se advogado nao atua no TJ
   identificado, ALERTAR (pode precisar correspondente)
```

## 8. OUTPUT (formato estruturado)

```yaml
competencia:
  uf: SP
  comarca: Sao Paulo
  valor_causa: 35000.00
  salario_minimo_referencia: 1518.00
  valor_em_salarios_minimos: 23.05
  parte_demandada: pessoa_juridica
  tribunal: TJSP
  tabela_correcao_oficial:
    url: "https://www.tjsp.jus.br/IndicesConversaoDebitosJudiciais"
    fonte: "Tribunal de Justica de Sao Paulo"
    aviso: "Confirmar URL atual no portal oficial. Plugin nao
            faz fetch em runtime."
  juizo: JEC_com_advogado
  prazo_regime: corridos_em_JEC | uteis_em_vara
  observacoes:
    - "Valor entre 20-40 SM: JEC com obrigatoriedade de advogado (Lei 9.099/95 art. 9o)"
    - "Atencao: Lei 9.099/95 art. 3o II exclui certas causas do JEC"
    - "Persona configurada atua em TJSP — sem necessidade de correspondente"
```

E recomendacao em markdown:

```markdown
## Competencia identificada — identificar-tj-aplicavel

**Tribunal:** TJSP (Tribunal de Justica de Sao Paulo)
**Tabela de correcao oficial:** [link]
**Juizo:** JEC com obrigatoriedade de advogado (35.000 = 23,05 SM)

⚠️ Validar URL no portal oficial antes de protocolar.

**Pre-requisito atendido para skill Tier 2** —
`calculo-cumprimento-sentenca-civel` pode rodar agora.
```

## 9. AVISOS OBRIGATORIOS

- URLs especificas dos portais TJ MUDAM com frequencia — sempre
  confirmar no portal oficial antes de usar a tabela
- Salario minimo de referencia: usar valor VIGENTE na data de
  proposicao da acao (nao do calculo)
- JEC tem prazo CONTINUO (corridos) na Lei 9.099/95 — diferente do
  CPC (uteis)
- Acidente do trabalho proposto pelo trabalhador contra empregador
  e da JUSTICA COMUM (Sum 15 STJ + Sum 366 STJ) — exceto direitos
  trabalhistas em si que vao pra JT
- Causa contra INSS por revisao de beneficio: JEF se ≤ 60 SM

## 10. PROIBICOES

1. Nao indicar TJ sem ter UF confirmada
2. Nao chutar URL — usar formato generico "<portal>/<servicos> →
   Calculo Judicial" se nao tem URL exata cacheada
3. Nao recomendar JEC se causa esta no rol do art. 3o II
   Lei 9.099/95 (cobrancas tributarias, causas de estado,
   capacidade, etc.)
4. Nao misturar TRT com TRF (areas totalmente distintas)
5. Nao esquecer marco TRF6 (criado 2022, desmembrou MG do TRF1)

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Ajuizar acao na competencia identificada | `/execucao peticao-inicial-cobranca` | `execucao-adv-os` |
| Verificar competencia territorial detalhada | `/execucao competencia-territorial` | `execucao-adv-os` |
| Liquidar e protocolar trabalhista | `/trabalhista liquidacao-execucao-trabalhista` | `trabalhista-adv-os` |

> Tabelas de correcao mudam — sempre validar URL no portal oficial
> antes de protocolar conta.
