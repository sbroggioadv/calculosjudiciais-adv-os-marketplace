---
name: gestao-prazo-impugnacao
description: >
  GESTAO-PRAZO-IMPUGNACAO — Calcula data limite para impugnacao de
  calculo da parte contraria conforme rito. Aplica contagem correta
  (UTEIS no CPC 219 vs CORRIDOS na CLT 775 §1º), feriados forenses
  (federais/estaduais/municipais/tribunal), recesso CPC 220 (20/12
  a 20/01) e expediente reduzido. Cobre 4 ritos: CPC 525 (impugnacao
  cumprimento civel = 15 uteis), CPC 535 (Fazenda Publica = 30 uteis),
  CLT 879 §2º (manifestacao liquidacao = 8 corridos), CLT 884
  (embargos execucao apos garantia = 5 corridos). ALERTA VERMELHO se
  prazo < 3 dias uteis. NUNCA presume intimacao automatica — exige
  data. Use quando mencionar prazo de impugnacao, contar prazo, data
  limite, CPC 525, CPC 535, CLT 879 §2º, CLT 884, prazo recursal.
---

# GESTAO-PRAZO-IMPUGNACAO — Calculo de Prazo para Impugnar

## 1. ESCOPO

Calcula a data limite para impugnacao em 4 ritos diferentes, aplicando
corretamente:
1. Tipo de contagem (UTEIS vs CORRIDOS) conforme rito
2. Termo inicial (1º dia util seguinte a intimacao — CPC 224)
3. Feriados forenses (federais, estaduais, municipais e do tribunal)
4. Suspensao do recesso forense (CPC 220 — 20/12 a 20/01)
5. Expediente reduzido (carnaval, Corpus Christi, etc.)

Output:
- Data limite calculada
- Alerta vermelho se prazo < 3 dias uteis (URGENTE)
- Recomendacao de protocolo com folga de seguranca

---

## 2. INPUT NECESSARIO

Perguntar ou propagar:

1. **Tipo de processo:**
   - Civil — cumprimento de sentenca contra particular (CPC 525)
   - Civil — cumprimento de sentenca contra Fazenda Publica (CPC 535)
   - Trabalhista — manifestacao sobre calculo na liquidacao (CLT 879 §2º)
   - Trabalhista — embargos a execucao apos garantia do juizo (CLT 884)
2. **Data da intimacao** (publicacao no diario oficial, ciencia
   pessoal, push do PJe, etc.)
3. **Forma de intimacao** (publicacao DJE / pessoal / eletronica) —
   afeta termo inicial em algumas hipoteses
4. **Tribunal** (afeta feriados locais)
5. **UF + Cidade** (afeta feriados municipais/estaduais)
6. **Houve intimacao na Justica do Trabalho via Domicilio Judicial
   Eletronico (DJEN)?** (CLT 9.1 — afeta contagem)

---

## 3. PROCESSAMENTO

### Passo 1 — Identificar regra de contagem por rito

| Rito | Prazo | Tipo dias | Base legal |
|------|-------|-----------|------------|
| CPC 525 (impugnacao cumprimento civel) | 15 | UTEIS | CPC 219 |
| CPC 535 (impugnacao Fazenda Publica) | 30 | UTEIS | CPC 219 |
| CPC 1.003 §5º (apelacao) | 15 | UTEIS | CPC 219 |
| CLT 879 §2º (manifestacao liquidacao) | 8 | CORRIDOS | CLT 775 §1º |
| CLT 884 (embargos execucao trabalhista) | 5 | CORRIDOS | CLT 775 §1º |
| Recurso Inominado JEC (Lei 9.099 art. 42) | 10 | CORRIDOS | Lei 9.099 art. 12-A |

⚠️ **REGRA DURA CLT 775 §1º (Reforma 13.467/17):** apesar da Reforma
ter introduzido dias UTEIS em algumas hipoteses (recurso ordinario),
os prazos do CPC 879 §2º e 884 permanecem em CORRIDOS — controversia
pacificada pela IN 39 TST e pela jurisprudencia firme do TST.

### Passo 2 — Aplicar termo inicial (CPC 224)

```
data_intimacao = input do advogado
termo_inicial = primeiro dia util seguinte a intimacao
```

CPC 224 §1º:
> "Os dias do comeco e do vencimento do prazo serao protraidos para o
> primeiro dia util seguinte, se coincidirem com dia em que NAO houver
> expediente forense."

CPC 231 — formas de contagem do termo:
- Publicacao DJE: conta-se da publicacao + 1 dia (Sum. 21 TJSP, Sum. 16
  STJ — conferir pratica local)
- Intimacao pessoal/eletronica com prazo proprio: conta da ciencia

### Passo 3 — Identificar feriados aplicaveis

⚠️ **REGRA DURA:** NAO presumir feriados — exigir confirmacao do
calendario do tribunal. Esta skill marca feriados nacionais conhecidos
+ recesso (20/12 a 20/01) e PEDE ao advogado os feriados locais.

**Feriados nacionais 2026 (conhecidos por padrao):**
- 01/01 — Confraternizacao
- 16-17/02 (segunda+terca de carnaval) — facultativo (suspenso na
  pratica forense)
- 18/02 — Quarta de cinzas (expediente reduzido ate 12h, muitos
  tribunais suspendem)
- 03/04 — Sexta-feira Santa
- 21/04 — Tiradentes
- 01/05 — Dia do Trabalho
- 04/06 — Corpus Christi (facultativo, suspenso em geral)
- 07/09 — Independencia
- 12/10 — N.S. Aparecida
- 02/11 — Finados
- 15/11 — Proclamacao da Republica
- 25/12 — Natal

**Recesso CPC 220** — suspende prazos de 20/12 a 20/jan (NAO conta
nenhum dia neste periodo em processo civel; trabalhista NAO suspende
salvo periodo de portaria do TST).

### Passo 4 — Contar prazo

Algoritmo simplificado:
```python
prazo_restante = N  # 5, 8, 15 ou 30 conforme rito
data_atual = termo_inicial
dias_decorridos = 0

while prazo_restante > 0:
    if tipo_dias == "UTEIS":
        if eh_dia_util(data_atual) and not eh_feriado(data_atual):
            prazo_restante -= 1
    elif tipo_dias == "CORRIDOS":
        prazo_restante -= 1
        # mas a data final, se cair em feriado/fds, vai pro proximo util
    data_atual += 1 dia
    dias_decorridos += 1

# CPC 224 §1º — se data final cair em feriado, vai pro proximo util
data_limite = primeiro_dia_util_seguinte(data_atual)
```

### Passo 5 — Avaliar urgencia

| Dias uteis restantes | Status |
|----------------------|--------|
| > 5 | ✅ NORMAL — protocolo com folga |
| 3 a 5 | ⚠️ ATENCAO — agendar protocolo |
| 1 a 2 | 🟠 URGENTE — preparar protocolo hoje |
| 0 ou negativo | 🛑 INTEMPESTIVO — prazo perdido (avaliar tese de tempestividade) |

---

## 4. OUTPUT — RELATORIO ESTRUTURADO

```markdown
## Gestao de Prazo — Impugnacao a Calculo

### Premissas

| Campo | Valor |
|-------|-------|
| Tipo rito | [CPC 525 / CPC 535 / CLT 879 §2º / CLT 884] |
| Prazo legal | [N dias UTEIS/CORRIDOS] |
| Data da intimacao | [DD/MM/AAAA] |
| Forma intimacao | [DJE / pessoal / eletronica DJEN] |
| Tribunal | [identificacao] |
| Foro/Comarca | [UF + Cidade] |
| Termo inicial (1º dia util seguinte) | [DD/MM/AAAA] |

### Calendario aplicado

**Feriados nacionais considerados:** [lista]
**Feriados locais (a confirmar pelo advogado):** [lista — pedir]
**Recesso CPC 220 incidente?** [sim 20/12-20/01 / nao]

### Calculo

| Data | Dia da semana | Tipo | Conta? | Acumulado |
|------|---------------|------|--------|-----------|
| [data] | [dia] | util / feriado / fds | sim/nao | N/N |
| ... | ... | ... | ... | ... |
| [data limite] | [dia] | util | SIM | N/N |

### Veredito

✅ **DATA LIMITE: [DD/MM/AAAA] — [dia da semana]**

**Dias uteis restantes:** [N]
**Status:** [✅ NORMAL / ⚠️ ATENCAO / 🟠 URGENTE / 🛑 INTEMPESTIVO]

**Recomendacao de protocolo:** ate [DD/MM/AAAA] (folga de 2 dias
uteis) para evitar imprevistos com sistema PJe/eproc/etc.
```

---

## 5. AVISOS OBRIGATORIOS NO OUTPUT FINAL

```
⚠️ VALIDACAO ANTES DE CONFIAR NO PRAZO:

1. CONFIRMAR INTIMACAO no proprio sistema (PJe/eproc/Projudi) — nao
   substitui consulta aos autos.

2. CONFIRMAR FERIADOS LOCAIS — skill conhece so nacionais + recesso
   CPC 220. Municipais e do tribunal (padroeira, dia do funcionario,
   etc.) DEVEM ser conferidos no calendario oficial.

3. CPC 219 = UTEIS (civil). CLT 775 §1º = CORRIDOS na maior parte
   (IN 39 TST). NAO confundir os dois sistemas.

4. DJEN (Res. 234 CNJ) — 10 dias corridos para visualizacao + prazo
   legal a partir da visualizacao (ou expiracao). Alterou contagem
   de prazos eletronicos.

5. RECESSO CPC 220 — suspende prazos 20/12 a 20/01 NO CIVEL. NAO se
   aplica automaticamente ao trabalhista (portaria TST/TRT).

6. CARNAVAL/CORPUS CHRISTI — facultativos por lei, suspensos por
   portaria do tribunal na pratica. Confirmar.

7. INTEMPESTIVIDADE — se ja perdido, avaliar: CPC 223 (vicio de
   intimacao, nome errado), CPC 282 (preclusao afastavel por
   impedimento — doenca, falha PJe), embargos declaracao infringentes
   (raro).

8. PROTOCOLO PJE/EPROC — sistemas podem cair nos ultimos dias.
   Provimento CNJ admite ate 24h do ultimo dia via email/fisico
   (excecional).
```

---

## 6. FUNDAMENTACAO LEGAL

- **CPC art. 219** — dias UTEIS no processo civil
- **CPC art. 220** — recesso forense 20/12 a 20/01
- **CPC art. 224** — 1º util seguinte; vencimento prorroga
- **CPC art. 231** — formas de contagem do termo inicial
- **CPC art. 525** — impugnacao cumprimento civel: 15 uteis apos 15
  para pagamento espontaneo
- **CPC art. 535** — impugnacao Fazenda: 30 uteis
- **CPC art. 1.003 §5º** — recursos em geral: 15 uteis
- **CLT art. 775 §1º** (Reforma 13.467/17) — uteis SO em recursos;
  demais prazos da execucao seguem CORRIDOS (TST firme)
- **CLT art. 879 §2º** — manifestacao liquidacao: 8 corridos
- **CLT art. 884** — embargos execucao apos garantia: 5 corridos
- **Lei 9.099/95 art. 42** — inominado JEC: 10 corridos
- **Res. 234 CNJ** — Domicilio Judicial Eletronico (DJEN)
- **IN 39/2016 TST** — prazos pos-Reforma
- **Sum. 21 TJSP / Sum. 16 STJ** — contagem publicacao DJE

---

## 7. INTEGRACAO

- **Upstream:** `calculos-master` (advogado pergunta "qual e o prazo")
- **Downstream:** se status 🟠/🛑 → sugere skill de geracao de
  impugnacao (em outro plugin)
- **Sugestao de plugin-irmao:**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Gerar impugnacao ao calculo (CPC 525) | /execucao impugnacao-cumprimento | execucao-adv-os |
| Gerar embargos a execucao trabalhista (CLT 884) | /trabalhista embargos-execucao | trabalhista-adv-os |
| Gerar manifestacao sobre laudo (CLT 879 §2º) | /trabalhista manifestacao-liquidacao | trabalhista-adv-os |
| Comparar calculo do exequente com o seu | /calculos comparador-calculos | (interno) |
| Auditar calculo proprio antes de impugnar | /calculos protocolo-p4 | (interno) |

> Se plugin nao instalado, copiar este relatorio de prazo e protocolar manualmente.
```

---

## 8. PROIBICOES

1. **NUNCA confundir CPC 219 (uteis) com CLT 775 §1º (corridos na
   execucao)** — erro comum gera intempestividade.
2. **NUNCA presumir feriados locais** — sempre pedir confirmacao do
   calendario do tribunal.
3. **NUNCA aplicar recesso CPC 220 automaticamente em trabalhista** —
   depende de portaria.
4. **NUNCA dar resposta unica para "qual o prazo"** sem identificar o
   rito especifico (CPC 525 vs 535 vs CLT 879 §2º vs CLT 884 — todos
   diferentes).
5. **NUNCA omitir alerta de urgencia** quando prazo < 3 dias uteis.
6. **NUNCA esquecer da regra do DJEN (Res. 234 CNJ)** — 10 dias
   corridos para visualizacao + prazo legal apos.
