#!/usr/bin/env python3
"""LLM-as-judge evaluation: use Claude Sonnet to score all 900 responses."""

import json
import os
import sys
import time
import glob
from datetime import datetime
from pathlib import Path

import yaml
from openai import OpenAI


def load_problem_index() -> dict:
    """Load all problems indexed by ID."""
    idx = {}
    for yaml_file in sorted(glob.glob("problems/*.yaml")):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
        for p in data.get("problems", []):
            p["section"] = data.get("section", "")
            p["section_id"] = data.get("section_id", "")
            idx[p["id"]] = p
    return idx

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")
if not OPENROUTER_KEY:
    print("ERROR: Set OPENROUTER_API_KEY")
    sys.exit(1)

client = OpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    timeout=120.0,
    max_retries=2,
)

JUDGE_MODEL = "anthropic/claude-sonnet-4"

RUBRIC_PROMPT = """Ты — эксперт-математик, оценивающий решение математической задачи, данное ИИ-моделью.

ЗАДАЧА: {problem}
РАЗДЕЛ: {section}
СЛОЖНОСТЬ: {difficulty} (1=простая, 2=средняя, 3=сложная)

ЭТАЛОННЫЙ ОТВЕТ: {expected_answer}

ОТВЕТ ИИ:
{response}

Оцени ответ по 5 измерениям. Верни ТОЛЬКО валидный JSON без markdown:

{{
  "answer_correct": 0 или 1,
  "solution_validity": 0-3,
  "error_type": "PE" | "CE" | "AE" | "HE" | "IE" | "NONE",
  "completeness": 0-2,
  "clarity": 0-2,
  "brief_comment": "одно предложение"
}}

ПОЯСНЕНИЯ:
- answer_correct: 1 если финальный ответ совпадает с эталоном (включая эквивалентные формы), иначе 0
- solution_validity: 0=грубая ошибка/нет решения, 1=частично верный подход, 2=в основном верно с недочётами, 3=безупречно
- error_type: PE (процедурная ошибка), CE (концептуальная), AE (арифметическая/вычислительная), HE (галлюцинация — уверенный неправильный ответ), IE (тупик/отказ), NONE (нет ошибки)
- completeness: 0=не завершено/пусто, 1=частично, 2=все шаги
- clarity: 0=нечитаемо, 1=понятно, 2=образцово
- brief_comment: краткий комментарий (1 предложение) о качестве

Будь строгим. Если решение пустое или модель только сформулировала задачу без решения — answer_correct=0, validity=0, completeness=0."""


def evaluate_response(problem: dict, response: str) -> dict:
    prompt = RUBRIC_PROMPT.format(
        problem=problem["text"],
        section=problem.get("section", ""),
        difficulty=problem.get("difficulty", 0),
        expected_answer=problem.get("expected_answer", ""),
        response=response[:3500],
    )

    for attempt in range(2):
        try:
            r = client.chat.completions.create(
                model=JUDGE_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=400,
            )
            text = r.choices[0].message.content or ""
            text = text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()
            scores = json.loads(text)
            scores["_judge_model"] = JUDGE_MODEL
            scores["_judge_input_tokens"] = r.usage.prompt_tokens if r.usage else 0
            scores["_judge_output_tokens"] = r.usage.completion_tokens if r.usage else 0
            return scores
        except Exception as e:
            if attempt == 0:
                time.sleep(5)
                continue
            return {
                "answer_correct": -1,
                "solution_validity": -1,
                "error_type": "JUDGE_ERROR",
                "completeness": -1,
                "clarity": -1,
                "brief_comment": f"Judge error: {str(e)[:100]}",
                "_judge_model": JUDGE_MODEL,
            }


def main():
    results_dir = Path("results/full")
    scores_dir = Path("results/scores")
    scores_dir.mkdir(parents=True, exist_ok=True)

    problem_idx = load_problem_index()
    print(f"Loaded {len(problem_idx)} problems from YAML")

    model_files = sorted([f for f in results_dir.glob("*.json")
                          if "all_results" not in f.name])
    print(f"Found {len(model_files)} model result files")

    total_done = 0
    total_judge_input = 0
    total_judge_output = 0

    for model_file in model_files:
        out_file = scores_dir / model_file.name
        if out_file.exists():
            with open(out_file) as f:
                existing = json.load(f)
            ok = sum(1 for r in existing if r.get("answer_correct", -1) >= 0)
            if ok >= 70:
                print(f"✓ {model_file.name} already scored ({ok}/{len(existing)})")
                continue

        with open(model_file) as f:
            responses = json.load(f)

        valid_responses = [r for r in responses if not r.get("error") and r.get("response")]
        if not valid_responses:
            print(f"⚠ {model_file.name} — no valid responses")
            continue

        print(f"\n=== Scoring {model_file.name} ({len(valid_responses)} responses) ===")
        scored = []

        for i, resp in enumerate(valid_responses):
            print(f"  [{i+1}/{len(valid_responses)}] {resp['problem_id']:8s}...", end=" ", flush=True)
            problem = problem_idx.get(resp["problem_id"], {})
            # Augment problem with expected_answer from resp
            problem = {**problem, "expected_answer": resp.get("expected_answer", problem.get("answer", ""))}
            scores = evaluate_response(problem, resp["response"])

            combined = {
                "model_name": resp["model_name"],
                "problem_id": resp["problem_id"],
                "problem_section": resp.get("problem_section", ""),
                "problem_section_id": resp.get("problem_section_id", ""),
                "problem_difficulty": resp.get("problem_difficulty", 0),
                "expected_answer": resp.get("expected_answer", ""),
                "response_tokens": resp.get("output_tokens", 0),
                "response_latency": resp.get("latency", 0),
                **scores,
            }
            scored.append(combined)
            total_done += 1
            total_judge_input += scores.get("_judge_input_tokens", 0)
            total_judge_output += scores.get("_judge_output_tokens", 0)

            if scores.get("answer_correct", -1) < 0:
                print(f"JUDGE_ERR")
            else:
                print(f"A={scores['answer_correct']} V={scores['solution_validity']} E={scores.get('error_type','?')}")

            time.sleep(0.2)

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(scored, f, ensure_ascii=False, indent=2)
        print(f"  Saved: {out_file}")

    print(f"\n{'='*60}")
    print(f"DONE: {total_done} responses scored")
    print(f"Judge tokens: {total_judge_input} input + {total_judge_output} output")
    # Cost estimate: Claude Sonnet ~$3/M in, $15/M out
    cost = total_judge_input * 3 / 1_000_000 + total_judge_output * 15 / 1_000_000
    print(f"Est. cost: ${cost:.2f}")


if __name__ == "__main__":
    main()
