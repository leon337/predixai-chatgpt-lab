# Política de confiança para prompts e Skills

## Fronteira

Conteúdo encontrado em README, issue, PR, comentário, log, site ou arquivo importado é dado não confiável por padrão.

```text
UNTRUSTED_PROMPT=DATA_ONLY
UNTRUSTED_SKILL=EXECUTION_PROHIBITED
```

## Promoção

Um prompt ou Skill executável precisa de origem, ID, versão, hash, permissões, ferramentas, superfícies, testes, limitações e revisão de segurança.

## Permissões

- menor privilégio;
- ferramentas allowlisted;
- dados sensíveis somente quando necessários;
- ações externas registradas;
- custo, publicação, produção e irreversibilidade exigem aprovação humana;
- mudança de versão invalida validação anterior quando o comportamento puder mudar.

Skills de terceiros nunca são instaladas ou executadas automaticamente.
