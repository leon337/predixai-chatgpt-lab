#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Callable


class ContractSemanticError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractSemanticError(message)


def validate_assessment_semantics(instance: dict[str, Any]) -> None:
    scores = instance.get("criterion_scores", [])
    _require(bool(scores), "criterion_scores must not be empty")
    weight_sum = sum(float(item["weight"]) for item in scores)
    _require(math.isclose(weight_sum, 1.0, rel_tol=0.0, abs_tol=1e-9), "criterion weights must sum to 1.0")
    computed_total = sum(float(item["score"]) * float(item["weight"]) for item in scores)
    _require(
        math.isclose(float(instance["total_score"]), computed_total, rel_tol=0.0, abs_tol=1e-6),
        f"total_score must equal weighted criterion total {computed_total:g}",
    )


def validate_prompt_semantics(instance: dict[str, Any]) -> None:
    if instance.get("status") != "VALIDATED":
        return
    test_cases = instance.get("test_cases", [])
    executions = instance.get("controlled_executions", [])
    test_variations = [item["variation_id"] for item in test_cases]
    execution_variations = [item["variation_id"] for item in executions]
    _require(len(set(test_variations)) == len(test_variations), "test case variation_id values must be unique")
    _require(len(set(execution_variations)) >= 3, "VALIDATED prompt requires at least three distinct execution variations")
    _require(set(execution_variations).issubset(set(test_variations)), "execution variation_id must reference a test case")
    _require(all(item["result"] == "PASS" for item in executions), "all controlled prompt executions must pass")
    summary = instance["validation_summary"]
    _require(summary["controlled_execution_count"] == len(executions), "prompt execution count summary mismatch")
    _require(summary["distinct_input_variations"] == len(set(execution_variations)), "prompt variation count summary mismatch")
    _require(summary["all_executions_passed"] is True, "prompt summary must record all executions passed")


def validate_skill_semantics(instance: dict[str, Any]) -> None:
    if instance.get("status") != "STABLE":
        return
    tests = instance.get("tests", [])
    executions = instance.get("controlled_executions", [])
    test_variations = [item["variation_id"] for item in tests]
    execution_variations = [item["variation_id"] for item in executions]
    _require(len(set(test_variations)) >= 3, "STABLE skill requires at least three distinct test variations")
    _require(len(set(execution_variations)) >= 3, "STABLE skill requires at least three distinct controlled execution variations")
    _require(set(execution_variations).issubset(set(test_variations)), "skill execution variation_id must reference a declared test")
    _require(all(item["result"] == "PASS" for item in executions), "all controlled skill executions must pass")

    supported = set(instance.get("supported_surfaces", []))
    validations = instance.get("surface_validations", [])
    validated_surfaces = [item["surface"] for item in validations if item["result"] == "PASS"]
    _require(len(validated_surfaces) == len(set(validated_surfaces)), "surface validations must not contain duplicate PASS entries")
    _require(set(validated_surfaces) == supported, "every and only declared skill surface must have a PASS validation")

    summary = instance["validation_summary"]
    _require(summary["controlled_execution_count"] == len(executions), "skill execution count summary mismatch")
    _require(summary["distinct_input_variations"] == len(set(execution_variations)), "skill variation count summary mismatch")
    _require(summary["all_declared_surfaces_validated"] is True, "skill summary must confirm all surfaces")
    _require(summary["limitations_documented"] is True, "skill limitations must be documented")


def validate_runtime_state_semantics(instance: dict[str, Any]) -> None:
    if instance.get("transition_status") != "COMPLETE":
        return
    observed = instance.get("observed_pr_head")
    reviewed = instance.get("reviewed_head_sha")
    _require(bool(observed) and bool(reviewed), "COMPLETE transition requires observed and reviewed PR heads")
    _require(observed == reviewed, "reviewed_head_sha must equal observed_pr_head")


VALIDATORS: dict[str, Callable[[dict[str, Any]], None]] = {
    "assessment": validate_assessment_semantics,
    "prompt": validate_prompt_semantics,
    "skill": validate_skill_semantics,
    "runtime-state": validate_runtime_state_semantics,
}


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in VALIDATORS:
        print("usage: contract_semantics.py <assessment|prompt|skill|runtime-state> <instance.json>")
        return 2
    instance = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    try:
        VALIDATORS[sys.argv[1]](instance)
    except ContractSemanticError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: semantic contract validation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
