# Review packet — AMB_SV_group_chat_before_support_032_associative

## Candidate
- User: `anon_social_user_05`
- Query type: `situational_fit`
- Polarity: `reject`
- Query: Based only on these records, should this always-on reunion role be flagged as a fit risk for this user?
- Latent C: The always-on reunion role should be flagged as a fit risk because it would impair the user's attention for the Sunday support call.
- Calibrated wording: flagged as a fit risk

## Co-activation claim
- ev_A (session 5): When I keep an always-on group chat active late into the evening, I am less patient in a next-day support conversation.
- ev_B (session 12): I lead a weekly Sunday support call where a friend expects my full attention.
- Bridge: ev_A describes why the proposed exposure needs recovery; ev_B establishes the specific responsibility that would be impaired. Together they support C: The always-on reunion role should be flagged as a fit risk because it would impair the user's attention for the Sunday support call.

## Deterministic audit
```json
{
  "kind": "deterministic",
  "scores": {
    "same_person_temporal_separation": 100,
    "a_only_insufficiency": null,
    "b_only_insufficiency": null,
    "joint_support_for_C": null,
    "C_novelty_no_leakage": 100,
    "query_natural_recall_trigger": null,
    "link_broken_validity": 100,
    "gold_scoreability": 100,
    "query_taxonomy_compliance": 100
  },
  "unscored_semantic_clauses": [
    "a_only_insufficiency",
    "b_only_insufficiency",
    "joint_support_for_C",
    "query_natural_recall_trigger"
  ],
  "failures": [],
  "pass": true
}
```

## Arm: `full`
- Expected mode: `infer_C`
- Lineage: `{"transform": "identity", "retained_sessions": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}`
```json
{
  "context": [
    {
      "session_id": 1,
      "timestamp": "2026-01-04T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I like hosting small dinners. I had a small lunch with a colleague."
        },
        {
          "role": "assistant",
          "content": "Smaller formats can leave room for the rest of the day."
        }
      ]
    },
    {
      "session_id": 2,
      "timestamp": "2026-01-07T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I cleared a few messages before bed."
        },
        {
          "role": "assistant",
          "content": "Closing small loops can make tomorrow easier."
        }
      ]
    },
    {
      "session_id": 3,
      "timestamp": "2026-01-10T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I chose a quiet route home."
        },
        {
          "role": "assistant",
          "content": "You protected a little decompression time."
        }
      ]
    },
    {
      "session_id": 4,
      "timestamp": "2026-01-13T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I checked my weekend plan once more."
        },
        {
          "role": "assistant",
          "content": "Seeing the plan makes trade-offs easier to notice."
        }
      ]
    },
    {
      "session_id": 5,
      "timestamp": "2026-01-16T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "When I keep an always-on group chat active late into the evening, I am less patient in a next-day support conversation."
        },
        {
          "role": "assistant",
          "content": "That sounds like a repeatable recovery pattern."
        }
      ]
    },
    {
      "session_id": 6,
      "timestamp": "2026-01-19T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I watered the plants before breakfast."
        },
        {
          "role": "assistant",
          "content": "A small routine can anchor the morning."
        }
      ]
    },
    {
      "session_id": 7,
      "timestamp": "2026-01-22T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I organized a drawer that had been bothering me."
        },
        {
          "role": "assistant",
          "content": "A contained task gave you a reset."
        }
      ]
    },
    {
      "session_id": 8,
      "timestamp": "2026-01-25T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I listened to a short podcast while cooking."
        },
        {
          "role": "assistant",
          "content": "You kept the evening low-pressure."
        }
      ]
    },
    {
      "session_id": 9,
      "timestamp": "2026-01-28T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I replied to an invitation with a clear boundary."
        },
        {
          "role": "assistant",
          "content": "Clear expectations reduce social friction."
        }
      ]
    },
    {
      "session_id": 10,
      "timestamp": "2026-01-31T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I made a note to call a relative next month."
        },
        {
          "role": "assistant",
          "content": "You planned the connection without rushing it."
        }
      ]
    },
    {
      "session_id": 11,
      "timestamp": "2026-02-03T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I booked a routine appointment."
        },
        {
          "role": "assistant",
          "content": "You handled a practical detail early."
        }
      ]
    },
    {
      "session_id": 12,
      "timestamp": "2026-02-06T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I lead a weekly Sunday support call where a friend expects my full attention."
        },
        {
          "role": "assistant",
          "content": "That responsibility has a specific interpersonal demand."
        }
      ]
    },
    {
      "session_id": 13,
      "timestamp": "2026-02-09T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I sent a short check-in to a friend after work."
        },
        {
          "role": "assistant",
          "content": "A brief check-in can still be meaningful."
        }
      ]
    },
    {
      "session_id": 14,
      "timestamp": "2026-02-12T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I took a quiet walk after dinner."
        },
        {
          "role": "assistant",
          "content": "A small reset can make an evening feel less crowded."
        }
      ]
    },
    {
      "session_id": 15,
      "timestamp": "2026-02-15T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I sorted a few photos from a recent trip."
        },
        {
          "role": "assistant",
          "content": "Low-pressure tasks can be restorative."
        }
      ]
    },
    {
      "session_id": 16,
      "timestamp": "2026-02-18T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I made tea before reading for a while."
        },
        {
          "role": "assistant",
          "content": "You made room for a calm transition."
        }
      ]
    },
    {
      "session_id": 17,
      "timestamp": "2026-02-21T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I wrote down a reminder for next week."
        },
        {
          "role": "assistant",
          "content": "External reminders protect follow-through."
        }
      ]
    },
    {
      "session_id": 18,
      "timestamp": "2026-02-24T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I had a small lunch with a colleague."
        },
        {
          "role": "assistant",
          "content": "Smaller formats can leave room for the rest of the day."
        }
      ]
    },
    {
      "session_id": 19,
      "timestamp": "2026-02-27T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I cleared a few messages before bed."
        },
        {
          "role": "assistant",
          "content": "Closing small loops can make tomorrow easier."
        }
      ]
    },
    {
      "session_id": 20,
      "timestamp": "2026-03-02T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "A reunion group asks me to keep a busy message thread running through Saturday night."
        },
        {
          "role": "assistant",
          "content": "It is worth checking the fit against the commitments you already described."
        }
      ]
    }
  ],
  "query": "Based only on these records, should this always-on reunion role be flagged as a fit risk for this user?"
}
```
- Why original C is or is not licensed: A and B jointly support the target proposition.

## Arm: `a_only`
- Expected mode: `withhold_C`
- Lineage: `{"transform": "remove_ev_B", "removed_sessions": [12]}`
```json
{
  "context": [
    {
      "session_id": 1,
      "timestamp": "2026-01-04T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I like hosting small dinners. I had a small lunch with a colleague."
        },
        {
          "role": "assistant",
          "content": "Smaller formats can leave room for the rest of the day."
        }
      ]
    },
    {
      "session_id": 2,
      "timestamp": "2026-01-07T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I cleared a few messages before bed."
        },
        {
          "role": "assistant",
          "content": "Closing small loops can make tomorrow easier."
        }
      ]
    },
    {
      "session_id": 3,
      "timestamp": "2026-01-10T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I chose a quiet route home."
        },
        {
          "role": "assistant",
          "content": "You protected a little decompression time."
        }
      ]
    },
    {
      "session_id": 4,
      "timestamp": "2026-01-13T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I checked my weekend plan once more."
        },
        {
          "role": "assistant",
          "content": "Seeing the plan makes trade-offs easier to notice."
        }
      ]
    },
    {
      "session_id": 5,
      "timestamp": "2026-01-16T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "When I keep an always-on group chat active late into the evening, I am less patient in a next-day support conversation."
        },
        {
          "role": "assistant",
          "content": "That sounds like a repeatable recovery pattern."
        }
      ]
    },
    {
      "session_id": 6,
      "timestamp": "2026-01-19T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I watered the plants before breakfast."
        },
        {
          "role": "assistant",
          "content": "A small routine can anchor the morning."
        }
      ]
    },
    {
      "session_id": 7,
      "timestamp": "2026-01-22T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I organized a drawer that had been bothering me."
        },
        {
          "role": "assistant",
          "content": "A contained task gave you a reset."
        }
      ]
    },
    {
      "session_id": 8,
      "timestamp": "2026-01-25T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I listened to a short podcast while cooking."
        },
        {
          "role": "assistant",
          "content": "You kept the evening low-pressure."
        }
      ]
    },
    {
      "session_id": 9,
      "timestamp": "2026-01-28T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I replied to an invitation with a clear boundary."
        },
        {
          "role": "assistant",
          "content": "Clear expectations reduce social friction."
        }
      ]
    },
    {
      "session_id": 10,
      "timestamp": "2026-01-31T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I made a note to call a relative next month."
        },
        {
          "role": "assistant",
          "content": "You planned the connection without rushing it."
        }
      ]
    },
    {
      "session_id": 11,
      "timestamp": "2026-02-03T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I booked a routine appointment."
        },
        {
          "role": "assistant",
          "content": "You handled a practical detail early."
        }
      ]
    },
    {
      "session_id": 13,
      "timestamp": "2026-02-09T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I sent a short check-in to a friend after work."
        },
        {
          "role": "assistant",
          "content": "A brief check-in can still be meaningful."
        }
      ]
    },
    {
      "session_id": 14,
      "timestamp": "2026-02-12T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I took a quiet walk after dinner."
        },
        {
          "role": "assistant",
          "content": "A small reset can make an evening feel less crowded."
        }
      ]
    },
    {
      "session_id": 15,
      "timestamp": "2026-02-15T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I sorted a few photos from a recent trip."
        },
        {
          "role": "assistant",
          "content": "Low-pressure tasks can be restorative."
        }
      ]
    },
    {
      "session_id": 16,
      "timestamp": "2026-02-18T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I made tea before reading for a while."
        },
        {
          "role": "assistant",
          "content": "You made room for a calm transition."
        }
      ]
    },
    {
      "session_id": 17,
      "timestamp": "2026-02-21T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I wrote down a reminder for next week."
        },
        {
          "role": "assistant",
          "content": "External reminders protect follow-through."
        }
      ]
    },
    {
      "session_id": 18,
      "timestamp": "2026-02-24T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I had a small lunch with a colleague."
        },
        {
          "role": "assistant",
          "content": "Smaller formats can leave room for the rest of the day."
        }
      ]
    },
    {
      "session_id": 19,
      "timestamp": "2026-02-27T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I cleared a few messages before bed."
        },
        {
          "role": "assistant",
          "content": "Closing small loops can make tomorrow easier."
        }
      ]
    },
    {
      "session_id": 20,
      "timestamp": "2026-03-02T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "A reunion group asks me to keep a busy message thread running through Saturday night."
        },
        {
          "role": "assistant",
          "content": "It is worth checking the fit against the commitments you already described."
        }
      ]
    }
  ],
  "query": "Based only on these records, should this always-on reunion role be flagged as a fit risk for this user?"
}
```
- Why original C is or is not licensed: A alone does not establish that the proposed event conflicts with a concrete responsibility.

## Arm: `b_only`
- Expected mode: `withhold_C`
- Lineage: `{"transform": "remove_ev_A", "removed_sessions": [5]}`
```json
{
  "context": [
    {
      "session_id": 1,
      "timestamp": "2026-01-04T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I like hosting small dinners. I had a small lunch with a colleague."
        },
        {
          "role": "assistant",
          "content": "Smaller formats can leave room for the rest of the day."
        }
      ]
    },
    {
      "session_id": 2,
      "timestamp": "2026-01-07T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I cleared a few messages before bed."
        },
        {
          "role": "assistant",
          "content": "Closing small loops can make tomorrow easier."
        }
      ]
    },
    {
      "session_id": 3,
      "timestamp": "2026-01-10T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I chose a quiet route home."
        },
        {
          "role": "assistant",
          "content": "You protected a little decompression time."
        }
      ]
    },
    {
      "session_id": 4,
      "timestamp": "2026-01-13T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I checked my weekend plan once more."
        },
        {
          "role": "assistant",
          "content": "Seeing the plan makes trade-offs easier to notice."
        }
      ]
    },
    {
      "session_id": 6,
      "timestamp": "2026-01-19T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I watered the plants before breakfast."
        },
        {
          "role": "assistant",
          "content": "A small routine can anchor the morning."
        }
      ]
    },
    {
      "session_id": 7,
      "timestamp": "2026-01-22T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I organized a drawer that had been bothering me."
        },
        {
          "role": "assistant",
          "content": "A contained task gave you a reset."
        }
      ]
    },
    {
      "session_id": 8,
      "timestamp": "2026-01-25T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I listened to a short podcast while cooking."
        },
        {
          "role": "assistant",
          "content": "You kept the evening low-pressure."
        }
      ]
    },
    {
      "session_id": 9,
      "timestamp": "2026-01-28T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I replied to an invitation with a clear boundary."
        },
        {
          "role": "assistant",
          "content": "Clear expectations reduce social friction."
        }
      ]
    },
    {
      "session_id": 10,
      "timestamp": "2026-01-31T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I made a note to call a relative next month."
        },
        {
          "role": "assistant",
          "content": "You planned the connection without rushing it."
        }
      ]
    },
    {
      "session_id": 11,
      "timestamp": "2026-02-03T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I booked a routine appointment."
        },
        {
          "role": "assistant",
          "content": "You handled a practical detail early."
        }
      ]
    },
    {
      "session_id": 12,
      "timestamp": "2026-02-06T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I lead a weekly Sunday support call where a friend expects my full attention."
        },
        {
          "role": "assistant",
          "content": "That responsibility has a specific interpersonal demand."
        }
      ]
    },
    {
      "session_id": 13,
      "timestamp": "2026-02-09T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I sent a short check-in to a friend after work."
        },
        {
          "role": "assistant",
          "content": "A brief check-in can still be meaningful."
        }
      ]
    },
    {
      "session_id": 14,
      "timestamp": "2026-02-12T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I took a quiet walk after dinner."
        },
        {
          "role": "assistant",
          "content": "A small reset can make an evening feel less crowded."
        }
      ]
    },
    {
      "session_id": 15,
      "timestamp": "2026-02-15T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I sorted a few photos from a recent trip."
        },
        {
          "role": "assistant",
          "content": "Low-pressure tasks can be restorative."
        }
      ]
    },
    {
      "session_id": 16,
      "timestamp": "2026-02-18T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I made tea before reading for a while."
        },
        {
          "role": "assistant",
          "content": "You made room for a calm transition."
        }
      ]
    },
    {
      "session_id": 17,
      "timestamp": "2026-02-21T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I wrote down a reminder for next week."
        },
        {
          "role": "assistant",
          "content": "External reminders protect follow-through."
        }
      ]
    },
    {
      "session_id": 18,
      "timestamp": "2026-02-24T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I had a small lunch with a colleague."
        },
        {
          "role": "assistant",
          "content": "Smaller formats can leave room for the rest of the day."
        }
      ]
    },
    {
      "session_id": 19,
      "timestamp": "2026-02-27T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I cleared a few messages before bed."
        },
        {
          "role": "assistant",
          "content": "Closing small loops can make tomorrow easier."
        }
      ]
    },
    {
      "session_id": 20,
      "timestamp": "2026-03-02T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "A reunion group asks me to keep a busy message thread running through Saturday night."
        },
        {
          "role": "assistant",
          "content": "It is worth checking the fit against the commitments you already described."
        }
      ]
    }
  ],
  "query": "Based only on these records, should this always-on reunion role be flagged as a fit risk for this user?"
}
```
- Why original C is or is not licensed: B alone does not establish that the proposed event would impair the responsibility.

## Arm: `link_broken`
- Expected mode: `withhold_C`
- Lineage: `{"transform": "replace_relation_in_ev_B", "changed_sessions": [12], "source_owner_preserved": true}`
```json
{
  "context": [
    {
      "session_id": 1,
      "timestamp": "2026-01-04T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I like hosting small dinners. I had a small lunch with a colleague."
        },
        {
          "role": "assistant",
          "content": "Smaller formats can leave room for the rest of the day."
        }
      ]
    },
    {
      "session_id": 2,
      "timestamp": "2026-01-07T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I cleared a few messages before bed."
        },
        {
          "role": "assistant",
          "content": "Closing small loops can make tomorrow easier."
        }
      ]
    },
    {
      "session_id": 3,
      "timestamp": "2026-01-10T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I chose a quiet route home."
        },
        {
          "role": "assistant",
          "content": "You protected a little decompression time."
        }
      ]
    },
    {
      "session_id": 4,
      "timestamp": "2026-01-13T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I checked my weekend plan once more."
        },
        {
          "role": "assistant",
          "content": "Seeing the plan makes trade-offs easier to notice."
        }
      ]
    },
    {
      "session_id": 5,
      "timestamp": "2026-01-16T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "When I keep an always-on group chat active late into the evening, I am less patient in a next-day support conversation."
        },
        {
          "role": "assistant",
          "content": "That sounds like a repeatable recovery pattern."
        }
      ]
    },
    {
      "session_id": 6,
      "timestamp": "2026-01-19T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I watered the plants before breakfast."
        },
        {
          "role": "assistant",
          "content": "A small routine can anchor the morning."
        }
      ]
    },
    {
      "session_id": 7,
      "timestamp": "2026-01-22T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I organized a drawer that had been bothering me."
        },
        {
          "role": "assistant",
          "content": "A contained task gave you a reset."
        }
      ]
    },
    {
      "session_id": 8,
      "timestamp": "2026-01-25T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I listened to a short podcast while cooking."
        },
        {
          "role": "assistant",
          "content": "You kept the evening low-pressure."
        }
      ]
    },
    {
      "session_id": 9,
      "timestamp": "2026-01-28T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I replied to an invitation with a clear boundary."
        },
        {
          "role": "assistant",
          "content": "Clear expectations reduce social friction."
        }
      ]
    },
    {
      "session_id": 10,
      "timestamp": "2026-01-31T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I made a note to call a relative next month."
        },
        {
          "role": "assistant",
          "content": "You planned the connection without rushing it."
        }
      ]
    },
    {
      "session_id": 11,
      "timestamp": "2026-02-03T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I booked a routine appointment."
        },
        {
          "role": "assistant",
          "content": "You handled a practical detail early."
        }
      ]
    },
    {
      "session_id": 12,
      "timestamp": "2026-02-06T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I have a Sunday call to confirm restaurant reservations; it is routine and can be rescheduled."
        },
        {
          "role": "assistant",
          "content": "That Sunday activity is low stakes and can be moved without affecting another person."
        }
      ]
    },
    {
      "session_id": 13,
      "timestamp": "2026-02-09T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I sent a short check-in to a friend after work."
        },
        {
          "role": "assistant",
          "content": "A brief check-in can still be meaningful."
        }
      ]
    },
    {
      "session_id": 14,
      "timestamp": "2026-02-12T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I took a quiet walk after dinner."
        },
        {
          "role": "assistant",
          "content": "A small reset can make an evening feel less crowded."
        }
      ]
    },
    {
      "session_id": 15,
      "timestamp": "2026-02-15T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I sorted a few photos from a recent trip."
        },
        {
          "role": "assistant",
          "content": "Low-pressure tasks can be restorative."
        }
      ]
    },
    {
      "session_id": 16,
      "timestamp": "2026-02-18T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I made tea before reading for a while."
        },
        {
          "role": "assistant",
          "content": "You made room for a calm transition."
        }
      ]
    },
    {
      "session_id": 17,
      "timestamp": "2026-02-21T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I wrote down a reminder for next week."
        },
        {
          "role": "assistant",
          "content": "External reminders protect follow-through."
        }
      ]
    },
    {
      "session_id": 18,
      "timestamp": "2026-02-24T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I had a small lunch with a colleague."
        },
        {
          "role": "assistant",
          "content": "Smaller formats can leave room for the rest of the day."
        }
      ]
    },
    {
      "session_id": 19,
      "timestamp": "2026-02-27T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "I cleared a few messages before bed."
        },
        {
          "role": "assistant",
          "content": "Closing small loops can make tomorrow easier."
        }
      ]
    },
    {
      "session_id": 20,
      "timestamp": "2026-03-02T18:00:00Z",
      "speaker_id": "anon_social_user_05",
      "speaker_label": "User",
      "dialogue": [
        {
          "role": "user",
          "content": "A reunion group asks me to keep a busy message thread running through Saturday night."
        },
        {
          "role": "assistant",
          "content": "It is worth checking the fit against the commitments you already described."
        }
      ]
    }
  ],
  "query": "Based only on these records, should this always-on reunion role be flagged as a fit risk for this user?"
}
```
- Why original C is or is not licensed: B-prime removes the responsibility connector while retaining same-user conversational form.
