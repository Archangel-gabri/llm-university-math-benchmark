# Judge validation: second independent LLM judge

To assess the reliability of the primary automated judge (**Claude Sonnet 4**), a **second, independent large language model — Claude Opus 4.8 — re-graded a stratified subset of 30 responses**, blind to the primary judge's scores. The subset spans all five mathematical areas, all twelve models, all solution-validity levels (0–3), and all error types.

This is an **inter-model reliability check**, not human validation: both judges are large language models. It measures how stable rubric grading is across independent models; it does not establish agreement with human experts. (The two judges are also from the same vendor family, which may inflate agreement — a caveat stated in the paper.)

## Results (Opus 4.8 vs. Sonnet 4, N = 30)

| Dimension | Exact agreement | Cohen's κ |
|-----------|-----------------|-----------|
| Answer correctness (0/1) | 76.7 % | 0.55 |
| Solution validity (0–3) | 53.3 % | **0.74** (quadratic-weighted) / 0.58 (linear) |
| Error type (6 classes) | 60.0 % | 0.48 |

Mean absolute difference on solution validity: **0.53** on the 0–3 scale. Agreement on validity (the primary endpoint) is **substantial** by the usual interpretation of weighted κ.

Per-response grades: [`experiment/judge_validation_opus_grades.json`](experiment/judge_validation_opus_grades.json).

## What the disagreements revealed

Most disagreements were borderline validity calls (±1) or error-type label differences. Two disagreements exposed **errors in the reference-answer key**, where the model was actually correct but the primary judge penalised it against a faulty reference:

- **DM-12** (generating function): the reference answer gave a₁₀ = 5120 with aₙ = n·2ⁿ⁻¹, but that formula yields a₁ = 1, contradicting the stated a₁ = 2. The correct closed form is **aₙ = n·2ⁿ**, so **a₁₀ = 10240** — which the model produced and the primary judge wrongly marked incorrect.
- **MS-13** (efficiency of an exponential-family estimator): the reference's intermediate variance expression is wrong; the correct variance is **D(α\*) = α²/(n−2)**, which the models derived correctly (the final conclusion "not efficient, asymptotically efficient" is unaffected).

Additionally, **NT-14** has no reference answer in the bank (marked TBD) and should be completed or excluded.

These reference-key issues are tracked for correction; the published per-response scores reflect grading against the original reference and should be read with this erratum in mind.
