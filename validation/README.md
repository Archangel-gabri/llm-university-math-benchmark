# Judge validation / Валидация судьи

[← Main README](../README.md) · [← Главный README](../README.ru.md)

> ## ⚠️ Correction, 2026-08-27
>
> Until this revision, this file stated that an **independent human expert (a co-author)** re-graded
> the 30-response subset, and presented a second LLM as independent corroboration of that human.
> **That was wrong. No human re-graded the subset — both grade sets were produced by language
> models.** The file `judge_validation_spivak_grades.json` carried a co-author's name for grades he
> did not produce and has been renamed. The numbers below are unchanged, but what they measure is
> not what was claimed: κ = 0.74 is *model vs. model*, and the κ = 0.97 comparison is between two
> model outputs and therefore corroborates nothing about human agreement.
>
> **Human validation of the judge remains outstanding work.** `HUMAN_VALIDATION_PROMPT.md` is the
> protocol for doing it, not a record that it was done.

---

## English — second-LLM reliability check

The primary automated judge is **Claude Sonnet 4**. Its reliability was checked on a **stratified
subset of 30 responses** (spanning all five areas, all twelve models, all validity levels, and all
error types), with the grader blind to the judge's scores and to the identity of the solving model.

The grader was **another language model**, not a person.

### Second LLM vs. primary judge

| Dimension | Exact agreement | Cohen's κ |
|-----------|-----------------|-----------|
| Answer correctness (0/1) | 73.3 % | 0.49 |
| Solution validity (0–3) | 53.3 % | **0.74** (quadratic-weighted) / 0.59 (linear) |
| Error type (6 classes) | 56.7 % | 0.44 |

Mean absolute difference on validity: **0.53** on the 0–3 scale. Where the two differed, the primary
judge was slightly **more conservative** (assigned the lower validity score in most cases).

This is an **inter-model consistency check**. It shows that two models applying the same rubric land
in roughly the same place; it does **not** establish that either matches expert human judgement.
A second grade set (`judge_validation_opus_grades.json`) exists and agrees closely with the first,
but since both are model output, that closeness measures shared model behaviour, not accuracy.

### What the disagreements revealed

Most disagreements were ±1 validity calls or error-type labels. Two exposed **errors in the
reference-answer key**, where the model was correct but the primary judge penalised it against a
faulty reference. These are real defects found by the check, and they are corrected in
`data/problems/`:

- **DM-12**: correct closed form aₙ = n·2ⁿ ⇒ a₁₀ = **10240** (key wrongly said 5120).
- **MS-13**: correct variance **D(α\*) = α²/(n−2)** (the "not efficient" conclusion is unaffected).

### Files

| File | What it is |
|---|---|
| `judge_validation_secondary_llm_grades.json` | Second-LLM grades for the 30-response subset. *(Formerly `judge_validation_spivak_grades.json` — renamed because the name implied human authorship.)* |
| `judge_validation_opus_grades.json` | A further model grade set over the same subset. |
| `judge_validation_30.xlsx` | Blind worksheet, empty. |
| `judge_validation_30_filled_by_llm.xlsx` | The same worksheet, filled by a model. *(Formerly `judge_validation_30_FILLED.xlsx`.)* |
| `HUMAN_VALIDATION_PROMPT.md` | Grading protocol for a human validation that **has not been carried out**. |

## Русский — проверка надёжности второй моделью

> **Поправка от 27.08.2026.** До этой правки здесь было написано, что подвыборку из 30 ответов
> переоценил **независимый человек-эксперт (соавтор)**, а вторая модель это независимо подтвердила.
> **Это неверно: человек подвыборку не оценивал — оба набора оценок сделаны языковыми моделями.**
> Файл `judge_validation_spivak_grades.json` нёс имя соавтора под оценками, которых тот не делал,
> и переименован. Числа ниже не изменились, но измеряют они не то, что заявлялось: κ = 0,74 — это
> *модель против модели*, а κ = 0,97 сравнивает два модельных вывода и ничего не говорит о согласии
> с человеком. **Человеческая валидация судьи остаётся невыполненной работой**;
> `HUMAN_VALIDATION_PROMPT.md` — протокол, как её провести, а не запись, что она проведена.

Основной автоматический судья — **Claude Sonnet 4**. Его надёжность проверена на
**стратифицированной подвыборке из 30 ответов** (все пять разделов, все двенадцать моделей, все
уровни валидности и все типы ошибок); оценщик не видел оценок судьи и не знал, какая модель решала.
Оценщиком была **другая языковая модель**, не человек.

### Вторая модель против основного судьи

| Измерение | Точное совпадение | κ Коэна |
|-----------|-------------------|---------|
| Правильность ответа (0/1) | 73,3 % | 0,49 |
| Валидность решения (0–3) | 53,3 % | **0,74** (взвешенная) / 0,59 (линейная) |
| Тип ошибки (6 классов) | 56,7 % | 0,44 |

Средняя абсолютная разница по валидности: **0,53** на шкале 0–3. В расхождениях основной судья был
чуть **строже** (чаще ставил более низкую валидность).

Это **проверка согласованности между моделями**. Она показывает, что две модели по одной рубрике
приходят примерно к одному; она **не** доказывает, что хоть одна из них совпадает с экспертной
человеческой оценкой.

### Что вскрыли расхождения

Большинство расхождений — ±1 по валидности или метка типа ошибки. Два расхождения вскрыли
**ошибки в ключе эталонных ответов**, где модель была права, а судья штрафовал её по неверному
эталону. Это настоящие дефекты, найденные проверкой; исправлено в `data/problems/`:

- **DM-12**: верная замкнутая форма aₙ = n·2ⁿ ⇒ a₁₀ = **10240** (в ключе ошибочно было 5120).
- **MS-13**: верная дисперсия **D(α\*) = α²/(n−2)** (вывод о «неэффективности» не меняется).
