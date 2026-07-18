from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pilot_validator_passes_on_checked_in_artifacts() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_pilot.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS: pilot V0.1 contracts validated" in result.stdout


def test_curriculum_references_exactly_ten_unique_missions() -> None:
    curriculum = json.loads((ROOT / "pilot" / "curriculum" / "pilot-v0.1.json").read_text(encoding="utf-8"))
    missions = [
        mission
        for world in curriculum["campaigns"][0]["worlds"]
        for module in world["modules"]
        for mission in module["missions"]
    ]
    assert missions == [f"MSN-{index:04d}" for index in range(1, 11)]
    assert len(missions) == len(set(missions))


def test_no_mission_is_published_before_independent_review() -> None:
    missions = sorted((ROOT / "pilot" / "missions").glob("MSN-*.json"))
    assert len(missions) == 10
    for path in missions:
        mission = json.loads(path.read_text(encoding="utf-8"))
        assert mission["status"] == "IN_REVIEW"
        assert mission["security"]["secrets_allowed"] is False
        assert mission["security"]["personal_data_allowed"] is False
        assert mission["security"]["evidence_classification"] == "PRIVATE"


def test_templates_do_not_claim_execution_or_stability() -> None:
    prompt = json.loads((ROOT / "pilot" / "prompts" / "PRM-0001_TEMPLATE.json").read_text(encoding="utf-8"))
    skill = json.loads((ROOT / "pilot" / "skills" / "SKL-0001_TEMPLATE.json").read_text(encoding="utf-8"))
    assert prompt["status"] == "DRAFT"
    assert prompt["controlled_executions"] == []
    assert prompt["security_review"]["status"] == "NOT_REVIEWED"
    assert skill["status"] == "EXPERIMENTAL"
    assert skill["controlled_executions"] == []
    assert skill["security"]["review_status"] == "NOT_REVIEWED"
