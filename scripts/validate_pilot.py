#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sqlite3
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "pilot"
EXPECTED_MISSIONS = [f"MSN-{index:04d}" for index in range(1, 11)]
EXPECTED_WORLDS = ["WRD-0001", "WRD-0002", "WRD-0003"]
EXPECTED_MODULES = [f"MOD-{index:04d}" for index in range(1, 7)]
REQUIRED_LEDGER_TABLES = {
    "users",
    "missions",
    "attempts",
    "evidence_metadata",
    "assessments",
    "assessment_criteria",
    "xp_transactions",
    "retention_reviews",
    "prompt_runs",
    "skill_candidates",
    "audit_events",
}


class PilotValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PilotValidationError(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_with_schema(instance: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = load_json(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(error.message for error in errors)
        raise PilotValidationError(f"{label} schema mismatch: {details}")


def validate_curriculum() -> None:
    curriculum = load_json(PILOT / "curriculum" / "pilot-v0.1.json")
    require(curriculum["track"]["id"] == "TRK-0001", "pilot track must be TRK-0001")
    campaigns = curriculum.get("campaigns", [])
    require(len(campaigns) == 1, "pilot must contain exactly one campaign")
    require(campaigns[0]["id"] == "CMP-0001", "pilot campaign must be CMP-0001")
    worlds = campaigns[0].get("worlds", [])
    require([world["id"] for world in worlds] == EXPECTED_WORLDS, "pilot worlds or order mismatch")
    modules = [module for world in worlds for module in world.get("modules", [])]
    require([module["id"] for module in modules] == EXPECTED_MODULES, "pilot modules or order mismatch")
    mission_refs = [mission for module in modules for mission in module.get("missions", [])]
    require(mission_refs == EXPECTED_MISSIONS, "curriculum mission references or order mismatch")
    require(len(mission_refs) == len(set(mission_refs)), "curriculum contains duplicate mission references")


def validate_missions() -> None:
    mission_dir = PILOT / "missions"
    files = sorted(mission_dir.glob("MSN-*.json"))
    require(len(files) == 10, f"expected 10 mission contracts, found {len(files)}")
    mission_schema = ROOT / "schemas" / "missions" / "mission.schema.json"
    ids: list[str] = []
    step_ids: list[str] = []
    missions: dict[str, dict[str, Any]] = {}
    for path in files:
        mission = load_json(path)
        validate_with_schema(mission, mission_schema, path.name)
        mission_id = mission["id"]
        require(path.stem == mission_id, f"filename and mission id mismatch for {path.name}")
        require(mission["status"] == "IN_REVIEW", f"{mission_id} must remain IN_REVIEW before independent review")
        require(mission["security"]["evidence_classification"] == "PRIVATE", f"{mission_id} evidence must default to PRIVATE")
        require(mission["security"]["secrets_allowed"] is False, f"{mission_id} must prohibit secrets")
        require(mission["security"]["personal_data_allowed"] is False, f"{mission_id} must prohibit personal data")
        ids.append(mission_id)
        step_ids.extend(step["id"] for step in mission["steps"])
        missions[mission_id] = mission
    require(ids == EXPECTED_MISSIONS, "mission IDs or file order mismatch")
    require(len(step_ids) == len(set(step_ids)), "step IDs must be globally unique in the pilot")
    for index, mission_id in enumerate(EXPECTED_MISSIONS[:-1]):
        require(missions[mission_id]["next_unlock"]["on_success"] == EXPECTED_MISSIONS[index + 1], f"{mission_id} success unlock mismatch")
    require(missions["MSN-0010"]["next_unlock"]["on_success"] is None, "boss mission must not auto-unlock another mission")
    require(missions["MSN-0010"]["type"] == "BOSS", "MSN-0010 must be the boss mission")
    require(missions["MSN-0010"]["security"]["human_approval_required"] is True, "boss mission requires human approval")


def validate_rubric() -> None:
    rubric = load_json(PILOT / "rubrics" / "RUB-0001.json")
    require(rubric["id"] == "RUB-0001", "rubric id mismatch")
    weights = [float(item["weight"]) for item in rubric.get("criteria", [])]
    require(len(weights) == 6, "pilot rubric must contain six criteria")
    require(math.isclose(sum(weights), 1.0, rel_tol=0.0, abs_tol=1e-9), "rubric weights must sum to 1.0")
    require(rubric["rules"]["mastery_minimum"] == 80, "mastery threshold must be 80")
    require(rubric["rules"]["boss_minimum"] == 80, "boss threshold must be 80")
    require(len(rubric.get("eliminatory_checks", [])) == 4, "four eliminatory checks are required")


def validate_templates() -> None:
    prompt = load_json(PILOT / "prompts" / "PRM-0001_TEMPLATE.json")
    validate_with_schema(prompt, ROOT / "schemas" / "prompts" / "prompt.schema.json", "PRM-0001_TEMPLATE")
    require(prompt["status"] == "DRAFT", "prompt template must not claim validation")
    require(prompt["controlled_executions"] == [], "prompt template must not contain fabricated executions")

    skill = load_json(PILOT / "skills" / "SKL-0001_TEMPLATE.json")
    validate_with_schema(skill, ROOT / "schemas" / "skills" / "skill.schema.json", "SKL-0001_TEMPLATE")
    require(skill["status"] == "EXPERIMENTAL", "Skill template must remain EXPERIMENTAL")
    require(skill["controlled_executions"] == [], "Skill template must not contain fabricated executions")
    require(skill["security"]["review_status"] == "NOT_REVIEWED", "Skill template must not claim security review")


def validate_ledger_schema() -> None:
    schema_path = PILOT / "ledger" / "schema.sql"
    sql = schema_path.read_text(encoding="utf-8")
    require("INSERT INTO" not in sql.upper(), "public ledger schema must not seed personal data")
    connection = sqlite3.connect(":memory:")
    try:
        connection.executescript(sql)
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        }
    finally:
        connection.close()
    require(REQUIRED_LEDGER_TABLES.issubset(tables), f"ledger tables missing: {sorted(REQUIRED_LEDGER_TABLES - tables)}")


def main() -> int:
    try:
        validate_curriculum()
        validate_missions()
        validate_rubric()
        validate_templates()
        validate_ledger_schema()
    except (OSError, KeyError, json.JSONDecodeError, sqlite3.Error, PilotValidationError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: pilot V0.1 contracts validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
