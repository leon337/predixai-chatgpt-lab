# Estado oficial do projeto

## Identidade

- repositório: `leon337/predixai-chatgpt-lab`;
- projeto técnico: PredixAI ChatGPT Lab;
- plataforma: PredixAI Quest;
- marca: PredixAI BR.

## Estado atual

```text
ACTIVE_PHASE=PILOT_MANUAL_V0_1
ACTIVE_DELIVERY=PIL-001_CONTRATOS_E_EXECUCAO_DAS_10_MISSOES
WORKING_BRANCH=pilot/LEA-24-v0.1
PULL_REQUEST=2_DRAFT
LINEAR_IMPLEMENTATION_ISSUE=LEA-24_IN_PROGRESS
LINEAR_REVIEW_ISSUE=LEA-28_TODO
FOUNDATION_PR=1_MERGED
DEC_0011=APPROVED_V1_0_0
DEC_0012=APPROVED_V1_1_0
APPLICATION_RUNTIME_IMPLEMENTED=NO
PILOT_EXECUTION_STARTED=NO
```

## Fundação encerrada

- PR #1 integrado na `main`;
- cinco ciclos de revisão independente;
- 23 achados dos quatro primeiros ciclos remediados;
- quinto ciclo com zero P1 e zero P2;
- `LEA-22` e `LEA-23` concluídas;
- governança DEC-0011 ratificada.

## Entrega atual

A branch do piloto contém:

- hierarquia `TRK-0001 → CMP-0001 → WRD-0001..0003 → MOD-0001..0006`;
- contratos `MSN-0001` a `MSN-0010`;
- rubrica `RUB-0001`;
- schema público do ledger SQLite privado;
- protocolo de execução e template de evidência;
- templates `PRM-0001` e `SKL-0001` sem alegações fabricadas;
- validador e testes automatizados;
- relatório final do piloto.

## Gates

```text
PILOT_CONTRACTS_AUTHORED=10/10
INITIAL_CI_RUN=83
INITIAL_AUTOMATED_VALIDATION=PASS
SECRET_SCAN=PASS
FOUNDATION_VALIDATION=PASS
PILOT_VALIDATION=PASS
TEST_SUITE=PASS
INDEPENDENT_REVIEW=NOT_STARTED
PERSONAL_EVIDENCE_IN_GITHUB=PROHIBITED
PILOT_EXECUTION=BLOCKED_UNTIL_CONTRACT_REVIEW_PASS
PLATFORM_WEB=OUT_OF_SCOPE
```

## Próxima ação

Executar o CI no SHA final de estado, iniciar a revisão independente `LEA-28` vinculada ao SHA exato e somente depois liberar a execução da `MSN-0001`.
