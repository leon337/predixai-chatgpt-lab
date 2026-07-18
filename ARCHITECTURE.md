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

## Domínios canônicos

A decomposição oficial é a mesma de `docs/architecture/DOMAIN_MAP.md`:

1. **Identity** — contas, sessões, papéis e associações;
2. **Curriculum** — trilhas, campanhas, mundos, módulos e competências;
3. **Missions** — contratos de missão, etapas e recursos;
4. **Learning** — matrículas, tentativas, domínio e progresso;
5. **Assessment** — rubricas, critérios, notas e feedback;
6. **Evidence** — referências, arquivos e revisões de evidência;
7. **Gamification** — XP, medalhas e desbloqueios;
8. **Retention** — revisões espaçadas e remediação;
9. **Prompts** — catálogo, versões, execuções e validações de prompts;
10. **Skills** — pacotes, versões, adaptadores e validações por superfície;
11. **Integrations** — conexões, adaptadores externos e sincronizações;
12. **Governance** — decisões, transições e gates de revisão;
13. **Audit** — eventos imutáveis e rastreabilidade;
14. **Publication** — catálogo público, releases e publicação de conteúdo;
15. **Operations** — configurações, jobs, feature flags e saúde da plataforma;
16. **Privacy** — consentimento, retenção, exclusão e direitos do titular.

Competências pertencem a **Curriculum**. Privacidade é um domínio independente de **Evidence**. O catálogo público pertence a **Publication**.

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
