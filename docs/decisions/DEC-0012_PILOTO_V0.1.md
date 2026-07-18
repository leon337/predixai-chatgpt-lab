# DEC-0012 — Piloto V0.1

```yaml
id: DEC-0012
status: APPROVED
version: 1.1.0
supersedes: 1.0.0
refinement_reason: corrigir critérios de evidência, remediação e retenção antes da execução
```

## Escopo

- trilha `TRK-0001 — CORE`;
- campanha `CMP-0001 — Domínio do Ecossistema ChatGPT`;
- 3 mundos;
- 6 módulos;
- 10 missões;
- aluno inicial: Leo;
- execução manual por ChatGPT e GitHub;
- Linear como governança operacional;
- ledger acadêmico SQLite privado;
- evidências reais em armazenamento privado;
- plataforma web fora desta etapa.

## Estrutura

- `WRD-0001 — Fundamentos`:
  - `MOD-0001 — Ecossistema e contexto`: MSN-0001 e MSN-0002;
  - `MOD-0002 — Engenharia de prompts`: MSN-0003.
- `WRD-0002 — Ferramentas e superfícies`:
  - `MOD-0003 — Arquivos e pesquisa`: MSN-0004 e MSN-0005;
  - `MOD-0004 — Agentes e integrações`: MSN-0006 e MSN-0007.
- `WRD-0003 — Reutilização e governança`:
  - `MOD-0005 — Prompts e Skills`: MSN-0008 e MSN-0009;
  - `MOD-0006 — Missão-chefe`: MSN-0010.

## Critérios de encerramento

- 10/10 contratos produzidos e aprovados antes da execução;
- 10/10 missões executadas;
- 10/10 pacotes de evidência válidos e classificados;
- meta de primeira tentativa: pelo menos 8/10 missões com nota maior ou igual a 80;
- após remediação: 10/10 missões com nota maior ou igual a 80 antes do encerramento;
- missão-chefe com nota maior ou igual a 80;
- remediação concluída para toda missão inicialmente abaixo de 80 antes da missão-chefe;
- revisão de 24 horas para cada competência dominada;
- revisão de 7 dias para cada um dos 6 módulos;
- revisões de 30 e 90 dias registradas como acompanhamento posterior;
- zero incidente crítico de privacidade ou segurança;
- ao menos 1 prompt validado após três execuções controladas com entradas distintas;
- ao menos 1 candidata a Skill em `EXPERIMENTAL` ou `PILOT`;
- feedback de usabilidade registrado;
- relatório final com defeitos, remediações e decisão `GO`, `GO_WITH_REMEDIATION` ou `NO_GO`.

## Separação de dados

- GitHub: contratos, conteúdo, schemas, testes e exemplos sanitizados;
- banco privado: tentativas, notas, XP, retenção e progresso;
- armazenamento privado: arquivos de evidência;
- conteúdo `PROHIBITED`: não persistido.

## Itens mantidos no roadmap

Cadastro público, plataforma completa, banco de produção, pagamentos, ranking, marketplace, multi-instrutor, integrações de produção, automações irreversíveis e aplicativo nativo permanecem no roadmap. Nenhum desses itens foi descartado.
