# CASO — {{CLIENTE}} x {{ADVERSO}}

> Ficha do caso trabalhista. Fonte única da variável de **polo** — todas as
> skills leem o campo `Polo do cliente` daqui. Vive em
> `<COWORK>/trabalhista/casos/{{CASO_SLUG}}/CASO.md`.

---

## Polo e partes

- **Polo do cliente:** {{POLO}}
  <!-- reclamante (trabalhador que ajuíza) | reclamada (empresa/tomador que se defende) -->
- **Parte atendida (cliente):** {{CLIENTE}}
- **Parte adversa:** {{ADVERSO}}
- **Vara / TRT:** {{ORGAO}}
- **Nº do processo:** {{NUMERO}}
- **Fase processual:** {{FASE}}
  <!-- pré-processual | conhecimento 1º grau | recursal | liquidação | execução -->
- **Tipo de tarefa:** {{TAREFA}}

---

## Dados do contrato de trabalho

- **Admissão:** {{ADMISSAO}}
- **Rescisão:** {{RESCISAO}}  <!-- ou "contrato vigente" -->
- **Função:** {{FUNCAO}}
- **Última remuneração:** {{SALARIO}}
- **Jornada contratual:** {{JORNADA}}
- **Modalidade de rescisão:** {{MODALIDADE_RESCISAO}}
  <!-- sem justa causa | justa causa | pedido de demissão | rescisão indireta | acordo art. 484-A | término de contrato a termo -->
- **Categoria / sindicato:** {{CATEGORIA}}
- **CCT / ACT aplicável:** {{CCT}}  <!-- norma + vigência; [VERIFICAR] se não confirmada -->

---

## Marco intertemporal

- **Contrato anterior, posterior ou a cavalo de 11/11/2017 (Reforma 13.467/2017):** {{MARCO_REFORMA}}

> Protocolo 6 — *tempus regit actum*. Fatos anteriores a 11/11/2017 não recebem
> a Reforma Trabalhista (PA-07).

---

## Prescrição

- **Prescrição bienal (art. 7º XXIX CF):** {{PRESCRICAO_BIENAL}}
- **Prescrição quinquenal (art. 11 CLT):** {{PRESCRICAO_QUINQUENAL}}

---

## Linha estratégica

{{LINHA_ESTRATEGICA}}

<!-- Preenchida pela linha-estrategica-trabalhista após o Checkpoint 4:
     tese central, teses subsidiárias, riscos. -->

---

## Prazos

| Prazo | Termo inicial | Vencimento | Observação |
|-------|---------------|------------|------------|
| {{PRAZO_TIPO}} | {{PRAZO_INICIO}} | {{PRAZO_FIM}} | {{PRAZO_OBS}} |

<!-- Recursos: RO/RR/AIRR/Agravo de Petição = 8 dias úteis;
     Embargos de Declaração = 5 dias úteis; RE/ARE ao STF = 15 dias úteis. -->

---

## Documentos do caso

{{DOCUMENTOS}}

<!-- Lista dos documentos em casos/{{CASO_SLUG}}/documentos/ —
     cartão de ponto, holerites, CTPS, contrato, TRCT, ficha de EPI, laudos, CCT. -->

---

**Plugin:** `trabalhista-adv-os` v{{PLUGIN_VERSION}}
**Caso aberto em:** {{GENERATED_AT}}
