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
restatement of this instruction. It must not be a dialogue/session object, transcript,
or metadata.
Conversation input: {_dump(visible)}
"""


def score_prompt(answer: dict[str, Any], ground_truth: dict[str, Any]) -> str:
    return f"""You are a strict benchmark annotator. Score the solver response using only
the hidden ground truth and evidence_contract. Do not award evidence credit for a
generic conclusion or unstated world knowledge.

Return exactly this JSON schema:
{{"conclusion_correct":bool,"recommendation_correct":bool,
"required_elements":[{{"hit":bool,"evidence_grounded":bool,"support":str}}],
"evidence_usage":{{"ev_A_used":bool,"ev_B_used":bool,"h_k":0,
"source_misattribution":bool}},"abstention":{{"abstains":bool,
"asserts_absent_pattern":bool}},"condition_correct":bool,
"failure_tags":[str],"reason":str}}.

Required-elements array must preserve the exact order and length of required_elements.
Set h_k to 0, 1, or 2 based only on evidence_contract facts explicitly quoted or
unambiguously paraphrased in the answer. A generic trait is not evidence usage.
Associative memory is person-bound: ev_A and ev_B support a user-specific conclusion
only when both facts belong to the same user. Semantic association between a user fact
and an other-person fact is not evidence for a conclusion about the user.
For expected_mode `answer`, condition_correct requires all required elements, an
evidence-grounded conclusion, and the required recommendation. For `abstain`,
condition_correct requires explicit withholding and no original personalized inference.
For `not_gold`, condition_correct requires withholding the original inference; mark
source_misattribution true whenever an other-person fact is treated as a user fact.
Solver response: {_dump(answer)}
Ground truth: {_dump(ground_truth)}
"""
