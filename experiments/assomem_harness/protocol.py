"""Strict prompt contracts for author, solver, and independent validator."""

from __future__ import annotations

import json
from typing import Any

from profile import DatasetProfile


def _dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def solver_prompt(visible: dict[str, Any], profile: DatasetProfile | None = None) -> str:
    if profile and profile.is_vnext():
        return f"""Decide whether the supplied conversation history supports `target_proposition`.

Return exactly one JSON object with exactly these keys:
{{"decision":"yes"|"no","answer":string,"evidence_session_ids":[integer]}}.

Answer `yes` only if specific dated episodes in this person's own history support
the proposition. Answer `no` if the history does not contain what the proposition
needs, even when the proposition sounds sensible in general: general social,
practical or common-sense plausibility is not evidence, and `no` does not assert
that the opposite is true.

Several sessions may look topically relevant without bearing on the proposition.
Cite in `evidence_session_ids` only the sessions your decision actually rests on,
and only IDs visible in the input. `answer` must briefly justify the decision by
reference to those sessions. Do not mention benchmark metadata or hidden labels.

Input: {_dump(visible)}
"""
    return f"""Answer the user's final query using only the supplied conversation.
If the evidence is insufficient, explicitly abstain. Do not mention benchmark metadata.
Return exactly one JSON object with exactly one key, `answer`. Its string value must
be your substantive answer to the user and must not be a placeholder, schema example,
restatement of this instruction. It must not be a dialogue/session object, transcript,
or metadata.
Conversation input: {_dump(visible)}
"""


def score_prompt(
    answer: dict[str, Any], ground_truth: dict[str, Any], profile: DatasetProfile | None = None
) -> str:
    if profile and profile.is_vnext():
        return f"""You are a strict benchmark annotator. Score the solver response against
the hidden binary target and its arm-specific requirements. Do not award credit for
world knowledge, generic advice, or evidence not visible in the arm.

Return exactly this JSON schema:
{{"binary_decision_correct":bool,"required_elements":[{{"hit":bool,
"evidence_grounded":bool,"support":str}}],"evidence_usage":{{"ev_A_used":bool,
"ev_B_used":bool,"h_k":0}},"abstention":{{"abstains":bool,
"asserts_absent_pattern":bool}},"source_misattribution":false,
"condition_correct":bool,"failure_tags":[str],"reason":str}}.

`condition_correct` requires the correct yes/no decision and all arm-specific
required elements. `h_k` is 0, 1, or 2 and counts only evidence explicitly cited or
unambiguously paraphrased from the visible input. With `withhold_C`, answer no and
do not assert the target proposition.
Solver response: {_dump(answer)}
Ground truth: {_dump(ground_truth)}
"""
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
For expected_mode `answer`, condition_correct requires all required elements, an
evidence-grounded conclusion, and the required recommendation. For `abstain`,
condition_correct requires explicit withholding and no original personalized inference.
For `not_gold`, condition_correct requires withholding the original inference; mark
source_misattribution true whenever a friend-sourced fact is treated as a user fact.
Solver response: {_dump(answer)}
Ground truth: {_dump(ground_truth)}
"""
