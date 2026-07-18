# Protocolo de transições

## Identidade

Toda mudança operacional usa `transition_id` único e `state_revision` monotônica.

## Fluxo

```text
NOT_STARTED
→ IN_PROGRESS
→ PARTIAL | BLOCKED | COMPLETE
```

## Regras

- `PARTIAL` preserva o mesmo `transition_id` e a mesma `state_revision`;
- retry é idempotente;
- nova missão é proibida durante sincronização parcial;
- `COMPLETE` incrementa a revisão uma única vez;
- ação baseada em snapshot obsoleto é bloqueada;
- merge não completa a transição sem recibo pós-merge;
- encerramento futuro nunca é registrado como fato.

## Pré-escrita

Comparar ao vivo:

```text
EXPECTED_MAIN_SHA == CURRENT_MAIN_SHA
EXPECTED_PR_HEAD == CURRENT_PR_HEAD
EXPECTED_STATE_REVISION == CURRENT_STATE_REVISION
EXPECTED_TRANSITION_ID == CURRENT_TRANSITION_ID
```

Falha produz `BLOCKED_BY_CONCURRENT_UPDATE` e exige reconstrução.
