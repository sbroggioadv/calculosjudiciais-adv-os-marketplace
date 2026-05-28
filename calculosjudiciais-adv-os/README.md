# calculosjudiciais-adv-os

> Plugin Claude Code para **calculos judiciais brasileiros** — qualquer area
> (civel, trabalhista, tributario, previdenciario, familia, criminal, consumidor)
> com diferencial brutal em **AUDITORIA** de calculos de terceiros (PJE-Calc,
> laudo pericial, contadoria judicial, parte adversa).

---

## O que faz

- Calcula 22 tipos de conta diferente sob o ponto de vista de qualquer area do
  Direito brasileiro — cumprimento de sentenca, RPV, dano moral/material,
  liquidacao trabalhista, verbas rescisorias, atrasados INSS, RMI, tributo
  federal Selic, alimentos atrasados, partilha de bens, restituicao em dobro
  CDC e mais.
- **Audita** calculos de terceiros (parte contraria, contadoria, perito) com
  parser proprio de PDF do PJE-Calc Cidadao + checklist NBC PP 01 CFC para
  laudo pericial contabil.
- **Compara** 2-3 calculos do mesmo caso lado a lado (autor × reu × contadoria,
  ou perito × perito-assistente), quantificando o gap monetario por divergencia.
- Atualiza valor unico entre datas com indice oficial cacheado (Selic, IPCA,
  IPCA-E, INPC, TR, Taxa Legal CC 406 pos Lei 14.905/2024).
- Gera quesitos tecnicos para perito contabil + contra-laudo baseado em NBC PP 01.

---

## Por que usar

| Diferencial | Plugins-mercado | calculosjudiciais-adv-os |
|---|---|---|
| Gera calculo? | Sim (PJE-Calc, Calculo Juridico, Debit, Doc9) | Sim |
| Audita calculo de terceiro? | **Nao** | **Sim — parser-auditor-pjecalc** ⭐ |
| Audita laudo pericial? | **Nao** | **Sim — auditor-laudo-pericial-contabil** ⭐ |
| Compara 2-3 calculos lado a lado? | **Nao** | **Sim — comparador-calculos** ⭐ |
| Anti-halucinacao por design? | **Nao garantido** | **Sim — cache JSON com data, fonte, range** |
| ADC 58/59 + Lei 14.905/2024? | **Mecanismo opaco** | **Tabela separada `taxa-legal-cc406.json`** |
| Stack | Software pago, web | Plugin Claude Code, roda no terminal local |
| LGPD | Dados na nuvem do fornecedor | Dados na maquina do operador, gitignored |

**Posicionamento:** plugin-mae entry-level (R$ 98,80 Kirvano) — dor universal
de advogado. Diferencial estrutural nas 3 skills transversais com ⭐.

---

## As 28 skills

| Tier | Conteudo |
|------|----------|
| **Tier 0** (2) | `calculos-master` (orquestrador) · `calculos-onboarding` (wizard) |
| **Tier 1** (2) | `classificar-tipo-calculo` · `identificar-tj-aplicavel` |
| **Tier 2 — Civeis** (7) | cumprimento de sentenca · RPV/precatorio · danos indenizatorios · debito condominial · debito locaticio · custas/honorarios · revisao bancaria |
| **Tier 2 — Trabalhistas** (5) | liquidacao · verbas rescisorias · horas extras+reflexos · adicionais (insalubridade/periculosidade/noturno) · deposito recursal |
| **Tier 2 — Tributarios** (3) | tributo federal Selic · REFIS/parcelamento · repeticao de indebito |
| **Tier 2 — Previdenciarios** (3) | RMI beneficio · atrasados INSS · aposentadoria especial |
| **Tier 2 — Familia/Criminal/Consumidor** (4) | alimentos atrasados · partilha de bens · pena de multa · restituicao em dobro CDC |
| **Tier 3 — Transversais ⭐** (6) | `parser-auditor-pjecalc` · `comparador-calculos` · `atualizador-indices-cache` · `auditor-laudo-pericial-contabil` · `gerador-quesitos-perito-contabil` · `contra-laudo-pericial` |
| **Tier 4 — Meta** (2) | `protocolo-p4-calculos` (Suprema Corte R1-R4 auto) · `gestao-prazo-impugnacao` (CPC 525 / CLT 879 §2º) |

---

## Como instalar

O plugin e distribuido via marketplace GitHub publico. Para instalar no Cowork:

1. Abra **Settings → Plugins → aba Pessoal**.
2. Clique em **"+" Uploads locais**.
3. Cole a URL do repositorio do marketplace (informada no checkout Kirvano).
4. Rode `/start-calculos` para configurar o plugin ao perfil do seu escritorio.

---

## Como usar

### Exemplo 1 — atualizar valor unico

```
/atualizar-valor R$ 5.000,00 de 01/03/2023 a 28/05/2026 pelo IPCA-E
```

Output: valor atualizado + fator acumulado + URL oficial IBGE + aviso de
validacao final.

### Exemplo 2 — auditar calculo da parte contraria

```
/auditar-pjecalc /Users/eu/Downloads/calculo-reu.pdf
```

Output: resumo do calculo + auditoria tecnica (✅/❌/⚠️) + erros identificados
com fundamentacao legal + base pronta para impugnacao.

### Exemplo 3 — comparar autor × reu × contadoria

```
/comparar-calculos calculo-autor.pdf calculo-reu.pdf calculo-contadoria.pdf
```

Output: tabela lado a lado verba a verba + gap monetario (R$ + %) + analise
tecnica de qual lado tem razao em cada divergencia + estrategia recomendada.

---

## Filosofia (3 pilares)

### 1. STANDALONE-FIRST

Zero API externa em runtime. Zero leitura de arquivos de outros plugins. Zero
auto-invocacao de skills de outros plugins. Cache local de indices (JSON
commitado) atualizado a cada release. Plugins-irmaos: **sugestao de comando**
(texto, nao execucao) no rodape.

### 2. ANTI-HALUCINACAO POR DESIGN

Indices vivem em `scripts/data/indices/*.json` com `data_extracao`, `fonte`,
`url_oficial`, `range_inicial`, `range_final`. Dentro do range → valor final.
Fora do range → formula + link oficial + placeholder. NUNCA "lembrar" indice.
Aviso obrigatorio no rodape de todo output final: "validar contra fonte
oficial antes de protocolar".

### 3. AUDITORIA, NAO SO GERACAO

Mercado ja tem PJE-Calc, Calculo Juridico, Debit, Doc9 para GERAR. Ninguem
AUDITA. Foco do plugin: `parser-auditor-pjecalc`, `auditor-laudo-pericial-contabil`,
`comparador-calculos`.

---

## Privacidade

A pasta `<cwd>/calculos/` onde vivem persona, configuracao e os calculos
e gitignored por padrao. O plugin emite aviso se o workspace estiver em pasta
sincronizada (iCloud / OneDrive / Dropbox / Drive). Nenhum dado de cliente
sai do seu ambiente.

---

## Commands

`/start-calculos` · `/calculos` · `/calculo-civel` · `/calculo-trabalhista` ·
`/auditar-pjecalc` ⭐ · `/auditar-laudo-pericial` ⭐ · `/comparar-calculos` ⭐ ·
`/atualizar-valor`

---

## Integracoes opcionais

Plugin **standalone**, mas os outputs incluem sugestoes (texto) de plugins-
irmaos quando fizerem sentido:

- `execucao-adv-os` — peticionamento de cumprimento de sentenca, embargos
- `trabalhista-adv-os` — peca completa de liquidacao trabalhista
- `previdenciario-adv-os` — peca administrativa/judicial pos calculo RMI
- `ia-combativa-adv-os` — auditoria final via Suprema Corte R1-R4
- `juris-adv-os` — busca + validacao de jurisprudencia

Detalhes em `docs/INTEGRACOES.md`.

---

**Licenca:** MIT · **Familia:** IA Combativa Adv-OS
