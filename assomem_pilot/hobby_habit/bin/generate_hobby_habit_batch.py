#!/usr/bin/env python3
"""Generate hobby/habit AssoMemBench batch for user1–9 (5/5/5 each).

Highest-mundane domain: everyday leisure tradeoffs where associative memory must
beat social FOMO and flat lexical RAG.

user10 is migrated from pilot HH and is NOT overwritten here.
Layout: assomem_pilot/hobby/hobby_{arm}_user{N}/
Gold standard: DATA_STANDARD v1 (format-consistent with health/ + work/).
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
HH = Path(__file__).resolve().parents[1]  # hobby_habit
DATA = ROOT / "hobby"
PERSONAS = json.loads((HH / "personas" / "personas_hobby_habit.json").read_text())

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
    """Five mundane A3 cores (aligned with pilot HH distractor set)."""
    return [
        {
            "sid": "S1",
            "name": "knee_incline_x_mountain_race",
            "forbidden": [
                "contraindicated_elevation_events",
                "incline_flare_prone",
                "skip the mountain race",
                "do not sign up for the race",
            ],
            "evolving": {"event_readiness": "contraindicated_elevation_events", "knee_pattern": "incline_flare_prone"},
            "ev_A_fact": "User jogs weekday mornings on flat park paths and feels knee discomfort on steeper neighborhood streets.",
            "ev_B_fact": "Clinic advised keeping elevation gentle for a couple of months.",
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "incline_knee_flare", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "elevation_load", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "poor_fit_steep_event", "hop": 2},
            ],
            "required_assoc": [
                "cites knee discomfort on steeper routes",
                "cites gentle-elevation clinic guidance",
                "recommends declining the mountain race (or heavily conditional)",
            ],
        },
        {
            "sid": "S2",
            "name": "budget_freeze_x_weekday_coastal_shoot",
            "forbidden": ["frozen_until_april", "weekend_mornings_only", "skip the coastal outing", "reject the borrowed body"],
            "evolving": {"gear_budget": "frozen_until_april", "daylight_window": "weekend_mornings_only"},
            "ev_A_fact": "Hobby spending frozen until April; developing at home; no new equipment.",
            "ev_B_fact": "Only outdoor shooting window is Saturday and Sunday mornings; weekday evenings indoors.",
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "gear_outlay", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "weekday_daylight", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "poor_fit_wednesday_coastal", "hop": 2},
            ],
            "required_assoc": [
                "cites spending freeze until April",
                "cites weekend-morning outdoor window",
                "recommends declining Wednesday coastal outing",
            ],
        },
        {
            "sid": "S3",
            "name": "batch_cook_x_standing_sunday_host",
            "forbidden": [
                "travel_disrupts_batch_cook",
                "poor_for_standing_dinners",
                "do not host Sunday dinner",
                "decline the standing dinner",
            ],
            "evolving": {"sunday_capacity": "travel_disrupts_batch_cook", "hosting_fit": "poor_for_standing_dinners"},
            "ev_A_fact": "Sunday batch cooking feeds the user for the work week.",
            "ev_B_fact": "Next several Sundays spent on trains visiting family; not home for kitchen block.",
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "meal_prep_load_bearing", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "home_kitchen_afternoons", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "cannot_host_standing_dinner", "hop": 2},
            ],
            "required_assoc": [
                "cites Sunday batch cooking / weekly meal-prep block",
                "cites Sunday family travel / not home",
                "recommends declining standing hosting",
            ],
        },
        {
            "sid": "S4",
            "name": "late_clay_x_predawn_bakery",
            "forbidden": [
                "pottery_vs_dawn_bakery",
                "pre_dawn_shift_protected",
                "drop the evening class",
                "do not add late studio nights",
            ],
            "evolving": {"schedule_conflict": "pottery_vs_dawn_bakery", "sleep_priority": "pre_dawn_shift_protected"},
            "ev_A_fact": "User's weekday wheel sessions at the studio often run past eleven and leave them wired.",
            "ev_B_fact": "User helps shape loaves before sunrise at a friend's shop and needs solid sleep the night before.",
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "late_wired_nights", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "prior_night_sleep", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "extra_late_class_conflicts", "hop": 2},
            ],
            "required_assoc": [
                "cites late studio wheel sessions",
                "cites pre-dawn shop/oven sleep need",
                "recommends against extra late class on those nights",
            ],
        },
        {
            "sid": "S5",
            "name": "home_games_x_roommate_quiet",
            "forbidden": [
                "roommate_quiet_constraint",
                "needs_quiet_or_elsewhere",
                "cancel loud game night",
                "do not host the party game night",
            ],
            "evolving": {"home_noise_budget": "roommate_quiet_constraint", "game_night_fit": "needs_quiet_or_elsewhere"},
            "ev_A_fact": "User regularly hosts small board game nights at home.",
            "ev_B_fact": "Roommate is noise-sensitive in the evenings and asks for quieter nights at the apartment.",
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "home_tabletop_habit", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "apartment_noise", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "loud_party_poor_fit", "hop": 2},
            ],
            "required_assoc": [
                "cites home board game hosting habit",
                "cites roommate evening noise sensitivity",
                "recommends against loud party hosting at home (or relocate/quiet format)",
            ],
        },
    ]


def paint_dialogues(persona: dict, core: dict, arm: str) -> dict[str, Any]:
    """Mundane paints: evidence ~0 overlap with query; lure fillers share FOMO/signup surface."""
    voice = persona["voice"]
    paints = {
        "S1": {
            "fillers": [
                ("Watered the balcony herbs. Basil is finally upright.", "Small wins count."),
                ("Resoled my walking shoes. Feels less slapdash.", "Good maintenance habit."),
            ],
            # avoid: mountain/race/signup/team/coworker/amazing
            "ev_A": [
                (
                    "Weekday mornings I stick to a flat park loop. When I cut through steeper neighborhood streets, my right knee starts complaining.",
                    "Flat comfort plus steeper-street discomfort points to incline load as the trigger.",
                ),
                ("Yeah. Soft paths are fine; the hills are not.", None),
            ],
            "ev_B": [
                (
                    "Clinic visit this week: keep elevation gentle for the next couple of months while things settle.",
                    "Clear constraint. Gentle elevation for a couple of months while you keep moving on softer surfaces.",
                ),
                ("I am treating that as non-negotiable.", None),
            ],
            "lures": [
                (
                    "Coworker group chat is hyping a mountain race signup this month — everyone saying it is amazing for the team.",
                    "Signup FOMO around trail events is loud. Just noting the pressure?",
                ),
                (
                    "Someone asked if joining the mountain race team is worth it for networking.",
                    "Networking and elevation load are different questions.",
                ),
            ],
            "distractor": (
                "My coworker is hyping a flat charity 5K race signup for their fundraising team. They keep saying the race "
                "is amazing and asking if joining the team is worth it for networking. I do not care about the fundraising angle.",
                "If the value is only networking, treat it as optional social time, not training advice. A flat charity race "
                "can be a yes for people reasons and still be unrelated to your incline limits.",
            ),
            "query": (
                "A coworker says a mountain race signup this month is amazing and wants me on the team. "
                "Should I? Is it worth it?"
            ),
            "gold_assoc": (
                "Decline. Your steeper-street knee pattern and the clinic's gentle-elevation guidance make a mountain race "
                "a poor fit. The flat charity 5K chatter is unrelated social noise."
            ),
            "gold_abs": (
                "Insufficient evidence about knee response to inclines or any clinical elevation guidance. Abstain; ask how "
                "steeper routes and recovery advice have gone before advising on a mountain race signup."
            ),
        },
        "S2": {
            "fillers": [
                ("Sorted old negatives into sleeves. Dusty but satisfying.", "Archive days feel good."),
                ("Tried a new tea while editing. Too floral.", "Back to the usual blend?"),
            ],
            # avoid: Wednesday/coastal/borrowed/high-end/body/outing/upgrade
            "ev_A": [
                (
                    "I am developing rolls at home. Hobby spending is frozen until April, so no new equipment before then.",
                    "A freeze until April is a hard budget boundary. Use what you already own.",
                ),
                ("Exactly. No impulse gear until then.", None),
            ],
            "ev_B": [
                (
                    "Weekday evenings I am indoors. My only outdoor shooting window is Saturday and Sunday mornings before winter light dies.",
                    "Weekend mornings are your scarce outdoor resource.",
                ),
                ("Midweek daylight is basically gone for me.", None),
            ],
            "lures": [
                (
                    "Someone floated a Wednesday coastal outing with a borrowed high-end body — friend said similar trips are amazing.",
                    "Daylight + gear FOMO often travel together. Logging the invite?",
                ),
                (
                    "Group chat keeps asking whether that upgrade-style coastal trip is worth it right now.",
                    "Worth-it talk can drown out calendar and budget facts.",
                ),
            ],
            "distractor": (
                "A friend said the museum gift-shop compact camera upgrade is amazing and that a spontaneous city trip with it "
                "is worth it. They want me to buy one for a tourist afternoon. I do not need another compact point-and-shoot.",
                "Gift-shop upgrades are usually impulse pricing. A tourist afternoon does not require a new compact body if you already have something that works.",
            ),
            "query": (
                "Someone offered a Wednesday coastal outing with a borrowed high-end body. Friend said similar trips are amazing. "
                "Is the upgrade-style trip worth it for me right now?"
            ),
            "gold_assoc": (
                "No. Your spending freeze until April and weekend-only outdoor window conflict with a Wednesday coastal outing. "
                "The gift-shop compact upgrade chatter is unrelated impulse talk."
            ),
            "gold_abs": (
                "Insufficient evidence about hobby budget freezes or outdoor shooting windows. Abstain; ask about spending "
                "constraints and when outdoor light is actually available before advising on a midweek coastal shoot."
            ),
        },
        "S3": {
            "fillers": [
                ("Wiped down the spice rack. Oddly calming.", "Kitchen resets help."),
                ("Put a reminder to buy rice. Staples again.", "Boring and useful."),
            ],
            # avoid query nouns: neighbor/standing/building/host/dinner/amazing — also minimize "Sunday" in evidence
            "ev_A": [
                (
                    "My weekly meal-prep block is how I eat all week. Skip it and I am buying takeout by midweek.",
                    "That block is load-bearing. Protect it from optional social cooking plans.",
                ),
                ("It is not optional for me.", None),
            ],
            "ev_B": [
                (
                    "For the next several weeks I will be on trains visiting family on my usual kitchen afternoon, so I will not be home.",
                    "Anything that assumes you are home those afternoons needs another plan.",
                ),
                ("Travel already ate that slot.", None),
            ],
            "lures": [
                (
                    "Neighbor wants me to host a standing Sunday dinner for our building — friend said it would be amazing.",
                    "Standing hosting invites are sticky. Just noting the ask?",
                ),
                (
                    "Building chat is full of Sunday dinner hosting FOMO. Everyone asking who will say yes.",
                    "Social pressure around hosting can outrun capacity.",
                ),
            ],
            "distractor": (
                "A friend said a prix-fixe Sunday dinner signup at a restaurant across town is amazing and asked if it is worth it. "
                "Should I grab a seat for that one night? I am not hosting anything.",
                "A one-night restaurant signup is just a reservation decision. Judge it on cost and travel time that evening, not on whether you want to become a host.",
            ),
            "query": (
                "My neighbor wants me to host a standing Sunday dinner for our building. Friend said it would be amazing. "
                "Should I say yes — is it worth it?"
            ),
            "gold_assoc": (
                "No. Weekly meal-prep and multi-week family travel leave no capacity to host a standing building dinner. "
                "The restaurant prix-fixe signup talk is a different, one-off decision."
            ),
            "gold_abs": (
                "Insufficient evidence about meal-prep habits or weekend travel. Abstain; ask whether weekly cooking blocks "
                "and upcoming family travel leave room before advising on standing Sunday hosting."
            ),
        },
        "S4": {
            "fillers": [
                ("Rinsed clay tools. Sink is less tragic.", "Future-you thanks you."),
                ("Folded laundry while a podcast played.", "Parallel chores work."),
            ],
            # avoid: studio/class/signup/bakery/late evening/amazing
            "ev_A": [
                (
                    "My weekday clay sessions on the wheel often run past eleven. I get home wired and it takes a while to settle.",
                    "Nights that run past eleven can push bedtime later even when the making itself is enjoyable.",
                ),
                ("The making is fun; the clock is not.", None),
            ],
            "ev_B": [
                (
                    "A few times a week I help shape loaves before sunrise at a friend's shop. I need solid sleep the night before or I am useless at the oven.",
                    "Pre-dawn oven shifts make the prior night non-negotiable.",
                ),
                ("Staying up late beforehand taxes that hard.", None),
            ],
            "lures": [
                (
                    "The studio opened another late evening class signup on nights before my bakery mornings — friends saying it is amazing.",
                    "Extra late slots look fun until they collide with dawn shifts.",
                ),
                (
                    "Someone asked whether adding that late evening class is worth it given bakery mornings the next day.",
                    "Worth-it talk often ignores the sleep math.",
                ),
            ],
            "distractor": (
                "A friend said a weekend glaze workshop signup is amazing and asked if the class is worth it. Should I grab "
                "that one tourist-style ticket? It is not my regular evening studio.",
                "Treat a one-off weekend workshop signup as a fun ticket decision. It does not automatically say anything about your recurring evening schedule.",
            ),
            "query": (
                "The studio opened another late evening class signup on nights before my bakery mornings. Friend said it is amazing. "
                "Should I add it — is it worth it?"
            ),
            "gold_assoc": (
                "Do not add it. Weekday wheel sessions already run past eleven, and pre-dawn loaf shifts need solid sleep the night "
                "before. An extra late evening class on those nights conflicts. The weekend glaze workshop is a different, one-off ticket."
            ),
            "gold_abs": (
                "Insufficient evidence about late clay sessions or pre-dawn bakery shifts. Abstain; ask how late making nights "
                "and next-morning oven duties have interacted before advising on another late class signup."
            ),
        },
        "S5": {
            "fillers": [
                ("Wiped the game-shelf dust. Cards look less sticky.", "Tiny resets help."),
                ("Bought snacks for later. Nothing fancy.", "Prepared enough."),
            ],
            # avoid: loud/party/signup/amazing/friends want me to host
            "ev_A": [
                (
                    "I like hosting small tabletop nights at home every couple of weeks. It is my main social hobby.",
                    "Home hosting is a real social outlet. Keep the format compatible with whoever shares the space.",
                ),
                ("Quiet games work well for me.", None),
            ],
            "ev_B": [
                (
                    "My roommate is sensitive to noise after dinner and asked me to keep apartment evenings calmer, especially with groups.",
                    "That is a hard household constraint. High-volume group nights at home will create conflict.",
                ),
                ("I do not want to blow up the household over one night.", None),
            ],
            "lures": [
                (
                    "Friends want me to host a loud party-game night signup at my place — they said it would be amazing.",
                    "Hosting FOMO can outrun roommate constraints.",
                ),
                (
                    "Group chat keeps asking if a loud party-game night at the apartment is worth it.",
                    "Worth-it for guests is not the same as worth-it for the household.",
                ),
            ],
            "distractor": (
                "A friend said a board-game cafe game night signup is amazing and asked if that public event is worth it. "
                "Should I grab a ticket? It is not at my apartment.",
                "A cafe game night signup is just an outing ticket. Judge noise and cost for that venue, not your apartment rules.",
            ),
            "query": (
                "Friends want me to host a loud party-game night signup at my place. They said it would be amazing. "
                "Should I — is it worth it?"
            ),
            "gold_assoc": (
                "Host somewhere else or pick a quiet game. You like home tabletop nights, but your roommate needs quieter evenings, "
                "so a loud party-game night at the apartment is a poor fit. The cafe ticket discussion is a different outing."
            ),
            "gold_abs": (
                "Insufficient evidence about home hosting habits or roommate noise constraints. Abstain; ask how apartment "
                "evenings and shared-space rules have gone before advising on a loud party-game night at home."
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
            {"role": "user", "content": f"Hobby mode today felt very '{trait}' — small routines, no drama."},
            {"role": "assistant", "content": f"Given that {voice.split(',')[0]} pace, protecting the quiet habits is reasonable."},
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
            ("Took a short walk after lunch.", "Nice reset."),
            ("Inbox quieter for an hour.", "Enjoy the gap."),
            ("Reorganized a drawer. Fine.", "One less sticky spot."),
        ]:
            add("filler", [{"role": "user", "content": msg}, {"role": "assistant", "content": resp}])

    for lu, la in p["lures"]:
        add(
            "filler",
            [{"role": "user", "content": lu}, {"role": "assistant", "content": la}],
            surface_lure=True,
            why_filler="Query-surface FOMO/signup vocabulary only; no capacity causal facts (V1 flat-RAG decoy).",
        )

    if arm == "distractor":
        du, da = p["distractor"]
        add(
            "distractor",
            [{"role": "user", "content": du}, {"role": "assistant", "content": da}],
            distractor_id="dist_1",
            why_distractor=(
                "Shares decision vocabulary (amazing / worth it / signup) but is a different mundane decision "
                "(flat 5K / gift-shop camera / restaurant seat / weekend workshop / cafe ticket); not capacity evidence for the cue."
            ),
        )
        distractor_ids.append("dist_1")
    else:
        add(
            "filler",
            [{"role": "user", "content": "Sky was grey. Stayed in with a book."}, {"role": "assistant", "content": "Quiet evening material."}],
        )

    add("filler", [{"role": "user", "content": "Put away a mug. Tiny close."}, {"role": "assistant", "content": "One less open loop."}])
    add("associative_cue", [{"role": "user", "content": p["query"]}], cue_id="cue_1")

    gold = p["gold_abs"] if arm == "absence" else p["gold_assoc"]
    required = (
        ["states insufficient evidence / abstain", "does not invent the hobby/habit capacity pattern"]
        if arm == "absence"
        else list(core["required_assoc"])
    )
    if arm == "distractor":
        required = required + ["does not treat near-miss FOMO distractor as decisive capacity evidence"]

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
    sample_id = f"AMB_HH_u{uidx:02d}_{arm}_{core['sid']}"
    item = {
        "sample_id": sample_id,
        "source": "partner_generated",
        "status": "rendered",
        "association_type": painted["atype"],
        "domain_tags": ["hobby/leisure", "daily_habits"],
        "pilot_arm": arm,
        "pilot_domain": "hobby_habit",
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
            "generator": "hobby_habit_batch_v1",
            "generated_by": "autoresearch_pilot",
            "persona_corpus": persona["source_corpus"],
            "persona_ref": persona["source_ref"],
            "scenario_id": core["sid"],
            "scenario_name": core["name"],
            "batch_id": PERSONAS["batch_id"],
            "standard": "DATA_STANDARD_v1",
            "domain_note": "highest_mundane_priority",
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
    target_sids = set()
    for s in item["context"]:
        meta = ann.get(str(s["session_id"]), {})
        text = sess_text(s)
        if meta.get("role_setup") == "target_evidence":
            ev_docs.append(text)
            target_sids.add(s["session_id"])
        if meta.get("role_setup") == "distractor":
            dist_docs.append(text)
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
            "computed_by": "hobby_habit/bin/generate_hobby_habit_batch.py",
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
        if not any(x in g for x in ("insufficient", "abstain", "cannot recommend", "can't", "not enough evidence")):
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
    return DATA / f"hobby_{arm}_{persona['folder_tag']}"


def main() -> int:
    cores = scenario_cores()
    assert len(cores) == 5
    results = []
    n_fail = 0
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

    u10_results = []
    for arm in ("associative", "distractor", "absence"):
        d = DATA / f"hobby_{arm}_user10"
        for path in sorted(d.glob("*.json")):
            item = json.loads(path.read_text())
            item["validity_metrics"] = compute_metrics(item)
            errs = schema_errors(item) + validity_errors(item)
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
    jsonl = HH / "manifests" / "hobby_habit_batch_v1.jsonl"
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
    (HH / "manifests" / "gate_report.json").write_text(json.dumps(report, indent=2) + "\n")
    tsv = ["sample_id\tuser\tarm\tstatus\terrors"]
    for r in all_results:
        tsv.append(
            f"{r['sample_id']}\t{r['user']}\t{r['arm']}\t{'keep' if r['pass'] else 'discard'}\t{'; '.join(r['errors'][:3]) or 'gate pass'}"
        )
    (HH / "manifests" / "results.tsv").write_text("\n".join(tsv) + "\n")
    print(f"\nSUMMARY {report['n_pass']}/{report['n']} PASS (generated {len(results)}, migrated {len(u10_results)})")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
