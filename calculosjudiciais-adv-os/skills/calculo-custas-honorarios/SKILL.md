---
name: calculo-custas-honorarios
description: >
  CALCULO-CUSTAS-HONORARIOS — Estrutura memoria de calculo de 3
  parcelas distintas: (1) custas processuais (tabela do TJ ou
  Justica Federal); (2) honorarios sucumbenciais (CPC art. 85 —
  10-20% sobre condenacao/proveito/valor da causa, com Tema 1.255
  STJ aplicavel a Fazenda); (3) honorarios contratuais (Lei
  8.906/94 art. 22-23, devidos ao advogado pelo cliente).
  Aborda sucumbencia reciproca (CPC 86) e beneficiario da
  justica gratuita (CPC 98 §3º — exigibilidade suspensa 5 anos).
  Use quando o advogado mencionar: "custas processuais",
  "honorarios sucumbenciais", "honorarios advocaticios",
  "honorarios contratuais", "fixacao de honorarios", "verba
  honoraria", "sucumbencia", "justica gratuita honorarios",
  "execucao de honorarios", "calculo Tema 1.255".
---

# CALCULO-CUSTAS-HONORARIOS — Memoria de Calculo Estruturada

## 1. ESCOPO

Calculo das 3 verbas pos-sentenca/transito:

- **Custas processuais:** tabela TJ ({{UF}}) ou JF; vencedor reembolsa do vencido (CPC 82 §2º).
- **Honorarios sucumbenciais (CPC 85):** 10-20% sobre condenacao/proveito/valor da causa. Fazenda = faixas escalonadas (§3º). Tema 1.255 STJ: precatorio segue natureza da obrigacao. Reciproca = rateio (CPC 86), vedada compensacao (§14).
- **Honorarios contratuais (Lei 8.906/94 art. 22-23):** advogado x cliente, contrato escrito, execucao autonoma (art. 24), credito proprio (Sum. 306 STJ).

---

## 2. INPUT NECESSARIO

Do contexto + perguntar:

1. **Verba(s):** custas / sucumbenciais / contratuais
2. **Tribunal:** TJ ({{UF}}) ou JF (regiao)
3. **Valor da causa atualizado**
4. **Condenacao OU proveito economico** (sucumbenciais)
5. **Sucumbencia reciproca?** Quanto cada parte ganhou
6. **Polo cliente:** vencedor / vencido / parcial
7. **Beneficiario justica gratuita?** (CPC 98)
8. **Fazenda e parte?** (CPC 85 §3º)
9. **Contratuais:** percentual + base (valor causa, ganho liquido, etc.)
10. **Sentenca ja fixou honorarios?** Qual percentual?

---

## 3. PROCESSAMENTO

1. Identificar verbas a calcular
2. CUSTAS: tabela TJ/JF (iniciais + intermediarias + finais), subtrair beneficios
3. SUCUMBENCIAIS: base (condenacao > proveito > valor causa), aplicar % da sentenca; se Fazenda, faixas escalonadas CPC 85 §3º
4. Reciproca: ratear proporcional (CPC 86), sem compensacao (§14)
5. Gratuita: exigibilidade suspensa 5 anos (CPC 98 §3º), executavel se cessar hipossuficiencia
6. CONTRATUAIS: aplicar clausula sobre base pactuada
7. Atualizar todas as verbas ate o termo final
8. Emitir aviso obrigatorio

---

## 4. OUTPUT — PLANILHA ESTRUTURADA

```markdown
## Memoria de calculo — Custas e Honorarios

**Atencao:** este calculo apresenta ESTRUTURA + FORMULA. Tabelas de
custas e indices de atualizacao devem ser consultados na FONTE
OFICIAL (site TJ {{UF}} / CJF). Esta skill NAO tem acesso a
tabelas/indices posteriores a Jan/2026.

### Premissas

| Campo | Valor |
|---|---|
| Processo | [numero CNJ] |
| Tribunal | [TJ {{UF}} / TRF X] |
| Valor da causa atualizado | R$ _____ |
| Valor da condenacao | R$ _____ |
| Proveito economico | R$ _____ |
| Polo cliente | autor / reu / 3o |
| Sucumbencia reciproca? | sim/nao (proporcao) |
| Beneficiario justica gratuita? | sim/nao |
| Fazenda Publica e parte? | sim/nao |
| Percentual honorarios fixado | [X%] (CPC 85) |
| Termo final do calculo | [data] |

---

### Parte 1 — CUSTAS PROCESSUAIS

| Etapa | Base de calculo | Aliquota | Valor |
|---|---|---|---|
| Custas iniciais (ajuizamento) | R$ _____ | _____ | R$ _____ |
| Custas intermediarias (diligencias) | _____ | _____ | R$ _____ |
| Custas finais (sentenca) | _____ | _____ | R$ _____ |
| Eventuais isencoes (CPC 98) | _____ | _____ | (R$ _____) |
| **TOTAL CUSTAS** | | | **R$ _____** |

**FONTE OBRIGATORIA:** consultar Tabela de Custas TJ {{UF}}
(site do tribunal) ou Lei de Custas da Justica Federal
(Lei 9.289/96 + Resolucoes CJF). Valores variam anualmente.

---

### Parte 2 — HONORARIOS SUCUMBENCIAIS (CPC art. 85)

**Base de calculo (ordem de preferencia CPC 85 §2º):**
1. Valor da condenacao (preferencial)
2. Proveito economico obtido (se sem condenacao)
3. Valor da causa atualizado (residual)

**Caso 1: parte privada x parte privada (CPC 85 §2º — 10% a 20%):**

honorarios = base × percentual_fixado_em_sentenca

| Base aplicada | Valor | Percentual | Honorarios |
|---|---|---|---|
| [condenacao/proveito/valor causa] | R$ _____ | [X%] | R$ _____ |

**Caso 2: Fazenda Publica e parte (CPC 85 §3º — faixas escalonadas):**

| Faixa do salario minimo (SM) | Aliquota |
|---|---|
| Ate 200 SM | 10% a 20% |
| 200 a 2.000 SM | 8% a 10% |
| 2.000 a 20.000 SM | 5% a 8% |
| 20.000 a 100.000 SM | 3% a 5% |
| Acima de 100.000 SM | 1% a 3% |

Calculo por faixas:
honorarios = (faixa_1 × aliquota_1) + (faixa_2 × aliquota_2) + ...

**FONTE OBRIGATORIA:** valor do salario minimo no ano da fixacao
(decreto federal anual).

**Sub-caso: sucumbencia reciproca (CPC 86):**
Rateio proporcional dos onus, VEDADA compensacao (CPC 85 §14).

| Parte | % ganho | Sucumbencia | Honorarios devidos a |
|---|---|---|---|
| Autor | [X%] | [100-X]% | adv. reu |
| Reu | [100-X]% | [X]% | adv. autor |

**Tema 1.255 STJ:** honorarios sucumbenciais em precatorio seguem
a natureza da obrigacao principal (alimentar ou nao). Verificar
quando o pagamento e via RPV/precatorio contra Fazenda.

**Atualizacao dos honorarios:** correcao monetaria desde o
arbitramento (Sum. 14 STJ — atualizacao desde a fixacao) + juros
de mora desde o transito em julgado.

---

### Parte 3 — HONORARIOS CONTRATUAIS (Lei 8.906/94)

**Base de calculo:** conforme contrato escrito entre advogado e
cliente. Comum: percentual sobre o ganho liquido do cliente OU
sobre o valor da condenacao.

| Base contratual | Valor | Percentual contratado | Honorarios |
|---|---|---|---|
| [definir] | R$ _____ | [X%] | R$ _____ |

**Titulo executivo:** contrato escrito firmado + sentenca
liquida (Lei 8.906 art. 24).

**Direito autonomo do advogado (Sum. 306 STJ + CPC 85 §14):**
honorarios contratuais e sucumbenciais sao verbas autonomas e
independentes, ambas devidas.

---

### Totalizacao

| Verba | Devedor | Beneficiario | Valor |
|---|---|---|---|
| Custas (reembolso) | [vencido] | [vencedor] | R$ _____ |
| Sucumbenciais | [vencido] | adv. do vencedor | R$ _____ |
| Contratuais | cliente | seu adv. | R$ _____ |
| **TOTAL** | | | **R$ _____** |

---

### Anexos obrigatorios

1. Esta memoria (planilha)
2. Sentenca/acordao com fixacao de honorarios
3. Tabela de custas vigente do TJ/JF
4. Contrato de honorarios (se contratual)
5. Decreto do salario minimo do ano (se Fazenda)
6. Comprovantes de pagamento das custas (se reembolso)
```

---

## 5. FUNDAMENTACAO LEGAL

- **CPC art. 82 §2º** — Vencido reembolsa custas do vencedor
- **CPC art. 85** — Sucumbenciais: 10% a 20% sobre condenacao/
  proveito/valor da causa
- **CPC art. 85 §3º** — Faixas escalonadas Fazenda Publica
- **CPC art. 85 §14** — Honorarios sucumbenciais sao verba autonoma,
  vedada compensacao
- **CPC art. 86** — Sucumbencia reciproca
- **CPC art. 98 §3º** — Beneficiario gratuita: exigibilidade suspensa
  5 anos (extincao se nao executado)
- **Lei 8.906/94 art. 22-23** — Honorarios advocaticios contratuais
- **Lei 8.906/94 art. 24** — Sentenca + contrato = titulo executivo
- **Sum. 14 STJ** — Atualizacao desde o arbitramento
- **Sum. 306 STJ** — Honorarios sucumbenciais e contratuais sao
  cumulaveis
- **Tema 1.255 STJ** — Honorarios em precatorio seguem natureza da
  obrigacao principal
- **Tema 1.076 STJ** — Forma de calculo dos honorarios escalonados
  contra Fazenda (faixa por faixa)

---

## 6. AVISOS OBRIGATORIOS NO OUTPUT

```
⚠️ VALIDACAO OBRIGATORIA ANTES DE PROTOCOLAR:

1. Conferir TABELA DE CUSTAS vigente do TJ {{UF}} / JF na fonte
   oficial. Tabelas variam anualmente. Esta skill NAO tem acesso
   a tabelas posteriores a Jan/2026.

2. Confirmar percentual de honorarios FIXADO em sentenca/acordao —
   nao recalcular fora dos limites estabelecidos.

3. Se Fazenda Publica e parte: calcular FAIXA POR FAIXA conforme
   CPC 85 §3º (Tema 1.076 STJ — nao aplicar aliquota unica a todo
   o valor).

4. Sucumbencia reciproca: VEDADA compensacao (CPC 85 §14). Cada
   parte paga ao advogado da outra o devido proporcional.

5. Beneficiario justica gratuita: exigibilidade suspensa 5 anos
   (CPC 98 §3º). Se nao executado, extingue. Pode ser executado
   se cessar a condicao de hipossuficiencia.

6. Honorarios contratuais sao devidos AO ADVOGADO (verba propria —
   Sum. 306 STJ) — nao ao cliente. Execucao autonoma.

7. Atualizar honorarios desde o ARBITRAMENTO (Sum. 14 STJ) + juros
   desde o transito.

8. Tema 1.255 STJ: em precatorio, honorarios seguem natureza da
   obrigacao principal — verificar antes de classificar como
   alimentar/comum.
```

---

## 7. INTEGRACAO

**Upstream:**
- `calculos-master` (orquestrador)
- `identificar-tj-aplicavel` (tabela correta de custas)
- `calculo-cumprimento-sentenca-civel` (frequente precede)

**Downstream:**
- `protocolo-p4-calculos` (auditoria Suprema Corte — auto)
- `gestao-prazo-impugnacao` (impugnacao do calculo de honorarios)

## 💡 Proximos passos opcionais

| Proximo passo | Comando | Plugin necessario |
|---|---|---|
| Execucao de honorarios advocaticios | `/execucao peticao-inicial-execucao` | `execucao-adv-os` (Kirvano) |
| Impugnacao a custas/honorarios | `/execucao embargos-execucao` | `execucao-adv-os` (Kirvano) |
| Auditoria final com IA | `/ia-combativa suprema-corte-r1-r4` | `ia-combativa-adv-os` (Kirvano) |
| Recurso para majorar honorarios (CPC 85 §11) | `/execucao apelacao` | `execucao-adv-os` (Kirvano) |

> Se plugin nao instalado, copiar memoria de calculo acima e usar manualmente.

---

## 8. PROIBICOES

1. **NUNCA aplicar aliquota unica** ao valor total quando Fazenda for
   parte — sempre faixas escalonadas (CPC 85 §3º + Tema 1.076 STJ).
2. **NUNCA compensar** sucumbenciais entre as partes (CPC 85 §14).
3. **NUNCA executar** beneficiario de gratuita sem comprovar
   superveniencia da capacidade (CPC 98 §3º).
4. **NUNCA citar tabela de custas hardcoded.** Sempre placeholder +
   fonte oficial.
5. **NUNCA recalcular** percentual de honorarios fora do fixado em
   sentenca — recurso proprio (apelacao/REsp).
6. **NUNCA omitir aviso de validacao final.**
