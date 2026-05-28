# CLAUDE.md — plugin-calculosjudiciais (interno do source)

> Regras internas do source `plugin-calculosjudiciais/`. Plugin alvo:
> `calculosjudiciais-adv-os`. Familia Adv-OS.

---

## Identidade

- **Plugin name (slug):** `calculosjudiciais-adv-os`
- **Marketplace publico (a criar nas FASES 2-7 do PLAYBOOK):** repo `calculosjudiciais-adv-os-marketplace` no GitHub do organizador (mesmo padrao dos plugins-irmaos da familia)
- **Source privado:** este diretorio
- **Modelo comercial:** plugin-mae entry-level Kirvano — **R$ 98,80**
- **Posicionamento:** acessivel (dor universal — todo advogado bate em calculo); diferencial brutal nas skills transversais (parser PJE-CALC + auditor laudo pericial + comparador)

## Filosofia do plugin (3 pilares)

### Pilar 1 — STANDALONE-FIRST
**Zero dependencia externa em runtime.** Plugin funciona 100% sozinho:
- NAO chama API externa (BCB, IBGE, CJF, Sicalc) em runtime
- NAO importa/le arquivos de outros plugins da familia
- NAO auto-invoca skills de outros plugins
- Cache local de indices (JSON commitado) atualizado a cada release
- Se faltar plugin-irmao, output gera **sugestao de comando** (texto, nao execucao)

### Pilar 2 — ANTI-HALUCINACAO POR DESIGN
- Indices vivos em `scripts/data/indices/*.json` com **data de extracao**, **fonte oficial** e **range valido**
- Calculo dentro do range → gera valor final com indice verificado
- Calculo fora do range → gera formula + link oficial + placeholder
- NUNCA "lembrar" indice — sempre consultar tabela commitada
- Aviso obrigatorio no rodape de todo output: "validar contra fonte oficial antes de protocolar"

### Pilar 3 — AUDITORIA E NAO SO GERACAO
O diferencial competitivo nao e "fazer calculo" (PJE-CALC, Calculo Juridico, Debit ja fazem). E **auditar calculo ja feito**:
- `parser-auditor-pjecalc` le PDF do PJE-CALC e identifica erros
- `auditor-laudo-pericial-contabil` audita laudo de perito contabil
- `comparador-calculos` posiciona 2-3 calculos lado a lado pra identificar divergencias

## Skill map (28 + orquestrador)

### Tier 0 — Orquestracao
- `calculos-master` (orquestrador)
- `calculos-onboarding` (`/start-calculos` — configura advogado, tribunais que atua, etc.)

### Tier 1 — Classificadores
- `classificar-tipo-calculo` (decide qual skill chamar)
- `identificar-tj-aplicavel` (TJ → tabela oficial correta)

### Tier 2 — CIVEIS (7)
- `calculo-cumprimento-sentenca-civel`
- `calculo-rpv-precatorio`
- `calculo-danos-indenizatorios` (dano material, moral, lucros cessantes)
- `calculo-debito-condominial`
- `calculo-debito-locaticio`
- `calculo-custas-honorarios`
- `calculo-revisao-bancaria` (anatocismo, Price vs SAC)

### Tier 2 — TRABALHISTAS (5)
- `calculo-liquidacao-trabalhista`
- `calculo-verbas-rescisorias`
- `calculo-horas-extras-reflexos`
- `calculo-adicionais-trabalhistas`
- `calculo-deposito-recursal`

### Tier 2 — TRIBUTARIOS (3)
- `calculo-tributo-federal-selic`
- `calculo-refis-parcelamento`
- `calculo-repeticao-indebito`

### Tier 2 — PREVIDENCIARIOS (3)
- `calculo-rmi-beneficio`
- `calculo-atrasados-inss`
- `calculo-aposentadoria-especial`

### Tier 2 — FAMILIA + CRIMINAL + CONSUMIDOR (4)
- `calculo-alimentos-atrasados`
- `calculo-partilha-bens`
- `calculo-pena-multa`
- `calculo-restituicao-dobro-cdc`

### Tier 3 — TRANSVERSAIS DIFERENCIAIS (6) ⭐ ouro
- `parser-auditor-pjecalc` (le PDF + audita)
- `comparador-calculos` (2-3 calculos lado a lado)
- `atualizador-indices-cache` (consulta tabela JSON local)
- `auditor-laudo-pericial-contabil`
- `gerador-quesitos-perito-contabil`
- `contra-laudo-pericial`

### Tier 4 — Meta
- `protocolo-p4-calculos` (Suprema Corte R1-R4 — Brief, Calculo, Compliance, Performance)
- `gestao-prazo-impugnacao` (15 dias CPC 525 / 8 dias CLT 879)

## Auto-chains criticas

- TODA conta final → auto-dispara `protocolo-p4-calculos`
- `classificar-tipo-calculo` → propaga contexto pra skill correta
- `calculo-*-trabalhista` → BLOQUEADO se `calculos-onboarding` nao configurou tribunais
- `parser-auditor-pjecalc` → auto-dispara `comparador-calculos` se houver calculo de referencia

## Cross-link com plugins-irmaos (SUGESTAO, NAO EXECUCAO)

Cada output do orquestrador termina com bloco fixo:

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Peticionar cumprimento de sentenca | /execucao cumprimento-sentenca | execucao-adv-os |
| Impugnar calculo do exequente | /execucao embargos-execucao | execucao-adv-os |
| Liquidar sentenca trabalhista | /trabalhista liquidacao-execucao-trabalhista | trabalhista-adv-os |
| Auditar com IA o calculo completo | /ia-combativa suprema-corte-r1-r4 | ia-combativa-adv-os |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.
```

NAO importar, NAO ler, NAO invocar. So sinalizar.

## Cache local de indices (Pilar 2)

```
scripts/data/indices/
├── selic-mensal.json         (BCB)
├── ipca-mensal.json          (IBGE)
├── ipca-e-mensal.json        (IBGE)
├── inpc-mensal.json          (IBGE)
├── tr-mensal.json            (BCB)
└── taxa-legal-cc406.json     (pos Lei 14.905/2024)
```

Cada JSON tem schema:

```json
{
  "indice": "SELIC",
  "fonte": "Banco Central do Brasil — https://www.bcb.gov.br",
  "url_oficial": "https://www3.bcb.gov.br/sgspub/...",
  "data_extracao": "2026-05-28",
  "release_plugin": "v0.1.0",
  "range_inicial": "2000-01",
  "range_final": "2026-04",
  "frequencia": "mensal",
  "valores": {
    "2000-01": 1.46,
    "2000-02": 1.45,
    ...
    "2026-04": 0.98
  },
  "aviso": "Indices apos 2026-04 devem ser consultados em <url> e atualizados via release nova do plugin."
}
```

Atualizacao = release nova do plugin (v0.2.0 = +6 meses de indices).

## Padroes de codigo

1. Stock first (WebSearch + WebFetch nativos — mas com cautela, so como fallback se algo critico).
2. Auto-chains so onde fazem sentido (calculo → P4; classificador → skill especifica).
3. Saida estruturada (markdown com blocos, tabelas, yaml de contexto, memoria de calculo auditavel).
4. Aviso legal em cada output final + em outputs criticos.
5. Skill folder = SO SKILL.md (regra dura da familia).
6. plugin.json minimal (4 campos canonicos).
7. Tabelas de indices = JSON commitado em `scripts/data/indices/` (NAO no Cowork — fica fora do package distribuido se possivel via .claudeignore? NAO — precisa estar acessivel pelas skills, vai junto).

## Roadmap pos-v0.1.0

- v0.2.0: atualizar 6 tabelas de indices (+6 meses), adicionar `calculo-icms-estadual` e `calculo-iss-municipal` por UF
- v0.3.0: parser laudo pericial contabil avancado (multi-formato — PDF, DOCX, XLSX)
- v0.4.0: integracao com `agentic-os-web` (cockpit) — dashboard de calculos pendentes
- v1.0.0: cobertura completa 27 TJs + TST + TRTs + STJ + STF

## Pre-mortem (cenarios mitigados em design)

1. **Indice desatualizado pos-cutoff** → cache com `range_final` explicito + fallback formula+link
2. **Plugin-irmao nao instalado** → sugestoes opcionais, nao quebra
3. **PJE-CALC PDF com layout diferente** → parser com fallback regex generico + aviso manual
4. **Calculo trabalhista pre-Reforma vs pos-Reforma** → flag `marco_intertemporal` no contexto + segmentacao contratual
5. **Confusao SELIC pre-2024 vs Taxa Legal pos-Lei 14.905/2024** → tabela separada `taxa-legal-cc406.json` + skill de transicao
6. **Operador cola dados de cliente em pasta sincronizada** → warning no `calculos-onboarding`

## Anti-despersonalizacao

`audit/forbidden-terms.json` deve bloquear menção a:
- Nome civil do criador da metodologia
- OAB pessoal
- Email pessoal
- Nome do escritorio-modelo
- Casos reais (nomes de clientes)
- Tokens runtime: `{{ADVOGADO_NOME}}`, `{{ADVOGADO_OAB}}`, `{{ADVOGADO_UF}}`, `{{FIRM_NAME}}`, `{{CIDADE}}`, `{{UF}}`, `{{TOM_VOZ_PERFIL}}`

Rodar `python3 audit/audit.py` antes de cada commit.

## Comunicacao

- **Idioma:** Portugues (Brasil)
- **Tom dos docs internos:** tecnico, direto, sem mencoes pessoais
- **Tom das skills/commands (para o usuario-cliente):** acolhedor, tecnico, respeita `tom_voz` configurado em runtime
- **Reportes:** ✅ concluido / 🔴 erro / 🏁 sprint finalizada

---

**Ultima atualizacao:** 2026-05-28 — scaffold inicial, FASE 4 do PLAYBOOK.
