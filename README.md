# LLM University-Level Mathematics Benchmark (process-level, Russian)

Open dataset accompanying the paper **"Comparative evaluation of large language models as assistants for solving university-level mathematics problems: a process-level rubric analysis"** (Kubrak V.A., Spivak D.R., Nozdryakov D.V., 2026).

Unlike answer-only math benchmarks, this dataset evaluates the **solution process**, not just the final answer, using a multidimensional rubric graded by an LLM-as-a-judge.

> Открытый датасет к статье «Сравнительная оценка больших языковых моделей как помощников при решении математических задач университетского уровня». В отличие от бенчмарков, оценивающих только итоговый ответ, здесь оценивается **процесс решения** по многомерной рубрике.

## What's inside

| Folder | Contents |
|--------|----------|
| `problems/` | 75 original university-level problems (5 areas × 15), with reference solutions and answers, in YAML. Areas: differential equations (DE), probability & statistics (MS), number theory & combinatorics (NT), discrete math & logic (DM), mathematical methods (MM). |
| `responses/` | Raw model responses (one JSON per model, 12 models). Each record has the full response text, latency, token counts, exact model snapshot, and problem metadata. |
| `scores/` | Per-response rubric scores from the LLM judge (answer_correct, solution_validity, error_type, completeness, clarity) with a one-sentence judge comment. |
| `tables/` | Aggregate CSVs (overall, by-section, by-difficulty, error distribution, all per-response scores). |
| `prompts/` | The solver prompt (sent to every model) and the judge rubric prompt. |
| `code/` | `evaluate.py` — the LLM-as-a-judge scoring script. |

## Method (as run)

- **12 models** via OpenRouter, 27–28 May 2026: Grok 4.3, Claude Opus 4, Claude Sonnet 4, GPT-4.1, Gemini 2.5 Flash, DeepSeek V4 Pro, DeepSeek V4 Flash, DeepSeek R1, Qwen3 235B, Llama 4 Maverick, Gemma 3 27B, Mistral Small.
- **75 problems**, single text track, **one run per problem** (N=1), `temperature=0`, `max_tokens=4096`.
- **Judge:** `anthropic/claude-sonnet-4` (LLM-as-a-judge) against a reference answer. 887/900 responses scored (13 parse failures excluded, concentrated in DeepSeek models).
- **Rubric:** answer correctness (0/1), solution validity (0–3), error type (PE/CE/AE/HE/IE/NONE), completeness (0–2), clarity (0–2).

### Limitations (exploratory study)

Single run per problem (N=1) and a **single automated judge without human validation** are acknowledged limitations. The judge model (Claude Sonnet 4) is itself among the evaluated models — a self-evaluation overlap that is disclosed and mitigated by grading against a fixed reference answer. Repeated runs, independent human grading (inter-rater reliability), multimodal/OCR tracks, and CAS systems are planned extensions.

## Headline results (mean solution validity, 0–3)

| Model | Accuracy | Validity | Median latency (s) | Avg tokens | n |
|-------|----------|----------|--------------------|------------|---|
| Grok 4.3 | 0.827 | **2.65** | 10.7 | 1180 | 75 |
| Claude Opus 4 | 0.787 | 2.60 | 41.7 | 940 | 75 |
| DeepSeek V4 Flash | 0.803 | 2.58 | 32.2 | 1981 | 71 |
| DeepSeek V4 Pro | 0.765 | 2.57 | 41.1 | 1984 | 68 |
| Claude Sonnet 4 | 0.773 | 2.52 | 12.1 | 949 | 75 |
| Qwen3 235B | 0.800 | 2.47 | 61.4 | 4217 | 75 |
| GPT-4.1 | 0.760 | 2.41 | 11.2 | 1022 | 75 |
| DeepSeek R1 | 0.699 | 2.34 | 146.2 | 3848 | 73 |
| Llama 4 Maverick | 0.693 | 2.29 | 22.6 | 844 | 75 |
| Gemini 2.5 Flash | 0.587 | 2.11 | 11.8 | 1807 | 75 |
| Gemma 3 27B | 0.573 | 2.07 | 30.7 | 903 | 75 |
| Mistral Small | 0.013 | 0.05 | 1.8 | 115 | 75 |

Differences across models are significant (Friedman test, χ²=351, p<0.001). See the paper for full analysis.

## License

Dataset (problems, responses, scores, tables): **CC BY 4.0**. Code: **MIT**. See `LICENSE`.

## Citation

```bibtex
@article{kubrak2026llmmath,
  title   = {Comparative evaluation of large language models as assistants for solving university-level mathematics problems: a process-level rubric analysis},
  author  = {Kubrak, V.A. and Spivak, D.R. and Nozdryakov, D.V.},
  year    = {2026}
}
```
