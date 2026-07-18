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

## Validação em duas camadas

JSON Schema governa forma, tipos, enums, campos obrigatórios e condicionais estruturais. Invariantes que dependem da comparação entre coleções ou de cálculos derivados são obrigatoriamente validados por `scripts/contract_semantics.py`.

| Contrato | Invariante semântico executável |
|---|---|
| Assessment | pesos somam 1 e `total_score` corresponde à soma ponderada |
| Prompt `VALIDATED` | existem pelo menos três `variation_id` distintos e o resumo corresponde às execuções |
| Skill `STABLE` | existem três execuções variadas e todas as superfícies declaradas possuem validação `PASS` |
| Transition `COMPLETE` | `reviewed_head_sha` é exatamente igual ao `observed_pr_head` |

Uma instância somente é válida quando passa pelas duas camadas:

```text
CONTRACT_VALID = SCHEMA_PASS AND SEMANTIC_PASS
```

Campos de resumo são projeções derivadas, nunca autoridades independentes. Um consumidor não pode conceder domínio, XP, promoção, publicação ou conclusão de transição usando somente declarações autorreferentes do payload.

Operações multi-domínio usam outbox transacional quando houver banco de produção. No ledger do piloto, a mesma transação SQLite registra estado e evento.
