---
name: calculos-master
description: >
  CALCULOS-MASTER — Orquestrador central do plugin calculosjudiciais-adv-os.
  Le o input do advogado (texto livre ou /calculos + argumentos),
  classifica a area e o subtipo de calculo, e ativa as skills corretas
  em sequencia. Mantem o contexto da sessao consistente (yaml calculo{}).
  Roteia por palavras-chave + estado do caso. Use SEMPRE como ponto de
  entrada do plugin OU quando o usuario disser "preciso calcular",
  "atualizar valor", "auditar calculo", "comparar calculos", "quanto
  vale", "como liquido", "como calculo", "PJE-CALC errado", "laudo
  pericial certo".
---

# CALCULOS-MASTER — Orquestrador do Plugin

## 1. PAPEL

Esta skill e o **maestro** do plugin calculosjudiciais-adv-os. Recebe
input do advogado e:

1. Classifica a **area do calculo** (civel/trabalhista/tributario/
   previdenciario/familia/criminal/consumidor)
2. Classifica o **subtipo** (cumprimento sentenca / RPV / liquidacao /
   verbas rescisorias / Selic federal / RMI / alimentos / etc.)
3. Ativa a skill correta para esse subtipo
4. Garante que pre-requisitos rodaram (`calculos-onboarding`,
   `identificar-tj-aplicavel`)
5. Mantem o contexto da sessao (yaml `calculo:`) coerente
6. Auto-dispara `protocolo-p4-calculos` apos conta final

## 2. ROTEAMENTO POR PALAVRA-CHAVE

| Input do usuario | Skill ativada |
|------------------|---------------|
| "configurar", "primeira vez", "/start-calculos", "OAB" | `calculos-onboarding` |
| "qual TJ", "qual tabela", "comarca", "competencia foro" | `identificar-tj-aplicavel` |
| "que tipo de calculo", "qual skill", "nao sei classificar" | `classificar-tipo-calculo` |
| "cumprimento sentenca", "fase de cumprimento", "executar sentenca civel" | `calculo-cumprimento-sentenca-civel` |
| "RPV", "precatorio", "Tema 810", "IPCA-E" | `calculo-rpv-precatorio` |
| "dano material", "dano moral", "lucros cessantes", "Sum 362" | `calculo-danos-indenizatorios` |
| "condominio", "taxa condominial", "CC 1336" | `calculo-debito-condominial` |
| "aluguel", "locacao", "Lei 8245" | `calculo-debito-locaticio` |
| "custas", "sucumbencia", "honorarios", "CPC 85" | `calculo-custas-honorarios` |
| "anatocismo", "revisao bancaria", "Price vs SAC", "Sum 539" | `calculo-revisao-bancaria` |
| "liquidacao trabalhista", "CLT 879", "ADC 58", "Lei 14.905" | `calculo-liquidacao-trabalhista` |
| "rescisao", "aviso previo", "13o proporcional", "FGTS 40", "Lei 12.506" | `calculo-verbas-rescisorias` |
| "hora extra", "DSR", "Sum 376", "OJ 394", "divisor 220" | `calculo-horas-extras-reflexos` |
| "insalubridade", "periculosidade", "noturno", "NR 15", "NR 16" | `calculo-adicionais-trabalhistas` |
| "deposito recursal", "RO RR ED AIRR", "Ato SEGJUD" | `calculo-deposito-recursal` |
| "IRPF atrasado", "IRPJ", "CSLL", "PIS", "COFINS", "Sicalc" | `calculo-tributo-federal-selic` |
| "REFIS", "PERT", "parcelamento tributario" | `calculo-refis-parcelamento` |
| "repeticao indebito", "restituicao tributo", "Sum 162 STJ" | `calculo-repeticao-indebito` |
| "RMI", "salario beneficio", "INSS calculo", "EC 103" | `calculo-rmi-beneficio` |
| "atrasados INSS", "revisao beneficio", "Tema 905 STJ" | `calculo-atrasados-inss` |
| "aposentadoria especial", "conversao tempo", "fator 1.40" | `calculo-aposentadoria-especial` |
| "alimentos atrasados", "Sum 309", "Tema 1137", "CNH passaporte" | `calculo-alimentos-atrasados` |
| "partilha", "meacao", "tornas", "CC 1658" | `calculo-partilha-bens` |
| "pena multa", "dia-multa", "CP 49" | `calculo-pena-multa` |
| "restituicao dobro", "CDC 42", "Tema 929 STJ" | `calculo-restituicao-dobro-cdc` |
| "PJE-CALC errado", "auditar PJE-CALC", "PDF calculo" | `parser-auditor-pjecalc` |
| "comparar calculos", "autor vs reu", "perito vs assistente" | `comparador-calculos` |
| "atualizar valor", "atualizar de X a Y", "SELIC entre" | `atualizador-indices-cache` |
| "laudo pericial", "auditar laudo", "NBC PP 01" | `auditor-laudo-pericial-contabil` |
| "quesitos perito", "quesitos contabil" | `gerador-quesitos-perito-contabil` |
| "contra-laudo", "impugnar laudo perito" | `contra-laudo-pericial` |
| "audita", "P4", "auditoria", "R1 R2 R3 R4" | `protocolo-p4-calculos` |
| "prazo impugnar", "15 dias", "CPC 525", "CLT 879 8 dias" | `gestao-prazo-impugnacao` |

## 3. ESTADO DO CASO (yaml mental)

```yaml
calculo:
  area: [civel | trabalhista | tributario | previdenciario | familia | criminal | consumidor]
  subtipo: [cumprimento_sentenca | RPV | liquidacao | verbas_rescisorias | ...]
  natureza_relacao: [consumo | civil | empresarial | trabalhista | tributaria | previdenciaria]
  marco_intertemporal:
    pre_lei_14905_2024: [true | false]
    pre_adc_58_59: [true | false]
    pre_ec_103: [true | false]
  competencia:
    tj: [TJSP | TJRJ | ... | TST | TRTn | TRFn | STJ | STF]
    juizo: [vara_civel | JEC | JEF | vara_federal | vara_trabalho | vara_fazenda]
    tabela_correcao_url: "<url oficial do TJ>"
  indices_aplicaveis:
    correcao: [IPCA | IPCA-E | INPC | TR | tabela_TJ | Selic]
    juros: [1pc_am | taxa_legal_CC406 | poupanca | Selic | art_406_CC_pre_2024]
  valor_atualizado:
    valor: R$ ...
    data_atualizacao: YYYY-MM-DD
  fonte_calculo:
    tipo: [original | PJE-CALC | laudo_pericial | contadoria_judicial | parte_adversa]
    documento_anexo: "<path>"
  calculos_gerados:
    - tipo: ...
      data: ...
      total: R$ ...
      selo_p4: APROVADO | REVISAR | BLOQUEADO
  prazo_impugnacao:
    data_intimacao: YYYY-MM-DD
    prazo_dias: [15 uteis | 8 corridos]
    data_limite: YYYY-MM-DD
    status: vivo | em_risco | perdido
```

## 4. WORKFLOW DE ATIVACAO

### Cenario A: Calculo novo (gerar do zero)

```
1. calculos-onboarding (se persona.md NAO existe em <cwd>/calculos/)
2. classificar-tipo-calculo (classifica area + subtipo)
3. identificar-tj-aplicavel (se area=civel/trab e UF+comarca+valor disponiveis)
4. Skill especifica do subtipo (Tier 2)
   ↓ (gera memoria de calculo)
5. atualizador-indices-cache (se a skill T2 nao consultou diretamente)
6. protocolo-p4-calculos (auto-disparo apos conta final)
7. Output: memoria + selo P4 + sugestoes plugins-irmaos
```

### Cenario B: Auditar calculo de terceiro (DIFERENCIAL ⭐)

```
1. Identificar fonte (PJE-CALC PDF / laudo pericial / contadoria / parte adversa)
2. Se PJE-CALC PDF → parser-auditor-pjecalc
   Se laudo pericial → auditor-laudo-pericial-contabil
   Se contadoria/adversa em texto → entrada manual + classificar-tipo-calculo
3. Comparar com parametros da sentenca (advogado fornece)
4. Se ha 2+ calculos do mesmo caso → comparador-calculos
5. Output: relatorio de auditoria + divergencias quantificadas + selo P4
```

### Cenario C: Atualizar valor unico (atalho)

```
1. atualizador-indices-cache (recebe valor + data_inicial + data_final + indice)
2. Output: valor final + memoria + range valido + aviso anti-halucinacao
```

### Cenario D: Verificar prazo de impugnacao

```
1. gestao-prazo-impugnacao (recebe data_intimacao + tipo de calculo)
2. Output: data_limite + status (vivo/em_risco/perdido) + alerta visual
```

## 5. BLOQUEIOS UPSTREAM

| Skill | Bloqueada se NAO rodou |
|-------|------------------------|
| Qualquer Tier 2 | `calculos-onboarding` (precisa de persona configurada) |
| `calculo-cumprimento-sentenca-civel` | `identificar-tj-aplicavel` (tabela correta) |
| `calculo-liquidacao-trabalhista` | flag `marco_intertemporal.pre_lei_14905_2024` definida |
| Qualquer conta final | `protocolo-p4-calculos` auto-disparado depois |
| `comparador-calculos` | 2+ memorias de calculo disponiveis |

Se faltar pre-requisito, **PARE** e ative a skill que falta antes.

## 6. FORMATO DE INTERACAO

```markdown
## Diagnostico inicial — calculos-master

**Input recebido:** "[copiar trecho relevante]"

**Area classificada:** [civel | trabalhista | tributario | ...]
**Subtipo:** [cumprimento_sentenca | liquidacao | RPV | ...]

**Skills que serao acionadas em sequencia:**
1. [skill X] — [razao]
2. [skill Y] — [razao]
3. ...

**Estado atual do calculo:**

```yaml
[yaml inicial preenchido com o que ja se sabe]
```

Vamos comecar pela primeira skill...
```

## 7. PRINCIPIOS DA ORQUESTRACAO

1. **Nunca pule classificacao.** Mesmo se o advogado diz "ja sei
   que e liquidacao trabalhista", rode `classificar-tipo-calculo`
   pra confirmar e propagar contexto correto.
2. **Sempre identifique TJ aplicavel** antes de gerar conta civel/
   trabalhista (impacta indice de correcao).
3. **Sempre P4 antes do output final** — nenhuma conta sai sem
   selo de auditoria.
4. **Sinalize marco intertemporal critico** com ⚠️:
   - Lei 14.905/2024 (vigencia 30/08/2024) — Taxa Legal CC 406
   - ADC 58/59 STF (junho/2020) — IPCA-E + Selic em trabalhista
   - EC 103/2019 (reforma previdenciaria) — RMI
5. **Em duvida sobre rotear**, pergunte UMA VEZ ao usuario.
6. **Nunca "lembre" indice** — sempre consulte
   `scripts/data/indices/*.json` via `atualizador-indices-cache`.

## 8. PROIBICOES

1. Nao gerar conta sem rodar Tier 0 + Tier 1 no minimo.
2. Nao confundir polo ativo vs passivo na hora de escolher skill
   (autor calcula pra cobrar; reu calcula pra impugnar — mesmas
   skills, framing diferente no output).
3. Nao bipassar `protocolo-p4-calculos`.
4. Nao perder o yaml `calculo:` entre skills da mesma sessao.
5. Nao importar/ler arquivos de outros plugins.
6. Nao chamar API externa em runtime (BCB, IBGE, CJF).

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Peticionar cumprimento de sentenca | `/execucao cumprimento-sentenca` | `execucao-adv-os` (Kirvano) |
| Impugnar calculo do exequente | `/execucao embargos-execucao` | `execucao-adv-os` |
| Liquidar sentenca trabalhista (peca) | `/trabalhista liquidacao-execucao-trabalhista` | `trabalhista-adv-os` |
| Auditoria suprema R1-R4 da peca + conta | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` |
| Validar jurisprudencia citada | `/juris buscar` | `juris-adv-os` (order bump) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar
> manualmente.
