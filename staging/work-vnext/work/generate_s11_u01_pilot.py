#!/usr/bin/env python3
"""Generate one hand-authored S11/U01 source triple for human review.

This pilot intentionally lives outside candidates-s11-s15-review/, whose prior
template-generated contents are rejected and must not be used for evaluation.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import generate_s1_s5_review_batch as base
from generate_s1_s5_review_batch import d, spec

HERE = Path(__file__).resolve().parent
OUT = HERE / "candidates-s11-s15-pilot"
AUDIT_PATH = HERE / "review" / "s11_u01_pilot_audit.json"
sys.path.insert(0, str(HERE.parents[2] / "experiments" / "assomem_vnext"))
from schema import render_arms, validate_candidate  # noqa: E402


S11_U01 = spec(
    "U01",
    "operations specialist",
    "cr",
    "conditional",
    ("supplier-status notes", "offsite reply", "operations desk", "handoff schedule"),
    d(
        "I took a twenty-minute walking catch-up after lunch and felt better afterward.",
        "So a short, low-stakes afternoon conversation is manageable?",
        "Usually. It is not the same as needing to stay switched on for hours.",
    ),
    d(
        "I went to last month's product-demo social because it lasted an hour and I could leave when I needed to.",
        "How did that go?",
        "Fine. It did not cost recovery time or collide with anything else.",
    ),
    d(
        "I agreed to cover the monitoring rotation next Tuesday night. If nothing escalates, handover ends Thursday at eleven, so I blocked Thursday morning for recovery.",
        "Is the block only for unusually difficult nights?",
        "No. I cannot know which rotation will be rough, so I protect the morning either way.",
    ),
    d(
        "Since I switched to the louder alarm for monitoring nights, my sleep has stayed unsettled. Even after a quiet shift I wake up braced for another alert.",
        "Are you back to normal the following day?",
        "Not really. I can do routine work, but I am foggy and need more recovery than I expected.",
    ),
    d(
        "The physio clinic had one opening this week: Thursday at 17:30 for the lower-back flare from overnight desk coverage, so I took it.",
        "Could you move it if something comes up?",
        "Not this week. The next opening is much later, and I have already delayed the treatment.",
    ),
    d(
        "I had coffee around three to finish the QBR slides and the palpitations were back by bedtime. I do not want to repeat that.",
        "Do you want a boundary for late coffee?",
        "Yes. No caffeine after two, even when a day is busy.",
    ),
    d(
        "Maya says the Thursday offsite is where the leadership team notices people and thinks I should confirm immediately.",
        "Visibility is not the same as whether the timing works.",
        "That is why I have not answered yet.",
    ),
    d(
        "The physio clinic can instead do a short telehealth check-in Friday morning, and the therapist says moving it does not delay treatment.",
        "So Thursday no longer carries the fixed appointment?",
        "Right. That would make the offsite question different.",
    ),
    "I just got this email: “Team offsite announced for Thursday afternoon, 14:00–16:30. Attendance expected. Please confirm.” What should I reply, and what should I prepare?",
    "Confirming the Thursday-afternoon offsite without accommodation is not supported for this user.",
    "request a remote, morning, or shorter alternative before confirming",
    "The user preserves capacity after overnight monitoring by holding recovery time, and the proposed afternoon also collides with scarce treatment; ongoing alarm-linked sleep disruption and the no-late-caffeine boundary rule out the obvious way to push through.",
    "The user can take short, bounded afternoon conversations and an optional one-hour social event after ordinary work.",
    "Those events have neither a post-rotation recovery demand nor a fixed treatment collision.",
    "Leadership visibility mentions the same offsite but says nothing about the user's recovery, treatment, sleep, or caffeine boundary.",
    (
        "overnight monitoring rotation",
        "cover alerts while preserving the next day's recovery",
        "accepted the rotation and blocked Thursday morning",
        "expects reduced capacity after an unpredictable night",
    ),
    (
        "Thursday physiotherapy booking",
        "treat the lower-back flare before it worsens",
        "kept the only available 17:30 appointment",
        "treatment would be delayed if the booking were lost",
    ),
)


def build_context(_sp: dict, _scenario_index: int, _user_index: int, user_id: str) -> list[dict]:
    """Place the hand-authored evidence in vNext's fixed 20-session slots."""
    start = datetime(2026, 8, 3, tzinfo=timezone.utc)
    dialogue_by_slot = {
        1: d(
            "I wrapped the supplier-status notes before lunch instead of leaving them for Friday.",
            "Did the shorter list make the afternoon easier to protect?",
            "Yes. I can see what actually needs a response now.",
        ),
        2: d(
            "The analytics group asked for a quick check on dashboard copy, so I gave comments in the document rather than adding another meeting.",
            "Was the written pass enough?",
            "For this one, yes. They only needed the wording tightened.",
        ),
        3: S11_U01["cx1"],
        4: d(
            "I moved the renewal spreadsheet into one tab per vendor.",
            "Easier to review?",
            "Much. I stop losing the small exceptions.",
        ),
        5: d(
            "I asked the team to send agenda questions before Wednesday planning.",
            "Why collect them beforehand?",
            "I make better decisions when I can sort dependencies before people start talking over each other.",
        ),
        6: S11_U01["a"],
        7: S11_U01["cx2"],
        8: d(
            "I turned off most group-chat badges for the weekend.",
            "Keeping only urgent alerts?",
            "Exactly. I do not want routine chatter to feel like an incident.",
        ),
        9: S11_U01["e1"],
        10: d(
            "I sent the client a concise update instead of trying to solve every question in one call.",
            "Did that lower the pressure?",
            "A lot. It gave me a clean next step.",
        ),
        11: d(
            "I asked Jamie to cover the first fifteen minutes of Friday's status call if I am delayed.",
            "Does that make the call less brittle?",
            "Yes. One small delay will not derail everyone.",
        ),
        12: d(
            "I drafted the offsite packing list but have not replied to the invite.",
            "What is still undecided?",
            "Whether the timing is realistic after the rotation.",
        ),
        13: d(
            "I finished the procurement notes before the afternoon got busy.",
            "Anything left that needs a decision?",
            "Just a small vendor question. I can handle it tomorrow.",
        ),
        14: S11_U01["b"],
        15: d(
            "I packed non-caffeinated tea for the monitoring night.",
            "Still holding the no-late-coffee rule?",
            "Yes. I would rather be slower than spend another night with my heart racing.",
        ),
        16: d(
            "The rotation was quieter than the last one, but the alarm still woke me twice.",
            "Are you keeping the morning open?",
            "Yes. I can handle handover and then need to reset before anything demanding.",
        ),
        17: S11_U01["e2"],
        18: S11_U01["lure"],
        19: d(
            "I wrote down the two possible offsite alternatives before replying.",
            "What are you considering?",
            "A morning slot or joining remotely for the part that needs me.",
        ),
        20: [{"role": "user", "content": S11_U01["query"]}],
    }
    sessions = []
    for session_id in range(1, 21):
        timestamp = start + timedelta(days=session_id - 1, hours=(8 + session_id) % 10)
        sessions.append({
            "session_id": session_id,
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:00Z"),
            "speaker_id": user_id,
            "speaker_label": "User",
            "dialogue": [dict(turn) for turn in dialogue_by_slot[session_id]],
        })
    return sessions


def main() -> int:
    base.FAMILY["S11"] = "offsite response under recovery, health, calendar, and messaging constraints"
    original_build_context = base.build_context
    base.build_context = build_context
    try:
        results = []
        for arm in ("associative", "distractor", "absence"):
            item = base.build_item("S11", 0, S11_U01, 0, arm)
            errors = validate_candidate(item)
            score, score_notes = base.score_item(item)
            results.append({
                "candidate_id": item["candidate_id"],
                "arm": arm,
                "score": score,
                "score_notes": score_notes,
                "schema_errors": errors,
            })
            if errors or score < 95:
                raise ValueError(f"{arm} rejected: {errors or score_notes}")
            path = OUT / arm / f"{item['candidate_id']}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        associative = json.loads(
            (OUT / "associative" / "AMB_WV_S11_U01_associative.json").read_text(encoding="utf-8")
        )
        rendered = render_arms(associative)
        if set(rendered) != {"full", "a_only", "b_only", "link_broken"}:
            raise ValueError(f"unexpected rendered arms: {sorted(rendered)}")
        AUDIT_PATH.write_text(json.dumps({
            "batch": "S11/U01 human-review pilot",
            "records": results,
            "rendered_arms": sorted(rendered),
            "status": "awaiting human approval before S11/U02 or S12-S15 authoring",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"PASS 3/3 source arms; rendered={sorted(rendered)}")
    finally:
        base.build_context = original_build_context
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
