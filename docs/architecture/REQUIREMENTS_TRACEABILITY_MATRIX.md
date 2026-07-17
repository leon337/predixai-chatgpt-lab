# Matriz inicial de rastreabilidade

| Requisito | Origem | Componente | Evidência prevista |
|---|---|---|---|
| REQ-ID-001 IDs imutáveis | DEC-0005 | schemas e banco | teste de unicidade |
| REQ-MSN-001 contrato modular | DEC-0006 | mission schema | validação de schema |
| REQ-EVL-001 requisitos eliminatórios | DEC-0007 | assessment service | testes de aprovação bloqueada |
| REQ-PRV-001 segredos fora do Git | DEC-0008 | CI e política | secret scan |
| REQ-PRM-001 três execuções | DEC-0009 | prompt registry | conjunto de runs |
| REQ-SKL-001 validação por superfície | DEC-0010 | skill registry | matriz de validação |
| REQ-GOV-001 PR obrigatório | DEC-0011 | GitHub workflow | branch/PR evidence |
| REQ-GOV-002 revisão por SHA | DEC-0011 | review gate | teste de stale review |
| REQ-PIL-001 dez missões | DEC-0012 | curriculum | inventário 10/10 |
| REQ-PIL-002 ledger privado | DEC-0003/0012 | pilot storage | arquivo ignorado e backup |

A matriz será ampliada campo a campo durante a especificação executável e implementação.
