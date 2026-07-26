"""Strict prompt contracts for author, solver, and independent validator."""

from __future__ import annotations

import json
from typing import Any

from profile import DatasetProfile


def _dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def solver_prompt(visible: dict[str, Any], profile: DatasetProfile | None = None) -> str:
    if profile and profile.data_format == "work-vnext-1":
        model_input = {
            "context": visible["context"],
            "query": visible["query"],
        }
        return f"""Answer the user's query using only the supplied conversation.
If the visible memories do not justify a personalized answer, withhold it rather
than guessing. Do not assume or infer any hidden proposition.
Return exactly one JSON object with exactly these keys:
{{"mode":"answer"|"withhold","answer":string,"evidence_session_ids":[integer]}}.
`mode` is `answer` only when the visible memories support the substantive answer;
otherwise use `withhold`. `answer` must respond naturally to the query and briefly
explain the evidence boundary. Cite only visible session IDs. Do not mention
benchmark metadata, evaluation arms, hidden labels, or a target proposition.
Conversation input: {_dump(model_input)}
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
    answer: dict[str, Any],
    ground_truth: dict[str, Any],
    profile: DatasetProfile | None = None,
    *,
    visible: dict[str, Any] | None = None,
) -> str:
    if profile and profile.data_format == "work-vnext-1":
        if visible is None:
            raise ValueError("vNext validator prompt requires the solver-visible arm")
        validator_visible = {
            "context": visible["context"],
            "query": visible["query"],
        }
        return f"""You are a strict benchmark annotator. Score the solver response against
the hidden target proposition using the exact conversation that was visible to the
solver. Do not award credit for world knowledge, generic advice, removed evidence,
or evidence not visible in this arm.

Return exactly this JSON schema:
{{"target_asserted":bool,"target_evidence_grounded":bool,
"evidence_usage":{{"ev_A_used":bool,"ev_B_used":bool,"h_k":0,
"source_misattribution":bool}},"abstention":{{"abstains":bool,
"asserts_absent_pattern":bool}},
"condition_correct":bool,"failure_tags":[str],"reason":str}}.

`target_asserted` means the substantive answer, regardless of wording or polarity,
asserts the hidden target proposition. `target_evidence_grounded` is true only when
that assertion is supported by the visible conversation. `ev_A_used` and `ev_B_used`
refer only to the original target facts identified in the ground truth; a neutral
replacement or B-prime is not the removed original fact. `h_k` is 0, 1, or 2 and
counts original target facts explicitly cited or unambiguously paraphrased.
`condition_correct` requires a grounded target assertion for `infer_C`; for
`withhold_C`, it requires no target assertion and no use of evidence absent from
`allowed_evidence_ids`. A refusal to assert the target must not be interpreted as
asserting the opposite arrangement.
Solver-visible conversation: {_dump(validator_visible)}
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
