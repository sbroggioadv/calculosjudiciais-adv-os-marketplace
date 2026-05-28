---
name: calculo-aposentadoria-especial
description: >
  CALCULO-APOSENTADORIA-ESPECIAL — Calcula tempo de aposentadoria
  especial (atividade insalubre/perigosa/penosa — 15/20/25 anos
  conforme grau) e conversao tempo especial em tempo comum. Fatores:
  1,40 (homem — 25 especial → 35 comum) e 1,20 (mulher — 20 especial
  → 24 comum). Lei 8.213/91 art. 57-58 + Decreto 3.048/99 anexo IV.
  CONVERSAO VEDADA a partir de 13/11/2019 (EC 103/2019 art. 25 §2º +
  Tema 942 STF + 709 STF — preservado direito adquirido). Comprovacao:
  PPP + LTCAT. Use quando o advogado precisar contar tempo especial,
  simular conversao, avaliar viabilidade de aposentadoria especial OU
  preparar acao de revisao por tempo especial nao reconhecido pelo
  INSS.
---

# CALCULO-APOSENTADORIA-ESPECIAL — Conversao e Contagem Tempo Especial

## 1. ESCOPO

Calcula **tempo de aposentadoria especial** (Lei 8.213/91 art. 57-58)
e **conversao para tempo comum** (em direito adquirido pre-EC 103).
Produz:

- Tempo especial reconhecido (anos/meses/dias) por periodo + agente
- Conversao para tempo comum (fator 1,40 H / 1,20 M)
- Tempo total apos conversao (especial convertido + comum + outros)
- Viabilidade da aposentadoria especial pura (15/20/25 anos + carencia)
- Documentos necessarios para comprovacao
- Alerta sobre vedacao pos-13/11/2019 (EC 103/2019)

NAO calcula: RMI (vide `calculo-rmi-beneficio`), atrasados (vide
`calculo-atrasados-inss`), insalubridade/periculosidade trabalhista.

---

## 2. INPUT NECESSARIO

Perguntar (ou extrair):

1. **Sexo** do segurado (H/M)
2. **Periodos de atividade especial:** inicio + fim, empresa,
   atividade (CBO), agente nocivo principal, tipo de exposicao
3. **Documento comprobatorio:** PPP (obrigatorio pos-01/01/2004 — Lei
   9.732/98), LTCAT, SB-40/DSS-8030 (formularios antigos), auto de
   inspecao / laudo pericial
4. **Grau de risco** (define qtd anos):
   - **15 anos:** mineracao de subsolo (frente de trabalho)
   - **20 anos:** alguns agentes (amianto, asbesto)
   - **25 anos:** regra geral (ruido, calor, quimicos, etc.)
5. **DIB pretendida** (DD/MM/AAAA) — para checar pre/pos EC 103
6. **Tempo comum tambem contribuido** (anos/meses)
7. **Atividade desempenhada apos 13/11/2019?** (vedacao parcial)

---

## 3. PROCESSAMENTO

### 3.1 Contar tempo especial por periodo

```
Para CADA periodo:
  dias = data_fim - data_inicio + 1
  anos = dias / 365,25  (considera bissextos)
```

### 3.2 Validar enquadramento como especial

| Periodo | Regra de enquadramento |
|---------|------------------------|
| Ate 28/04/1995 | Categoria profissional (Decreto 53.831/64 + 83.080/79) — CBO basta |
| 29/04/1995 a 05/03/1997 | Formulario (SB-40 / DSS-8030) — agente nocivo descrito |
| 06/03/1997 a 31/12/2003 | Formulario + laudo tecnico LTCAT |
| Pos 01/01/2004 | **PPP obrigatorio** (Lei 9.732/98 + IN INSS) |

### 3.3 Conversao tempo especial → comum (Lei 8.213 art. 57 §5º)

**FATORES (Decreto 3.048/99 anexo IV):**

| Sexo | Atividade-base | Fator |
|------|----------------|-------|
| Homem | 15 anos = 35 comum | **2,33** |
| Homem | 20 anos = 35 comum | **1,75** |
| Homem | 25 anos = 35 comum | **1,40** |
| Mulher | 15 anos = 30 comum | **2,00** |
| Mulher | 20 anos = 30 comum | **1,50** |
| Mulher | 25 anos = 30 comum | **1,20** |

```
tempo_convertido = tempo_especial × fator
```

Exemplo: homem com 10 anos em atividade de 25 → 10 × 1,40 =
**14 anos** de tempo comum.

### 3.4 ⚠️ VEDACAO POS-EC 103/2019

**Tempo especial exercido a partir de 13/11/2019 NAO converte em
tempo comum** (EC 103/2019 art. 25 §2º).

Pode apenas contar para:
- Aposentadoria especial pura (15/20/25 anos especificamente)
- Comprovacao de tempo total para regras de transicao

**Tema 942 STF (2021):** confirmou vedacao da conversao pos-EC.
**Tema 709 STF (2020):** vedou enquadramento por categoria sem
exposicao efetiva — cada periodo precisa comprovar agente nocivo.

### 3.5 Aposentadoria especial pura (sem conversao)

Requisitos:
- 15 / 20 / 25 anos efetivos especiais conforme grau
- **+ Carencia: 180 contribuicoes** (Lei 8.213/91 art. 25 II)
- **+ Pos-EC 103:** idade minima 55 (15) / 58 (20) / 60 (25) quando
  aplicavel regra de transicao

### 3.6 Apuracao total apos conversao

```
TEMPO TOTAL = (tempo_especial_pre_EC × fator) + tempo_especial_pos_EC + tempo_comum

ATENCAO:
- pre-EC: converte (multiplica pelo fator)
- pos-EC (13/11/2019+): NAO converte — soma como simples
- comum: soma direto
```

---

## 4. OUTPUT — Memoria de Calculo

```markdown
## Memoria de calculo — aposentadoria especial / conversao

**Segurado:** [nome em runtime]
**Sexo:** [H/M]
**DIB pretendida:** [DD/MM/AAAA]

---

### Tabela 1 — Periodos de atividade especial

| Periodo | Empresa | Agente | Atividade | Documento | Tempo |
|---------|---------|--------|-----------|-----|-------|
| [ini - fim] | [nome] | [agente] | [CBO] | PPP/LTCAT | ___ a ___ m ___ d |
| [ini - fim] | [nome] | [agente] | [CBO] | PPP | ___ a ___ m ___ d |
| **TOTAL ESPECIAL** | | | | | **___ a ___ m ___ d** |

---

### Tabela 2 — Conversao especial → comum (apenas PRE-EC 103)

| Periodo | Tempo especial | Sexo | Atividade-base | Fator | Tempo convertido |
|---------|----------------|------|----------------|-------|------------------|
| [pre 13/11/19] | ___ anos | H | 25 anos | 1,40 | ___ anos |
| [pre 13/11/19] | ___ anos | M | 25 anos | 1,20 | ___ anos |
| **TOTAL convertido** | | | | | **___ anos** |

⚠️ **Tempo especial pos-13/11/2019 = ___ anos** (NAO converte — soma como simples)

---

### Tabela 3 — Tempo total computado

| Origem | Tempo (a/m) |
|--------|-------------|
| Tempo especial PRE-EC × fator | ___ |
| Tempo especial POS-EC (sem conversao) | ___ |
| Tempo comum | ___ |
| **TOTAL** | **___** |

---

### Viabilidade de beneficios

**Aposentadoria especial pura:**

| Requisito | Tem? |
|-----------|------|
| Tempo especial >= 15/20/25 | [SIM/NAO — ___ anos] |
| Carencia 180 contribuicoes | [SIM/NAO — ___] |
| Idade minima (pos-EC: 55/58/60) | [SIM/NAO — ___ anos] |

**Aposentadoria por tempo (apos conversao — so direito adquirido em
13/11/2019):**

| Requisito | Tem? |
|-----------|------|
| Tempo total 35 H / 30 M | [SIM/NAO — ___ anos] |
| Pre-Reforma | [SIM direito adquirido / NAO — usar transicao] |

---

### Documentos exigidos pelo INSS por periodo

| Periodo | Documento |
|---------|-----------|
| Ate 28/04/1995 | Categoria CBO + carteira de trabalho |
| 29/04/1995 a 05/03/1997 | Formulario SB-40 / DSS-8030 |
| 06/03/1997 a 31/12/2003 | Formulario + LTCAT |
| Pos 01/01/2004 | **PPP obrigatorio** |
```

---

## 5. FUNDAMENTACAO LEGAL

| Norma | Cobertura |
|-------|-----------|
| Lei 8.213/91 art. 57 | Aposentadoria especial 15/20/25 |
| Lei 8.213/91 art. 57 §5º | Conversao especial → comum |
| Lei 8.213/91 art. 58 | Carencia 180 contribuicoes |
| Lei 9.732/98 | PPP obrigatorio pos-01/01/2004 |
| Decreto 3.048/99 anexo IV | Agentes nocivos + fatores |
| Decreto 53.831/64 + 83.080/79 | Tabelas antigas (ate 28/04/1995) |
| EC 103/2019 art. 25 §2º | VEDACAO conversao pos-13/11/2019 |
| Tema 709 STF | Vedacao enquadramento sem exposicao efetiva |
| Tema 942 STF | Confirma vedacao conversao pos-EC |
| Tema 174 TNU | Ruido — limite 85 dB |
| Tema 555 STJ | EPI nao descaracteriza especial para ruido |
| Sum. 09 TNU | EPI nao impede reconhecimento para ruido |
| Sum. 32 TNU | LTCAT extemporaneo serve se ratifica condicoes |

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. CONVERSAO VEDADA pos-13/11/2019 (EC 103 art. 25 §2º + Tema 942
   STF). Periodos exercidos a partir dessa data NAO convertem —
   somam apenas como tempo simples.

2. Direito adquirido em 13/11/2019: cliente com 35/30 anos completos
   via conversao ANTES da EC mantem direito (acao judicial via
   revisao).

3. PPP eh OBRIGATORIO pos-01/01/2004 (Lei 9.732/98). Periodos
   anteriores aceitam SB-40/DSS-8030 + LTCAT.

4. Tema 709 STF: cada periodo precisa COMPROVAR exposicao EFETIVA.
   Enquadramento por mera categoria CBO so vale ate 28/04/1995.

5. Ruido: limite 85 dB (Tema 174 TNU). EPI NAO descaracteriza
   ruido (Sum. 09 TNU + Tema 555 STJ). Outros agentes: depende de
   neutralizacao efetiva.

6. Carencia: 180 contribuicoes (Lei 8.213 art. 25 II). Pode ser
   atendida com combinacao especial + comum.

7. LTCAT pode ser EXTEMPORANEO (Sum. 32 TNU): produzido apos o
   periodo mas valido se ratificar condicoes do periodo.

8. Atividades de risco: enquadramento depende da norma vigente AO
   TEMPO da prestacao (tempus regit actum).
```

---

## 7. INTEGRACAO

**Upstream:** `classificar-tipo-calculo` → "previdenciario / especial"
→ chama esta skill.

**Downstream:**
- `calculo-rmi-beneficio` (calcula RMI com tempo apurado)
- `calculo-atrasados-inss` (se acao judicial com atrasados)
- `protocolo-p4-calculos` (auditoria R1-R4)

**Cross-link (sugestao soft):**

```markdown
## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin |
|---|---|---|
| Acao reconhecimento tempo especial | /previdenciario peticao-reconhecimento-especial | previdenciario-adv-os |
| Calculo atrasados c/ tempo reconhecido | /calculos atrasados-inss | calculosjudiciais-adv-os |
| Pedido administrativo revisao INSS | /previdenciario revisao-administrativa-INSS | previdenciario-adv-os |
```

---

## 8. PROIBICOES

1. **NUNCA** converter tempo especial exercido pos-13/11/2019
   (EC 103 art. 25 §2º + Tema 942 STF).
2. **NUNCA** enquadrar como especial periodo pos-28/04/1995 sem
   formulario + comprovacao do agente nocivo.
3. **NUNCA** enquadrar como especial periodo pos-01/01/2004 sem PPP.
4. **NUNCA** afirmar que EPI descaracteriza ruido (Sum. 09 TNU).
5. **NUNCA** usar fator de conversao errado — Decreto 3.048/99 anexo
   IV define fatores por sexo e tempo-base.
6. **NUNCA** prometer aposentadoria especial sem checar carencia
   (180 contribuicoes — Lei 8.213 art. 25 II).
7. **NUNCA** ignorar idade minima pos-EC 103 (55/58/60).
8. **NUNCA** confundir RGPS (Lei 8.213) com RPPS (servidor —
   LC 51/85 e normas proprias).
