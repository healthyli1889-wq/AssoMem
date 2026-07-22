# Author prompt: one Work vNext candidate

You are authoring one candidate for a same-person associative-memory benchmark.

Create two temporally separated memories A and B about the **same user**. Each
memory alone must be insufficient for the latent inference C. Together, under a
natural query Q, A and B must support C as a useful but calibrated personal
inference.

Do not write a dual-constraint decision item. Do not use two independent reasons
that both point toward accepting or rejecting the same option. Do not make C an
explicit sentence or close paraphrase in any session or in Q.

Use exactly one approved query type:

1. preference generalization;
2. situational fit;
3. recommendation ranking;
4. predicted reaction;
5. behavior explanation;
6. conditional recommendation.

Specify:

```text
ev_A: dated, user-owned episode
ev_B: dated, user-owned episode
coactivation_bridge: why A+B jointly support C
latent_C: calibrated, not directly stated inference
query: realistic recall trigger
polarity: accept | reject | conditional | non_decision
```

Write matched counterfactual arms:

- `a_only`: B is unavailable; original C must not be established.
- `b_only`: A is unavailable; original C must not be established.
- `link_broken`: A and B remain facts about the same user with comparable surface
  structure, but their relationship no longer licenses C.
- `source_swap`: optional source-monitoring control; one fact belongs to another
  person and must never be called link-broken.

For every arm, state why original C is or is not licensed. Return a DRAFT only.
It cannot be released until deterministic checks pass, an independent evaluator
assigns at least 96/100 to every core clause, and a human reviewer explicitly
approves the current stage.
