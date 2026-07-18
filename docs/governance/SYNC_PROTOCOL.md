# Protocolo de sincronização GitHub + Linear

## Princípio

Os sistemas são complementares. Não duplicar a mesma autoridade.

## Estados

```text
SYNC_PENDING_GITHUB
SYNC_PENDING_LINEAR
SYNC_PARTIAL
SYNC_PASS
SYNC_FAIL
```

## Contrato

Cada sincronização possui `sync_id`, `transition_id`, origem, destino, recurso, versão esperada e chave de idempotência.

Em falha parcial:

```text
TRANSITION_STATUS=PARTIAL
STATE_REVISION=UNCHANGED
TRANSITION_ID=UNCHANGED
AUTOMATIC_ADVANCE=NO
```

A conclusão exige confirmação independente do GitHub e do Linear. PR aberto não implica issue em andamento; issue concluída não implica PR integrado.
