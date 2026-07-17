# Contratos entre módulos

## Objetos de valor compartilhados

```text
StableId
SemanticVersion
Slug
LifecycleStatus
SensitivityLevel
ExecutionSurface
CapabilityStatus
ActorRef
ResourceRef
EvidenceRef
CorrelationId
CausationId
AuditMetadata
```

## Envelope de comando

```yaml
command_id: CMD-000001
command_type: string
actor_id: USR-0001
correlation_id: UUID
causation_id: UUID|null
issued_at: ISO-8601
expected_version: integer|null
payload: object
```

## Envelope de evento

```yaml
event_id: EVT-000001
event_type: string
aggregate_id: string
aggregate_version: integer
actor_id: string
correlation_id: UUID
causation_id: UUID|null
occurred_at: ISO-8601
sensitivity: INTERNAL
payload: object
```

## Contratos críticos

- `MissionPublished` habilita a missão, mas não cria progresso;
- `AttemptSubmitted` congela a entrega avaliada;
- `AssessmentCompleted` produz nota e achados, mas não XP diretamente;
- `MasteryConfirmed` autoriza XP e desbloqueios;
- `EvidenceAccepted` referencia o artefato sem copiar conteúdo sensível;
- `PromptValidated` exige conjunto de execuções e revisão;
- `SkillPromoted` exige validações por superfície;
- `TransitionCompleted` exige sincronização idempotente.

Operações multi-domínio usam outbox transacional quando houver banco de produção. No ledger do piloto, a mesma transação SQLite registra estado e evento.
