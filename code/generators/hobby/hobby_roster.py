"""Anonymous U01-U10 roster for the hobby-vNext batch.

Same MemoryQuest anchors as the social batch, read through their Games / Music /
Sports / Shopping domain summaries instead of their Events / Messaging ones, so
each profile gets a craft they actually practise. Nothing from `demographics`
reaches visible dialogue.

`craft` is the skill the practice scenarios hang on; `circle` is the group they
practise around; `voice` fixes the register so ten profiles do not read as one.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    index: int
    persona_file: str
    persona_anchor: str
    role: str
    craft: str
    circle: str
    voice: str


ROSTER: tuple[Profile, ...] = (
    Profile(1, "user0", "mq_user0", "console RPG player who plays guitar and runs",
            "guitar", "the Thursday jam", "clipped, dry, slightly self-deprecating"),
    Profile(2, "user5", "mq_user5", "student story-game player and bedroom producer",
            "producing", "the res-hall music lot", "warm, chatty, quick to use shorthand"),
    Profile(3, "user10", "mq_user10", "open-world gamer who plays bass and boxes",
            "bass", "the Sunday band", "easygoing, practical, a bit blunt"),
    Profile(4, "user15", "mq_user15", "strategy-game builder, mandolin player and cyclist",
            "mandolin", "the folk-night regulars", "matter-of-fact, logistics-first"),
    Profile(5, "user20", "mq_user20", "retired puzzle-game player, potter and gardener",
            "the pottery wheel", "the ceramics class", "measured, precise, a little formal"),
    Profile(6, "user25", "mq_user25", "student PC gamer and EDM producer",
            "production", "the campus games society", "upbeat, casual, uses lowercase"),
    Profile(7, "user30", "mq_user30", "Switch player and sampler-based musician",
            "the sampler", "the indie-games group", "organized, gently ironic"),
    Profile(8, "user35", "mq_user35", "sim-game player and fiddle player",
            "the fiddle", "the folk session", "open, self-aware, a little tired"),
    Profile(9, "user40", "mq_user40", "student sim-and-puzzle player who plays keys",
            "the keyboard", "the halls music group", "observant, understated"),
    Profile(10, "user44", "mq_user44", "solo narrative-game player, synth builder and plant grower",
            "the modular synth", "the synth-builders group", "thoughtful, deliberate, quietly funny"),
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
