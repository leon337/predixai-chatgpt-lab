# Protocolo de revisão

## Tipos

- auto-revisão do construtor: preliminar;
- revisão crítica independente: gate final quando exigido;
- revisão humana: autorização de merge e decisões de negócio.

## Vínculo

Toda revisão registra repositório, PR, SHA analisado, escopo, revisor, data, achados e resultado.

```text
CURRENT_PR_HEAD != REVIEWED_HEAD_SHA
→ REVIEW_STATUS=STALE
→ MERGE_AUTHORIZATION=BLOCKED
```

## Severidade

- `CRITICAL`: risco de segurança, perda de dados ou arquitetura inviável;
- `MAJOR`: contrato incorreto, schema incompatível ou requisito essencial ausente;
- `MINOR`: melhoria necessária sem bloquear objetivo principal.

## Resultado

`PASS`, `WARN`, `FAIL` ou `BLOCKED`. Especificação criada não equivale a runtime executado. Threads bloqueantes não podem permanecer abertas no merge.
