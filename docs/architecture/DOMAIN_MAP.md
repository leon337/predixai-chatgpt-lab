# Mapa de domínios

| Domínio | Responsabilidade | Dados principais |
|---|---|---|
| Identity | contas, sessões e papéis | User, Role, Membership |
| Curriculum | estrutura de aprendizagem | Track, Campaign, World, Module, Competency |
| Missions | contrato e execução pedagógica | Mission, MissionStep, MissionResource |
| Learning | tentativas, domínio e progresso | Attempt, Progress, Mastery |
| Assessment | rubricas, notas e feedback | Rubric, Criterion, Assessment |
| Evidence | referências e ciclo de vida | Evidence, EvidenceReview |
| Gamification | XP, medalhas e desbloqueios | XPTransaction, Badge, Unlock |
| Retention | revisões e remediação | RetentionReview, RemediationPlan |
| Prompts | catálogo e validações | Prompt, PromptVersion, PromptRun |
| Skills | pacotes e superfícies | Skill, SkillVersion, SkillValidation |
| Integrations | adaptadores externos | Integration, Connection, SyncJob |
| Governance | decisões e transições | Decision, Transition, ReviewGate |
| Audit | eventos imutáveis | AuditEvent |
| Publication | conteúdo liberado | Release, Publication |
| Operations | configurações e saúde | FeatureFlag, Job, HealthCheck |
| Privacy | consentimento e retenção | Consent, RetentionPolicy, DeletionRequest |

Domínios comunicam-se por contratos; nenhum pode escrever diretamente nas tabelas internas de outro domínio.
