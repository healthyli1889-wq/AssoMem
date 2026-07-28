"""Rewrite work-vNext B-prime so it severs the A-B contingency.

Why
---
The 200-pair work re-run gave Δ_mem +0.655 but Δ_assoc only +0.150, with the
link-broken arm still asserting the target on 77% of items. B-prime is not a
copy-paste of ev_B — it keeps just 22% of ev_B's distinctive vocabulary — but it
**removes the obstacle** instead of severing the contingency, and the target
proposition is about the arrangement, so it survives the fix. From S01_U01:

    target : "Taking the standing 06:00 incident bridge as currently run, with
              overnight notes arriving after it starts, is a poor fit for this user."
    B-prime: "The tooling change shipped: overnight notes now publish at 05:15, so
              the dependency picture is ready before the 06:00 bridge starts."

A solver can still answer yes: the bridge *as currently run* was a poor fit, and
here is the fix. ev_A plus the background carries that alone.

What this does
--------------
Each item's ev_A and ev_B carry complete `event_elements`. The relation is always
"the outcome of ev_B's situation depends on whether ev_A's action happened first".
So B-prime is rebuilt to say that the ev_B situation recurred both with and without
ev_A's action and the outcome did not track it — which is what DATA CRITERIA §0
means by preserving the user, chronology and session form while breaking the
connector.

It never mentions ev_B's outcome, so nothing about the removed episode leaks, and
it holds the turn count at ev_B's (3 everywhere in this batch).

    python3 rewrite_bprime.py --gold /tmp/work_data          # write bprime_v2.json
    python3 rewrite_bprime.py --gold /tmp/work_data --apply   # also patch in place

The patch is emitted as one JSON of pair_id -> replacement_dialogue so the change
is reviewable in a single file and the gold can stay owned by `main`.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# Trailing ordering words: ev_A actions often already end in "first"/"beforehand",
# and the template supplies its own ordering, so leaving them doubles the word.
TRAILING_ORDER = re.compile(
    r"\s+(first|beforehand|in advance|up front|ahead of time|before(?:hand)?)\s*$", re.I
)
ARTICLE = re.compile(r"^(the|a|an|my|our|his|her|their|this|that|these|those)\b", re.I)


def _action(text: str) -> str:
    """ev_A's action as a bare verb phrase usable after 'I'd ...'."""
    return TRAILING_ORDER.sub("", text.strip().rstrip(".")).strip()


def _situation(text: str) -> str:
    """ev_B's context as a noun phrase usable after 'been through ...'."""
    value = text.strip().rstrip(".")
    return value if ARTICLE.match(value) else f"the {value}"


def build(candidate: dict) -> list[dict[str, str]]:
    annotations = candidate["episode_annotations"]
    evidence = candidate["evidence"]
    a_elements = annotations[str(evidence["ev_A"]["session_id"])]["event_elements"]
    b_elements = annotations[str(evidence["ev_B"]["session_id"])]["event_elements"]
    action = _action(a_elements["action"])
    situation = _situation(b_elements["context"])
    return [
        {
            "role": "user",
            "content": (
                f"I've been through {situation} several more times since — some where "
                f"I'd {action} first, some where I hadn't — and how it went didn't "
                f"track that at all."
            ),
        },
        {"role": "assistant", "content": "so that isn't what decides it?"},
        {
            "role": "user",
            "content": (
                f"doesn't look like it. whether I'd {action} first turns out not to "
                f"change the outcome either way."
            ),
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, required=True, help="root holding associative/")
    parser.add_argument("--apply", action="store_true", help="patch the gold in place")
    parser.add_argument(
        "--out", type=Path, default=Path(__file__).resolve().parent / "bprime_v2.json"
    )
    args = parser.parse_args()

    patch: dict[str, list[dict[str, str]]] = {}
    problems: list[str] = []
    for path in sorted((args.gold / "associative").glob("*.json")):
        candidate = json.loads(path.read_text(encoding="utf-8"))
        original = candidate["link_broken"]["replacement_dialogue"]
        dialogue = build(candidate)
        if len(dialogue) != len(original):
            problems.append(f"{candidate['pair_id']}: turn count {len(dialogue)} != {len(original)}")
        # A B-prime that repeats ev_B's outcome would leak the removed episode. The
        # test is on the outcome's *distinctive* vocabulary: the template quotes
        # ev_A's action verbatim, and an action like "worked seated booth with
        # partner rotations" legitimately shares words with an outcome like "flare
        # that cost two booth days".
        annotations = candidate["episode_annotations"]
        b_outcome = annotations[str(candidate["evidence"]["ev_B"]["session_id"])][
            "event_elements"
        ]["outcome_or_affect"].lower()
        a_action = annotations[str(candidate["evidence"]["ev_A"]["session_id"])][
            "event_elements"
        ]["action"].lower()
        b_context = annotations[str(candidate["evidence"]["ev_B"]["session_id"])][
            "event_elements"
        ]["context"].lower()
        text = " ".join(turn["content"] for turn in dialogue).lower()
        distinctive = (
            set(re.findall(r"[a-z']{5,}", b_outcome))
            - set(re.findall(r"[a-z']{5,}", a_action))
            - set(re.findall(r"[a-z']{5,}", b_context))
        )
        if distinctive and len(distinctive & set(re.findall(r"[a-z']{5,}", text))) / len(
            distinctive
        ) > 0.4:
            problems.append(f"{candidate['pair_id']}: B-prime echoes ev_B's outcome")
        patch[candidate["pair_id"]] = dialogue
        if args.apply:
            candidate["link_broken"]["replacement_dialogue"] = dialogue
            path.write_text(
                json.dumps(candidate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )

    args.out.write_text(json.dumps(patch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"built {len(patch)} B-prime replacements -> {args.out}")
    if args.apply:
        print(f"applied in place under {args.gold}/associative")
    if problems:
        print(f"\n{len(problems)} problems:")
        for line in problems[:10]:
            print("   ", line)
        return 1
    print("no turn-count or outcome-leak problems")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
