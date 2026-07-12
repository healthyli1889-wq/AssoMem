#!/usr/bin/env python3
"""Generate health/diet AssoMemBench batch: 10 users × 15 items (5/5/5).

Gold standard: DATA_STANDARD v1.
Arms: associative (A3), distractor (A3+V2), absence (A5).
Writes under data/diet_{arm}_user{N}/ and stamps validity_metrics.
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]  # assomem_pilot
HD = Path(__file__).resolve().parents[1]  # health_diet (generator + personas + manifests)
# User-facing item layout: assomem_pilot/health/diet_{arm}_user{N}/
DATA = ROOT / "health"
PERSONAS = json.loads((HD / "personas" / "personas_health_diet.json").read_text())

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


# ─── 5 health/diet A3 scenario cores (shared logic; persona paints surface) ──


def scenario_cores() -> list[dict[str, Any]]:
    """Five distinct A3 cores. Evidence domains ≠ query decision domain."""
    return [
        {
            "sid": "S1",
            "name": "dairy_reaction_x_late_social",
            "latent": "avoid_early_dairy_tasting",
            "forbidden": ["lactose intolerant label", "dairy avoidance rule", "do not go to cheese tasting"],
            "evolving": {"gi_trigger": "dairy_cream_heavy", "social_peak": "late_evening"},
            "ev_A_fact": "Cream-heavy dairy in the morning causes bloating and fogginess within an hour.",
            "ev_B_fact": "User's social energy and appetite peak after 9pm, not early morning.",
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "morning_dairy_impairment", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "late_social_appetite", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "poor_fit_early_cheese_event", "hop": 2},
                {"source": "poor_fit_early_cheese_event", "relation": "constrains", "target": "answer_to_cue", "hop": 3},
            ],
            "required_assoc": [
                "cites cream/dairy morning symptom pattern",
                "cites late-evening social/appetite pattern",
                "recommendation is negative or conditional for early cheese tasting",
            ],
        },
        {
            "sid": "S2",
            "name": "afternoon_caffeine_x_sleep",
            "latent": "block_late_stimulant_before_early_duty",
            "forbidden": ["caffeine curfew rule", "stimulant ban after noon", "will fail the morning duty"],
            "evolving": {"stimulant_cutoff": "post_14h_fragile", "sleep_dependency": "high"},
            "ev_A_fact": "Caffeine after mid-afternoon delays sleep onset and fragments the night.",
            "ev_B_fact": "After a fragmented night, next-morning focus collapses on demanding tasks.",
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "sleep_fragmentation", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "morning_focus_collapse", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "late_stimulant_harms_early_duty", "hop": 2},
            ],
            "required_assoc": [
                "cites post-afternoon caffeine sleep effect",
                "cites fragmented-night morning focus cost",
                "recommendation against late stimulant before early duty (or heavily conditional)",
            ],
        },
        {
            "sid": "S3",
            "name": "sodium_migraine_x_ramen",
            "latent": "decline_high_sodium_challenge",
            "forbidden": ["sodium migraine diagnosis", "never eat ramen", "must decline ramen crawl"],
            "evolving": {"sodium_sensitivity": "migraine_linked", "recovery_cost": "half_day"},
            "ev_A_fact": "Very high-sodium meals are followed by migraine-like headaches within hours.",
            "ev_B_fact": "After those headaches, the user loses half a workday of usable focus.",
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "post_sodium_headache", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "next_day_capacity", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "high_sodium_social_risk", "hop": 2},
            ],
            "required_assoc": [
                "cites high-sodium → headache pattern",
                "cites half-day focus loss after headaches",
                "recommendation against all-you-can-eat high-sodium crawl as-is (or conditional alternative)",
            ],
        },
        {
            "sid": "S4",
            "name": "skip_breakfast_x_pastry_workshop",
            "latent": "need_protein_before_long_morning",
            "forbidden": ["hypoglycemia diagnosis", "must never skip breakfast", "pastry workshop forbidden"],
            "evolving": {"morning_fuel": "protein_dependent", "sugar_only_crash": True},
            "ev_A_fact": "Skipping a real morning meal leads to a sharp mid-morning energy crash.",
            "ev_B_fact": "Pastry-only mornings produce a crash without lasting satiety for the user.",
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "midmorning_crash", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "pastry_insufficient_fuel", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "constrains", "target": "workshop_fueling_plan", "hop": 2},
            ],
            "required_assoc": [
                "cites skip-meal mid-morning crash",
                "cites pastry-only insufficiency",
                "recommends adding substantial fuel / not relying on pastry table alone",
            ],
        },
        {
            "sid": "S5",
            "name": "spicy_reflux_x_early_call",
            "latent": "avoid_late_spicy_before_early_call",
            "forbidden": ["GERD diagnosis", "spicy food ban", "must cancel the call"],
            "evolving": {"night_reflux_trigger": "spicy_late", "early_voice_quality": "fragile"},
            "ev_A_fact": "Spicy dinners close to bedtime trigger night reflux and poor sleep.",
            "ev_B_fact": "After reflux nights, morning voice and composure are unreliable on early calls.",
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "night_reflux", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "morning_voice_impairment", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "late_spicy_harms_early_call", "hop": 2},
            ],
            "required_assoc": [
                "cites late spicy → night reflux/sleep hit",
                "cites morning voice/composure cost",
                "recommendation against late spicy feast before early call (or milder alternative)",
            ],
        },
    ]


def paint_dialogues(persona: dict, core: dict, arm: str) -> dict[str, Any]:
    """Persona-colored dialogues for one scenario×arm. Lexically careful for V1/V2.

    V1 design (matches pilot):
    - Evidence text must share ~0 content tokens with the query (paraphrase bodily facts).
    - Add ≥2 surface-lure fillers that share query decision vocabulary so TF-IDF top-3
      is occupied by cue + lures, not target_evidence (cue always ranks #1).
    - Distractor arm: labeled distractor carries the same surface lure (V2 ≥ evidence).
    """
    voice = persona["voice"]
    uid = persona["user_id"]
    # Evidence nouns stay OUT of query; lure fillers share query surface only.
    paints = {
        "S1": {
            "fillers": [
                ("Repainted a shelf in the kitchen. Oddly satisfying.", "Small resets help. Keeping the project going?"),
                ("Finished a long email thread. Brain feels flat.", "Worth a short walk before the next block?"),
            ],
            # Zero overlap with query tokens: tasting/cheeses/cream/networking/artisan/8am
            "ev_A": [
                (
                    "Weird pattern — if I start the day with a rich milk-fat plate, I get bloated and foggy within about an hour.",
                    "That sounds unpleasant. Does it clear later?",
                ),
                ("Yeah by late morning I'm fine. It's specifically that early milk-fat load that wrecks me.", None),
            ],
            "ev_B": [
                (
                    "Honestly my social battery and real appetite only show up after nine. Pre-noon gatherings feel forced.",
                    "So evenings are when you actually enjoy food with people?",
                ),
                ("Exactly. Pre-noon food events feel like a different person.", None),
            ],
            "lures": [
                (
                    "Saw a flyer for an artisan tasting with soft cheeses — mostly networking talk on the invite.",
                    "Sounds like a food-forward mixer. Are you collecting invites like that?",
                ),
                (
                    "Someone asked if I'd go to an 8am cheese-and-cream bites event for networking. Pure logistics chat.",
                    "Early food mixers are a specific kind of calendar item.",
                ),
            ],
            "distractor": (
                "A friend said the downtown artisan tasting club is amazing for networking and that I should say yes "
                "to every soft-cheese / cream-based bites invite if I want to grow my circle.",
                "Networking pressure around tasting invites is real. Does that match how your body handles those mornings?",
            ),
            "query": "There's an 8am artisan tasting tomorrow — mostly soft cheeses and cream-based bites, plus networking. Should I go?",
            "gold_assoc": (
                "Lean no, or go only with a clear dairy-light plan. Morning cream-heavy foods have triggered bloating/fog within an hour, "
                "and social appetite peaks late evening — an 8am cheese/cream tasting is a poor fit. Suggest a later non-dairy meetup instead."
            ),
            "gold_abs": (
                "Insufficient evidence. Prior chats do not establish morning dairy tolerance or timing preferences for food events. "
                "Abstain from yes/no; ask about past reactions to cream-heavy breakfasts and early social meals."
            ),
        },
        "S2": {
            "fillers": [
                ("Sorted research PDFs into folders. Feels cleaner.", "Nice. Any deadline attached to that pile?"),
                ("Tried a new tea. Too floral.", "Back to the usual blend then?"),
            ],
            # Avoid: energy/drink/strong/8am/session/prep/slides/tonight
            "ev_A": [
                (
                    "If I take a potent stimulant after mid-afternoon, I don't fall asleep on time and the night gets chopped up.",
                    "Does that show up the next day?",
                ),
                ("Always. The night itself is the first casualty.", None),
            ],
            "ev_B": [
                (
                    "After a chopped-up night I'm useless on anything that needs sharp dawn focus — details just slip.",
                    "So recovery sleep is load-bearing for early demanding work.",
                ),
                ("Yes. I can't fake it with willpower.", None),
            ],
            "lures": [
                (
                    "Friends keep hyping a strong energy drink during evening slide prep before a high-stakes 8am session.",
                    "That's a common productivity folklore loop. Logging the suggestion, nothing more?",
                ),
                (
                    "Saw energy-drink cans next to laptop chargers in the study room — tonight-prep vibes everywhere.",
                    "Campus culture around caffeine before early sessions is loud.",
                ),
            ],
            "distractor": (
                "People keep saying a strong energy drink tonight while I prep slides is amazing for productivity and that I should say yes "
                "if I care about crushing the high-stakes 8am session.",
                "Productivity folklore around stimulants is loud. How have your nights gone when you tried that?",
            ),
            "query": "I have a high-stakes 8am session tomorrow. Friends say I should grab a strong energy drink tonight while I prep slides. Should I?",
            "gold_assoc": (
                "No — or only a very early, mild option long before evening. Stimulants after mid-afternoon have delayed/fragmented sleep, "
                "and fragmented nights collapse morning focus. Protect sleep instead of stacking a late energy drink."
            ),
            "gold_abs": (
                "Insufficient evidence about stimulant timing or sleep sensitivity. Cannot recommend an evening energy drink for an 8am session from memory — ask about past late-caffeine nights."
            ),
        },
        "S3": {
            "fillers": [
                ("Fixed my bike light. Commute rides feel safer.", "Good maintenance habit."),
                ("Library was packed. Still got two chapters done.", "Solid focus given the noise."),
            ],
            # Avoid: ramen/salt/midnight/crawl/broth/bond/friends/weekend
            "ev_A": [
                (
                    "Whenever I do a really briny, sodium-heavy plate I get this migraine-like headache a few hours later.",
                    "How often has that happened?",
                ),
                ("Enough times that I notice the pattern. It's not subtle.", None),
            ],
            "ev_B": [
                (
                    "Those headaches wipe out half my usable workday afterward. I just can't hold complex tasks.",
                    "So the recovery cost is basically a half-day.",
                ),
                ("Yeah. It's expensive.", None),
            ],
            "lures": [
                (
                    "Group chat is all about an all-you-can-eat midnight ramen crawl this weekend — huge broth bowls, lots of salt, bonding.",
                    "Sounds like a classic FOMO invite. Just noting the logistics?",
                ),
                (
                    "Someone posted photos from last month's ramen crawl — salt, broth, midnight hangouts.",
                    "Food crawls photograph well even when they wreck the next day.",
                ),
            ],
            "distractor": (
                "Everyone says the midnight ramen crawl is amazing for bonding and that saying yes to the all-you-can-eat broth bowls "
                "with lots of salt is how you stay in the friend group this weekend.",
                "Social FOMO around food crawls is strong. Does your body tolerate those sodium loads?",
            ),
            "query": "Friends invited me to an all-you-can-eat midnight ramen crawl this weekend — huge broth bowls, lots of salt. Should I say yes to bond with the group?",
            "gold_assoc": (
                "Lean no, or set a hard limit / share bowls. Very high-sodium meals have been followed by migraine-like headaches and then half a lost workday. "
                "Group bonding is real but is not evidence of sodium tolerance — propose a lower-salt alternative hangout."
            ),
            "gold_abs": (
                "Insufficient evidence on sodium tolerance or post-meal headaches. Abstain; ask whether heavy broth/salt meals have caused problems before."
            ),
        },
        "S4": {
            "fillers": [
                ("Reorganized notes for a seminar. Less chaos.", "That should speed retrieval later."),
                ("Watched a short documentary. Decent.", "Any takeaway worth keeping?"),
            ],
            # Avoid: pastry/pastries/workshop/morning/lunch/table/4-hour
            "ev_A": [
                (
                    "If I skip a real first meal of the day I crash hard before noon — focus just drops.",
                    "Is that pretty consistent?",
                ),
                ("Very. It's not a maybe.", None),
            ],
            "ev_B": [
                (
                    "Sweet laminated bakery items alone never save me. I still crash; there's no lasting satiety.",
                    "So sugar-forward starts aren't enough fuel for you.",
                ),
                ("Right. They feel like a meal but don't act like one.", None),
            ],
            "lures": [
                (
                    "The 4-hour morning workshop catering note says they only put out pastries — no other food until lunch.",
                    "Event catering often defaults to a pastry table. Planning around it?",
                ),
                (
                    "Someone asked whether relying on the pastry table for a long morning workshop is fine.",
                    "Common question when venues skip real fuel options.",
                ),
            ],
            "distractor": (
                "The organizers said the pastry table is amazing and that saying yes to a pastry-only morning workshop "
                "with no other food until lunch is totally fine for a full 4-hour block.",
                "Event catering spin is common. How do pastry-only starts actually go for you?",
            ),
            "query": "I have a 4-hour morning workshop and they only put out pastries — no other food until lunch. Should I rely on that pastry table?",
            "gold_assoc": (
                "Do not rely on the pastry table alone. Skipping a real morning meal causes a mid-morning crash, and pastry-only mornings have already failed to provide lasting satiety. "
                "Bring a substantial snack/protein or eat beforehand."
            ),
            "gold_abs": (
                "Insufficient evidence about morning fueling needs. Cannot advise relying on pastries; ask how skip-breakfast or pastry-only mornings have gone historically."
            ),
        },
        "S5": {
            "fillers": [
                ("Bought new earphones. Commute is quieter.", "Helpful for focus blocks."),
                ("Cleared old downloads. Disk space returned.", "Future-you appreciates that."),
            ],
            # Avoid: spicy/tasting/menu/late-night/7:30am/call/book
            "ev_A": [
                (
                    "Chili-forward dinners close to bedtime give me reflux and I sleep badly.",
                    "Does timing matter as much as the heat level?",
                ),
                ("Timing matters — close to bedtime is what triggers it.", None),
            ],
            "ev_B": [
                (
                    "After those reflux nights my dawn speaking voice is rough and I'm less steady on early meetings.",
                    "So early speaking days need a calmer evening plate.",
                ),
                ("Exactly. I can't count on sounding clear.", None),
            ],
            "lures": [
                (
                    "There's a late-night spicy tasting menu circulating — people asking who will book it before a delicate 7:30am call.",
                    "Experience FOMO plus an early commitment is a rough combo on the calendar.",
                ),
                (
                    "Friend forwarded the spicy tasting menu for tonight and mentioned the 7:30am call conflict jokingly.",
                    "Calendar collisions around food experiences show up a lot.",
                ),
            ],
            "distractor": (
                "They said the late-night spicy tasting menu is amazing and that saying yes / booking it tonight is worth it "
                "for the experience before any delicate 7:30am call plans.",
                "Experience marketing is persuasive. How do late chili-heavy plates affect your next morning?",
            ),
            "query": "There's a late-night spicy tasting menu tonight, and I have a delicate 7:30am call tomorrow. Should I book the spicy menu?",
            "gold_assoc": (
                "Skip the late spicy tasting, or choose a mild early dinner instead. Late spicy meals have triggered night reflux/poor sleep, "
                "and those nights make morning voice and composure unreliable for early calls."
            ),
            "gold_abs": (
                "Insufficient evidence about spicy-meal timing or morning voice effects. Abstain; ask about past late spicy dinners before early speaking commitments."
            ),
        },
    }
    p = paints[core["sid"]]
    # slight voice nudge in fillers via persona trait mention occasionally
    trait = persona["stable_traits"][0]

    def turns(pairs):
        out = []
        for a, b in pairs:
            if isinstance(a, tuple):
                u, s = a[0], a[1] if len(a) > 1 else None
            else:
                u, s = a, b
            out.append({"role": "user", "content": u})
            if s:
                out.append({"role": "assistant", "content": s})
        return out

    # Build sessions differently by arm
    sessions = []
    annotation = {}
    sid = 1

    def add(role_setup, dialogue, **meta):
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

    # filler 1
    f0, f1 = p["fillers"][0]
    add("filler", [{"role": "user", "content": f0}, {"role": "assistant", "content": f1}])
    # optional persona-colored filler
    add(
        "filler",
        [
            {"role": "user", "content": f"Work mode today felt very '{trait}' — long blocks, little slack."},
            {"role": "assistant", "content": f"Given that {voice.split(',')[0]} pace, worth protecting recovery tonight."},
        ],
    )

    target_ids = []
    distractor_ids = []

    if arm != "absence":
        # evidence A
        ev_a_dialog = []
        for u, s in [(p["ev_A"][0][0], p["ev_A"][0][1]), (p["ev_A"][1][0], None)]:
            ev_a_dialog.append({"role": "user", "content": u})
            if s:
                ev_a_dialog.append({"role": "assistant", "content": s})
        add(
            "target_evidence",
            ev_a_dialog,
            evidence_id="ev_A",
            atomic_fact=core["ev_A_fact"],
        )
        target_ids.append("ev_A")

        add("filler", [{"role": "user", "content": p["fillers"][1][0]}, {"role": "assistant", "content": p["fillers"][1][1]}])

        # evidence B
        ev_b_dialog = []
        for u, s in [(p["ev_B"][0][0], p["ev_B"][0][1]), (p["ev_B"][1][0], None)]:
            ev_b_dialog.append({"role": "user", "content": u})
            if s:
                ev_b_dialog.append({"role": "assistant", "content": s})
        add(
            "target_evidence",
            ev_b_dialog,
            evidence_id="ev_B",
            atomic_fact=core["ev_B_fact"],
        )
        target_ids.append("ev_B")
    else:
        # more fillers instead of evidence
        for msg, resp in [
            ("Booked a short walk after lunch.", "Nice reset."),
            ("Inbox zero for an hour. Rare.", "Enjoy the quiet."),
            ("Tried a new grocery store. Fine.", "Any keepers?"),
        ]:
            add("filler", [{"role": "user", "content": msg}, {"role": "assistant", "content": resp}])

    # Surface-lure fillers: share query decision vocabulary so flat TF-IDF top-3
    # is cue + lures (not target_evidence). Not labeled as evidence.
    for lu, la in p["lures"]:
        add(
            "filler",
            [{"role": "user", "content": lu}, {"role": "assistant", "content": la}],
            surface_lure=True,
            why_filler="Query-surface vocabulary only; no bodily causal facts (V1 flat-RAG decoy).",
        )

    if arm == "distractor":
        du, da = p["distractor"]
        add(
            "distractor",
            [
                {"role": "user", "content": du},
                {"role": "assistant", "content": da},
            ],
            distractor_id="dist_1",
            why_distractor=(
                "Shares decision vocabulary with the query (say yes / amazing / invite / bonding / productivity) "
                "but provides no bodily evidence; surface lure toward acceptance."
            ),
        )
        distractor_ids.append("dist_1")
    else:
        add("filler", [{"role": "user", "content": "Weather was grey. Stayed indoors."}, {"role": "assistant", "content": "Good day for quiet tasks."}])

    add("filler", [{"role": "user", "content": "Wrapped a small admin task."}, {"role": "assistant", "content": "One less open loop."}])

    # cue + query
    add(
        "associative_cue",
        [{"role": "user", "content": p["query"]}],
        cue_id="cue_1",
    )

    gold = p["gold_abs"] if arm == "absence" else p["gold_assoc"]
    required = (
        ["states insufficient evidence / abstain", "does not invent the bodily causal pattern"]
        if arm == "absence"
        else list(core["required_assoc"])
    )
    if arm == "distractor":
        required = required + ["does not treat social/productivity distractor as bodily evidence"]

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


def assemble_item(persona: dict, core: dict, arm: str, idx: int) -> dict[str, Any]:
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
    # final_turn identity
    last_user = None
    for s in context:
        for t in s["dialogue"]:
            if t["role"] == "user":
                last_user = t["content"]
    assert last_user == painted["query"]

    uidx = persona["user_index"]
    sample_id = f"AMB_HD_u{uidx:02d}_{arm[:4]}_{core['sid']}_{idx:02d}"
    # clearer sample ids
    sample_id = f"AMB_HD_u{uidx:02d}_{arm}_{core['sid']}"

    item = {
        "sample_id": sample_id,
        "source": "partner_generated",
        "status": "rendered",
        "association_type": painted["atype"],
        "domain_tags": ["health/wellness", "food/cooking"],
        "pilot_arm": arm if arm != "associative" else "associative",
        "pilot_domain": "health_diet",
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
            "generator": "health_diet_batch_v1",
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
                "metrics": ["answer_vs_gold+required_elements", "validity_metrics.flat_rag_hit_top3", "distractor_cosine>=evidence_cosine for distractor arm"],
            },
        },
    }
    item["context_length_tokens"] = count_tokens(item["context"])
    item["validity_metrics"] = compute_metrics(item)
    return item


def _cf(sample_id: str, arm: str, painted: dict) -> list[dict]:
    if arm == "absence":
        return [
            {
                "variant_id": f"{sample_id}_cf_add_evidence",
                "type": "evidence_added",
                "expected_gold": "associative recommendation becomes answerable",
            }
        ]
    # find evidence session ids
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
            "computed_by": "health_diet/bin/generate_health_diet_batch.py",
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
    # evolving_state leak
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
    tag = persona["folder_tag"]  # user1..user10
    return DATA / f"diet_{arm}_{tag}"


def main() -> int:
    cores = scenario_cores()
    assert len(cores) == 5
    results = []
    n_fail = 0
    for persona in PERSONAS["users"]:
        for arm in ("associative", "distractor", "absence"):
            out_dir = folder_for(persona, arm)
            out_dir.mkdir(parents=True, exist_ok=True)
            for i, core in enumerate(cores, start=1):
                item = assemble_item(persona, core, arm, i)
                # recompute metrics after any future edits
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

    # write jsonl + manifest
    jsonl = HD / "manifests" / "health_diet_batch_v1.jsonl"
    jsonl.parent.mkdir(parents=True, exist_ok=True)
    with jsonl.open("w", encoding="utf-8") as fh:
        for r in results:
            p = ROOT / r["path"]
            fh.write(json.dumps(json.loads(p.read_text()), ensure_ascii=False) + "\n")

    report = {
        "n": len(results),
        "n_pass": sum(1 for r in results if r["pass"]),
        "n_fail": n_fail,
        "by_arm": {
            a: sum(1 for r in results if r["arm"] == a and r["pass"]) for a in ("associative", "distractor", "absence")
        },
        "results": results,
    }
    (HD / "manifests" / "gate_report.json").write_text(json.dumps(report, indent=2) + "\n")
    tsv = ["sample_id\tuser\tarm\tstatus\terrors"]
    for r in results:
        tsv.append(
            f"{r['sample_id']}\t{r['user']}\t{r['arm']}\t{'keep' if r['pass'] else 'discard'}\t{'; '.join(r['errors'][:3]) or 'gate pass'}"
        )
    (HD / "manifests" / "results.tsv").write_text("\n".join(tsv) + "\n")
    print(f"\nSUMMARY {report['n_pass']}/{report['n']} PASS")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
