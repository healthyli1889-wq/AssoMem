"""Strict prompt contracts for author, solver, and independent validator."""

from __future__ import annotations

import json
from typing import Any


def _dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def author_prompt(visible: dict[str, Any]) -> str:
    return f"""Create an associative-memory benchmark item from visible dialogue only.
Keep the decision focus of the final query, but rewrite it naturally. Return JSON:
{{"query":str,"gold":str,"required_elements":[str],"evidence_roles":[str,str],"type":str}}.
The gold must require two user-specific experiences; do not expose session labels,
annotations, or benchmark mechanics.
Visible input: {_dump(visible)}
"""


def validate_query_prompt(visible: dict[str, Any], candidate: dict[str, Any]) -> str:
    return f"""Independently validate this candidate associative-memory query and ground truth.
Use only the visible dialogue. Return JSON:
{{"accept":bool,"answer_table":{{"prior":bool,"ev_a_only":bool,"ev_b_only":bool,"full":bool}},
"gold_supported":bool,"required_elements_supported":[bool],"reasons":[str]}}.
Acceptance requires prior/A-only/B-only false and full true, plus supported gold/elements.
Visible dialogue: {_dump(visible)}
Candidate: {_dump(candidate)}
"""


def solver_prompt(visible: dict[str, Any]) -> str:
    return f"""Answer the user's final query using only the supplied conversation.
If the evidence is insufficient, explicitly abstain. Do not mention benchmark metadata.
Conversation input: {_dump(visible)}
"""


def score_prompt(answer: dict[str, Any], ground_truth: dict[str, Any]) -> str:
    return f"""Score a solver response against hidden ground truth. Return JSON:
{{"element_hits":[bool],"cited_evidence_count":0,"abstains":bool,
"asserts_absent_pattern":bool,"reason":str}}.
element_hits must align in order with required_elements; cite count is 0, 1, or 2.
Solver response: {_dump(answer)}
Ground truth: {_dump(ground_truth)}
"""
