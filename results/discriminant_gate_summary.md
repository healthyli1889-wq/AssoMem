# Discriminant-validity gate results

Total items: 1879
Evidence unavailable (excluded): 170 (9.0%)
Evidence available but chunk match failed (excluded): 699
Scored items: 1010
gate_pass (flat_rag_hit@3 == False): 588 / 1010 (58.2%)

## By source

| value | n scored | n unavailable | pass rate | median lex_jaccard | median cosine |
|---|---|---|---|---|---|
| locomo | 930 | 7 | 63.2% | 0.125 | 0.304 |
| longmemeval | 78 | 163 | 0.0% | 0.037 | 0.335 |
| memoryarena | 2 | 699 | 0.0% | 0.333 | 0.561 |

## By association_type

| value | n scored | n unavailable | pass rate | median lex_jaccard | median cosine |
|---|---|---|---|---|---|
| (none) | 2 | 699 | 0.0% | 0.333 | 0.561 |
| A1_relational_binding | 58 | 128 | 74.1% | 0.071 | 0.232 |
| A2_cue_chain | 872 | 30 | 62.5% | 0.128 | 0.306 |
| A4_temporal_consistency | 72 | 0 | 0.0% | 0.037 | 0.335 |
| A5_absence_control | 6 | 12 | 0.0% | 0.000 | 0.398 |

## By f9_strength (LoCoMo only)

| value | n scored | n unavailable | pass rate | median lex_jaccard | median cosine |
|---|---|---|---|---|---|
| (none) | 80 | 862 | 0.0% | 0.037 | 0.335 |
| absent | 0 | 4 | n/a | n/a | n/a |
| strong | 32 | 0 | 50.0% | 0.040 | 0.285 |
| weak | 898 | 3 | 63.7% | 0.125 | 0.305 |

## Threshold sensitivity (embed_cosine, mock=lexical-proxy)

| cosine < threshold | pass rate |
|---|---|
| 0.2 | 19.7% |
| 0.3 | 47.7% |
| 0.4 | 78.6% |
| 0.5 | 94.3% |
| 0.6 | 98.6% |
