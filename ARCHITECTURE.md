# Arquitetura — visão geral

## Sistemas

```text
PredixAI ChatGPT Lab
├── Conteúdo versionado no GitHub
├── Governança GitHub + Linear
├── Catálogo de prompts e Skills
├── Piloto acadêmico privado
└── PredixAI Quest
    ├── Aplicação web mobile-first
    ├── API acadêmica
    ├── Banco acadêmico
    ├── Armazenamento de evidências
    └── Integrações controladas
```

## Domínios

1. identidade e acesso;
2. currículo;
3. missões e etapas;
4. competências;
5. tentativas e progresso;
6. avaliações e rubricas;
7. evidências e privacidade;
8. gamificação;
9. retenção e remediação;
10. prompts;
11. Skills;
12. integrações e superfícies;
13. governança e decisões;
14. auditoria;
15. catálogo e publicação;
16. operações da plataforma.

## Fontes de verdade

| Domínio | Autoridade |
|---|---|
| Código e documentação consolidados | GitHub `main` |
| Trabalho não integrado | branch e PR ativos |
| Estado operacional do projeto | manifesto versionado + Linear por campo |
| Tarefas, dependências e bloqueios | Linear |
| Progresso acadêmico | banco privado |
| Evidências pessoais e sensíveis | armazenamento privado |
| Referência oficial do produto OpenAI | documentação oficial externa |
| Contexto temporário | ChatGPT |

## Estilo arquitetural

- monólito modular no MVP, evitando microsserviços prematuros;
- contratos explícitos entre domínios;
- eventos de domínio para auditoria e integrações;
- IDs estáveis independentes da posição curricular;
- schemas legíveis por máquina;
- separação entre conteúdo público e estado privado;
- adaptadores por superfície para Skills e integrações.

## Gate atual

A arquitetura está em construção. Implementação da plataforma somente começa após a baseline de decisões, contratos e dados passar por revisão crítica.
