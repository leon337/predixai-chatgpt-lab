# Modelo de dados

## Estratégia

- piloto: SQLite privado;
- MVP: PostgreSQL;
- conteúdo curricular: arquivos versionados no GitHub e importados por ID/versão;
- evidências binárias: object storage privado;
- metadados e progresso: banco acadêmico;
- auditoria: tabela append-only e exportação periódica.

## Entidades por domínio canônico

### Identity

`users`, `roles`, `user_roles`, `sessions`, `memberships`.

### Curriculum

`tracks`, `campaigns`, `worlds`, `modules`, `competencies`, `module_competencies`.

### Missions

`missions`, `mission_versions`, `mission_steps`, `mission_prerequisites`, `mission_resources`, `mission_competencies`.

### Learning

`enrollments`, `attempts`, `attempt_step_states`, `mastery_records`, `progress_snapshots`.

### Assessment

`rubrics`, `rubric_criteria`, `assessments`, `criterion_scores`, `feedback_items`.

### Evidence

`evidence_records`, `evidence_files`, `evidence_reviews`.

O domínio Evidence administra somente metadados, arquivos e revisões. Solicitações de exclusão pertencem ao domínio Privacy.

### Gamification

`xp_ledger`, `badges`, `badge_awards`, `unlock_rules`, `unlock_events`.

### Retention

`retention_reviews`, `remediation_plans`, `retention_schedules`.

### Prompts

`prompts`, `prompt_versions`, `prompt_runs`, `prompt_evaluations`.

### Skills

`skills`, `skill_versions`, `skill_validations`, `surface_adapters`.

### Integrations

`integration_connections`, `integration_grants`, `sync_jobs`, `integration_receipts`, `outbox_events`.

### Governance

`decisions`, `transitions`, `review_gates`, `authorization_grants`.

### Audit

`audit_events`, `audit_exports`, `audit_checkpoints`.

### Publication

`publications`, `releases`, `catalog_entries`, `publication_reviews`.

### Operations

`feature_flags`, `background_jobs`, `health_checks`, `runtime_configurations`.

### Privacy

`consents`, `retention_policies`, `deletion_requests`, `privacy_reviews`.

Privacy é a única autoridade para criar, alterar ou concluir consentimentos, políticas de retenção e solicitações de exclusão. Identity, Evidence e demais domínios apenas referenciam esses registros por ID estável ou solicitam operações por contrato.

## Invariantes

- IDs públicos são únicos e imutáveis;
- versões publicadas não são editadas;
- XP é ledger, nunca contador editável sem evento compensatório;
- conteúdo de evidência proibida não é persistido;
- tentativa avaliada referencia versão exata da missão e rubrica;
- exclusão de arquivo preserva somente metadados mínimos legalmente necessários;
- consentimento, retenção e exclusão são governados exclusivamente por Privacy;
- nenhum domínio escreve diretamente em tabelas pertencentes a outro domínio;
- estado derivado pode ser reconstruído a partir de fatos e versões.
