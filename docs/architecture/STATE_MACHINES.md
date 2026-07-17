# Máquinas de estado

## Missão

`DRAFT → IN_REVIEW → PUBLISHED → DEPRECATED → ARCHIVED`.

## Tentativa

`CREATED → IN_PROGRESS → SUBMITTED → UNDER_REVIEW → REMEDIATION_REQUIRED|MASTERED|REJECTED`.

Uma tentativa submetida é imutável; correções criam nova tentativa relacionada.

## Evidência

`DECLARED → UPLOADED → SCANNING → AVAILABLE → ACCEPTED|REJECTED → RETENTION_EXPIRED → DELETED`.

`PROHIBITED` bloqueia antes do upload.

## Prompt

`DRAFT → IN_TESTING → VALIDATED → DEPRECATED → ARCHIVED`.

Novo conteúdo após validação cria nova versão e retorna a `IN_TESTING`.

## Skill

`EXPERIMENTAL → PILOT → VALIDATED → STABLE → DEPRECATED → ARCHIVED`.

Cada superfície possui estado de validação próprio.

## Transição de projeto

`NOT_STARTED → IN_PROGRESS → PARTIAL|BLOCKED|COMPLETE`.

`PARTIAL` mantém `transition_id` e não incrementa `state_revision`. `COMPLETE` incrementa uma vez.

## Revisão

`NOT_REQUESTED → REQUESTED → IN_PROGRESS → PASS|FAIL|STALE`.

Mudança no SHA revisado converte `PASS` em `STALE`.
