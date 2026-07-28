"""Anonymous U01-U10 roster for the finance-vNext v3 batch.

Same MemoryQuest anchors as the social and hobby batches, read through their
Finance / Shopping / Services summaries. Nothing from `demographics` reaches
visible dialogue; what survives is a de-identified money-management role.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    index: int
    persona_file: str
    persona_anchor: str
    role: str
    circle: str
    voice: str


ROSTER: tuple[Profile, ...] = (
    Profile(1, "user0", "mq_user0", "full-time earner who checks a dashboard daily",
            "the money-talk group chat", "clipped, dry, slightly self-deprecating"),
    Profile(2, "user5", "mq_user5", "student on a tight monthly budget",
            "the res-hall lot", "warm, chatty, quick to use shorthand"),
    Profile(3, "user10", "mq_user10", "salaried saver with a mid-range spending habit",
            "the Sunday table", "easygoing, practical, a bit blunt"),
    Profile(4, "user15", "mq_user15", "deal-tracking value shopper on a salary",
            "the match-day group", "matter-of-fact, logistics-first"),
    Profile(5, "user20", "mq_user20", "retired household planner running things with a partner",
            "the two of us", "measured, precise, a little formal"),
    Profile(6, "user25", "mq_user25", "student watching every subscription",
            "the four-person group chat", "upbeat, casual, uses lowercase"),
    Profile(7, "user30", "mq_user30", "married planner who batches the household spend",
            "the two of us plus my sister", "organized, gently ironic"),
    Profile(8, "user35", "mq_user35", "job-seeker running a very tight month",
            "the neighbourhood regulars", "open, self-aware, a little tired"),
    Profile(9, "user40", "mq_user40", "student living on a part-time income",
            "the halls group", "observant, understated"),
    Profile(10, "user44", "mq_user44", "household budgeter buying for two and a pet",
            "the two of us", "thoughtful, deliberate, quietly funny"),
)

ANONYMIZATION_NOTE = (
    "External MemoryQuest persona material was used only during authoring; no corpus, "
    "legal name, country, or demographic metadata is in visible dialogue."
)


def profile_for(user_index: int) -> Profile:
    for profile in ROSTER:
        if profile.index == user_index:
            return profile
    raise KeyError(f"no roster profile for U{user_index:02d}")
