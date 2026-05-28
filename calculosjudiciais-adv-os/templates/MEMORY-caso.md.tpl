# MEMORY.md — Caso {{CLIENTE}} x {{ADVERSO}}

> Log evolutivo deste caso trabalhista. Persistente entre sessões do Claude Code.
> Vive em `<COWORK>/trabalhista/casos/{{CASO_SLUG}}/MEMORY.md`. Atualizado a cada etapa do pipeline.

---

## Identificação do Caso

- **Cliente (parte atendida):** {{CLIENTE}}
- **Parte adversa:** {{ADVERSO}}
- **Polo do cliente:** {{POLO}}  <!-- reclamante | reclamada -->
- **Vara / TRT:** {{ORGAO}}
- **Nº do processo:** {{NUMERO}}
- **Fase processual:** {{FASE}}

---

## Como Funciona

**Leitura automática:** o Claude lê este arquivo ao iniciar trabalho no caso. Usa o que encontra para retomar de onde parou.

**Escrita:** a skill `memoria-de-caso-trabalhista` registra aqui cada etapa concluída do pipeline (triagem, auditoria documental, trilateral, jurisprudência, linha estratégica, peça produzida, auditoria R1-R4). Anotações manuais do operador (pedidas com "lembre disso", "anote") também entram aqui.

**Compartimentação (PA-22):** este MEMORY.md cobre **apenas** este caso. Nunca misturar informação de outro caso aqui.

---

## Linha do Tempo do Caso

| Data | Etapa | Resultado / Observação |
|------|-------|------------------------|
| {{GENERATED_AT}} | Caso aberto | Polo: {{POLO}} · Fase: {{FASE}} |

---

## Decisões Estratégicas

*(Vazio. A `linha-estrategica-trabalhista` registra aqui a tese central e as subsidiárias após o Checkpoint 4.)*

---

## Pendências e Pontos de Omissão

*(Documentos essenciais faltantes, prazos a confirmar, dados a colher. Sinalizados pela auditoria documental e pela Suprema Corte R1.)*

---

## Peças Produzidas

*(Cada peça produzida e auditada é listada aqui com data e veredito R1-R4.)*

---

**Workspace:** `{{COWORK_PATH}}`
**Caso:** {{CLIENTE}} x {{ADVERSO}}
**Plugin:** `trabalhista-adv-os` v{{PLUGIN_VERSION}}
**Inicializado em:** {{GENERATED_AT}}
