# Máquinas de estado

## Missão

`DRAFT → IN_REVIEW → PUBLISHED → DEPRECATED → ARCHIVED`.

## Tentativa

`CREATED → IN_PROGRESS → SUBMITTED → UNDER_REVIEW → REMEDIATION_REQUIRED|MASTERED|REJECTED`.

Uma tentativa submetida é imutável; correções criam nova tentativa relacionada.

## Evidência

Fluxo permitido:

```text
DECLARED
├── BLOCKED
└── UPLOADED → SCANNING → AVAILABLE → ACCEPTED|REJECTED
                                      └── RETENTION_EXPIRED → DELETED
```

Regras:

- `classification=PROHIBITED` produz `status=BLOCKED` antes de qualquer upload;
- `BLOCKED` não possui `storage_ref` nem `content_hash` de conteúdo;
- somente metadados sanitizados de bloqueio podem ser enviados ao Audit;
- `BLOCKED → DELETED` encerra qualquer registro transitório de intake;
- `REJECTED` não significa exclusão automática; a política de retenção continua sendo autoridade do domínio Privacy;
- conteúdo proibido nunca é persistido.

## Avaliação

`CREATED → CALCULATED → VALIDATED → PUBLISHED|INVALIDATED`.

Uma avaliação somente entra em `VALIDATED` quando a nota, as verificações eliminatórias e o resultado pertencem à mesma faixa acadêmica.

## Prompt

`DRAFT → IN_TESTING → VALIDATED → DEPRECATED → ARCHIVED`.

Novo conteúdo após validação cria nova versão e retorna a `IN_TESTING`. `VALIDATED` exige três execuções controladas variadas e revisão de segurança aprovada.

## Skill

`EXPERIMENTAL → PILOT → VALIDATED → STABLE → DEPRECATED → ARCHIVED`.

Cada superfície possui estado de validação próprio. `STABLE` exige três execuções variadas, revisão de segurança e validação de todas as superfícies declaradas.

## Transição de projeto

`NOT_STARTED → IN_PROGRESS → PARTIAL|BLOCKED|COMPLETE`.

`PARTIAL` mantém `transition_id` e não incrementa `state_revision`. `COMPLETE` incrementa uma vez e exige `gate_status=PASS`, GitHub e Linear sincronizados, zero bloqueadores e revisão ligada ao SHA exato.

## Revisão

`NOT_REQUESTED → REQUESTED → IN_PROGRESS → PASS|FAIL|STALE`.

Mudança no SHA revisado converte `PASS` em `STALE`.
