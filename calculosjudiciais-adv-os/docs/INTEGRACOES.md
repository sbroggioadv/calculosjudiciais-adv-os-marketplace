# INTEGRACOES — calculosjudiciais-adv-os

> Como o plugin `calculosjudiciais-adv-os` se relaciona com os outros plugins
> da familia Adv-OS — e por que essa relacao e **soft** (sugestao, nao acoplamento).

---

## Filosofia: por que sugerir e nao acoplar

O plugin segue o **Pilar 1 — STANDALONE-FIRST** (ver `README.md` e `CLAUDE.md`).
Isso significa que:

- O plugin funciona 100% sozinho. Pode ser comprado isoladamente e usado sem
  depender de mais nada da familia.
- O plugin **nao importa, nao le, nao invoca** skills de outros plugins. Isso
  evita 3 problemas recorrentes:
  1. **Quebra silenciosa** quando um plugin-irmao e desinstalado.
  2. **Colisao de namespace** entre skills de plugins diferentes.
  3. **Vendor lock-in** que prejudica o operador que so quer o calculo.
- Em vez de chamar outros plugins, os outputs das skills incluem **bloco
  fixo** "💡 Proximos passos opcionais" — texto que mostra ao operador qual
  comando rodaria se ele tivesse o plugin-irmao instalado.

Resultado pratico:

- **Tem o plugin-irmao instalado?** Operador copia o comando sugerido e
  executa — fluxo encadeado natural.
- **Nao tem o plugin-irmao?** Operador copia a **memoria de calculo gerada**
  e usa manualmente onde precisar — nada quebra.

---

## Plugins-irmaos e quando sugerir

### `execucao-adv-os` — peticionamento de execucao

**Quando sugerir:** apos qualquer calculo civel que va virar peca de execucao.

- Apos `calculo-cumprimento-sentenca-civel` → sugerir `/execucao cumprimento-sentenca`
- Apos `calculo-rpv-precatorio` → sugerir `/execucao peticao-inicial-execucao`
- Apos `calculo-debito-condominial` ou `calculo-debito-locaticio` (titulos
  extrajudiciais) → sugerir `/execucao peticao-inicial-execucao` ou
  `/execucao peticao-inicial-monitoria`

**Por que faz sentido:** o calculo gerado aqui ja vem pronto pra ser
peticionado. O `execucao-adv-os` cobre todo o ciclo (notificacao → peticao →
defesa → recurso).

---

### `trabalhista-adv-os` — peca trabalhista completa

**Quando sugerir:** apos qualquer calculo trabalhista, especialmente liquidacao.

- Apos `calculo-liquidacao-trabalhista` → sugerir `/trabalhista liquidacao`
- Apos `calculo-verbas-rescisorias` → sugerir `/trabalhista peticao-inicial`
- Apos `calculo-deposito-recursal` → sugerir `/trabalhista recurso`

**Por que faz sentido:** o `trabalhista-adv-os` e side-aware (reclamante x
reclamada) e tem governanca completa (CLT + CPC subsidiario + CCT + Suprema
Corte R1-R4). Calculo + peca = entrega completa.

---

### `previdenciario-adv-os` — peca administrativa/judicial pos calculo RMI

**Quando sugerir:** apos `calculo-rmi-beneficio`, `calculo-atrasados-inss`,
`calculo-aposentadoria-especial`.

- Apos `calculo-rmi-beneficio` → sugerir `/previdenciario revisao-rmi` (ou
  peticao judicial conforme caso)
- Apos `calculo-atrasados-inss` → sugerir `/previdenciario cumprimento` ou
  `/previdenciario acao-cobranca-atrasados`
- Apos `calculo-aposentadoria-especial` → sugerir `/previdenciario tempo-especial`

**Por que faz sentido:** plugin previdenciario cobre RGPS + RPPS + Acidentario
+ Complementar — calculo aqui vira fundamentacao da peca la.

---

### `tributario-societario-adv-os` — defesa fiscal

**Quando sugerir:** apos calculo de tributo federal, repeticao de indebito,
REFIS.

- Apos `calculo-tributo-federal-selic` → sugerir `/tributario auto-infracao`
  ou `/tributario impugnacao-fiscal`
- Apos `calculo-repeticao-indebito` → sugerir `/tributario acao-restituicao`
- Apos `calculo-refis-parcelamento` → sugerir `/tributario adesao-parcelamento`

**Por que faz sentido:** o tributario tem o conhecimento da defesa fiscal
(materia + processo + Tema STJ/STF), o calculosjudiciais entrega o numero.

---

### `direito-familia-adv-os` — peca de familia pos calculo

**Quando sugerir:** apos `calculo-alimentos-atrasados` ou `calculo-partilha-bens`.

- Apos `calculo-alimentos-atrasados` → sugerir `/familia execucao-alimentos`
  (incluindo Sumula 309 STJ — 3 ultimas + vincendas para prisao)
- Apos `calculo-partilha-bens` → sugerir `/familia partilha` ou
  `/familia inventario-judicial`

**Por que faz sentido:** calculo de alimentos atrasados + execucao no rito
da prisao (CPC 528) e operacao de alta especializacao — o plugin familia
cobre os 11 trilhas de operacao.

---

### `ia-combativa-adv-os` — auditoria Suprema Corte R1-R4 final

**Quando sugerir:** ao final de qualquer entrega critica, especialmente apos
um dos 3 transversais (⭐ killer features).

- Apos `parser-auditor-pjecalc` → sugerir `/ia-combativa suprema-corte`
- Apos `auditor-laudo-pericial-contabil` → sugerir `/ia-combativa suprema-corte`
- Apos `comparador-calculos` → sugerir `/ia-combativa suprema-corte`

**Por que faz sentido:** o `protocolo-p4-calculos` (Tier 4 deste plugin) e
uma versao especializada de R1-R4 focada em **matematica + indices**. O
plugin-mae `ia-combativa-adv-os` audita a **peca completa** — tese, base
juridica, narrativa, completude.

---

### `juris-adv-os` — buscar jurisprudencia para sustentar impugnacao

**Quando sugerir:** quando o calculo gera impugnacao (cliente perdeu/ganhou
com base em divergencia juridica, nao so aritmetica).

- Apos `auditar-pjecalc` se identificou que adversario ignorou ADC 58/59 →
  sugerir `/juris buscar "ADC 58 59 STF correcao trabalhista"`
- Apos `auditar-laudo-pericial` se perito usou indice errado → sugerir
  `/juris buscar "Sumula 362 STJ correcao dano moral"`
- Apos qualquer calculo cujo indice/criterio dependa de tema STJ/STF →
  sugerir `/juris validar` para garantir que a tese citada esta atualizada

**Por que faz sentido:** o `juris-adv-os` e order bump de R$ 29,80 com
anti-halucinacao por design. Combina perfeitamente com a anti-halucinacao
deste plugin (tabelas JSON cacheadas).

---

## Como cada output da skill traz o bloco "💡 Proximos passos opcionais"

Toda skill final do `calculosjudiciais-adv-os` termina com um bloco
estruturado:

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| [acao contextual] | `/<plugin> <skill>` | `<plugin>-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.
```

Esse bloco e **sempre soft** — nunca falha se o plugin nao estiver
instalado, nunca importa nada, nunca invoca skill de fora.

---

## O que fazer se o plugin-irmao nao estiver instalado

Cenario: voce gerou o calculo aqui, viu a sugestao "para peticionar,
rodar `/execucao cumprimento-sentenca`" — mas voce nao tem o
`execucao-adv-os`.

**Opcoes:**

1. **Comprar o plugin-irmao** (links Kirvano nos rodapes dos respectivos
   READMEs).
2. **Copiar a memoria de calculo gerada** e levar para o seu fluxo manual —
   o output desta skill ja vem auditavel, com fundamentacao legal completa,
   pronto para colar em qualquer peca.
3. **Pedir ao Claude no modo livre** (sem plugin) para usar a memoria de
   calculo como base de uma peca — funciona, mas sem governanca pesada
   (Hierarquia 4 Camadas + Proibicoes Absolutas + Suprema Corte R1-R4)
   que so o plugin-irmao traz.

---

## Resumo da regra

> **Este plugin sugere. Nunca acopla. Nunca quebra.**

Comprar so o `calculosjudiciais-adv-os` deve ser uma experiencia completa.
Comprar mais um plugin da familia deve **encadear naturalmente** sem
configuracao extra. Comprar a familia inteira deve produzir um sistema
operacional juridico de ponta a ponta — sem que nenhum plugin sofra de
"so funciona se o outro estiver instalado".
