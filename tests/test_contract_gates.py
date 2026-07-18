from __future__ import annotations

import importlib.util
import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from scripts.contract_semantics import (
    ContractSemanticError,
    validate_assessment_semantics,
    validate_prompt_semantics,
    validate_runtime_state_semantics,
    validate_skill_semantics,
)

ROOT = Path(__file__).resolve().parents[1]


def load_schema(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def assert_valid(schema: dict, instance: dict) -> None:
    errors = list(Draft202012Validator(schema).iter_errors(instance))
    assert not errors, "; ".join(error.message for error in errors)


def assert_invalid(schema: dict, instance: dict) -> None:
    errors = list(Draft202012Validator(schema).iter_errors(instance))
    assert errors, "instance unexpectedly passed validation"


def mission_instance() -> dict:
    return {
        "id": "MSN-0001",
        "slug": "mapear-ecossistema",
        "version": "1.0.0",
        "status": "DRAFT",
        "title": "Mapear o ecossistema",
        "type": "EXPLORATION",
        "difficulty": "BEGINNER",
        "estimated_minutes": 20,
        "xp": 100,
        "context": "Entender as superfícies antes de escolher ferramentas.",
        "objectives": ["Distinguir superfícies"],
        "prerequisites": [],
        "core_concept": "Cada superfície possui capacidades e limites próprios.",
        "analogy": "Uma oficina possui bancadas diferentes para tarefas diferentes.",
        "execution_environment": {
            "primary_surface": "CHAT",
            "availability_status": "PRACTICAL_AVAILABLE",
            "setup": ["Abrir o ChatGPT"],
        },
        "execution_surfaces": ["CHAT"],
        "allowed_tools": [],
        "forbidden_actions": ["Publicar segredos"],
        "practical_mission": "Classificar três tarefas por superfície.",
        "steps": [{"id": "STP-0001", "title": "Classificar", "instructions": "Classifique as tarefas.", "saveable": True}],
        "evidence_requirements": ["Tabela de classificação"],
        "success_criteria": ["Três classificações justificadas"],
        "assessment": {"rubric_id": "RUB-0001"},
        "own_words_explanation": {"required": True, "prompt": "Explique a escolha.", "minimum_words": 20},
        "feedback": {"success_message": "Domínio demonstrado.", "remediation_message": "Revise as diferenças entre superfícies."},
        "next_unlock": {"on_success": "MSN-0002", "on_remediation": "MSN-0001-R1"},
        "security": {
            "evidence_classification": "INTERNAL",
            "restrictions": ["Não incluir dados pessoais nem credenciais"],
            "human_approval_required": False,
            "secrets_allowed": False,
            "personal_data_allowed": False,
        },
    }


def assessment_instance(score: int, result: str) -> dict:
    return {
        "id": "EVL-0001",
        "attempt_id": "ATT-0001",
        "rubric_version": "1.0.0",
        "criterion_scores": [{"criterion_id": "CRI-001", "score": score, "weight": 1}],
        "eliminatory_checks": {
            "valid_evidence": True,
            "own_explanation": True,
            "security_compliant": True,
            "not_fabricated": True,
        },
        "total_score": score,
        "result": result,
    }


def prompt_instance() -> dict:
    executions = [
        {"run_id": f"RUN-{index}", "variation_id": f"VAR-{index}", "surface": "CHAT", "result": "PASS", "executed_at": f"2026-07-1{index}T10:00:00Z"}
        for index in range(1, 4)
    ]
    return {
        "id": "PRM-0001",
        "slug": "avaliar-missao",
        "version": "1.0.0",
        "status": "VALIDATED",
        "category": "EVALUATION",
        "purpose": "Avaliar uma missão com rubrica.",
        "inputs": {"attempt": "object"},
        "expected_output": "Resultado estruturado.",
        "output_schema": {"type": "object"},
        "supported_surfaces": ["CHAT"],
        "allowed_tools": [],
        "forbidden_actions": ["Inventar evidência"],
        "success_criteria": ["Resultado compatível com a rubrica"],
        "test_cases": [
            {"id": f"TST-{index}", "variation_id": f"VAR-{index}", "input_variant": f"variação-{index}", "expected_assertions": ["válido"]}
            for index in range(1, 4)
        ],
        "limitations": ["Depende de evidência legível"],
        "origin": {"source": "PredixAI Lab", "author": "Leo", "reviewed": True},
        "content_hash": "a" * 64,
        "security_review": {"status": "PASS", "reviewer": "reviewer-1", "reviewed_at": "2026-07-17T10:00:00Z"},
        "controlled_executions": executions,
        "validation_summary": {"controlled_execution_count": 3, "distinct_input_variations": 3, "all_executions_passed": True},
        "changelog": ["1.0.0 — validação inicial"],
    }


def skill_instance() -> dict:
    executions = [
        {"run_id": f"RUN-{index}", "variation_id": f"VAR-{index}", "surface": "CHAT", "result": "PASS", "executed_at": f"2026-07-1{index}T10:00:00Z"}
        for index in range(1, 4)
    ]
    return {
        "id": "SKL-0001",
        "slug": "avaliar-missao",
        "version": "1.0.0",
        "status": "STABLE",
        "purpose": "Avaliar missões de forma reutilizável.",
        "activation": "Quando uma tentativa for submetida.",
        "inputs": {"attempt": "object"},
        "outputs": {"assessment": "object"},
        "supported_surfaces": ["CHAT"],
        "required_tools": [],
        "permissions": [],
        "dependencies": [],
        "tests": [
            {"test_id": f"TST-{index}", "variation_id": f"VAR-{index}", "input_variant": f"variação-{index}", "result": "PASS"}
            for index in range(1, 4)
        ],
        "controlled_executions": executions,
        "examples": [{"case": "avaliação básica"}],
        "resources": [],
        "limitations": ["Não substitui revisão humana em gate crítico"],
        "security": {"review_status": "PASS", "reviewer": "reviewer-1", "reviewed_at": "2026-07-17T10:00:00Z"},
        "surface_validations": [{"surface": "CHAT", "adapter_version": "1.0.0", "result": "PASS", "validated_at": "2026-07-17T10:00:00Z"}],
        "validation_summary": {
            "controlled_execution_count": 3,
            "distinct_input_variations": 3,
            "all_declared_surfaces_validated": True,
            "limitations_documented": True,
        },
        "changelog": ["1.0.0 — promoção para stable"],
    }


def runtime_complete_instance() -> dict:
    head = "a" * 40
    return {
        "schema_version": "0.1.0",
        "state_revision": 2,
        "project": "PredixAI ChatGPT Lab / PredixAI Quest",
        "repository": "leon337/predixai-chatgpt-lab",
        "main_branch": "main",
        "active_phase": "FOUNDATION_ARCHITECTURE",
        "transition_id": "FOUNDATION-T01",
        "transition_status": "COMPLETE",
        "observed_pr_head": head,
        "reviewed_head_sha": head,
        "current_gate": "FOUNDATION_REVIEW",
        "gate_status": "PASS",
        "next_action": "START_PILOT",
        "blockers": [],
        "authorizations": {
            "implementation": True,
            "code_change": True,
            "database_design": True,
            "migration_execution": False,
            "merge": False,
            "production_integration": False,
            "irreversible_automation": False,
        },
        "sync": {"github": "PASS", "linear": "PASS"},
        "safety": {
            "public_secrets_allowed": False,
            "personal_evidence_in_public_repo": False,
            "production_actions_allowed": False,
            "automatic_advance": False,
        },
    }


def prohibited_evidence(status: str = "BLOCKED") -> dict:
    return {
        "id": "EVD-0001",
        "attempt_id": "ATT-0001",
        "classification": "PROHIBITED",
        "status": status,
        "storage_ref": None,
        "content_hash": None,
        "redacted": False,
        "retention_until": None,
        "block_reason": "Conteúdo proibido detectado antes da persistência",
        "deleted_at": "2026-07-17T10:00:00Z" if status == "DELETED" else None,
    }


def load_secret_scanner():
    module_path = ROOT / "scripts" / "scan_secrets.py"
    spec = importlib.util.spec_from_file_location("scan_secrets", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_mission_requires_every_contract_block() -> None:
    schema = load_schema("schemas/missions/mission.schema.json")
    valid = mission_instance()
    assert_valid(schema, valid)
    invalid = deepcopy(valid)
    invalid.pop("context")
    assert_invalid(schema, invalid)


def test_mission_security_block_rejects_placeholder() -> None:
    schema = load_schema("schemas/missions/mission.schema.json")
    invalid = mission_instance()
    invalid["security"] = {"placeholder": None}
    assert_invalid(schema, invalid)


def test_assessment_result_band_and_eliminatories() -> None:
    schema = load_schema("schemas/assessments/assessment.schema.json")
    valid = assessment_instance(85, "MASTERED")
    assert_valid(schema, valid)
    validate_assessment_semantics(valid)
    impossible = assessment_instance(0, "MASTERED_EXCELLENCE")
    impossible["eliminatory_checks"]["valid_evidence"] = False
    assert_invalid(schema, impossible)


def test_assessment_semantics_rejects_fabricated_total() -> None:
    dishonest = assessment_instance(0, "MASTERED_EXCELLENCE")
    dishonest["total_score"] = 100
    schema = load_schema("schemas/assessments/assessment.schema.json")
    assert_valid(schema, dishonest)
    with pytest.raises(ContractSemanticError):
        validate_assessment_semantics(dishonest)


def test_assessment_semantics_requires_weights_sum_to_one() -> None:
    invalid = assessment_instance(80, "MASTERED")
    invalid["criterion_scores"] = [
        {"criterion_id": "CRI-001", "score": 80, "weight": 0.4},
        {"criterion_id": "CRI-002", "score": 80, "weight": 0.4},
    ]
    with pytest.raises(ContractSemanticError):
        validate_assessment_semantics(invalid)


def test_prompt_validated_requires_runs_and_security_review() -> None:
    schema = load_schema("schemas/prompts/prompt.schema.json")
    valid = prompt_instance()
    assert_valid(schema, valid)
    validate_prompt_semantics(valid)
    invalid = deepcopy(valid)
    invalid["controlled_executions"] = []
    invalid["security_review"]["status"] = "NOT_REVIEWED"
    assert_invalid(schema, invalid)


def test_prompt_semantics_rejects_repeated_variations() -> None:
    invalid = prompt_instance()
    for execution in invalid["controlled_executions"]:
        execution["variation_id"] = "VAR-1"
    with pytest.raises(ContractSemanticError):
        validate_prompt_semantics(invalid)


def test_skill_stable_requires_surface_validation() -> None:
    schema = load_schema("schemas/skills/skill.schema.json")
    valid = skill_instance()
    assert_valid(schema, valid)
    validate_skill_semantics(valid)
    invalid = deepcopy(valid)
    invalid["surface_validations"] = []
    invalid["validation_summary"]["all_declared_surfaces_validated"] = False
    assert_invalid(schema, invalid)


def test_skill_semantics_rejects_repeated_execution_variations() -> None:
    invalid = skill_instance()
    for execution in invalid["controlled_executions"]:
        execution["variation_id"] = "VAR-1"
    with pytest.raises(ContractSemanticError):
        validate_skill_semantics(invalid)


def test_skill_semantics_requires_every_supported_surface() -> None:
    invalid = skill_instance()
    invalid["supported_surfaces"] = ["CHAT", "CODEX"]
    with pytest.raises(ContractSemanticError):
        validate_skill_semantics(invalid)


def test_complete_transition_requires_passed_sync_and_exact_head() -> None:
    schema = load_schema("schemas/project-runtime-state.schema.json")
    valid = runtime_complete_instance()
    assert_valid(schema, valid)
    validate_runtime_state_semantics(valid)
    invalid = deepcopy(valid)
    invalid["sync"]["linear"] = "FAIL"
    invalid["blockers"] = ["LINEAR_SYNC_FAILED"]
    assert_invalid(schema, invalid)


def test_runtime_semantics_rejects_stale_reviewed_head() -> None:
    invalid = runtime_complete_instance()
    invalid["reviewed_head_sha"] = "b" * 40
    with pytest.raises(ContractSemanticError):
        validate_runtime_state_semantics(invalid)


def test_prohibited_evidence_blocks_persisted_content() -> None:
    schema = load_schema("schemas/evidence/evidence.schema.json")
    valid = prohibited_evidence()
    assert_valid(schema, valid)
    invalid_hash = deepcopy(valid)
    invalid_hash["content_hash"] = "a" * 64
    assert_invalid(schema, invalid_hash)
    invalid_payload = deepcopy(valid)
    invalid_payload["payload"] = "conteúdo não permitido"
    assert_invalid(schema, invalid_payload)


def test_prohibited_evidence_can_transition_to_deleted() -> None:
    schema = load_schema("schemas/evidence/evidence.schema.json")
    assert_valid(schema, prohibited_evidence("DELETED"))


def test_secret_scanner_detects_signature_even_with_inline_allow() -> None:
    module = load_secret_scanner()
    fake_secret = "sk-" + ("A" * 24)
    assert module.scan_text(f"TOKEN={fake_secret}  # secret-scan: allow")
    assert not module.scan_text("TOKEN=placeholder-not-a-secret")


def test_secret_scanner_scans_large_text_files(tmp_path: Path) -> None:
    module = load_secret_scanner()
    fake_secret = "sk-" + ("B" * 24)
    large = tmp_path / "large-config.txt"
    with large.open("w", encoding="utf-8") as handle:
        handle.write("x" * (2 * 1024 * 1024 + 128))
        handle.write("\nTOKEN=" + fake_secret + "\n")
    findings = module.scan_repository(tmp_path)
    assert findings and "large-config.txt" in findings[0]
