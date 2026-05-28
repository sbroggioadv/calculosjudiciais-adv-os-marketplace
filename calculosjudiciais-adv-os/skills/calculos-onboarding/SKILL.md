---
name: calculos-onboarding
description: >
  CALCULOS-ONBOARDING — Comando `/start-calculos`. Configura a persona
  do advogado operador: nome, OAB, UF de inscricao, tribunais que
  atua (TJSP/TJRJ/TST/TRTn/etc.), areas que pratica (civel/trab/trib/
  prev/fam/crim/cons), tom de voz preferido. Persiste em
  `<cwd>/calculos/persona.md`. AVISO LGPD: orienta a NAO criar a
  pasta `calculos/` dentro de iCloud Drive, Google Drive, Dropbox ou
  OneDrive (dados de cliente nao podem viver em sync nuvem). Use
  SEMPRE na primeira sessao do plugin OU quando o usuario disser
  "configurar", "primeira vez", "trocar tom de voz", "adicionar
  tribunal", "atualizar OAB", "/start-calculos".
---

# CALCULOS-ONBOARDING — Configuracao da Persona

## 1. ESCOPO

Cria/atualiza arquivo `<cwd>/calculos/persona.md` com identidade do
advogado operador. Toda skill Tier 2 consulta esse arquivo via
tokens runtime `{{ADVOGADO_NOME}}`, `{{ADVOGADO_OAB}}`, etc.

**Pre-requisito de TODAS as skills Tier 2.** Sem persona configurada,
o orquestrador roda esta skill primeiro.

## 2. QUANDO RODAR

- Primeira sessao do plugin (persona.md nao existe)
- Comando explicito `/start-calculos`
- Usuario disse "configurar plugin", "trocar OAB", "adicionar
  tribunal", "mudar tom"
- Persona.md desatualizado (>6 meses sem revisao — alerta opcional)

## 3. FLUXO DE ONBOARDING

### Passo 1 — Aviso LGPD (CRITICO)

```
⚠️ ANTES DE COMECAR: AVISO DE PRIVACIDADE (LGPD)

A pasta `calculos/` que vou criar guardara configuracoes da sua
operacao + possivelmente memorias de calculo de processos reais.

NAO crie esta pasta dentro de:
- iCloud Drive (~/Library/Mobile Documents/...)
- Google Drive (~/Google Drive/...)
- Dropbox (~/Dropbox/...)
- OneDrive (~/OneDrive/...)
- Pastas pessoais do sistema (Documents, Desktop, Downloads)

Recomendado: pasta local fora de qualquer sync de nuvem.
Sugestao: `~/Documentos-Locais/escritorio/` ou `~/Workspace/`.

Sua sessao Claude Code esta em: <cwd atual>

Esta pasta esta dentro de servico de sync? (verifica caminho acima)
- Se SIM: encerre e mude para pasta local
- Se NAO: prossiga
```

Se cwd contem `iCloud`, `Google Drive`, `Dropbox`, `OneDrive`,
`Mobile Documents`, `CloudDocs` → **PARAR** e pedir mudanca de cwd.

### Passo 2 — Coletar dados (perguntar UMA pergunta por vez)

```
1. Nome completo profissional (como aparece nas pecas)?
   Ex: "Dra. Maria Silva" / "Joao Santos"

2. Numero de inscricao OAB (formato UF Numero, ex: SP 123.456)?

3. UF de inscricao principal?
   Ex: SP, RJ, MG, RS, BA, ...

4. Em quais tribunais voce atua regularmente? (responda lista)
   Opcoes comuns:
   - Justica Estadual: TJSP, TJRJ, TJMG, TJRS, TJBA, TJPR, TJSC, ...
   - Justica Federal: TRF1, TRF2, TRF3, TRF4, TRF5, TRF6
   - Justica do Trabalho: TST, TRT1, TRT2, ..., TRT24
   - Superiores: STJ, STF
   - JEC, JEF, JEFP
   Resposta: lista separada por virgula (ex: "TJSP, TRT15, TRF3, STJ")

5. Em quais areas voce pratica calculo judicial?
   Opcoes:
   - civel (cumprimento sentenca, dano material/moral, condominio,
     locacao, custas, bancario)
   - trabalhista (liquidacao, rescisao, horas extras, adicionais)
   - tributario (Selic federal, REFIS, repeticao indebito)
   - previdenciario (RMI, atrasados INSS, aposentadoria especial)
   - familia (alimentos, partilha)
   - criminal (pena multa)
   - consumidor (restituicao dobro CDC)
   Resposta: lista separada por virgula

6. Nome do escritorio (opcional — usado em pecas e relatorios)?

7. Cidade-base?

8. Tom de voz preferido para outputs:
   - "tecnico-direto" (sem floreio, vai ao ponto, default)
   - "didatico" (explica conceitos, util pra estagiarios e clientes)
   - "formal" (linguagem juridica tradicional, vocativo "Excelencia")
   - "consultivo" (mais conversacional, util pra parecer)
   Resposta: 1 opcao
```

### Passo 3 — Confirmacao

```
## Resumo da configuracao

| Campo | Valor |
|---|---|
| Nome | {{ADVOGADO_NOME}} |
| OAB | {{ADVOGADO_OAB}} |
| UF | {{ADVOGADO_UF}} |
| Tribunais ativos | {{TRIBUNAIS_LISTA}} |
| Areas | {{AREAS_LISTA}} |
| Escritorio | {{FIRM_NAME}} |
| Cidade | {{CIDADE}} |
| Tom de voz | {{TOM_VOZ_PERFIL}} |

Posso salvar em `<cwd>/calculos/persona.md`? (s/n)
```

### Passo 4 — Persistir

Criar `<cwd>/calculos/persona.md` com o conteudo:

```markdown
# Persona — calculosjudiciais-adv-os

> Arquivo de configuracao do operador. NAO commitar em repositorio
> publico. NAO incluir dados de processo de cliente aqui.

## Identidade

- **Nome:** [nome coletado]
- **OAB:** [UF + numero]
- **UF de inscricao:** [UF]
- **Escritorio:** [nome ou "advogacia individual"]
- **Cidade-base:** [cidade]

## Atuacao

- **Tribunais ativos:** [lista CSV]
- **Areas praticadas:** [lista CSV]

## Preferencias

- **Tom de voz:** [tecnico-direto | didatico | formal | consultivo]
- **Intensidade:** [media (default) | alta (mais assertivo) | baixa (mais cautelar)]

## Auditoria interna

- **Data de configuracao:** [YYYY-MM-DD]
- **Ultima atualizacao:** [YYYY-MM-DD]
- **Versao plugin:** v0.1.0

## Notas

[espaco livre para o advogado anotar particularidades da sua
operacao — ex: "atua majoritariamente em JEC SP zona leste", "foco
em direito bancario revisional", etc.]
```

### Passo 5 — Confirmacao final

```
✅ Persona configurada em `<cwd>/calculos/persona.md`

Proximos passos sugeridos:
- Use `/calculos` para conta livre (orquestrador roteia)
- Use `/calculo-civel` ou `/calculo-trabalhista` para atalhos
- Use `/auditar-pjecalc` para auditar PDF do PJE-CALC
- Use `/auditar-laudo-pericial` para auditar laudo pericial
- Use `/comparar-calculos` para comparar 2-3 calculos

Tudo pronto. Qual conta posso te ajudar agora?
```

## 4. ATUALIZACAO DE PERSONA EXISTENTE

Se `<cwd>/calculos/persona.md` ja existe:

```
Persona ja configurada (ultima atualizacao: YYYY-MM-DD).

O que voce quer atualizar?
1. Tribunais (adicionar/remover)
2. Areas (adicionar/remover)
3. Tom de voz
4. OAB / nome / escritorio
5. Resetar tudo (re-onboarding completo)
6. Cancelar
```

Aplicar mudanca pontual e atualizar `Ultima atualizacao:`.

## 5. OUTPUT (resumo final)

```yaml
persona:
  configurada: true
  arquivo: "<cwd>/calculos/persona.md"
  nome: "<nome>"
  oab: "<UF Numero>"
  tribunais: [...]
  areas: [...]
  tom_voz: "<perfil>"
  status: pronto_para_uso
```

## 6. AVISOS OBRIGATORIOS

- **LGPD por design:** alerta de pasta sync no Passo 1 e bloqueador
- **Persona.md NAO vai pra repo publico** — adicionar `calculos/`
  ao `.gitignore` do projeto do operador (lembrete no output final)
- **Nenhum dado coletado sai do disco local** — plugin nao envia
  telemetria
- **Atualizar persona** se mudar de UF, escritorio ou areas

## 7. INTEGRACAO

- **Upstream:** nenhuma (skill raiz)
- **Downstream:** todas as Tier 2 leem `<cwd>/calculos/persona.md`
  via tokens runtime
- **Cross-skill:** `identificar-tj-aplicavel` usa
  `persona.tribunais` para sugerir TJ aplicavel quando UF do caso
  bate com UF de atuacao

## 8. PROIBICOES

1. Nao salvar persona em pasta sync (iCloud/GDrive/Dropbox/OneDrive)
2. Nao coletar dados de cliente (CPF, processo, endereco) — persona
   e da OPERACAO do advogado, nao do caso
3. Nao enviar dados para API externa — tudo fica em disco local
4. Nao perguntar tudo de uma vez — UMA pergunta por vez (UX)
5. Nao prosseguir se cwd estiver em pasta sync (LGPD bloqueador)

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Configurar persona de execucao processual | `/start-execucao` | `execucao-adv-os` |
| Configurar persona de trabalhista | `/start-trabalhista` | `trabalhista-adv-os` |
| Configurar persona do plugin-mae | `/start` | `ia-combativa-adv-os` |

> Cada plugin Adv-OS tem onboarding proprio — todos seguem o mesmo
> padrao de aviso LGPD + persona local em `<cwd>/<plugin>/`.
