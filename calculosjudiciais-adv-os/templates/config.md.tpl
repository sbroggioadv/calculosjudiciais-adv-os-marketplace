# Configuração — trabalhista-adv-os

> Configuração operacional do plugin no ambiente do escritório. Vive em
> `<COWORK>/trabalhista/config.md`. Gerada pelo `/start-trabalhista`. Editável
> manualmente — mudanças valem na próxima sessão.

---

## Polos de atuação

- **Polos:** {{POLOS}}
  <!-- reclamante | reclamada | ambos -->

> Define para quais lados da Reclamação Trabalhista o escritório atua. A
> `triagem-trabalhista` confirma o polo caso a caso e grava no `CASO.md`.

---

## Especialidades

- **Especialidades:** {{ESPECIALIDADES}}
  <!-- ex: horas extras, insalubridade/periculosidade, vínculo, acidente de
       trabalho, rescisão indireta, execução, recursal, consultivo preventivo -->

---

## Tom de voz

- **Perfil:** {{TOM_VOZ_PERFIL}}
  <!-- tecnico-combativo | tecnico-cordial | tecnico-didatico | personalizado -->
- **Intensidade combativa:** {{TOM_VOZ_INTENSIDADE}}/10
- **Postura default:** {{POSTURA_DEFAULT}}

---

## Modo de fluxo

- **Modo:** {{MODO_FLUXO}}
  <!-- checkpoint (default) | continuo -->

> `checkpoint` — o pipeline para e confirma com o advogado ao fim de cada fase
> (4 checkpoints). `continuo` — entrega o pacote completo de uma vez, sem parar.

---

## Suprema Corte

- **Auditoria R1-R4:** {{SUPREMA_CORTE_STATUS}}
  <!-- ATIVA (default) | DESATIVADA -->
- Bypass por demanda: `--no-corte`, `--quick`, `/corte off`.

---

## Ferramentas declaradas

- **Ferramentas:** {{FERRAMENTAS}}
  <!-- sistema de gestão processual, transcrição, CRM, etc. — campos livres -->

---

**Plugin:** `trabalhista-adv-os` v{{PLUGIN_VERSION}}
**Gerado em:** {{GENERATED_AT}}
**State source:** `{{COWORK_PATH}}/trabalhista/cowork-state.json`
