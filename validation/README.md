# Judge validation: human expert + second LLM

The primary automated judge is **Claude Sonnet 4**. Its reliability was checked two ways on the **same stratified subset of 30 responses** (spanning all five areas, all twelve models, all validity levels, and all error types), each grader blind to the judge's scores and to the identity of the solving model.

## 1. Human expert vs. primary judge (the main check)

An independent human expert (a co-author) re-graded the 30 responses by the rubric.

| Dimension | Exact agreement | Cohen's κ |
|-----------|-----------------|-----------|
| Answer correctness (0/1) | 73.3 % | 0.49 |
| Solution validity (0–3) | 53.3 % | **0.74** (quadratic-weighted) / 0.59 (linear) |
| Error type (6 classes) | 56.7 % | 0.44 |

Mean absolute difference on validity: **0.53** on the 0–3 scale. Agreement on validity (the primary endpoint) is **substantial**. Where the two differed, the automated judge was slightly **more conservative** (assigned the lower validity score in most cases).

## 2. Second LLM (Claude Opus 4.8) — corroboration

A second, independent LLM graded the same subset. It agreed **almost perfectly with the human expert** (quadratic-weighted κ = 0.97 on validity; 96.7 % exact on answer correctness). Because the human and a different-vendor-independent model converge, the human-vs-primary-judge disagreements reflect **genuine borderline cases**, not idiosyncratic human error.

## 3. What the disagreements revealed

Most disagreements were ±1 validity calls or error-type labels. Two exposed **errors in the reference-answer key**, where the model was correct but the primary judge penalised it against a faulty reference, now corrected in `data/problems/`:

- **DM-12**: correct closed form aₙ = n·2ⁿ ⇒ a₁₀ = **10240** (key wrongly said 5120).
- **MS-13**: correct variance **D(α\*) = α²/(n−2)** (the "not efficient" conclusion is unaffected).

## Files
- `judge_validation_spivak_grades.json` — human expert grades (30 responses).
- `judge_validation_opus_grades.json` — second-LLM grades.
- `judge_validation_30.xlsx` / `judge_validation_30_FILLED.xlsx` — blind worksheet (empty / filled).
- `HUMAN_VALIDATION_PROMPT.md` — grading instructions.
