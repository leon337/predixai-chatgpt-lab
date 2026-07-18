#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.contract_semantics import ContractSemanticError, validate_runtime_state_semantics

REQUIRED_ARCHITECTURE = [
    "DOMAIN_MAP.md",
    "MODULE_BOUNDARIES.md",
    "CROSS_MODULE_CONTRACTS.md",
    "DATA_MODEL.md",
    "ENTITY_RELATIONSHIP_MODEL.md",
    "STATE_MACHINES.md",
    "EVENT_CATALOG.md",
    "PERMISSION_MODEL.md",
    "STORAGE_ARCHITECTURE.md",
    "INTEGRATION_CONTRACTS.md",
    "AUDIT_MODEL.md",
    "MIGRATION_STRATEGY.md",
    "REQUIREMENTS_TRACEABILITY_MATRIX.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def validate_decisions() -> None:
    decision_dir = ROOT / "docs" / "decisions"
    files = sorted(decision_dir.glob("DEC-[0-9][0-9][0-9][0-9]_*.md"))
    if len(files) != 12:
        fail(f"expected 12 decision files, found {len(files)}")
    ids: list[str] = []
    for file in files:
        match = re.search(r"DEC-[0-9]{4}", file.name)
        if not match:
            fail(f"invalid decision filename: {file}")
        ids.append(match.group(0))
    if len(ids) != len(set(ids)):
        fail("duplicate decision IDs")
    registry = (decision_dir / "DECISION_REGISTRY.md").read_text(encoding="utf-8")
    for decision_id in ids:
        if decision_id not in registry:
            fail(f"{decision_id} missing from registry")


def validate_runtime_state() -> None:
    state = yaml.safe_load((ROOT / "PROJECT_RUNTIME_STATE.yaml").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas" / "project-runtime-state.schema.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(state), key=lambda e: list(e.path))
    if errors:
        fail("runtime schema mismatch: " + "; ".join(error.message for error in errors))
    try:
        validate_runtime_state_semantics(state)
    except ContractSemanticError as exc:
        fail(f"runtime semantic mismatch: {exc}")


def validate_architecture() -> None:
    base = ROOT / "docs" / "architecture"
    missing = [name for name in REQUIRED_ARCHITECTURE if not (base / name).exists()]
    if missing:
        fail("missing architecture files: " + ", ".join(missing))


def validate_private_files() -> None:
    forbidden_suffixes = {".sqlite", ".sqlite3", ".db", ".env"}
    found: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix in forbidden_suffixes or path.name == ".env":
            found.append(str(path.relative_to(ROOT)))
    if found:
        fail("private files tracked: " + ", ".join(found))


def validate_json_schemas() -> None:
    for schema_path in (ROOT / "schemas").rglob("*.schema.json"):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def main() -> None:
    validate_decisions()
    validate_runtime_state()
    validate_architecture()
    validate_private_files()
    validate_json_schemas()
    print("PASS: foundation validation completed")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        fail(str(exc))
