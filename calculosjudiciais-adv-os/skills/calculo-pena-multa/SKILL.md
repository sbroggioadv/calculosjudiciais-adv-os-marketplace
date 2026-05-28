---
name: calculo-pena-multa
description: >
  CALCULO-PENA-MULTA — Estrutura memoria de calculo da pena de multa
  criminal (CP art. 49-52). Calcula em duas fases: (1) numero de
  dias-multa fixado na sentenca (10 a 360, conforme dosimetria) ×
  (2) valor do dia-multa (entre 1/30 e 5 vezes o salario minimo
  vigente NA DATA DO FATO — CP art. 49 §1º, NAO data da sentenca).
  Considera aumento ate o triplo (CP art. 60 §1º) quando o juiz
  reputa ineficaz pela situacao economica. Aplica atualizacao SELIC
  quando inscrita em divida ativa (Lei 9.430/96 + Lei 4.320/64).
  Identifica hipoteses de conversao em prestacao pessoal de servicos
  (raras pos-Lei 9.268/96 — multa NAO mais converte em PPL por
  inadimplemento). NUNCA gera salario minimo "lembrado" para data
  futura (anti-halucinacao). Use sempre que o advogado mencionar
  pena de multa, dias-multa, multa criminal, conversao de pena,
  execucao de multa criminal ou divida ativa de multa penal.
---

# CALCULO-PENA-MULTA — Pena Pecuniaria Criminal

## 1. ESCOPO

Estrutura memoria de calculo da pena de multa em 3 contextos:

1. **Fixacao inicial** — alegacoes finais / sentenca / acordao
   (calcula dias-multa × valor unitario)
2. **Atualizacao para pagamento** — entre sentenca e pagamento
   espontaneo (atualiza pelo SM vigente NA DATA DO FATO + correcao)
3. **Inscricao em divida ativa** — pos-transito julgado sem pagamento
   (aplica SELIC, Lei 9.430/96, conforme posicao do MP/PGE)

NAO substitui sentenca nem peticao — gera memoria auditavel.

---

## 2. INPUT NECESSARIO

Perguntar ou propagar:

1. **Tipo penal + pena** (qual crime, qual sentenca aplicou)
2. **Data do fato** (CRUCIAL — define SM aplicavel, CP 49 §1º)
3. **Data da sentenca** (transito em julgado se ja transitou)
4. **Numero de dias-multa fixado** (entre 10 e 360 — CP 49 caput)
5. **Valor do dia-multa fixado** (entre 1/30 e 5 SM vigente na data
   do fato — CP 49 §1º)
6. **Houve aumento ate o triplo?** (CP 60 §1º — fundamentacao na
   situacao economica do reu)
7. **Data prevista do pagamento** (para atualizacao)
8. **Status:** ja inscrito em divida ativa? Em que data?

---

## 3. PROCESSAMENTO

### Passo 1 — Calcular valor base na data do fato

```
SM_data_fato = salario minimo vigente NA DATA DO FATO (input obrigatorio)
valor_dia_multa_base = SM_data_fato × fracao_fixada
                       (entre 1/30 e 5)
valor_total_base = dias_multa × valor_dia_multa_base
```

⚠️ **REGRA DURA CP 49 §1º:** o SM e o VIGENTE NA DATA DO FATO, nao da
sentenca, nao do pagamento. Isso e contraintuitivo mas e a lei.

### Passo 2 — Aplicar aumento ate o triplo (se houver)

CP art. 60 §1º:
> "A multa pode ser aumentada ate o triplo, se o juiz considerar que,
> em virtude da situacao economica do reu, e ineficaz, embora aplicada
> no maximo."

Se a sentenca aplicou esse aumento:
```
valor_total_aumentado = valor_total_base × fator_aumento (max 3)
```

### Passo 3 — Atualizacao monetaria entre fato e pagamento

CP art. 49 §2º:
> "O valor da multa sera atualizado, quando da execucao, pelos indices
> de correcao monetaria."

Indice usado:
- ANTES da inscricao em divida ativa: tabela do TJ do foro da execucao
  (geralmente IPCA-E ou equivalente)
- APOS inscricao em divida ativa: SELIC (Lei 9.430/96 art. 61 + Lei
  4.320/64 — entendimento da Fazenda + maioria dos TJs)

### Passo 4 — Marcar conversao em PPL (raro pos-Lei 9.268/96)

**IMPORTANTE:** desde a Lei 9.268/96 a multa criminal NAO converte
em pena privativa de liberdade por inadimplemento. Cobrada como
DIVIDA ATIVA da Fazenda Publica (CP art. 51).

Excecoes residuais (so para fatos anteriores a Lei 9.268/96, hoje
historico): conversao 1 dia-multa = 1 dia-detencao (revogada).

### Passo 5 — Identificar regime de execucao

| Hipotese | Quem executa | Foro |
|----------|--------------|------|
| Multa criminal pos-Lei 9.268/96 | MP/PGE (apos inscricao DA) | Vara das Execucoes Fiscais |
| Multa criminal nao paga (10d apos transito) | Inscricao em DA pela Fazenda | Procedimento administrativo |
| Multa de delegado/MP em transacao penal (Lei 9.099) | Juizo criminal | JEC criminal |
| Multa cumulada com PPL/PRD em sentenca | Executada como condicao adicional | Vara das Execucoes Penais (acessorio) |

---

## 4. OUTPUT — PLANILHA ESTRUTURADA

```markdown
## Memoria de Calculo — Pena de Multa Criminal

**Atencao:** Esta skill NAO "lembra" salario minimo de datas
especificas — exige input do advogado com a fonte (Decreto presidencial
ou Lei que fixou o SM da data). SM e o VIGENTE NA DATA DO FATO
(CP art. 49 §1º).

### Premissas

| Campo | Valor |
|-------|-------|
| Tipo penal | [art. X CP / Lei especifica] |
| Data do fato | [DD/MM/AAAA] |
| Data da sentenca | [DD/MM/AAAA] |
| Transito em julgado | [DD/MM/AAAA ou "pendente"] |
| Dias-multa fixados | [N entre 10 e 360] |
| Valor dia-multa fixado | [fracao SM, ex: 1/3 SM] |
| Aumento art. 60 §1º? | [sim, fator X / nao] |
| SM vigente data fato | [R$ X — fonte: Dec. nº ____] |
| Status inscricao DA | [pendente / inscrita em DD/MM/AAAA] |

---

### Tabela 1 — Calculo base (data do fato)

| Componente | Calculo | Valor |
|------------|---------|-------|
| Valor unitario dia-multa | SM × fracao | SM × ___ = R$ ___ |
| Total base | dias-multa × valor unitario | ___ × R$ ___ = R$ ___ |
| (Aumento art. 60 §1º) | base × fator (max 3) | R$ ___ × ___ = R$ ___ |
| **VALOR FIXADO NA SENTENCA** | | **R$ ___** |

---

### Tabela 2 — Atualizacao monetaria

#### Fase A — Antes da inscricao em DA (correcao pelo TJ)

| Periodo | Indice [TABELA TJ] | Acumulado | Valor atualizado |
|---------|---------------------|-----------|------------------|
| [data fato] | _____ | 1,0 | R$ ___ |
| [data sentenca] | _____ | _____ | R$ ___ |
| [data inscricao DA ou hoje] | _____ | _____ | R$ ___ |

#### Fase B — Apos inscricao em DA (SELIC + 1% mes do pagamento — Lei 9.430/96)

| Periodo | SELIC mensal [TABELA BCB] | Acumulado | Valor atualizado |
|---------|----------------------------|-----------|------------------|
| [data inscricao] | _____ | _____ | R$ ___ |
| ... | _____ | _____ | _____ |
| [data pagamento] | _____ + 1% | _____ | **R$ ___** |

---

### Totalizacao

| Item | Valor |
|------|-------|
| Valor base (data do fato) | R$ ___ |
| Correcao monetaria (fato → DA) | R$ ___ |
| SELIC + 1% (DA → pagamento) | R$ ___ |
| **TOTAL DEVIDO ATE [data]** | **R$ ___** |
```

---

## 5. AVISOS OBRIGATORIOS NO OUTPUT FINAL

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR/PAGAR:

1. SALARIO MINIMO — confirmar o SM VIGENTE NA DATA DO FATO. Esta skill
   NAO armazena tabela historica de SM. Fonte: Decreto presidencial
   anual / Lei 14.358/2026 (SM vigente apos 01/01/2026).

2. CP art. 49 §1º — fracao deve estar entre 1/30 e 5 SM. Fora desse
   range = sentenca nula nessa parte (apelacao art. 593 II CPP).

3. CP art. 60 §1º — aumento ate o triplo so vale se a sentenca tem
   FUNDAMENTACAO ESPECIFICA na situacao economica. Aumento generico
   = nulidade (REsp 1.281.560/MG).

4. LEI 9.268/96 — multa criminal NAO converte em PPL por
   inadimplemento (desde 1996). Executada como divida ativa da
   Fazenda (CP 51). Nao usar fundamentacao revogada.

5. SELIC pos-inscricao em DA — entendimento dominante (Lei 9.430/96
   art. 61), mas alguns TJs aplicam IPCA + 1% mes (CTN 161). Conferir
   posicao do MP/PGE local.

6. PRESCRICAO da pretensao executoria — CP art. 109 + 110. Multa
   prescrita NAO pode ser cobrada. Verificar interrupcoes (CP 117) e
   suspensoes.

7. PARCELAMENTO — CP art. 50 admite parcelamento pelo juiz da execucao
   (em geral 5 a 30 prestacoes mensais). Pedir antes da inscricao em
   DA se possivel.

8. TRANSACAO PENAL (Lei 9.099/95) — multa fixada em transacao tem
   regime proprio (administrativo). Nao confundir com sentenca
   condenatoria.
```

---

## 6. FUNDAMENTACAO LEGAL

- **CP art. 49** — pena de multa: 10 a 360 dias-multa, valor 1/30 a 5
  SM vigente na DATA DO FATO
- **CP art. 49 §2º** — atualizacao monetaria na execucao
- **CP art. 50** — pagamento + parcelamento (juiz da execucao)
- **CP art. 51** (com redacao Lei 9.268/96) — multa nao paga vira
  divida ativa (NAO converte em PPL)
- **CP art. 52** — suspensao da execucao por doenca mental
- **CP art. 60 §1º** — aumento ate o triplo (situacao economica)
- **Lei 9.268/96** — alterou CP 51, fim da conversao em PPL
- **Lei 9.430/96 art. 61** — SELIC sobre debitos da Fazenda
- **Lei 4.320/64** — normas gerais de direito financeiro (inscricao
  em DA)
- **Lei 14.358/2026** — SM vigente apos 01/01/2026 (confirmar Decreto
  de revisao anual)
- **CPP art. 593 II** — apelacao por aplicacao indevida da multa
- **REsp 1.281.560/MG** — fundamentacao especifica para aumento art.
  60 §1º
- **Tema 931 STJ** — competencia para execucao de multa criminal

---

## 7. INTEGRACAO

- **Upstream:** `calculos-master`, `classificar-tipo-calculo`,
  `identificar-tj-aplicavel`, `atualizador-indices-cache`
- **Downstream:** auto-dispara `protocolo-p4-calculos`
- **Sugestao de plugin-irmao:**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Calcular prescricao da pretensao executoria | /ia-combativa prescricao-penal | ia-combativa-adv-os |
| Peticionar parcelamento (CP 50) | /ia-combativa peticao-criminal | ia-combativa-adv-os |
| Auditar calculo (R1-R4) antes do pagamento | /calculos protocolo-p4 | (interno) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.
```

---

## 8. PROIBICOES

1. **NUNCA usar SM "lembrado"** — sempre exigir input do advogado com
   fonte (Decreto/Lei).
2. **NUNCA usar SM da data da sentenca ou do pagamento** — sempre da
   DATA DO FATO (CP 49 §1º).
3. **NUNCA mencionar conversao em PPL** por inadimplemento — revogada
   desde Lei 9.268/96.
4. **NUNCA aplicar aumento art. 60 §1º sem confirmar fundamentacao**
   especifica na sentenca.
5. **NUNCA omitir avaliacao de prescricao** — multa pode estar
   prescrita.
6. **NUNCA confundir multa de transacao penal** (Lei 9.099) com multa
   de sentenca condenatoria — regimes distintos.
