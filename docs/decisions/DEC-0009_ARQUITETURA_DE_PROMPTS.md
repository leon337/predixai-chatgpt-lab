# DEC-0009 — Arquitetura de prompts

```yaml
id: DEC-0009
status: APPROVED
version: 1.0.0
```

O prompt é montado em camadas: base, papel, objetivo, contexto, restrições, ferramentas, formato, avaliação e dados da missão.

Categorias: system, mission, tool, evaluation, recovery e security.

Todo prompt possui ID, versão, finalidade, entradas, saída, superfícies, ferramentas, proibições, testes, limitações e changelog.

Estados: `DRAFT`, `IN_TESTING`, `VALIDATED`, `DEPRECATED`, `ARCHIVED`. Promoção exige no mínimo três execuções controladas com variações e revisão de segurança.
