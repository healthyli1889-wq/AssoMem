# Solver prompt (vNext)

Sent once per evaluation arm. The payload carries only `context`, `query` and
`target_proposition`; every annotation, gold field and arm label stays behind
the boundary in `dataset.solver_input`.

```text
Decide whether the supplied conversation history supports `target_proposition`.

Return exactly one JSON object with exactly these keys:
{"decision":"yes"|"no","answer":string,"evidence_session_ids":[integer]}.

Answer `yes` only if specific dated episodes in this person's own history support
the proposition. Answer `no` if the history does not contain what the proposition
needs, even when the proposition sounds sensible in general: general social,
practical or common-sense plausibility is not evidence, and `no` does not assert
that the opposite is true.

Several sessions may look topically relevant without bearing on the proposition.
Cite in `evidence_session_ids` only the sessions your decision actually rests on,
and only IDs visible in the input. `answer` must briefly justify the decision by
reference to those sessions. Do not mention benchmark metadata or hidden labels.

Input: {"context": ["<20 dated sessions>"], "query": "<the final user turn>", "target_proposition": "<the binary proposition being judged>"}
```
