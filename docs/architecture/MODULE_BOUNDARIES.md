# Fronteiras dos módulos

## Regras universais

1. módulos expõem serviços e eventos, não tabelas internas;
2. referências cruzadas usam IDs estáveis;
3. operações que afetam mais de um domínio registram `correlation_id`;
4. dados privados não são copiados para o conteúdo público;
5. toda mudança de estado acadêmico gera evento de auditoria;
6. integrações externas não governam progresso acadêmico diretamente.

## Dependências permitidas

```text
Identity <- Learning, Evidence, Governance
Curriculum <- Missions
Missions <- Learning, Assessment
Learning <- Gamification, Retention
Prompts <- Missions
Skills <- Missions
Evidence <- Assessment
Governance <- Integrations
Audit <- todos os domínios (somente append)
```

## Proibições

- Gamification não aprova uma missão;
- Evidence não calcula nota;
- Linear não altera domínio acadêmico;
- GitHub não armazena evidência privada;
- PromptRun não promove PromptVersion sem avaliação;
- SkillValidation não concede permissões além do manifesto;
- adaptadores externos não fazem ação irreversível sem grant humano válido.
