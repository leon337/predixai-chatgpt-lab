from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.contract_semantics import ContractSemanticError, validate_skill_semantics
from tests.test_contract_gates import skill_instance


def test_stable_skill_rejects_duplicate_controlled_execution_variation_ids() -> None:
    invalid = deepcopy(skill_instance())
    invalid["controlled_executions"] = [
        {
            "run_id": "RUN-1",
            "variation_id": "VAR-1",
            "surface": "CHAT",
            "result": "PASS",
            "executed_at": "2026-07-11T10:00:00Z",
        },
        {
            "run_id": "RUN-2",
            "variation_id": "VAR-2",
            "surface": "CHAT",
            "result": "PASS",
            "executed_at": "2026-07-12T10:00:00Z",
        },
        {
            "run_id": "RUN-3",
            "variation_id": "VAR-2",
            "surface": "CHAT",
            "result": "PASS",
            "executed_at": "2026-07-13T10:00:00Z",
        },
        {
            "run_id": "RUN-4",
            "variation_id": "VAR-3",
            "surface": "CHAT",
            "result": "PASS",
            "executed_at": "2026-07-14T10:00:00Z",
        },
    ]
    invalid["validation_summary"]["controlled_execution_count"] = 4

    with pytest.raises(ContractSemanticError, match="controlled execution variation_id values must be unique"):
        validate_skill_semantics(invalid)
