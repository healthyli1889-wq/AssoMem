"""Strict prompt contracts for author, solver, and independent validator."""

from __future__ import annotations

import json
from typing import Any


def _dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def solver_prompt(visible: dict[str, Any]) -> str:
    return f"""Answer the user's final query using only the supplied conversation.
If the evidence is insufficient, explicitly abstain. Do not mention benchmark metadata.
Return exactly one JSON object with exactly one key, `answer`. Its string value must
be your substantive answer to the user and must not be a placeholder, schema example,
or restatement of this instruction.
Conversation input: {_dump(visible)}
"""


def score_prompt(answer: dict[str, Any], ground_truth: dict[str, Any]) -> str:
    return f"""Score a solver response against hidden ground truth. Return JSON:
{{"element_hits":[bool],"cited_evidence_count":0,"abstains":bool,
"asserts_absent_pattern":bool,"source_misattribution":bool,"condition_correct":bool,"reason":str}}.
element_hits must align in order with required_elements; cite count is 0, 1, or 2.
When expected_mode is `not_gold`, condition_correct is true only when the solver
withholds the original personalized inference. For a broken-link input, mark
source_misattribution true if a friend's statement is used as the user's fact.
Solver response: {_dump(answer)}
Ground truth: {_dump(ground_truth)}
"""
