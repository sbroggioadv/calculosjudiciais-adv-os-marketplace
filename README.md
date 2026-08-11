# Calculosjudiciais-Adv-OS — Marketplace

> ## ⚖️ Este repositório NÃO é software livre
>
> O código fica visível para viabilizar a instalação no Claude/Cowork — não porque seja gratuito.
>
> **CALCULOS JUDICIAIS ADV-OS — R$ 98,80, pagamento único** (sem assinatura, sem recorrência)
> 👉 **[Adquirir a licença](https://pay.kirvano.com/d839e376-57cc-4335-bb0a-7a4986029367)**
>
> **Ao forkar ou clonar este repositório você adere à [licença de uso](LICENSE)**, devendo efetuar o
> pagamento no link acima e enviar o comprovante para **luis@sbroggio.com.br**.
>
> Os forks são públicos no GitHub e são registrados pelo titular (data, conta e repositório).
>
> **Já comprou?** Nada a fazer — sua licença cobre o uso e o fork para instalação. Este aviso vale de
> 11/08/2026 em diante, para quem chega ao repositório sem ter adquirido.


> ## ⚖️ Este repositório NÃO é software livre
>
> O código fica visível para viabilizar a instalação no Claude/Cowork — não porque seja gratuito.
>
> **CALCULOS JUDICIAIS ADV-OS — R$ 98,80, pagamento único** (sem assinatura, sem recorrência)
> 👉 **[Adquirir a licença](https://pay.kirvano.com/d839e376-57cc-4335-bb0a-7a4986029367)**
>
> **Ao forkar ou clonar este repositório você adere à [licença de uso](LICENSE)**, devendo efetuar o
> pagamento no link acima e enviar o comprovante para **luis@sbroggio.com.br**.
>
> Os forks são públicos no GitHub e são registrados pelo titular (data, conta e repositório).
>
> **Já comprou?** Nada a fazer — sua licença cobre o uso e o fork para instalação. Este aviso vale de
> 11/08/2026 em diante, para quem chega ao repositório sem ter adquirido.


> Marketplace oficial do plugin **Calculosjudiciais-Adv-OS** para Claude Code.

Sistema operacional do advogado brasileiro em **cálculos judiciais** — cível, trabalhista, tributário, previdenciário, família, criminal e consumidor.

---

## 📦 Plugins neste marketplace

| Plugin | Versão | Descrição |
|---|---|---|
| `calculosjudiciais-adv-os` | 0.1.0 | 34 skills cobrindo todas as áreas + parser auditor PJE-CALC PDF + auditor de laudo pericial contábil |

---

## 🎯 Diferenciais

- **34 skills** em 5 Tiers (orquestração + classificação + cálculos por área + transversais diferenciais + meta)
- **Parser auditor PJE-CALC PDF** — lê a planilha gerada pelo PJE-Calc Cidadão e audita 6 critérios (ADC 58/59 STF, Súm. 368 TST, IRPF Lei 7.713 art. 12-A, juros pós Lei 14.905/2024)
- **Comparador de cálculos** — posiciona 2-3 cálculos lado a lado, identifica divergências e quantifica gap
- **Auditor de laudo pericial contábil** — audita laudos contra NBC PP 01 CFC
- **Cache local de 6 índices oficiais** (Selic, IPCA, IPCA-E, INPC, TR, Taxa Legal CC406 pós Lei 14.905/2024)
- **Anti-halucinação por design** — zero índice numérico "lembrado"; sempre consulta tabela JSON commitada com data de extração e fonte oficial

---

## 🚀 Como instalar (via Cowork UI)

1. Abrir Cowork (aba lateral)
2. Settings → Plugins → aba "Pessoal" → "+" → "Adicionar marketplace"
3. Colar a URL deste repositório
4. Sincronizar
5. Instalar o plugin `calculosjudiciais-adv-os`
6. Rodar `/start-calculos` para configurar seu perfil

---

## 📜 Licença

Uso licenciado mediante aquisição — ver [`LICENSE`](./LICENSE). As cópias obtidas até 11/08/2026 permanecem sob MIT; a partir dessa data o código é proprietário.

---

## 🔗 Família Adv-OS

Plugins-irmãos opcionais (não obrigatórios):
- `execucao-adv-os` — peças de execução + monitória + cobrança
- `trabalhista-adv-os` — peças trabalhistas completas
- `previdenciario-adv-os` — direito previdenciário (RGPS + RPPS)
- `tributario-societario-adv-os` — defesa fiscal + societário
- `direito-familia-adv-os` — peças de família judiciais
- `ia-combativa-adv-os` — plugin-mãe (Mentoria IA Combativa)
- `juris-adv-os` — busca + validação de jurisprudência (anti-halucinação)

Sugestões de uso integrado aparecem no rodapé de cada output do plugin. Não há dependência hard — cada plugin funciona standalone.
