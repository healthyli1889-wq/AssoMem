"""Anonymous U01-U10 roster for the social-vNext batch.

Each profile is anchored to one MemoryQuest respondent file. The anchor is an
authoring aid only: nothing from `demographics` (age band, gender, country,
employment, education, marital status) reaches visible dialogue. What survives
into the batch is a de-identified *social role* plus the shape of the person's
circle, both derived from that respondent's Events / Messaging / Services /
Restaurants domain summaries.

`role` answers "what kind of social life does this person run?".
`circle` names the recurring others without naming a person.
`voice` fixes the register so ten profiles do not read as one narrator.
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
    Profile(
        index=1,
        persona_file="user0",
        persona_anchor="mq_user0",
        role="weeknight networking-and-gig regular",
        circle="the weeknight crew",
        voice="clipped, dry, slightly self-deprecating",
    ),
    Profile(
        index=2,
        persona_file="user5",
        persona_anchor="mq_user5",
        role="student festival-goer who keeps family threads on top",
        circle="the res-hall group",
        voice="warm, chatty, quick to use shorthand",
    ),
    Profile(
        index=3,
        persona_file="user10",
        persona_anchor="mq_user10",
        role="weekend food-fair and match-day organizer",
        circle="the Sunday table",
        voice="easygoing, practical, a bit blunt",
    ),
    Profile(
        index=4,
        persona_file="user15",
        persona_anchor="mq_user15",
        role="group-ticket organizer who calls family abroad",
        circle="the match-day group",
        voice="matter-of-fact, logistics-first",
    ),
    Profile(
        index=5,
        persona_file="user20",
        persona_anchor="mq_user20",
        role="retired culture-series attendee who goes as a couple",
        circle="the season-ticket pair",
        voice="measured, precise, a little formal",
    ),
    Profile(
        index=6,
        persona_file="user25",
        persona_anchor="mq_user25",
        role="student small-group meetup planner",
        circle="the four-person group chat",
        voice="upbeat, casual, uses lowercase",
    ),
    Profile(
        index=7,
        persona_file="user30",
        persona_anchor="mq_user30",
        role="theatre-for-two planner who batches long threads",
        circle="the two of us plus the old book group",
        voice="organized, gently ironic",
    ),
    Profile(
        index=8,
        persona_file="user35",
        persona_anchor="mq_user35",
        role="community-event and career-meetup attendee",
        circle="the neighbourhood regulars",
        voice="open, self-aware, a little tired",
    ),
    Profile(
        index=9,
        persona_file="user40",
        persona_anchor="mq_user40",
        role="indie-gig and gallery regular who prefers text to calls",
        circle="the gallery-night friends",
        voice="observant, understated, prefers text",
    ),
    Profile(
        index=10,
        persona_file="user44",
        persona_anchor="mq_user44",
        role="solo-friendly workshop and panel attendee",
        circle="the workshop circle",
        voice="thoughtful, deliberate, quietly funny",
    ),
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
