# Matriz inicial de rastreabilidade

| Requisito | Origem | Componente | Evidência automatizada |
|---|---|---|---|
| REQ-ID-001 IDs imutáveis | DEC-0005 | schemas e banco | `validate_decisions` e testes futuros de unicidade no banco |
| REQ-MSN-001 contrato modular com 16 blocos | DEC-0006 | `mission.schema.json` | `test_mission_requires_every_contract_block` |
| REQ-EVL-001 requisitos eliminatórios | DEC-0007 | `assessment.schema.json` | `test_assessment_rejects_impossible_mastery` |
| REQ-EVL-002 faixas compatíveis com resultado | DEC-0007 | `assessment.schema.json` | `test_assessment_rejects_impossible_mastery` |
| REQ-PRV-001 segredos fora do Git | DEC-0008 | CI e política | `scan_secrets.py` e `test_secret_scanner_detects_supported_signature` |
| REQ-PRV-002 conteúdo proibido não persistido | DEC-0008 | evidence schema e state machine | `test_prohibited_evidence_is_blocked_without_storage` |
| REQ-PRM-001 três execuções variadas | DEC-0009 | `prompt.schema.json` | `test_prompt_validated_requires_runs_and_security_review` |
| REQ-PRM-002 revisão de segurança para VALIDATED | DEC-0009 | `prompt.schema.json` | `test_prompt_validated_requires_runs_and_security_review` |
| REQ-SKL-001 validação por superfície | DEC-0010 | `skill.schema.json` | `test_skill_stable_requires_surface_validation` |
| REQ-SKL-002 três execuções e segurança para STABLE | DEC-0010 | `skill.schema.json` | `test_skill_stable_requires_surface_validation` |
| REQ-GOV-001 PR obrigatório | DEC-0011 | GitHub workflow | branch e PR Draft `#1` |
| REQ-GOV-002 revisão por SHA | DEC-0011 | review gate | revisão Codex ligada ao SHA e protocolo de stale review |
| REQ-GOV-003 COMPLETE exige sync e zero bloqueadores | DEC-0011 | runtime state schema | `test_complete_transition_requires_passed_sync_and_no_blockers` |
| REQ-DOM-001 16 domínios canônicos sem propriedade ambígua | DEC-0003/0011 | `ARCHITECTURE.md`, `DOMAIN_MAP.md`, `DATA_MODEL.md` | revisão documental cruzada |
| REQ-PIL-001 dez missões | DEC-0012 | curriculum | inventário futuro 10/10 |
| REQ-PIL-002 ledger privado | DEC-0003/0012 | pilot storage | arquivo ignorado, backup privado e teste de ausência no Git |

A matriz será ampliada campo a campo durante a especificação executável e implementação.
