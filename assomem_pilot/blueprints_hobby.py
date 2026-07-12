# AssoMemBench pilot blueprints — hobby/habit domain (15 items).
# Annotation fields are co-located on sessions; assemble.py splits them out.

from __future__ import annotations

BLUEPRINTS: list[dict] = [
    # -------------------------------------------------------------------------
    # ASSOCIATIVE (5): A3 x3, A2 x2 — no distractor sessions
    # -------------------------------------------------------------------------
    {
        "sample_id": "AMB_A3_HH_0001",
        "pilot_arm": "associative",
        "pilot_domain": "hobby_habit",
        "association_type": "A3_cross_domain",
        "domain_tags": ["hobbies/leisure", "health/wellness"],
        "persona": {
            "user_id": "u_hh_01",
            "stable_traits": [
                "prefers outdoor movement before work",
                "cautious about overuse injuries",
                "asks for concrete tradeoffs",
            ],
            "evolving_state": {
                "event_readiness": "contraindicated_elevation_events",
                "knee_pattern": "incline_flare_prone",
            },
        },
        "latent_forbidden_phrases": [
            "contraindicated_elevation_events",
            "incline_flare_prone",
            "skip the mountain race",
            "do not sign up for the race",
            "avoid hilly races",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-01-06T07:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Can you remind me how to stretch calves after an easy park loop?",
                    },
                    {
                        "role": "assistant",
                        "content": "Sure. After you cool down, do a wall calf stretch for 30 seconds each side, then a gentle seated hamstring reach. Keep the knee soft if anything feels sharp.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-01-09T21:05:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "I keep getting invites to random weekend group activities. How do I politely decline without sounding antisocial?",
                    },
                    {
                        "role": "assistant",
                        "content": "A short honest line works: thank them, say this weekend is already spoken for, and offer a different low-key hang another time. You do not owe a long explanation.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-01-12T07:40:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "User jogs most weekday mornings on flat park paths and feels knee discomfort when routes include steeper neighborhood streets.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "My weekday mornings are usually a flat park loop. Whenever I cut through those steeper neighborhood streets instead, my right knee starts complaining by the end.",
                    },
                    {
                        "role": "assistant",
                        "content": "That pattern is useful information. Flat loops that feel fine plus discomfort on steeper streets often means the incline load is the trigger, not the total distance alone.",
                    },
                    {
                        "role": "user",
                        "content": "Yeah, on the flat path I feel fine. It is specifically those uphill blocks that bother me.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-01-15T12:10:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What is a simple way to log how a workout felt without turning it into a spreadsheet hobby?",
                    },
                    {
                        "role": "assistant",
                        "content": "Use three words after each session: effort, mood, and one body note. That is enough to spot patterns later without extra tooling.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-01-18T19:30:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_B",
                "atomic_fact": "A clinician advised the user to keep elevation gentle for the next couple of months while the knee settles.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "I saw the clinic this week. They said keep elevation gentle for the next couple of months while things settle, and stick to softer surfaces when I can.",
                    },
                    {
                        "role": "assistant",
                        "content": "That is a clear constraint. Gentle elevation and softer surfaces for a couple of months gives the joint a quieter loading pattern while you keep moving.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-01-22T08:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Do foam rollers actually help after easy sessions or is that mostly placebo?",
                    },
                    {
                        "role": "assistant",
                        "content": "They can reduce next-day stiffness for some people. If it feels good and does not irritate the joint, a short roll is fine; it is not mandatory.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-01-25T20:15:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A friend keeps saying community signups are a great way to stay motivated. I am not sure I agree.",
                    },
                    {
                        "role": "assistant",
                        "content": "Group signups help some people and pressure others. Match the format to what actually keeps you consistent, not what sounds impressive.",
                    },
                ],
            },
            {
                "session_id": 8,
                "timestamp": "2026-01-28T21:10:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Quick one. A coworker says a mountain race signup this month is amazing and wants me to join the team. Should I?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Probably not right now. Your mornings already show knee discomfort on steeper streets, "
            "and the clinic asked you to keep elevation gentle for a couple of months. A mountain race "
            "is the opposite loading pattern, so decline or pick a flat alternative later."
        ),
        "required_elements": [
            "cites knee discomfort on steeper routes",
            "cites clinic guidance to keep elevation gentle",
            "recommends declining or delaying the mountain race",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "indicates", "target": "elevation_intolerance", "hop": 1},
            {"source": "ev_B", "relation": "constrains", "target": "elevation_events", "hop": 1},
            {
                "source": "elevation_intolerance",
                "relation": "causes",
                "target": "decline_mountain_race",
                "hop": 2,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_ev_A",
                "type": "evidence_removed",
                "removed_session_ids": [3],
                "expected_gold": (
                    "With only the clinic note about gentle elevation, lean cautious and ask how hilly "
                    "the course is before committing."
                ),
            },
            {
                "variant_id": "cf_remove_ev_B",
                "type": "evidence_removed",
                "removed_session_ids": [5],
                "expected_gold": (
                    "Your steeper-street knee pattern alone is a warning; treat a mountain race as high risk "
                    "unless you confirm a flat course."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A3_HH_0002",
        "pilot_arm": "associative",
        "pilot_domain": "hobby_habit",
        "association_type": "A3_cross_domain",
        "domain_tags": ["hobbies/leisure"],
        "persona": {
            "user_id": "u_hh_02",
            "stable_traits": [
                "shoots film as a slow hobby",
                "budget-conscious about gear",
                "plans weekends carefully",
            ],
            "evolving_state": {
                "gear_budget": "frozen_until_april",
                "daylight_window": "weekend_mornings_only",
            },
        },
        "latent_forbidden_phrases": [
            "frozen_until_april",
            "weekend_mornings_only",
            "skip the coastal outing",
            "do not take the midweek shoot",
            "reject the borrowed body",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-01-07T18:40:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Any tips for storing undeveloped rolls so they do not get ruined in a warm apartment?",
                    },
                    {
                        "role": "assistant",
                        "content": "Keep them in a sealed bag in the fridge if you will wait more than a couple of weeks, and let them warm up before opening to avoid condensation.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-01-11T11:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "People keep telling me gear upgrades are worth it. I am skeptical.",
                    },
                    {
                        "role": "assistant",
                        "content": "Upgrades help only when a specific limitation is blocking you. Otherwise they mostly spend money and attention.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-01-14T20:05:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "User's hobby spending is frozen until April; they are developing rolls at home and not buying new equipment.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "I have been developing rolls at home lately. My hobby spending is basically frozen until April, so I am not buying any new equipment before then.",
                    },
                    {
                        "role": "assistant",
                        "content": "Working within a freeze is a solid constraint. Home developing plus what you already own can carry you until April without new purchases.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-01-17T09:15:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Is there a cheap way to scan negatives that does not look terrible?",
                    },
                    {
                        "role": "assistant",
                        "content": "A simple light pad plus a phone clamp can look surprisingly good if you keep dust down and shoot RAW. Dedicated scanners can wait.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-01-20T19:50:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_B",
                "atomic_fact": "User only gets outdoor shooting time on Saturday and Sunday mornings because weekday evenings are indoors and winter light dies early.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Weekday evenings I am stuck indoors. The only outdoor shooting window I really get is Saturday and Sunday mornings, and even then the winter light dies early.",
                    },
                    {
                        "role": "assistant",
                        "content": "That makes weekend mornings your scarce resource. Protecting those hours matters more than collecting more tools.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-01-23T12:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A friend said a midweek coastal outing with fancy kit would be amazing. I have not answered yet.",
                    },
                    {
                        "role": "assistant",
                        "content": "No rush. Check whether the timing and cost fit your actual constraints before you commit.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-01-26T21:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I tell if a trip invitation is actually aligned with my hobbies versus just FOMO?",
                    },
                    {
                        "role": "assistant",
                        "content": "Ask what concrete practice it enables that you cannot do at home. If the answer is vague prestige, it is probably FOMO.",
                    },
                ],
            },
            {
                "session_id": 8,
                "timestamp": "2026-01-29T20:40:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Okay, deciding now. Someone offered a Wednesday coastal outing with a borrowed high-end body. Is that a smart move for me right now?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Not a smart fit right now. Your hobby spending is frozen until April, and your only reliable "
            "outdoor window is weekend mornings. A Wednesday coastal outing fights both constraints, even "
            "with a borrowed high-end body."
        ),
        "required_elements": [
            "cites hobby spending freeze until April",
            "cites weekend-morning outdoor window only",
            "recommends declining the Wednesday coastal outing",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "constrains", "target": "new_or_rental_gear_outings", "hop": 1},
            {"source": "ev_B", "relation": "constrains", "target": "weekday_outdoor_sessions", "hop": 1},
            {
                "source": "weekday_outdoor_sessions",
                "relation": "causes",
                "target": "decline_wednesday_coastal_outing",
                "hop": 2,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_budget",
                "type": "evidence_removed",
                "removed_session_ids": [3],
                "expected_gold": (
                    "Even without the budget freeze, Wednesday still conflicts with your weekend-only outdoor window."
                ),
            },
            {
                "variant_id": "cf_remove_light",
                "type": "evidence_removed",
                "removed_session_ids": [5],
                "expected_gold": (
                    "Borrowed gear avoids purchase cost, but a freeze until April still argues for staying put unless the outing is free and low-friction."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A3_HH_0003",
        "pilot_arm": "associative",
        "pilot_domain": "hobby_habit",
        "association_type": "A3_cross_domain",
        "domain_tags": ["hobbies/leisure", "household"],
        "persona": {
            "user_id": "u_hh_03",
            "stable_traits": [
                "batch-cooks on Sundays",
                "visits family on recurring weekends",
                "dislikes last-minute food chaos",
            ],
            "evolving_state": {
                "sunday_capacity": "travel_disrupts_batch_cook",
                "hosting_fit": "poor_for_standing_dinners",
            },
        },
        "latent_forbidden_phrases": [
            "travel_disrupts_batch_cook",
            "poor_for_standing_dinners",
            "do not host Sunday dinner",
            "decline the standing dinner",
            "cannot commit to hosting",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-02-01T10:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What are good freezer containers for soups that do not leak in a backpack?",
                    },
                    {
                        "role": "assistant",
                        "content": "Look for latch lids with a silicone gasket. Leave headspace when freezing liquids so the lid does not pop.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-02-03T21:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Neighbors keep pitching building socials. How do I stay friendly without becoming the default organizer?",
                    },
                    {
                        "role": "assistant",
                        "content": "Attend selectively, contribute a small dish when you can, and never volunteer to own the calendar. Organizer roles expand fast.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-02-05T18:45:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "User relies on Sunday batch cooking to feed themselves for the work week.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Sunday batch cooking is how I eat all week. If I skip it, I end up buying expensive takeout by Wednesday.",
                    },
                    {
                        "role": "assistant",
                        "content": "That habit is doing real logistical work for you. Protecting that block is more important than adding optional social cooking plans.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-02-08T09:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Any quick breakfast ideas that use leftover roasted vegetables?",
                    },
                    {
                        "role": "assistant",
                        "content": "Warm them in a skillet with eggs, or fold them into a wrap with yogurt sauce. Both take under ten minutes.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-02-10T20:10:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_B",
                "atomic_fact": "For the next several Sundays the user will be on trains visiting family and unavailable at home.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "For the next several Sundays I will be on trains visiting family. I will not be home during the afternoon block I usually use for kitchen work.",
                    },
                    {
                        "role": "assistant",
                        "content": "That is a multi-week schedule conflict. Anything that assumes you are home on those afternoons will need a different plan.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-02-12T12:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Is a meal kit that delivers Sunday ingredients worth it if my weekends are messy?",
                    },
                    {
                        "role": "assistant",
                        "content": "Only if the delivery day matches when you are actually home. Otherwise the ingredients just become fridge clutter.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-02-14T19:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Someone in the building said a standing Sunday dinner would be amazing for community. I have not replied.",
                    },
                    {
                        "role": "assistant",
                        "content": "Standing commitments are harder than one-offs. Check your recurring Sunday constraints before you answer.",
                    },
                ],
            },
            {
                "session_id": 8,
                "timestamp": "2026-02-16T21:05:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "My neighbor wants me to host a standing Sunday dinner for our building. Should I say yes?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Say no for now. You depend on Sunday batch cooking for the week, and the next several Sundays "
            "you will be on trains visiting family. Hosting a standing Sunday dinner conflicts with both."
        ),
        "required_elements": [
            "cites Sunday batch-cooking dependence",
            "cites multi-week Sunday family travel",
            "recommends declining standing Sunday hosting",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "constrains", "target": "sunday_afternoon_availability", "hop": 1},
            {"source": "ev_B", "relation": "causes", "target": "sunday_afternoon_unavailability", "hop": 1},
            {
                "source": "sunday_afternoon_unavailability",
                "relation": "constrains",
                "target": "standing_sunday_hosting",
                "hop": 2,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_mealprep",
                "type": "evidence_removed",
                "removed_session_ids": [3],
                "expected_gold": (
                    "Even without the batch-cook habit, recurring Sunday train travel still blocks hosting."
                ),
            },
            {
                "variant_id": "cf_remove_travel",
                "type": "evidence_removed",
                "removed_session_ids": [5],
                "expected_gold": (
                    "Without travel, hosting still competes with the batch-cook block that feeds your week."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A2_HH_0004",
        "pilot_arm": "associative",
        "pilot_domain": "hobby_habit",
        "association_type": "A2_cue_chain",
        "domain_tags": ["hobbies/leisure", "health/wellness"],
        "persona": {
            "user_id": "u_hh_04",
            "stable_traits": [
                "trains finger strength on a hangboard",
                "history of overuse caution",
                "likes measurable progress",
            ],
            "evolving_state": {
                "finger_status": "post_pulley_guarded",
                "max_hang_readiness": "not_cleared",
            },
        },
        "latent_forbidden_phrases": [
            "post_pulley_guarded",
            "not_cleared",
            "skip the max-hang challenge",
            "do not join the hang challenge",
            "avoid max hangs",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-02-02T18:10:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What warm-up do you recommend before any board session?",
                    },
                    {
                        "role": "assistant",
                        "content": "Start with open-hand dead hangs at bodyweight, then easy pull-ups, then short edge touches. Stop if anything feels pinchy in a finger joint.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-02-05T20:30:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "User had a prior finger pulley strain and still avoids peak one-arm edge efforts while recovering cautiously.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "I tweaked a finger pulley last season. It feels mostly okay now, but I am still avoiding peak one-arm edge efforts and sticking to easier open-hand work.",
                    },
                    {
                        "role": "assistant",
                        "content": "That is a sensible guardrail. Easier open-hand loading while you stay away from peak one-arm edge efforts reduces re-injury risk.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-02-08T11:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Should I ice after every session or only when something feels irritated?",
                    },
                    {
                        "role": "assistant",
                        "content": "Only when something feels irritated. Routine icing after normal sessions is usually unnecessary.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-02-11T19:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Gyms love challenge signups. How do I evaluate whether a signup is useful training or just marketing?",
                    },
                    {
                        "role": "assistant",
                        "content": "Check whether the challenge signup matches your current limits. If it pushes a quality you are deliberately avoiding, it is marketing, not training.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-02-14T10:15:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Any non-board forearm work that will not spike tendon load?",
                    },
                    {
                        "role": "assistant",
                        "content": "Rice-bucket rotations and light wrist curls with high control are usually gentler than dense edge work.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-02-17T21:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A friend said the gym challenge signup this month is amazing. I am on the fence about whether I should join.",
                    },
                    {
                        "role": "assistant",
                        "content": "Filter any challenge signup against what you already decided to protect. Hype alone is not a reason to join.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-02-20T18:45:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "The climbing gym is pushing a max-hang challenge signup this month. Should I join?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "No. After a prior finger pulley strain you are still avoiding peak one-arm edge efforts. "
            "A max-hang challenge signup is the same kind of peak loading, so skip it for now."
        ),
        "required_elements": [
            "cites prior finger pulley strain",
            "cites current avoidance of peak one-arm edge efforts",
            "recommends not joining the challenge",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "constrains", "target": "max_hang_protocols", "hop": 1},
            {
                "source": "cue_1",
                "relation": "indicates",
                "target": "max_hang_protocols",
                "hop": 1,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_ev_A",
                "type": "evidence_removed",
                "removed_session_ids": [2],
                "expected_gold": (
                    "Without the pulley history on record, there is insufficient personal evidence to advise for or against the challenge."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A2_HH_0005",
        "pilot_arm": "associative",
        "pilot_domain": "hobby_habit",
        "association_type": "A2_cue_chain",
        "domain_tags": ["hobbies/leisure", "health/wellness"],
        "persona": {
            "user_id": "u_hh_05",
            "stable_traits": [
                "reads before sleep",
                "sensitive to evening screen light",
                "values sleep consistency",
            ],
            "evolving_state": {
                "bedtime_medium": "paper_only_working",
                "screen_risk": "insomnia_trigger",
            },
        },
        "latent_forbidden_phrases": [
            "paper_only_working",
            "insomnia_trigger",
            "skip the e-ink upgrade",
            "do not buy the bedtime tablet",
            "avoid glowing screens at night",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-02-03T22:10:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What is a good wind-down playlist length before sleep?",
                    },
                    {
                        "role": "assistant",
                        "content": "Fifteen to twenty minutes is enough for most people. Longer playlists can keep you waiting for the end instead of settling.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-02-06T21:40:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "Phone and tablet use before bed caused insomnia for the user; switching to paper books restored sleep.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Phone and tablet time before bed was wrecking my sleep. Since I switched to paper books only in that last hour, I fall asleep much faster.",
                    },
                    {
                        "role": "assistant",
                        "content": "That is a clear before-and-after. Protecting a paper-only last hour is doing real work for your sleep.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-02-09T12:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Any book-light recommendations that are dim enough for a dark room?",
                    },
                    {
                        "role": "assistant",
                        "content": "Choose a warm clip light with a low brightness setting and aim it at the page, not toward your eyes.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-02-12T19:50:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Friends keep saying device upgrades for bedtime reading are worth it. I am unsure.",
                    },
                    {
                        "role": "assistant",
                        "content": "Worth it only if the device preserves whatever already fixed your sleep. Novelty alone is a weak reason.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-02-15T10:05:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I keep a reading streak without turning it into another performance metric?",
                    },
                    {
                        "role": "assistant",
                        "content": "Track presence, not pages. A checkbox for sitting down with a book is enough.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-02-18T20:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Someone said an e-ink tablet for bedtime is amazing. Still thinking about it.",
                    },
                    {
                        "role": "assistant",
                        "content": "Compare it against the routine that already works. If it reintroduces late glowing interfaces, be careful.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-02-21T21:15:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A friend says a new e-ink tablet for bedtime is amazing and worth the upgrade. Should I get one?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Only if it truly stays paper-like with no stimulating apps. Phone and tablet time before bed "
            "previously caused insomnia, and paper books fixed it. An upgrade that reopens late-night device "
            "habits is not worth it."
        ),
        "required_elements": [
            "cites prior screen-related insomnia",
            "cites paper-book bedtime fix",
            "cautions against upgrade that reintroduces device habits",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "causes", "target": "paper_only_bedtime_rule", "hop": 1},
            {
                "source": "cue_1",
                "relation": "indicates",
                "target": "risk_to_paper_only_bedtime_rule",
                "hop": 1,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_ev_A",
                "type": "evidence_removed",
                "removed_session_ids": [2],
                "expected_gold": (
                    "Without the insomnia history, there is not enough personal evidence to recommend for or against the tablet."
                ),
            },
        ],
    },
    # -------------------------------------------------------------------------
    # DISTRACTOR (5): A3 + distractor session with higher query surface overlap
    # -------------------------------------------------------------------------
    {
        "sample_id": "AMB_A3_HH_0006",
        "pilot_arm": "distractor",
        "pilot_domain": "hobby_habit",
        "association_type": "A3_cross_domain",
        "secondary_association_type": "distractor_interference",
        "domain_tags": ["hobbies/leisure", "health/wellness"],
        "persona": {
            "user_id": "u_hh_06",
            "stable_traits": [
                "morning jogger",
                "knee-aware",
                "weighs social pressure carefully",
            ],
            "evolving_state": {
                "event_readiness": "contraindicated_elevation_events",
                "knee_pattern": "incline_flare_prone",
            },
        },
        "latent_forbidden_phrases": [
            "contraindicated_elevation_events",
            "incline_flare_prone",
            "skip the mountain race",
            "do not sign up for the race",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-01-06T07:25:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Quick calf stretch reminder after an easy park loop?",
                    },
                    {
                        "role": "assistant",
                        "content": "Wall calf stretch thirty seconds each side, then a soft hamstring reach. Stop if the joint complains.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-01-10T19:00:00Z",
                "role_setup": "distractor",
                "distractor_id": "dist_1",
                "why_distractor": (
                    "Talks about race signup, team, friend said amazing, and whether it is worth it — "
                    "sharing the query's decision vocabulary — but discusses a flat charity 5K for a "
                    "coworker, which is associatively irrelevant to the user's incline knee constraint."
                ),
                "dialogue": [
                    {
                        "role": "user",
                        "content": "My coworker is hyping a flat charity 5K race signup for their fundraising team. They keep saying the race is amazing and asking if joining the team is worth it for networking. I do not care about the fundraising angle.",
                    },
                    {
                        "role": "assistant",
                        "content": "If the value is only networking, treat it as optional social time, not training advice. A flat charity race signup can be a yes for people reasons and still be unrelated to your own training limits.",
                    },
                    {
                        "role": "user",
                        "content": "Yeah. Friend said it is amazing, but I am mostly annoyed by the signup pressure from the team chat.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-01-12T07:40:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "User jogs weekday mornings on flat park paths and feels knee discomfort on steeper neighborhood streets.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Weekday mornings I stick to a flat park loop. When I cut through steeper neighborhood streets, my right knee starts complaining.",
                    },
                    {
                        "role": "assistant",
                        "content": "Flat comfort plus steeper-street discomfort points to incline load as the trigger.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-01-16T12:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Simple way to note how a session felt without a fancy app?",
                    },
                    {
                        "role": "assistant",
                        "content": "Three words: effort, mood, body note. That is enough.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-01-18T19:30:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_B",
                "atomic_fact": "Clinic advised keeping elevation gentle for a couple of months.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Clinic visit this week: keep elevation gentle for the next couple of months while things settle.",
                    },
                    {
                        "role": "assistant",
                        "content": "Clear constraint. Gentle elevation for a couple of months while you keep moving on softer surfaces.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-01-22T08:10:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Foam roller after easy sessions — useful or skippable?",
                    },
                    {
                        "role": "assistant",
                        "content": "Optional. Use it if it feels good; skip if it irritates anything.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-01-25T20:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Community signups are everywhere. How do I ignore the hype?",
                    },
                    {
                        "role": "assistant",
                        "content": "Ask what constraint of yours the event respects. Hype is not a constraint check.",
                    },
                ],
            },
            {
                "session_id": 8,
                "timestamp": "2026-01-28T21:10:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A coworker says a mountain race signup this month is amazing and wants me on the team. Should I? Is it worth it?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Decline. Your steeper-street knee pattern and the clinic's gentle-elevation guidance make a "
            "mountain race a poor fit. The flat charity 5K chatter is unrelated social noise."
        ),
        "required_elements": [
            "cites knee discomfort on steeper routes",
            "cites gentle-elevation clinic guidance",
            "recommends declining the mountain race",
            "does not treat the charity 5K as decisive evidence",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "indicates", "target": "elevation_intolerance", "hop": 1},
            {"source": "ev_B", "relation": "constrains", "target": "elevation_events", "hop": 1},
            {
                "source": "dist_1",
                "relation": "analogous",
                "target": "surface_race_signup_language_only",
                "hop": 1,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_distractor",
                "type": "evidence_removed",
                "removed_session_ids": [2],
                "expected_gold": (
                    "Same recommendation: decline the mountain race based on knee incline pattern and clinic guidance."
                ),
            },
            {
                "variant_id": "cf_remove_ev_A",
                "type": "evidence_removed",
                "removed_session_ids": [3],
                "expected_gold": (
                    "With only clinic elevation guidance, remain cautious about a mountain race until course profile is known."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A3_HH_0007",
        "pilot_arm": "distractor",
        "pilot_domain": "hobby_habit",
        "association_type": "A3_cross_domain",
        "secondary_association_type": "distractor_interference",
        "domain_tags": ["hobbies/leisure"],
        "persona": {
            "user_id": "u_hh_07",
            "stable_traits": [
                "film hobbyist",
                "budget freeze until spring",
                "weekend-light dependent",
            ],
            "evolving_state": {
                "gear_budget": "frozen_until_april",
                "daylight_window": "weekend_mornings_only",
            },
        },
        "latent_forbidden_phrases": [
            "frozen_until_april",
            "weekend_mornings_only",
            "skip the coastal outing",
            "reject the borrowed body",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-01-08T18:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How should I store undeveloped rolls in a warm apartment?",
                    },
                    {
                        "role": "assistant",
                        "content": "Sealed bag in the fridge for longer waits; warm them before opening.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-01-12T20:20:00Z",
                "role_setup": "distractor",
                "distractor_id": "dist_1",
                "why_distractor": (
                    "Uses trip, upgrade, worth it, friend said amazing, and camera-body language matching "
                    "the final query, but the topic is a museum gift-shop compact camera impulse buy for "
                    "a tourist day — irrelevant to budget freeze and weekend daylight constraints."
                ),
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A friend said the museum gift-shop compact camera upgrade is amazing and that a spontaneous city trip with it is worth it. They want me to buy one for a tourist afternoon. I do not need another compact point-and-shoot.",
                    },
                    {
                        "role": "assistant",
                        "content": "Gift-shop upgrades are usually impulse pricing. A tourist afternoon trip does not require a new compact body if you already have something that works.",
                    },
                    {
                        "role": "user",
                        "content": "Exactly. Friend said it is amazing, but the upgrade does not feel worth it for one afternoon trip.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-01-14T20:05:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "Hobby spending frozen until April; developing at home; no new equipment.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "I am developing rolls at home. Hobby spending is frozen until April, so no new equipment before then.",
                    },
                    {
                        "role": "assistant",
                        "content": "A freeze until April is a hard budget boundary. Use what you already own.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-01-17T09:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Cheap negative scanning ideas?",
                    },
                    {
                        "role": "assistant",
                        "content": "Light pad plus phone clamp can work if you control dust and shoot RAW.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-01-20T19:50:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_B",
                "atomic_fact": "Only outdoor shooting window is Saturday and Sunday mornings; weekday evenings indoors; winter light dies early.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Weekday evenings I am indoors. My only outdoor shooting window is Saturday and Sunday mornings before winter light dies.",
                    },
                    {
                        "role": "assistant",
                        "content": "Weekend mornings are your scarce outdoor resource.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-01-24T11:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I tell FOMO trip invitations from useful practice?",
                    },
                    {
                        "role": "assistant",
                        "content": "Ask what concrete practice it unlocks that home cannot. Vague prestige is FOMO.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-01-27T18:40:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "People keep saying midweek coastal outings are amazing. Still undecided.",
                    },
                    {
                        "role": "assistant",
                        "content": "Decide from your calendar and budget constraints, not from how often people repeat amazing.",
                    },
                ],
            },
            {
                "session_id": 8,
                "timestamp": "2026-01-29T20:40:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Someone offered a Wednesday coastal outing with a borrowed high-end body. Friend said similar trips are amazing. Is the upgrade-style trip worth it for me right now?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "No. Your spending freeze until April and weekend-only outdoor window conflict with a Wednesday "
            "coastal outing. The gift-shop compact upgrade chatter is unrelated impulse talk."
        ),
        "required_elements": [
            "cites spending freeze until April",
            "cites weekend-morning outdoor window",
            "recommends declining Wednesday coastal outing",
            "ignores gift-shop compact as decisive",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "constrains", "target": "gear_outings", "hop": 1},
            {"source": "ev_B", "relation": "constrains", "target": "weekday_outdoor_sessions", "hop": 1},
            {
                "source": "dist_1",
                "relation": "analogous",
                "target": "surface_trip_upgrade_language_only",
                "hop": 1,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_dist",
                "type": "evidence_removed",
                "removed_session_ids": [2],
                "expected_gold": (
                    "Still decline: budget freeze and weekend-only light make the Wednesday outing a poor fit."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A3_HH_0008",
        "pilot_arm": "distractor",
        "pilot_domain": "hobby_habit",
        "association_type": "A3_cross_domain",
        "secondary_association_type": "distractor_interference",
        "domain_tags": ["hobbies/leisure", "household"],
        "persona": {
            "user_id": "u_hh_08",
            "stable_traits": [
                "Sunday batch cooker",
                "recurring family travel Sundays",
                "avoids default organizer roles",
            ],
            "evolving_state": {
                "sunday_capacity": "travel_disrupts_batch_cook",
                "hosting_fit": "poor_for_standing_dinners",
            },
        },
        "latent_forbidden_phrases": [
            "travel_disrupts_batch_cook",
            "poor_for_standing_dinners",
            "do not host Sunday dinner",
            "decline the standing dinner",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-02-01T10:10:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Leak-proof freezer containers for soup?",
                    },
                    {
                        "role": "assistant",
                        "content": "Latch lids with silicone gaskets, and leave headspace when freezing.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-02-04T19:30:00Z",
                "role_setup": "distractor",
                "distractor_id": "dist_1",
                "why_distractor": (
                    "Shares should I, signup, Sunday, dinner, friend said amazing, worth it with the query, "
                    "but discusses a one-time restaurant prix-fixe signup across town — not building hosting "
                    "and irrelevant to batch-cook plus travel constraints."
                ),
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A friend said a prix-fixe Sunday dinner signup at a restaurant across town is amazing and asked if it is worth it. Should I grab a seat for that one night? I am not hosting anything.",
                    },
                    {
                        "role": "assistant",
                        "content": "A one-night restaurant signup is just a reservation decision. Judge it on cost and travel time that evening, not on whether you want to become a host.",
                    },
                    {
                        "role": "user",
                        "content": "True. Friend said it is amazing, but I only care whether that single Sunday dinner out is worth it.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-02-05T18:45:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "Sunday batch cooking feeds the user for the work week.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Sunday batch cooking is how I eat all week. Skip it and I am buying takeout by Wednesday.",
                    },
                    {
                        "role": "assistant",
                        "content": "That block is load-bearing. Protect it from optional social cooking plans.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-02-08T09:40:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Breakfast ideas using leftover roasted vegetables?",
                    },
                    {
                        "role": "assistant",
                        "content": "Skillet eggs or a wrap with yogurt sauce. Both are fast.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-02-10T20:10:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_B",
                "atomic_fact": "Next several Sundays spent on trains visiting family; not home for kitchen block.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Next several Sundays I will be on trains visiting family, so I will not be home for my usual kitchen afternoon.",
                    },
                    {
                        "role": "assistant",
                        "content": "Anything that assumes you are home those afternoons needs another plan.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-02-13T12:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Meal kits that deliver Sunday ingredients — useful when weekends are messy?",
                    },
                    {
                        "role": "assistant",
                        "content": "Only if you are actually home on delivery day.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-02-15T19:10:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Building socials keep calling standing dinners amazing. Still thinking.",
                    },
                    {
                        "role": "assistant",
                        "content": "Standing plans need recurring capacity. Check that first.",
                    },
                ],
            },
            {
                "session_id": 8,
                "timestamp": "2026-02-16T21:05:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "My neighbor wants me to host a standing Sunday dinner for our building. Friend said it would be amazing. Should I say yes — is it worth it?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "No. Sunday batch cooking and multi-week Sunday family travel leave no capacity to host a "
            "standing building dinner. The restaurant prix-fixe signup talk is a different, one-off decision."
        ),
        "required_elements": [
            "cites Sunday batch cooking",
            "cites Sunday family travel",
            "recommends declining standing hosting",
            "does not treat restaurant signup as the answer",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "constrains", "target": "sunday_hosting", "hop": 1},
            {"source": "ev_B", "relation": "causes", "target": "sunday_absence", "hop": 1},
            {
                "source": "dist_1",
                "relation": "analogous",
                "target": "surface_sunday_dinner_language_only",
                "hop": 1,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_dist",
                "type": "evidence_removed",
                "removed_session_ids": [2],
                "expected_gold": (
                    "Still decline hosting based on batch-cook dependence and Sunday travel."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A3_HH_0009",
        "pilot_arm": "distractor",
        "pilot_domain": "hobby_habit",
        "association_type": "A3_cross_domain",
        "secondary_association_type": "distractor_interference",
        "domain_tags": ["hobbies/leisure", "health/wellness"],
        "persona": {
            "user_id": "u_hh_09",
            "stable_traits": [
                "evening pottery student",
                "early bakery shift hobby helper",
                "guards sleep before dawn shifts",
            ],
            "evolving_state": {
                "schedule_conflict": "pottery_vs_dawn_bakery",
                "sleep_priority": "pre_dawn_shift_protected",
            },
        },
        "latent_forbidden_phrases": [
            "pottery_vs_dawn_bakery",
            "pre_dawn_shift_protected",
            "drop the evening class",
            "do not add late studio nights",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-03-01T09:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I keep clay from drying out between weekly classes?",
                    },
                    {
                        "role": "assistant",
                        "content": "Wrap pieces in damp paper towels inside a sealed bag, and check moisture midweek.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-03-03T20:15:00Z",
                "role_setup": "distractor",
                "distractor_id": "dist_1",
                "why_distractor": (
                    "Uses class signup, evenings, friend said amazing, worth it, should I — matching the "
                    "query — but about a one-off weekend glaze workshop tourist ticket, not the recurring "
                    "evening class versus dawn bakery conflict."
                ),
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A friend said a weekend glaze workshop signup is amazing and asked if the class is worth it. Should I grab that one tourist-style ticket? It is not my regular evening studio.",
                    },
                    {
                        "role": "assistant",
                        "content": "Treat a one-off weekend workshop signup as a fun ticket decision. It does not automatically say anything about your recurring evening schedule.",
                    },
                    {
                        "role": "user",
                        "content": "Friend said it is amazing, but I only care whether that single workshop class signup is worth it.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-03-05T21:00:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "User's weekday wheel sessions at the studio often run past eleven and leave them wired.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "My weekday wheel sessions at the studio often run past eleven. I get home wired and it takes a while to settle.",
                    },
                    {
                        "role": "assistant",
                        "content": "Studio nights that run past eleven can push bedtime later even when the making itself is enjoyable.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-03-07T08:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Best way to clean tools without clogging the sink?",
                    },
                    {
                        "role": "assistant",
                        "content": "Wipe scraps into the trash first, then rinse in a bucket and dump settled water outside if allowed.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-03-09T06:40:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_B",
                "atomic_fact": "User helps shape loaves before sunrise at a friend's shop and needs solid sleep the night before.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A few times a week I help shape loaves before sunrise at a friend's shop. I need solid sleep the night before or I am useless at the oven.",
                    },
                    {
                        "role": "assistant",
                        "content": "Pre-dawn oven shifts make the prior night non-negotiable. Staying up late beforehand will tax that.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-03-11T12:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I choose between hobbies when both feel meaningful?",
                    },
                    {
                        "role": "assistant",
                        "content": "Rank by recovery cost, not by which one sounds cooler to friends.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-03-13T19:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "People keep saying an extra late evening class signup would be amazing and asking if it is worth it.",
                    },
                    {
                        "role": "assistant",
                        "content": "An extra late evening class signup only helps if it does not steal sleep you already allocated elsewhere. Amazing is not the test.",
                    },
                ],
            },
            {
                "session_id": 8,
                "timestamp": "2026-03-15T20:50:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "The studio opened another late evening class signup on nights before my bakery mornings. Friend said it is amazing. Should I add it — is it worth it?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Do not add it. Your weekday wheel sessions already run past eleven, and pre-dawn loaf shifts "
            "need solid sleep the night before. An extra late evening class signup on those nights conflicts. "
            "The weekend workshop ticket talk is unrelated."
        ),
        "required_elements": [
            "cites late studio wheel sessions",
            "cites pre-dawn shop/oven sleep need",
            "recommends against extra late class on those nights",
            "does not treat weekend workshop as decisive",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "causes", "target": "late_bedtime", "hop": 1},
            {"source": "ev_B", "relation": "constrains", "target": "late_bedtime_before_shifts", "hop": 1},
            {
                "source": "dist_1",
                "relation": "analogous",
                "target": "surface_class_signup_language_only",
                "hop": 1,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_dist",
                "type": "evidence_removed",
                "removed_session_ids": [2],
                "expected_gold": (
                    "Still decline the extra late class on bakery-eve nights based on sleep needs."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A3_HH_0010",
        "pilot_arm": "distractor",
        "pilot_domain": "hobby_habit",
        "association_type": "A3_cross_domain",
        "secondary_association_type": "distractor_interference",
        "domain_tags": ["hobbies/leisure"],
        "persona": {
            "user_id": "u_hh_10",
            "stable_traits": [
                "hosts board game nights",
                "lives with noise-sensitive roommate",
                "prefers low-conflict home hobbies",
            ],
            "evolving_state": {
                "home_noise_budget": "roommate_quiet_constraint",
                "game_night_fit": "needs_quiet_or_elsewhere",
            },
        },
        "latent_forbidden_phrases": [
            "roommate_quiet_constraint",
            "needs_quiet_or_elsewhere",
            "cancel loud game night",
            "do not host the party game night",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-03-02T18:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Good cooperative games for three people that are not too long?",
                    },
                    {
                        "role": "assistant",
                        "content": "Try short co-ops under ninety minutes with low table talk spikes if your space is shared.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-03-04T21:10:00Z",
                "role_setup": "distractor",
                "distractor_id": "dist_1",
                "why_distractor": (
                    "Shares game night, signup, friend said amazing, worth it, should I with the query, "
                    "but is about a public board-game cafe event ticket — not hosting at home and "
                    "irrelevant to roommate noise constraints."
                ),
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A friend said a board-game cafe game night signup is amazing and asked if that public event is worth it. Should I grab a ticket? It is not at my apartment.",
                    },
                    {
                        "role": "assistant",
                        "content": "A cafe game night signup is just an outing ticket. Judge noise and cost for that venue, not your apartment rules.",
                    },
                    {
                        "role": "user",
                        "content": "Friend said it is amazing. I only need to know if that cafe signup is worth it for a fun night out.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-03-06T19:40:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_A",
                "atomic_fact": "User regularly hosts small board game nights at home.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "I like hosting small board game nights at home every couple of weeks. It is my main social hobby.",
                    },
                    {
                        "role": "assistant",
                        "content": "Home hosting is a real social outlet. Keep the format compatible with whoever shares the space.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-03-08T11:15:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I teach a new game without a twenty-minute rules lecture?",
                    },
                    {
                        "role": "assistant",
                        "content": "Teach one round as a demo with open hands, then start for real. Keep the first score low-stakes.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-03-10T20:00:00Z",
                "role_setup": "target_evidence",
                "evidence_id": "ev_B",
                "atomic_fact": "Roommate is noise-sensitive in the evenings and asks for quieter nights at the apartment.",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "My roommate is noise-sensitive in the evenings and asked me to keep apartment nights quieter, especially with groups.",
                    },
                    {
                        "role": "assistant",
                        "content": "That is a hard household constraint. Loud party-style games at home will create conflict even if you love them.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-03-12T13:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Any soft-voice games that still feel social?",
                    },
                    {
                        "role": "assistant",
                        "content": "Tile-laying and quiet engine builders usually stay calmer than shouting party games.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-03-14T18:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "People keep saying loud party game nights are amazing. I am hesitant.",
                    },
                    {
                        "role": "assistant",
                        "content": "Hesitation is useful when someone else shares your walls. Match volume to the room.",
                    },
                ],
            },
            {
                "session_id": 8,
                "timestamp": "2026-03-16T21:20:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Friends want me to host a loud party-game night signup at my place. They said it would be amazing. Should I — is it worth it?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Host somewhere else or pick a quiet game. You like home game nights, but your roommate needs "
            "quieter evenings, so a loud party-game night at the apartment is a poor fit. The cafe ticket "
            "discussion is a separate outing."
        ),
        "required_elements": [
            "cites home board game hosting habit",
            "cites roommate evening noise sensitivity",
            "recommends against loud party hosting at home",
            "does not treat cafe signup as the answer",
        ],
        "associative_links": [
            {"source": "ev_A", "relation": "co_occurs", "target": "home_social_hobby", "hop": 1},
            {"source": "ev_B", "relation": "constrains", "target": "loud_home_events", "hop": 1},
            {
                "source": "dist_1",
                "relation": "analogous",
                "target": "surface_game_night_signup_language_only",
                "hop": 1,
            },
        ],
        "counterfactual_variants": [
            {
                "variant_id": "cf_remove_dist",
                "type": "evidence_removed",
                "removed_session_ids": [2],
                "expected_gold": (
                    "Still avoid loud party hosting at home because of the roommate quiet request."
                ),
            },
        ],
    },
    # -------------------------------------------------------------------------
    # ABSENCE (5): A5 — same query shapes, no target_evidence, abstain gold
    # -------------------------------------------------------------------------
    {
        "sample_id": "AMB_A5_HH_0011",
        "pilot_arm": "absence",
        "pilot_domain": "hobby_habit",
        "association_type": "A5_absence_control",
        "domain_tags": ["hobbies/leisure", "health/wellness"],
        "persona": {
            "user_id": "u_hh_11",
            "stable_traits": [
                "occasionally jogs",
                "asks for advice before committing to events",
            ],
            "evolving_state": {
                "event_readiness": "unknown_no_evidence",
                "knee_pattern": "unobserved",
            },
        },
        "latent_forbidden_phrases": [
            "unknown_no_evidence",
            "unobserved",
            "skip the mountain race",
            "knee cannot handle hills",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-01-07T07:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What is a gentle warm-up before an easy outdoor session?",
                    },
                    {
                        "role": "assistant",
                        "content": "Two minutes of brisk walking, then a few leg swings and ankle circles. Keep it light.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-01-11T19:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I politely decline weekend group invites?",
                    },
                    {
                        "role": "assistant",
                        "content": "Thank them, say you cannot make it, and optionally suggest another time. Short is fine.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-01-15T12:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Is foam rolling necessary after easy sessions?",
                    },
                    {
                        "role": "assistant",
                        "content": "No. Use it if it feels good; otherwise skip it.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-01-19T08:10:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Simple way to log how a workout felt?",
                    },
                    {
                        "role": "assistant",
                        "content": "Effort, mood, and one body note. Three words are enough.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-01-23T20:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Community signups are everywhere. How do I ignore hype?",
                    },
                    {
                        "role": "assistant",
                        "content": "Check the event against your known limits. If you have no personal limits on record, say you need more information.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-01-26T18:40:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What should I ask before joining any team event?",
                    },
                    {
                        "role": "assistant",
                        "content": "Ask about distance, elevation, pacing norms, and recovery time afterward.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-01-28T21:10:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A coworker says a mountain race signup this month is amazing and wants me to join the team. Should I?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Insufficient evidence in memory. You have not shared personal training limits, knee history, "
            "or elevation tolerance here, so I cannot recommend for or against the mountain race from prior "
            "conversations. Ask about the course profile and how your body has handled hills lately."
        ),
        "required_elements": [
            "states insufficient evidence / cannot recommend from memory",
            "notes absence of personal elevation or injury history",
            "suggests gathering course and body-status information",
        ],
        "associative_links": [],
        "counterfactual_variants": [
            {
                "variant_id": "cf_add_knee_evidence",
                "type": "evidence_added_hypothetical",
                "removed_session_ids": [],
                "expected_gold": (
                    "If incline knee flares and gentle-elevation guidance were on record, recommend declining."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A5_HH_0012",
        "pilot_arm": "absence",
        "pilot_domain": "hobby_habit",
        "association_type": "A5_absence_control",
        "domain_tags": ["hobbies/leisure"],
        "persona": {
            "user_id": "u_hh_12",
            "stable_traits": [
                "curious about cameras",
                "asks before spending on outings",
            ],
            "evolving_state": {
                "gear_budget": "unknown",
                "daylight_window": "unknown",
            },
        },
        "latent_forbidden_phrases": [
            "frozen_until_april",
            "weekend_mornings_only",
            "skip the coastal outing",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-01-09T18:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I keep dust off a lens without special gear?",
                    },
                    {
                        "role": "assistant",
                        "content": "A clean microfiber cloth and a blower bulb handle most dust. Avoid wiping dry grit across glass.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-01-13T12:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "People say gear upgrades are worth it. How do I stay skeptical?",
                    },
                    {
                        "role": "assistant",
                        "content": "Name the specific limitation you hit last month. If you cannot name one, skip the upgrade.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-01-17T10:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Any tips for packing light for a day out?",
                    },
                    {
                        "role": "assistant",
                        "content": "One body, one lens, spare battery, and a weather layer. Leave the rest.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-01-21T19:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I tell FOMO invitations from useful practice?",
                    },
                    {
                        "role": "assistant",
                        "content": "Ask what skill the outing practices that you cannot practice nearby.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-01-24T11:40:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Midweek coastal outings sound amazing in theory.",
                    },
                    {
                        "role": "assistant",
                        "content": "Theory is cheap. Check schedule and budget before you commit.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-01-27T20:10:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What questions should I ask before borrowing someone else's equipment?",
                    },
                    {
                        "role": "assistant",
                        "content": "Ask about insurance, replacement value, and whether you are comfortable with the learning curve on a short outing.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-01-29T20:40:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Someone offered a Wednesday coastal outing with a borrowed high-end body. Is that a smart move for me right now?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Not enough evidence in memory. You have not told me about your hobby budget, available daylight "
            "windows, or weekday constraints, so I cannot say whether the Wednesday coastal outing is smart "
            "for you. Share those constraints and I can help decide."
        ),
        "required_elements": [
            "states insufficient evidence / cannot recommend from memory",
            "notes missing budget and schedule constraints",
            "invites user to provide those facts",
        ],
        "associative_links": [],
        "counterfactual_variants": [
            {
                "variant_id": "cf_add_budget_and_light",
                "type": "evidence_added_hypothetical",
                "removed_session_ids": [],
                "expected_gold": (
                    "If a spending freeze and weekend-only outdoor window were known, recommend declining."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A5_HH_0013",
        "pilot_arm": "absence",
        "pilot_domain": "hobby_habit",
        "association_type": "A5_absence_control",
        "domain_tags": ["hobbies/leisure", "household"],
        "persona": {
            "user_id": "u_hh_13",
            "stable_traits": [
                "cooks sometimes",
                "friendly with neighbors",
            ],
            "evolving_state": {
                "sunday_capacity": "unknown",
                "hosting_fit": "unknown",
            },
        },
        "latent_forbidden_phrases": [
            "travel_disrupts_batch_cook",
            "poor_for_standing_dinners",
            "do not host Sunday dinner",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-02-02T10:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Good freezer containers for leftovers?",
                    },
                    {
                        "role": "assistant",
                        "content": "Latch lids with gaskets work well. Leave headspace for liquids.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-02-05T21:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I stay friendly in the building without becoming the default organizer?",
                    },
                    {
                        "role": "assistant",
                        "content": "Show up sometimes, bring a small dish, and never volunteer to own the calendar.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-02-08T09:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Quick breakfasts with leftover vegetables?",
                    },
                    {
                        "role": "assistant",
                        "content": "Eggs in a skillet or a wrap. Both are fast.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-02-11T12:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Are meal kits worth it when weekends are unpredictable?",
                    },
                    {
                        "role": "assistant",
                        "content": "Only if delivery matches days you are home.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-02-14T19:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "People say standing Sunday dinners are amazing for community.",
                    },
                    {
                        "role": "assistant",
                        "content": "They are amazing only if your Sundays are actually free on a recurring basis.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-02-15T16:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What should I clarify before agreeing to host anything recurring?",
                    },
                    {
                        "role": "assistant",
                        "content": "Clarify frequency, who shops, who cleans, and what happens when you travel.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-02-16T21:05:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "My neighbor wants me to host a standing Sunday dinner for our building. Should I say yes?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Insufficient evidence. You have not shared whether Sundays are free, whether you rely on that "
            "block for meal prep, or any travel pattern, so I cannot recommend yes or no from memory. Tell "
            "me your Sunday constraints first."
        ),
        "required_elements": [
            "states insufficient evidence / cannot recommend from memory",
            "notes missing Sunday schedule constraints",
            "asks user to provide those constraints",
        ],
        "associative_links": [],
        "counterfactual_variants": [
            {
                "variant_id": "cf_add_mealprep_travel",
                "type": "evidence_added_hypothetical",
                "removed_session_ids": [],
                "expected_gold": (
                    "If Sunday batch cooking and multi-week travel were known, recommend declining."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A5_HH_0014",
        "pilot_arm": "absence",
        "pilot_domain": "hobby_habit",
        "association_type": "A5_absence_control",
        "domain_tags": ["hobbies/leisure", "health/wellness"],
        "persona": {
            "user_id": "u_hh_14",
            "stable_traits": [
                "interested in climbing training",
                "asks before joining gym challenges",
            ],
            "evolving_state": {
                "finger_status": "unknown",
                "max_hang_readiness": "unknown",
            },
        },
        "latent_forbidden_phrases": [
            "post_pulley_guarded",
            "not_cleared",
            "skip the max-hang challenge",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-02-04T18:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Basic warm-up before any board session?",
                    },
                    {
                        "role": "assistant",
                        "content": "Easy dead hangs, light pull-ups, then short edge touches. Stop if a finger joint feels pinchy.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-02-07T11:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Ice after every session or only when irritated?",
                    },
                    {
                        "role": "assistant",
                        "content": "Only when irritated. Routine icing is usually unnecessary.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-02-10T19:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I evaluate gym challenge signups?",
                    },
                    {
                        "role": "assistant",
                        "content": "Check whether the protocol matches limits you already set for yourself.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-02-13T10:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Forearm work that is gentler than dense edge sessions?",
                    },
                    {
                        "role": "assistant",
                        "content": "Rice-bucket rotations and light controlled wrist curls are usually gentler.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-02-16T20:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Friends say this month's gym challenge is amazing for progress.",
                    },
                    {
                        "role": "assistant",
                        "content": "Progress still has to respect your injury history if you have one on record.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-02-18T12:15:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What should I ask a coach before a max-intensity block?",
                    },
                    {
                        "role": "assistant",
                        "content": "Ask about prior tendon issues, current pain flags, and how they would regress the plan.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-02-20T18:45:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "The climbing gym is pushing a max-hang challenge signup this month. Should I join?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Insufficient evidence in memory. You have not shared finger injury history or whether "
            "max hangs are currently in your training, so I cannot recommend joining or skipping from prior "
            "chats. Tell me how your fingers have felt with hard hangs lately."
        ),
        "required_elements": [
            "states insufficient evidence / cannot recommend from memory",
            "notes missing finger or max-hang history",
            "asks for current finger status",
        ],
        "associative_links": [],
        "counterfactual_variants": [
            {
                "variant_id": "cf_add_pulley_history",
                "type": "evidence_added_hypothetical",
                "removed_session_ids": [],
                "expected_gold": (
                    "If a prior pulley strain and max-hang avoidance were known, recommend not joining."
                ),
            },
        ],
    },
    {
        "sample_id": "AMB_A5_HH_0015",
        "pilot_arm": "absence",
        "pilot_domain": "hobby_habit",
        "association_type": "A5_absence_control",
        "domain_tags": ["hobbies/leisure", "health/wellness"],
        "persona": {
            "user_id": "u_hh_15",
            "stable_traits": [
                "reads in the evening",
                "curious about reading devices",
            ],
            "evolving_state": {
                "bedtime_medium": "unknown",
                "screen_risk": "unknown",
            },
        },
        "latent_forbidden_phrases": [
            "paper_only_working",
            "insomnia_trigger",
            "skip the e-ink upgrade",
        ],
        "sessions": [
            {
                "session_id": 1,
                "timestamp": "2026-02-05T22:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Good wind-down playlist length before sleep?",
                    },
                    {
                        "role": "assistant",
                        "content": "Fifteen to twenty minutes is usually enough.",
                    },
                ],
            },
            {
                "session_id": 2,
                "timestamp": "2026-02-08T12:30:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Dim book-light tips for a dark room?",
                    },
                    {
                        "role": "assistant",
                        "content": "Warm light, low brightness, aimed at the page rather than your eyes.",
                    },
                ],
            },
            {
                "session_id": 3,
                "timestamp": "2026-02-11T19:40:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Friends say bedtime device upgrades are worth it.",
                    },
                    {
                        "role": "assistant",
                        "content": "Worth it only if they preserve whatever already helps you sleep.",
                    },
                ],
            },
            {
                "session_id": 4,
                "timestamp": "2026-02-14T10:20:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "How do I keep a reading habit without turning it into a streak contest?",
                    },
                    {
                        "role": "assistant",
                        "content": "Track showing up, not page counts.",
                    },
                ],
            },
            {
                "session_id": 5,
                "timestamp": "2026-02-17T20:00:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "Someone said an e-ink tablet for bedtime is amazing.",
                    },
                    {
                        "role": "assistant",
                        "content": "Compare it to the routine you already use, especially anything that affects sleep.",
                    },
                ],
            },
            {
                "session_id": 6,
                "timestamp": "2026-02-19T21:10:00Z",
                "role_setup": "filler",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "What should I check before buying any bedtime reading device?",
                    },
                    {
                        "role": "assistant",
                        "content": "Check light temperature, app distractions, and whether you have a sleep issue tied to screens.",
                    },
                ],
            },
            {
                "session_id": 7,
                "timestamp": "2026-02-21T21:15:00Z",
                "role_setup": "associative_cue_query",
                "cue_id": "cue_1",
                "dialogue": [
                    {
                        "role": "user",
                        "content": "A friend says a new e-ink tablet for bedtime is amazing and worth the upgrade. Should I get one?",
                    },
                ],
            },
        ],
        "gold_answer": (
            "Insufficient evidence in memory. You have not shared whether evening screens affect your sleep "
            "or what bedtime reading method currently works, so I cannot recommend buying or skipping the "
            "tablet from prior chats. Tell me how screens affect your sleep and I can advise."
        ),
        "required_elements": [
            "states insufficient evidence / cannot recommend from memory",
            "notes missing sleep-and-screen history",
            "asks for current bedtime routine facts",
        ],
        "associative_links": [],
        "counterfactual_variants": [
            {
                "variant_id": "cf_add_screen_insomnia",
                "type": "evidence_added_hypothetical",
                "removed_session_ids": [],
                "expected_gold": (
                    "If screen-caused insomnia and a working paper-only habit were known, caution against the upgrade."
                ),
            },
        ],
    },
]

assert len(BLUEPRINTS) == 15
assert [b["sample_id"] for b in BLUEPRINTS] == [
    "AMB_A3_HH_0001",
    "AMB_A3_HH_0002",
    "AMB_A3_HH_0003",
    "AMB_A2_HH_0004",
    "AMB_A2_HH_0005",
    "AMB_A3_HH_0006",
    "AMB_A3_HH_0007",
    "AMB_A3_HH_0008",
    "AMB_A3_HH_0009",
    "AMB_A3_HH_0010",
    "AMB_A5_HH_0011",
    "AMB_A5_HH_0012",
    "AMB_A5_HH_0013",
    "AMB_A5_HH_0014",
    "AMB_A5_HH_0015",
]
