# Modelo de dados

## Estratégia

- piloto: SQLite privado;
- MVP: PostgreSQL;
- conteúdo curricular: arquivos versionados no GitHub e importados por ID/versão;
- evidências binárias: object storage privado;
- metadados e progresso: banco acadêmico;
- auditoria: tabela append-only e exportação periódica.

## Entidades centrais

### Identidade

`users`, `roles`, `user_roles`, `sessions`, `consents`.

### Currículo

`tracks`, `campaigns`, `worlds`, `modules`, `competencies`, `module_competencies`.

### Missões

`missions`, `mission_versions`, `mission_steps`, `mission_prerequisites`, `mission_resources`, `mission_competencies`.

### Aprendizagem

`enrollments`, `attempts`, `attempt_step_states`, `mastery_records`, `progress_snapshots`, `remediation_plans`, `retention_reviews`.

### Avaliação

`rubrics`, `rubric_criteria`, `assessments`, `criterion_scores`, `feedback_items`.

### Evidências

`evidence_records`, `evidence_files`, `evidence_reviews`, `deletion_requests`.

### Gamificação

`xp_ledger`, `badges`, `badge_awards`, `unlock_rules`, `unlock_events`.

### Prompts e Skills

`prompts`, `prompt_versions`, `prompt_runs`, `prompt_evaluations`, `skills`, `skill_versions`, `skill_validations`, `surface_adapters`.

### Governança e integração

`decisions`, `transitions`, `review_gates`, `integration_connections`, `sync_jobs`, `audit_events`, `outbox_events`.

## Invariantes

- IDs públicos são únicos e imutáveis;
- versões publicadas não são editadas;
- XP é ledger, nunca contador editável sem evento compensatório;
- evidência proibida não possui registro persistente;
- tentativa avaliada referencia versão exata da missão e rubrica;
- exclusão de arquivo preserva somente metadados mínimos legalmente necessários;
- estado derivado pode ser reconstruído a partir de fatos e versões.
