# Modelo de permissões

## Papéis

- `STUDENT`;
- `INSTRUCTOR`;
- `REVIEWER`;
- `CONTENT_CONTRIBUTOR`;
- `ADMIN`;
- `SYSTEM_SERVICE`.

## Princípio

RBAC define capacidade geral; ABAC aplica contexto, propriedade, sensibilidade, superfície e estado do recurso.

## Regras essenciais

- aluno lê conteúdo publicado e gerencia suas tentativas;
- instrutor cria conteúdo, mas não publica sozinho quando revisão for obrigatória;
- revisor avalia conteúdo ou tentativas sem alterar a evidência original;
- colaborador envia proposta por workflow de revisão;
- administrador gerencia usuários e políticas, mas ações sensíveis são auditadas;
- serviço opera somente com escopos mínimos e credenciais rotacionáveis.

## Grants de integração

Todo grant possui ator, ação, recurso, superfície, escopo, expiração e justificativa. Mudança de alvo ou ação invalida o grant. Produção, custo, publicação e ações irreversíveis exigem aprovação humana explícita.
