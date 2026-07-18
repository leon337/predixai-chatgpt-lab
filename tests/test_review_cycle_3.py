from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts import validate_foundation
from scripts.contract_semantics import (
    ContractSemanticError,
    validate_prompt_semantics,
    validate_skill_semantics,
)

ROOT = Path(__file__).resolve().parents[1]


def test_foundation_validator_applies_semantics_to_checked_in_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir(parents=True)
    schema = json.loads((ROOT / "schemas" / "project-runtime-state.schema.json").read_text(encoding="utf-8"))
    (schema_dir / "project-runtime-state.schema.json").write_text(json.dumps(schema), encoding="utf-8")

    state = {
        "schema_version": "0.1.0",
        "state_revision": 3,
        "project": "PredixAI ChatGPT Lab / PredixAI Quest",
        "repository": "leon337/predixai-chatgpt-lab",
        "main_branch": "main",
        "active_phase": "FOUNDATION_ARCHITECTURE",
        "transition_id": "FOUNDATION-T01",
        "transition_status": "COMPLETE",
        "observed_pr_head": "a" * 40,
        "reviewed_head_sha": "b" * 40,
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
    (tmp_path / "PROJECT_RUNTIME_STATE.yaml").write_text(yaml.safe_dump(state), encoding="utf-8")
    monkeypatch.setattr(validate_foundation, "ROOT", tmp_path)

    with pytest.raises(SystemExit):
        validate_foundation.validate_runtime_state()


def test_validated_prompt_requires_distinct_input_content() -> None:
    prompt = {
        "status": "VALIDATED",
        "test_cases": [
            {"variation_id": "VAR-1", "input_variant": "mesma entrada"},
            {"variation_id": "VAR-2", "input_variant": "mesma entrada"},
            {"variation_id": "VAR-3", "input_variant": "mesma entrada"},
        ],
        "controlled_executions": [
            {"variation_id": "VAR-1", "result": "PASS"},
            {"variation_id": "VAR-2", "result": "PASS"},
            {"variation_id": "VAR-3", "result": "PASS"},
        ],
        "validation_summary": {
            "controlled_execution_count": 3,
            "distinct_input_variations": 3,
            "all_executions_passed": True,
        },
    }

    with pytest.raises(ContractSemanticError):
        validate_prompt_semantics(prompt)


def test_stable_skill_rejects_duplicate_test_variation_ids() -> None:
    skill = {
        "status": "STABLE",
        "tests": [
            {"variation_id": "VAR-1", "input_variant": "entrada 1"},
            {"variation_id": "VAR-1", "input_variant": "entrada duplicada"},
            {"variation_id": "VAR-2", "input_variant": "entrada 2"},
            {"variation_id": "VAR-3", "input_variant": "entrada 3"},
        ],
        "controlled_executions": [
            {"variation_id": "VAR-1", "result": "PASS"},
            {"variation_id": "VAR-2", "result": "PASS"},
            {"variation_id": "VAR-3", "result": "PASS"},
        ],
        "supported_surfaces": ["CHAT"],
        "surface_validations": [{"surface": "CHAT", "result": "PASS"}],
        "validation_summary": {
            "controlled_execution_count": 3,
            "distinct_input_variations": 3,
            "all_declared_surfaces_validated": True,
            "limitations_documented": True,
        },
    }

    with pytest.raises(ContractSemanticError):
        validate_skill_semantics(skill)
