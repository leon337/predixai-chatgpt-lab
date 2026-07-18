# DEC-0011 — Governança GitHub + Linear

```yaml
id: DEC-0011
status: APPROVED_PROVISIONAL
version: 0.9.0
constitutional: true
final_retest_pending: true
```

## Regra central

GitHub e Linear são complementares e vinculados por IDs estáveis, sem duplicar fontes de verdade.

- `main`: código e documentação consolidados;
- PR ativo: trabalho não integrado;
- Linear: tarefas, dependências, responsáveis e bloqueios;
- manifesto: continuidade operacional estruturada;
- históricos: evidências, não instruções atuais;
- ChatGPT: contexto temporário.

## Fluxo

Reconstruir estado → validar pré-condições → planejar → executar escopo autorizado → testar → PR → revisão independente → autorização humana → merge → recibo pós-merge → sincronização Linear.

## Concorrência

Antes de escrever, consultar ao vivo `main`, PR head, `state_revision` e `transition_id`. Divergência bloqueia escrita e exige reconstrução.

## Gates

- escrita direta na `main` proibida após o bootstrap inicial;
- revisão vinculada ao SHA exato;
- novo commit invalida revisão anterior;
- threads bloqueantes precisam ser resolvidas;
- sincronização parcial mantém a mesma transição;
- merge e ações irreversíveis exigem autorização humana.

A ratificação final depende de reteste do modelo endurecido no projeto Robô de Listas.
