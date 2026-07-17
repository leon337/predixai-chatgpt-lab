from __future__ import annotations

import importlib.util
import json
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator

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
        "steps": [
            {
                "id": "STP-0001",
                "title": "Classificar",
                "instructions": "Classifique as tarefas.",
                "saveable": True,
            }
        ],
        "evidence_requirements": ["Tabela de classificação"],
        "success_criteria": ["Três classificações justificadas"],
        "assessment": {"rubric_id": "RUB-0001"},
        "own_words_explanation": {
            "required": True,
            "prompt": "Explique a escolha.",
            "minimum_words": 20,
        },
        "feedback": {
            "success_message": "Domínio demonstrado.",
            "remediation_message": "Revise as diferenças entre superfícies.",
        },
        "next_unlock": {"on_success": "MSN-0002", "on_remediation": "MSN-0001-R1"},
        "security": {"evidence_classification": "INTERNAL"},
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
        {
            "run_id": f"RUN-{index}",
            "variation_id": f"VAR-{index}",
            "surface": "CHAT",
            "result": "PASS",
            "executed_at": f"2026-07-1{index}T10:00:00Z",
        }
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
            {"id": f"TST-{index}", "input_variant": f"variação-{index}", "expected_assertions": ["válido"]}
            for index in range(1, 4)
        ],
        "limitations": ["Depende de evidência legível"],
        "origin": {"source": "PredixAI Lab", "author": "Leo", "reviewed": True},
        "content_hash": "a" * 64,
        "security_review": {"status": "PASS", "reviewer": "reviewer-1", "reviewed_at": "2026-07-17T10:00:00Z"},
        "controlled_executions": executions,
        "validation_summary": {
            "controlled_execution_count": 3,
            "distinct_input_variations": 3,
            "all_executions_passed": True,
        },
        "changelog": ["1.0.0 — validação inicial"],
    }


def skill_instance() -> dict:
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
            {"test_id": f"TST-{index}", "input_variant": f"variação-{index}", "result": "PASS"}
            for index in range(1, 4)
        ],
        "examples": [{"case": "avaliação básica"}],
        "resources": [],
        "limitations": ["Não substitui revisão humana em gate crítico"],
        "security": {"review_status": "PASS", "reviewer": "reviewer-1", "reviewed_at": "2026-07-17T10:00:00Z"},
        "surface_validations": [
            {"surface": "CHAT", "adapter_version": "1.0.0", "result": "PASS", "validated_at": "2026-07-17T10:00:00Z"}
        ],
        "validation_summary": {
            "controlled_execution_count": 3,
            "diverse_inputs": True,
            "all_declared_surfaces_validated": True,
            "limitations_documented": True,
        },
        "changelog": ["1.0.0 — promoção para stable"],
    }


def runtime_complete_instance() -> dict:
    return {
        "schema_version": "0.1.0",
        "state_revision": 2,
        "project": "PredixAI ChatGPT Lab / PredixAI Quest",
        "repository": "leon337/predixai-chatgpt-lab",
        "main_branch": "main",
        "active_phase": "FOUNDATION_ARCHITECTURE",
        "transition_id": "FOUNDATION-T01",
        "transition_status": "COMPLETE",
        "reviewed_head_sha": "a" * 40,
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


def test_mission_requires_every_contract_block() -> None:
    schema = load_schema("schemas/missions/mission.schema.json")
    valid = mission_instance()
    assert_valid(schema, valid)
    invalid = deepcopy(valid)
    invalid.pop("context")
    assert_invalid(schema, invalid)


def test_assessment_rejects_impossible_mastery() -> None:
    schema = load_schema("schemas/assessments/assessment.schema.json")
    assert_valid(schema, assessment_instance(85, "MASTERED"))
    impossible = assessment_instance(0, "MASTERED_EXCELLENCE")
    impossible["eliminatory_checks"]["valid_evidence"] = False
    assert_invalid(schema, impossible)


def test_prompt_validated_requires_runs_and_security_review() -> None:
    schema = load_schema("schemas/prompts/prompt.schema.json")
    valid = prompt_instance()
    assert_valid(schema, valid)
    invalid = deepcopy(valid)
    invalid["controlled_executions"] = []
    invalid["security_review"]["status"] = "NOT_REVIEWED"
    assert_invalid(schema, invalid)


def test_skill_stable_requires_surface_validation() -> None:
    schema = load_schema("schemas/skills/skill.schema.json")
    valid = skill_instance()
    assert_valid(schema, valid)
    invalid = deepcopy(valid)
    invalid["surface_validations"] = []
    invalid["validation_summary"]["all_declared_surfaces_validated"] = False
    assert_invalid(schema, invalid)


def test_complete_transition_requires_passed_sync_and_no_blockers() -> None:
    schema = load_schema("schemas/project-runtime-state.schema.json")
    valid = runtime_complete_instance()
    assert_valid(schema, valid)
    invalid = deepcopy(valid)
    invalid["sync"]["linear"] = "FAIL"
    invalid["blockers"] = ["LINEAR_SYNC_FAILED"]
    assert_invalid(schema, invalid)


def test_prohibited_evidence_is_blocked_without_storage() -> None:
    schema = load_schema("schemas/evidence/evidence.schema.json")
    valid = {
        "id": "EVD-0001",
        "attempt_id": "ATT-0001",
        "classification": "PROHIBITED",
        "status": "BLOCKED",
        "storage_ref": None,
        "content_hash": None,
        "redacted": False,
        "retention_until": None,
    }
    assert_valid(schema, valid)
    invalid = deepcopy(valid)
    invalid["status"] = "UPLOADED"
    invalid["storage_ref"] = "private/object"
    assert_invalid(schema, invalid)


def test_secret_scanner_detects_supported_signature() -> None:
    module_path = ROOT / "scripts" / "scan_secrets.py"
    spec = importlib.util.spec_from_file_location("scan_secrets", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fake_secret = "sk-" + ("A" * 24)
    assert module.scan_text(f"TOKEN={fake_secret}")
    assert not module.scan_text("TOKEN=placeholder-not-a-secret")
