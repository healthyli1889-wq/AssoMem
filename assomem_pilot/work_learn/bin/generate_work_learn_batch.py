#!/usr/bin/env python3
"""Generate work/learning AssoMemBench batch for user1–9 (5/5/5 each).

user10 is migrated from pilot WL and is NOT overwritten here.
Layout: assomem_pilot/work/work_{arm}_user{N}/
Gold standard: DATA_STANDARD v1.
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]  # assomem_pilot
WL = Path(__file__).resolve().parents[1]  # work_learn
DATA = ROOT / "work"
PERSONAS = json.loads((WL / "personas" / "personas_work_learn.json").read_text())

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "so", "to", "of", "in", "on", "at",
    "for", "with", "about", "as", "by", "from", "is", "are", "was", "were", "be", "been",
    "i", "me", "my", "we", "you", "your", "it", "its", "this", "that", "do", "does", "did",
    "have", "has", "had", "will", "would", "can", "could", "should", "just", "really", "like",
    "get", "got", "also", "too", "very", "into", "out", "up", "what", "when", "where", "who",
    "how", "why", "there", "here", "them", "they", "their", "our", "im", "ive", "dont",
}
TOKEN_RE = re.compile(r"[a-z0-9']+")


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS and len(t) > 1]


def jaccard(a: str, b: str) -> float:
    sa, sb = set(tokenize(a)), set(tokenize(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def tfidf_vectors(docs: list[str]) -> list[dict[str, float]]:
    tokenized = [tokenize(d) for d in docs]
    df: Counter[str] = Counter()
    for toks in tokenized:
        df.update(set(toks))
    n = len(docs)
    vecs = []
    for toks in tokenized:
        tf = Counter(toks)
        length = len(toks) or 1
        vec = {}
        for term, count in tf.items():
            idf = math.log((n + 1) / (df[term] + 1)) + 1.0
            vec[term] = (count / length) * idf
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vecs.append({k: v / norm for k, v in vec.items()})
    return vecs


def cosine(u: dict[str, float], v: dict[str, float]) -> float:
    keys = set(u) & set(v)
    return sum(u[k] * v[k] for k in keys) if keys else 0.0


def count_tokens(context: list[dict]) -> int:
    payload = json.dumps(context, ensure_ascii=False)
    try:
        import tiktoken

        return len(tiktoken.get_encoding("cl100k_base").encode(payload))
    except Exception:
        return max(1, len(payload) // 4)


def sess_text(s: dict) -> str:
    return " ".join(t["content"] for t in s["dialogue"])


def scenario_cores() -> list[dict[str, Any]]:
    """Five A3 cores aligned with pilot WL distractor set (canonical for user1–9)."""
    return [
        {
            "sid": "S1",
            "name": "early_headache_x_late_deepwork",
            "forbidden": ["night_oriented_pattern", "evening chronotype", "would not thrive at 7am", "decline the standup"],
            "evolving": {"chronotype_pattern": "night_oriented_pattern"},
            "ev_A_fact": "Rising before 6am for early calls causes dull morning headaches that ease by noon.",
            "ev_B_fact": "The user's peak deep-work window is roughly midnight to 3am.",
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "morning_impairment", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "evening_peak", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "night_oriented_pattern", "hop": 2},
                {"source": "night_oriented_pattern", "relation": "constrains", "target": "answer_to_cue", "hop": 3},
            ],
            "required_assoc": [
                "cites early-rising headache fact",
                "cites late-night peak productivity",
                "recommendation negative or conditional for mandatory dawn standup",
            ],
        },
        {
            "sid": "S2",
            "name": "project_learning_x_video_dropout",
            "forbidden": ["always choose beta", "alpha is wrong", "learning style diagnosis"],
            "evolving": {"learning_mode": "build_first", "passive_video": "dropout"},
            "ev_A_fact": "User retains skills by building small projects, not by passive reading.",
            "ev_B_fact": "Long recorded lecture videos cause the user to zone out and quit courses.",
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "build_based_retention", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "lecture_dropout", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "prefer_lab_track", "hop": 2},
            ],
            "required_assoc": [
                "cites project-based learning preference",
                "cites lecture-video abandonment",
                "recommends lab/build track over long pre-recorded theory",
            ],
        },
        {
            "sid": "S3",
            "name": "afternoon_crash_x_late_workshop",
            "forbidden": ["ADHD diagnosis", "never take late meetings", "must decline workshop"],
            "evolving": {"post_lunch_dip": "severe_after_14h", "late_meeting_risk": "high"},
            "ev_A_fact": "After a morning coffee peak, the user crashes hard after 2pm and cannot sustain detailed review work.",
            "ev_B_fact": "A prior late-afternoon account review went poorly because the user was already cognitively empty.",
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "post_2pm_crash", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "late_slot_failure", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "avoid_late_workshop_block", "hop": 2},
            ],
            "required_assoc": [
                "cites post-2pm crash",
                "cites prior late afternoon meeting failure",
                "recommendation negative or time-shift conditional",
            ],
        },
        {
            "sid": "S4",
            "name": "handwriting_x_tablet_bootcamp",
            "forbidden": ["dyslexia diagnosis", "never use tablets", "must reject bootcamp"],
            "evolving": {"note_medium": "paper_handwriting", "digital_slate": "failed_pilot"},
            "ev_A_fact": "The user remembers material best when handwriting notes in a paper notebook.",
            "ev_B_fact": "A prior digital-slate study experiment failed; the user could not retain material.",
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "paper_retention", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "digital_fail", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "constrains", "target": "tablet_only_program", "hop": 2},
            ],
            "required_assoc": [
                "cites handwriting/notebook retention",
                "cites prior digital-slate / non-paper failure",
                "recommendation against tablet-only or requires paper accommodation",
            ],
        },
        {
            "sid": "S5",
            "name": "night_alert_x_sre_rotation",
            "forbidden": ["insomnia diagnosis", "never do on-call", "must reject SRE"],
            "evolving": {"sleep_fragility": "alert_sensitive", "night_continuity": "non_negotiable"},
            "ev_A_fact": "A prior night-alert stretch caused multi-night sleep disruption and lingering daytime impairment.",
            "ev_B_fact": "The user needs unbroken night sleep to stay effective; fragmented nights cascade into sloppy mistakes.",
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "alert_sleep_debt", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "work_quality", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "sre_nights_risky", "hop": 2},
            ],
            "required_assoc": [
                "cites prior night-alert / sleep disruption history",
                "cites unbroken-sleep requirement",
                "recommendation negative or heavily conditional",
            ],
        },
    ]


def paint_dialogues(persona: dict, core: dict, arm: str) -> dict[str, Any]:
    """V1-safe paints: evidence ~0 overlap with query; lure fillers share query surface."""
    voice = persona["voice"]
    paints = {
        "S1": {
            "fillers": [
                ("Repainted a shelf. Oddly satisfying.", "Small resets help."),
                ("Cleared a long email thread. Brain feels flat.", "Worth a short walk?"),
            ],
            # avoid: platform/pod/standup/7am/mandatory/thrive/manager
            "ev_A": [
                (
                    "Keep getting dull headaches when I am up before six for those early calls.",
                    "Do they fade later?",
                ),
                ("By noon I am fine. The early stretch is the problem.", None),
            ],
            "ev_B": [
                (
                    "It is past midnight and I just finished a clean refactor. This window is when my brain actually locks in.",
                    "Late focus can be powerful if you protect recovery somehow.",
                ),
                ("I sleep in on weekends to compensate.", None),
            ],
            "lures": [
                (
                    "Heard the platform pod runs a mandatory daily 7am standup — people asking who would thrive there.",
                    "Dawn standups are a specific culture signal. Just noting the rumor?",
                ),
                (
                    "Manager floated an internal move onto a team with a hard 7am check-in every day.",
                    "Calendar constraints like that change fit as much as the tech stack.",
                ),
            ],
            "distractor": (
                "I really love my current team though. Honestly I would do almost anything to work more closely with them — "
                "they are amazing. If a move kept me near that crew, I would be tempted to say yes just for the people.",
                "That kind of team bond is rare — worth protecting. Still, people-fit is not the same as schedule-fit.",
            ),
            "query": (
                "Manager offered a move onto the platform pod. They run a mandatory daily 7am standup and she asked "
                "if I would thrive there. Based on what you know about me, should I take it?"
            ),
            "gold_assoc": (
                "Probably not as-is despite liking people. Early rising already causes morning headaches and peak work "
                "happens late at night, so a mandatory 7am standup conflicts with known patterns. Negotiate flexible hours "
                "or decline rather than accepting unchanged."
            ),
            "gold_abs": (
                "Insufficient evidence about chronotype, early-call symptoms, or deep-work timing. Abstain from yes/no; "
                "ask how early mornings and late-night focus have gone historically."
            ),
        },
        "S2": {
            "fillers": [
                ("Sorted research PDFs into folders.", "Nice. Any deadline on that pile?"),
                ("Tried a new tea. Too floral.", "Back to the usual blend?"),
            ],
            # avoid: stipend/Track/Alpha/Beta/pre-recorded/lab/certificate
            "ev_A": [
                (
                    "Python finally stuck after I rebuilt a tiny ETL script myself. Tutorials alone never lasted.",
                    "Making something real is a strong teacher.",
                ),
                ("If I am not typing the solution, it fades.", None),
            ],
            "ev_B": [
                (
                    "Abandoned another course full of forty-minute talking-head recordings. I kept drifting and then felt lost.",
                    "Passive video can be brutal. Did any format work better before?",
                ),
                ("Short exercises with feedback. That is about it.", None),
            ],
            "lures": [
                (
                    "HR mailed two stipend options — Track Alpha is mostly pre-recorded theory modules; Track Beta is a live lab cohort.",
                    "Learning-budget choices often split theory vs build. Logging the options?",
                ),
                (
                    "A coworker said everyone picks the Alpha stipend track for the certificate prestige.",
                    "Prestige signals around course tracks are loud.",
                ),
            ],
            "distractor": (
                "A friend said Track Alpha is amazing — everyone at her company picks that stipend course track because "
                "the certificate looks great, even if the modules are long talking-head recordings.",
                "Prestige signals can be tempting. Is that driving your shortlist?",
            ),
            "query": (
                "For the stipend, should I pick Track Alpha (pre-recorded theory modules) or Track Beta "
                "(live lab cohort with weekly builds)? Friend says Alpha is amazing."
            ),
            "gold_assoc": (
                "Choose Track Beta despite the friend's Alpha praise. The user learns by building and abandons long "
                "talking-head recordings; certificate prestige is not evidence of retention fit."
            ),
            "gold_abs": (
                "Insufficient evidence about learning format preferences. Abstain; ask whether project-building vs "
                "long lecture videos have worked historically before recommending a stipend track."
            ),
        },
        "S3": {
            "fillers": [
                ("Fixed a bike light. Commute feels safer.", "Good maintenance habit."),
                ("Library was packed. Still finished two chapters.", "Solid focus given the noise."),
            ],
            # avoid: workshop/client/3:30/5:30/visibility/lead/recurring
            "ev_A": [
                (
                    "My coffee high dies after two o'clock. After that I am foggy and slow no matter what I drink.",
                    "That afternoon dip is common. Does it hit focus hard?",
                ),
                ("Yeah. Detailed reviews after that are a mess.", None),
            ],
            "ev_B": [
                (
                    "That 4pm account review last month was embarrassing. I lost the thread twice and someone else had to rescue the room.",
                    "Harsh memory. Was the material unfamiliar?",
                ),
                ("No, I knew it. I was just empty by then.", None),
            ],
            "lures": [
                (
                    "They want someone to lead a recurring late client workshop block from 3:30 to 5:30 — visibility talk everywhere.",
                    "Late facilitation slots are a common growth ask. Noting the invite?",
                ),
                (
                    "A senior keeps saying late client workshops are amazing for visibility if you want to grow.",
                    "Career-story framing around late blocks is persuasive on paper.",
                ),
            ],
            "distractor": (
                "A senior said late client workshops are amazing for visibility — if you want to grow, you should say yes "
                "to every late facilitation invite for the career story.",
                "Visibility advice is common. Does it match how you actually perform after mid-afternoon?",
            ),
            "query": (
                "They asked me to lead a recurring late client workshop block from 3:30 to 5:30. A senior said those "
                "workshops are amazing for visibility. Should I take it?"
            ),
            "gold_assoc": (
                "Lean no or renegotiate to a morning slot. The user crashes after 2pm and already failed a late account "
                "review while cognitively empty; career-visibility talk does not override that pattern."
            ),
            "gold_abs": (
                "Insufficient evidence about afternoon energy or prior late-meeting outcomes. Abstain; ask how post-2pm "
                "focus and late reviews have gone before advising on the workshop block."
            ),
        },
        "S4": {
            "fillers": [
                ("Reorganized notes for a seminar.", "That should speed retrieval later."),
                ("Watched a short documentary. Decent.", "Any takeaway worth keeping?"),
            ],
            # avoid: tablet/bootcamp/signup/upgrade/amazing
            "ev_A": [
                (
                    "Handwriting notes in my paper notebook is still how I remember anything. Typing feels like it slides off.",
                    "Motor memory helps a lot of learners. Do you rewrite summaries too?",
                ),
                ("Sometimes. The first pass on paper is the key.", None),
            ],
            "ev_B": [
                (
                    "That digital-slate highlighting experiment last fall was a disaster. I marked forever and still blanked on the quiz.",
                    "Frustrating when the tool fights your process.",
                ),
                ("I went back to paper the next week and scores jumped.", None),
            ],
            "lures": [
                (
                    "Classmates are pushing a tablet-only bootcamp signup — sleek app, automatic sync, everyone says the upgrade is amazing.",
                    "Digital-first program marketing is loud right now.",
                ),
                (
                    "Someone asked whether a tablet-only bootcamp is worth it versus keeping a paper notebook workflow.",
                    "Format fit matters more than the gadget story.",
                ),
            ],
            "distractor": (
                "A classmate said the tablet-only bootcamp is amazing — sleek app, automatic sync, and everyone says the "
                "upgrade is worth it; they made it sound like paper is outdated.",
                "Marketing around digital-first programs is loud. Does the format match how you study?",
            ),
            "query": (
                "Should I signup for the tablet-only bootcamp? People say the upgrade is amazing and worth it, "
                "but I want your read based on what you know about me."
            ),
            "gold_assoc": (
                "Do not choose the tablet-only bootcamp as-is. Handwritten notebook notes are how the user retains material, "
                "and a prior digital-slate pilot failed; marketing about an amazing upgrade is not retention evidence. "
                "Require a paper accommodation or pick another program."
            ),
            "gold_abs": (
                "Insufficient evidence about note-taking medium or prior digital study experiments. Abstain; ask how "
                "handwriting vs screen-only study has gone before advising on a tablet-only bootcamp."
            ),
        },
        "S5": {
            "fillers": [
                ("Bought new earphones. Commute is quieter.", "Helpful for focus blocks."),
                ("Cleared old downloads. Disk space returned.", "Future-you appreciates that."),
            ],
            # avoid: SRE/rotation/on-call/career/friend/amazing/promotion
            "ev_A": [
                (
                    "That two-week night-alert stretch last year wrecked me. I woke at every buzz and felt useless the next days.",
                    "Sleep debt from alerts is brutal. Did recovery take long?",
                ),
                ("Almost a month before I felt normal again.", None),
            ],
            "ev_B": [
                (
                    "If my night gets chopped up, the next day I ship sloppy mistakes. Unbroken sleep is non-negotiable for me.",
                    "That is important self-knowledge. Protecting sleep is protecting work quality.",
                ),
                ("Exactly. I schedule around it when I can.", None),
            ],
            "lures": [
                (
                    "Friend on an ops team said an SRE rotation offer is amazing — fast promotion path if you want career growth.",
                    "Prestige and growth stories around rotations are persuasive.",
                ),
                (
                    "People keep forwarding the SRE rotation blurb and brushing past the night-alert schedule.",
                    "Career upside and night duty often get sold together.",
                ),
            ],
            "distractor": (
                "A friend on the SRE team said the rotation offer is amazing — fast promotion path, you should take it "
                "if you want career growth. They mostly sold the upside and brushed past the nights.",
                "Prestige and growth stories are persuasive. How does the schedule sound to you?",
            ),
            "query": (
                "I got an SRE rotation offer. Friend says the team is amazing and I should take it for career growth. "
                "Based on what you know about me, should I?"
            ),
            "gold_assoc": (
                "Lean no unless nights are protected. A prior night-alert stretch caused multi-week impairment, and "
                "unbroken sleep is non-negotiable; friend prestige talk does not override that."
            ),
            "gold_abs": (
                "Insufficient evidence about sleep fragility or prior night-alert outcomes. Abstain; ask how fragmented "
                "nights and alert stretches have affected next-day work before advising on an SRE rotation."
            ),
        },
    }
    p = paints[core["sid"]]
    trait = persona["stable_traits"][0]

    sessions: list[dict] = []
    annotation: dict[str, Any] = {}
    sid = 1

    def add(role_setup: str, dialogue: list[dict], **meta: Any) -> None:
        nonlocal sid
        sessions.append(
            {
                "session_id": sid,
                "timestamp": f"2026-{1 + (sid // 3):02d}-{10 + sid:02d}T18:00:00Z",
                "dialogue": dialogue,
            }
        )
        annotation[str(sid)] = {"role_setup": role_setup, **meta}
        sid += 1

    f0, f1 = p["fillers"][0]
    add("filler", [{"role": "user", "content": f0}, {"role": "assistant", "content": f1}])
    add(
        "filler",
        [
            {"role": "user", "content": f"Work mode today felt very '{trait}' — long blocks, little slack."},
            {"role": "assistant", "content": f"Given that {voice.split(',')[0]} pace, worth protecting recovery tonight."},
        ],
    )

    target_ids: list[str] = []
    distractor_ids: list[str] = []

    if arm != "absence":
        ev_a = []
        for u, s in [(p["ev_A"][0][0], p["ev_A"][0][1]), (p["ev_A"][1][0], None)]:
            ev_a.append({"role": "user", "content": u})
            if s:
                ev_a.append({"role": "assistant", "content": s})
        add("target_evidence", ev_a, evidence_id="ev_A", atomic_fact=core["ev_A_fact"])
        target_ids.append("ev_A")

        add("filler", [{"role": "user", "content": p["fillers"][1][0]}, {"role": "assistant", "content": p["fillers"][1][1]}])

        ev_b = []
        for u, s in [(p["ev_B"][0][0], p["ev_B"][0][1]), (p["ev_B"][1][0], None)]:
            ev_b.append({"role": "user", "content": u})
            if s:
                ev_b.append({"role": "assistant", "content": s})
        add("target_evidence", ev_b, evidence_id="ev_B", atomic_fact=core["ev_B_fact"])
        target_ids.append("ev_B")
    else:
        for msg, resp in [
            ("Booked a short walk after lunch.", "Nice reset."),
            ("Inbox zero for an hour. Rare.", "Enjoy the quiet."),
            ("Tried a new grocery store. Fine.", "Any keepers?"),
        ]:
            add("filler", [{"role": "user", "content": msg}, {"role": "assistant", "content": resp}])

    for lu, la in p["lures"]:
        add(
            "filler",
            [{"role": "user", "content": lu}, {"role": "assistant", "content": la}],
            surface_lure=True,
            why_filler="Query-surface vocabulary only; no bodily/work-capacity causal facts (V1 flat-RAG decoy).",
        )

    if arm == "distractor":
        du, da = p["distractor"]
        add(
            "distractor",
            [{"role": "user", "content": du}, {"role": "assistant", "content": da}],
            distractor_id="dist_1",
            why_distractor=(
                "Shares decision vocabulary with the query (amazing / say yes / career / prestige / team love) "
                "but provides no capacity evidence; surface lure toward acceptance."
            ),
        )
        distractor_ids.append("dist_1")
    else:
        add("filler", [{"role": "user", "content": "Weather was grey. Stayed indoors."}, {"role": "assistant", "content": "Good day for quiet tasks."}])

    add("filler", [{"role": "user", "content": "Wrapped a small admin task."}, {"role": "assistant", "content": "One less open loop."}])
    add("associative_cue", [{"role": "user", "content": p["query"]}], cue_id="cue_1")

    gold = p["gold_abs"] if arm == "absence" else p["gold_assoc"]
    required = (
        ["states insufficient evidence / abstain", "does not invent the work-capacity causal pattern"]
        if arm == "absence"
        else list(core["required_assoc"])
    )
    if arm == "distractor":
        required = required + ["does not treat social/prestige distractor as decisive capacity evidence"]

    return {
        "sessions": sessions,
        "annotation": annotation,
        "target_ids": target_ids,
        "distractor_ids": distractor_ids,
        "query": p["query"],
        "gold": gold,
        "required": required,
        "links": [] if arm == "absence" else core["links"],
        "forbidden": core["forbidden"],
        "evolving": core["evolving"],
        "atype": "A5_absence_control" if arm == "absence" else "A3_cross_domain",
    }


def _cf(sample_id: str, arm: str, painted: dict) -> list[dict]:
    if arm == "absence":
        return [
            {
                "variant_id": f"{sample_id}_cf_add_evidence",
                "type": "evidence_added",
                "expected_gold": "associative recommendation becomes answerable",
            }
        ]
    ev_sids = [int(k) for k, v in painted["annotation"].items() if v.get("role_setup") == "target_evidence"]
    out = [
        {
            "variant_id": f"{sample_id}_cf_no_evidence",
            "type": "evidence_removed",
            "removed_session_ids": ev_sids,
            "expected_gold": "insufficient evidence / abstain",
        }
    ]
    if arm == "distractor":
        dist_sids = [int(k) for k, v in painted["annotation"].items() if v.get("role_setup") == "distractor"]
        out.append(
            {
                "variant_id": f"{sample_id}_cf_no_distractor",
                "type": "distractor_removed",
                "removed_session_ids": dist_sids,
                "expected_gold": "same associative recommendation, easier inhibition",
            }
        )
    return out


def assemble_item(persona: dict, core: dict, arm: str) -> dict[str, Any]:
    painted = paint_dialogues(persona, core, arm)
    context = []
    for s in painted["sessions"]:
        context.append(
            {
                "session_id": s["session_id"],
                "timestamp": s["timestamp"],
                "dialogue": [{"role": t["role"], "content": t["content"]} for t in s["dialogue"]],
            }
        )
    last_user = None
    for s in context:
        for t in s["dialogue"]:
            if t["role"] == "user":
                last_user = t["content"]
    assert last_user == painted["query"]

    uidx = persona["user_index"]
    sample_id = f"AMB_WL_u{uidx:02d}_{arm}_{core['sid']}"
    item = {
        "sample_id": sample_id,
        "source": "partner_generated",
        "status": "rendered",
        "association_type": painted["atype"],
        "domain_tags": ["work/career", "education/learning"],
        "pilot_arm": arm,
        "pilot_domain": "work_learning",
        "persona_source": {
            "corpus": persona["source_corpus"],
            "ref": persona["source_ref"],
            "display_name": persona["display_name"],
        },
        "context_length_tokens": 0,
        "persona": {
            "user_id": persona["user_id"],
            "stable_traits": persona["stable_traits"],
            "evolving_state": painted["evolving"],
        },
        "context": context,
        "query": painted["query"],
        "query_source": "final_turn",
        "gold_answer": painted["gold"],
        "required_elements": painted["required"],
        "target_evidence_ids": painted["target_ids"],
        "associative_cue_id": "cue_1",
        "distractor_ids": painted["distractor_ids"],
        "associative_links": painted["links"],
        "annotation": painted["annotation"],
        "latent_forbidden_phrases": painted["forbidden"],
        "counterfactual_variants": _cf(sample_id, arm, painted),
        "validity_metrics": {},
        "provenance": {
            "generator": "work_learn_batch_v1",
            "generated_by": "autoresearch_pilot",
            "persona_corpus": persona["source_corpus"],
            "persona_ref": persona["source_ref"],
            "scenario_id": core["sid"],
            "scenario_name": core["name"],
            "batch_id": PERSONAS["batch_id"],
            "standard": "DATA_STANDARD_v1",
        },
        "dataset_meta": {
            "human_verified_by": [],
            "iaa_cohort_kappa": None,
            "iaa_n_overlap": None,
            "reproduce": {
                "loader_rule": "serialize context dialogue role+content only; strip annotation/evolving_state",
                "metrics": [
                    "answer_vs_gold+required_elements",
                    "validity_metrics.flat_rag_hit_top3",
                    "distractor_cosine>=evidence_cosine for distractor arm",
                ],
            },
        },
    }
    item["context_length_tokens"] = count_tokens(item["context"])
    item["validity_metrics"] = compute_metrics(item)
    return item


def compute_metrics(item: dict) -> dict:
    query = item["query"]
    ann = item["annotation"]
    ev_docs, dist_docs = [], []
    target_sids, dist_sids = set(), set()
    for s in item["context"]:
        meta = ann.get(str(s["session_id"]), {})
        text = sess_text(s)
        if meta.get("role_setup") == "target_evidence":
            ev_docs.append(text)
            target_sids.add(s["session_id"])
        if meta.get("role_setup") == "distractor":
            dist_docs.append(text)
            dist_sids.add(s["session_id"])
    session_docs = [sess_text(s) for s in item["context"]]
    ev_concat = " ".join(ev_docs)
    lex = jaccard(query, ev_concat) if ev_concat else 0.0
    corpus = [query] + ev_docs + dist_docs + session_docs
    vecs = tfidf_vectors(corpus)
    qv = vecs[0]
    o = 1
    ev_cos = [cosine(qv, vecs[o + i]) for i in range(len(ev_docs))]
    o += len(ev_docs)
    dist_cos = [cosine(qv, vecs[o + i]) for i in range(len(dist_docs))]
    o += len(dist_docs)
    sess_cos = [cosine(qv, vecs[o + i]) for i in range(len(session_docs))]
    evidence_cosine = max(ev_cos) if ev_cos else 0.0
    distractor_cosine = max(dist_cos) if dist_cos else 0.0
    ranked = sorted(enumerate(sess_cos), key=lambda x: -x[1])
    top3 = {item["context"][i]["session_id"] for i, _ in ranked[:3]}
    flat_hit = bool(target_sids & top3) if target_sids else False
    return {
        "lexical_jaccard_query_evidence": round(lex, 4),
        "embed_cosine_query_evidence": round(evidence_cosine, 4),
        "flat_rag_hit_top3": flat_hit,
        "distractor_cosine_query": round(distractor_cosine, 4),
        "evidence_cosine_query": round(evidence_cosine, 4),
        "validity_method": {
            "embedder": "tfidf-local-proxy",
            "lexical": "jaccard-stopword-filtered",
            "computed_by": "work_learn/bin/generate_work_learn_batch.py",
            "computed_at": date.today().isoformat(),
        },
    }


def schema_errors(item: dict) -> list[str]:
    errs = []
    for s in item["context"]:
        for bad in ("evidence_id", "atomic_fact", "role_setup", "distractor_id", "why_distractor", "cue_id"):
            if bad in s:
                errs.append(f"leak {bad} in session {s['session_id']}")
        for t in s["dialogue"]:
            if set(t) - {"role", "content", "timestamp"}:
                errs.append(f"extra turn keys {sorted(t)}")
    last = None
    for s in item["context"]:
        for t in s["dialogue"]:
            if t["role"] == "user":
                last = t["content"]
    if item.get("query_source") == "final_turn" and last != item.get("query"):
        errs.append("query != final user turn")
    if not item.get("required_elements"):
        errs.append("empty required_elements")
    blob = " ".join(sess_text(s) for s in item["context"]).lower()
    for v in item.get("persona", {}).get("evolving_state", {}).values():
        s = str(v).lower()
        if len(s) >= 8 and s in blob:
            errs.append(f"evolving_state leaked: {v}")
    for phrase in item.get("latent_forbidden_phrases", []):
        if phrase.lower() in blob:
            errs.append(f"forbidden phrase in context: {phrase}")
    atype = item["association_type"]
    if atype.startswith("A5"):
        if any(m.get("role_setup") == "target_evidence" for m in item["annotation"].values()):
            errs.append("A5 has target_evidence")
        g = item["gold_answer"].lower()
        if not any(x in g for x in ("insufficient", "abstain", "cannot recommend", "can't")):
            errs.append("A5 gold not abstaining")
    return errs


def validity_errors(item: dict) -> list[str]:
    errs = []
    m = item["validity_metrics"]
    arm = item["pilot_arm"]
    if item["association_type"].startswith("A5"):
        return errs
    if not item["association_type"].startswith("A4"):
        if m["lexical_jaccard_query_evidence"] > 0.08:
            errs.append(f"V1 lex high {m['lexical_jaccard_query_evidence']}")
        if m["embed_cosine_query_evidence"] > 0.22:
            errs.append(f"V1 cos high {m['embed_cosine_query_evidence']}")
        if m["flat_rag_hit_top3"]:
            errs.append("V1 flat_rag_hit_top3")
    if arm == "distractor":
        if m["distractor_cosine_query"] < m["evidence_cosine_query"]:
            errs.append("V2 distractor < evidence")
        if not item.get("distractor_ids"):
            errs.append("missing distractor_ids")
    return errs


def folder_for(persona: dict, arm: str) -> Path:
    return DATA / f"work_{arm}_{persona['folder_tag']}"


def main() -> int:
    cores = scenario_cores()
    assert len(cores) == 5
    results = []
    n_fail = 0
    # only user1–9; user10 is migrated pilot
    for persona in PERSONAS["users"]:
        for arm in ("associative", "distractor", "absence"):
            out_dir = folder_for(persona, arm)
            out_dir.mkdir(parents=True, exist_ok=True)
            for core in cores:
                item = assemble_item(persona, core, arm)
                item["validity_metrics"] = compute_metrics(item)
                errs = schema_errors(item) + validity_errors(item)
                ok = not errs
                if not ok:
                    n_fail += 1
                path = out_dir / f"{item['sample_id']}.json"
                path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                results.append(
                    {
                        "sample_id": item["sample_id"],
                        "path": str(path.relative_to(ROOT)),
                        "arm": arm,
                        "user": persona["folder_tag"],
                        "pass": ok,
                        "errors": errs,
                        "metrics": item["validity_metrics"],
                    }
                )
                status = "PASS" if ok else "FAIL"
                print(f"{status}\t{item['sample_id']}\t{arm}\t{persona['folder_tag']}")
                for e in errs:
                    print(f"  - {e}")

    # include migrated user10 in manifest (validate only)
    u10_results = []
    for arm in ("associative", "distractor", "absence"):
        d = DATA / f"work_{arm}_user10"
        for path in sorted(d.glob("*.json")):
            item = json.loads(path.read_text())
            # recompute metrics with local gate for consistency
            try:
                item["validity_metrics"] = compute_metrics(item)
            except Exception as ex:
                u10_results.append({"sample_id": path.stem, "pass": False, "errors": [str(ex)], "arm": arm, "user": "user10", "path": str(path.relative_to(ROOT))})
                n_fail += 1
                continue
            errs = schema_errors(item) + validity_errors(item)
            # migrated items may have slightly different schema (no persona_source originally) — already added
            ok = not errs
            if not ok:
                n_fail += 1
            path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n")
            u10_results.append(
                {
                    "sample_id": item["sample_id"],
                    "path": str(path.relative_to(ROOT)),
                    "arm": arm,
                    "user": "user10",
                    "pass": ok,
                    "errors": errs,
                    "metrics": item["validity_metrics"],
                    "migrated": True,
                }
            )
            print(f"{'PASS' if ok else 'FAIL'}\t{item['sample_id']}\tmigrated\tuser10")
            for e in errs:
                print(f"  - {e}")

    all_results = results + u10_results
    jsonl = WL / "manifests" / "work_learn_batch_v1.jsonl"
    jsonl.parent.mkdir(parents=True, exist_ok=True)
    with jsonl.open("w", encoding="utf-8") as fh:
        for r in all_results:
            p = ROOT / r["path"]
            fh.write(json.dumps(json.loads(p.read_text()), ensure_ascii=False) + "\n")

    report = {
        "n": len(all_results),
        "n_pass": sum(1 for r in all_results if r["pass"]),
        "n_fail": n_fail,
        "n_generated_user1_9": len(results),
        "n_migrated_user10": len(u10_results),
        "by_arm": {
            a: sum(1 for r in all_results if r["arm"] == a and r["pass"]) for a in ("associative", "distractor", "absence")
        },
        "results": all_results,
    }
    (WL / "manifests" / "gate_report.json").write_text(json.dumps(report, indent=2) + "\n")
    tsv = ["sample_id\tuser\tarm\tstatus\terrors"]
    for r in all_results:
        tsv.append(
            f"{r['sample_id']}\t{r['user']}\t{r['arm']}\t{'keep' if r['pass'] else 'discard'}\t{'; '.join(r['errors'][:3]) or 'gate pass'}"
        )
    (WL / "manifests" / "results.tsv").write_text("\n".join(tsv) + "\n")
    print(f"\nSUMMARY {report['n_pass']}/{report['n']} PASS (generated {len(results)}, migrated {len(u10_results)})")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
