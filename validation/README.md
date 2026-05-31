# Judge validation / Валидация судьи

[← Main README](../README.md) · [← Главный README](../README.ru.md)

## English — human expert + second LLM

The primary automated judge is **Claude Sonnet 4**. Its reliability was checked two ways on the **same stratified subset of 30 responses** (spanning all five areas, all twelve models, all validity levels, and all error types), each grader blind to the judge's scores and to the identity of the solving model.

### 1. Human expert vs. primary judge (the main check)

An independent human expert (a co-author) re-graded the 30 responses by the rubric.

| Dimension | Exact agreement | Cohen's κ |
|-----------|-----------------|-----------|
| Answer correctness (0/1) | 73.3 % | 0.49 |
| Solution validity (0–3) | 53.3 % | **0.74** (quadratic-weighted) / 0.59 (linear) |
| Error type (6 classes) | 56.7 % | 0.44 |

Mean absolute difference on validity: **0.53** on the 0–3 scale. Agreement on validity (the primary endpoint) is **substantial**. Where the two differed, the automated judge was slightly **more conservative** (assigned the lower validity score in most cases).

### 2. Second LLM (Claude Opus 4.8) — corroboration

A second, independent LLM graded the same subset. It agreed **almost perfectly with the human expert** (quadratic-weighted κ = 0.97 on validity; 96.7 % exact on answer correctness). Because the human and a different-vendor-independent model converge, the human-vs-primary-judge disagreements reflect **genuine borderline cases**, not idiosyncratic human error.

### 3. What the disagreements revealed

Most disagreements were ±1 validity calls or error-type labels. Two exposed **errors in the reference-answer key**, where the model was correct but the primary judge penalised it against a faulty reference, now corrected in `data/problems/`:

- **DM-12**: correct closed form aₙ = n·2ⁿ ⇒ a₁₀ = **10240** (key wrongly said 5120).
- **MS-13**: correct variance **D(α\*) = α²/(n−2)** (the "not efficient" conclusion is unaffected).

### Files
- `judge_validation_spivak_grades.json` — human expert grades (30 responses).
- `judge_validation_opus_grades.json` — second-LLM grades.
- `judge_validation_30.xlsx` / `judge_validation_30_FILLED.xlsx` — blind worksheet (empty / filled).
- `HUMAN_VALIDATION_PROMPT.md` — grading instructions.

## Русский — человек-эксперт + вторая модель

Основной автоматический судья — **Claude Sonnet 4**. Его надёжность проверена двумя способами на **одной и той же стратифицированной подвыборке из 30 ответов** (все пять разделов, все двенадцать моделей, все уровни валидности и все типы ошибок); каждый оценщик не видел оценок судьи и не знал, какая модель решала.

### 1. Человек-эксперт против основного судьи (главная проверка)

Независимый человек-эксперт (соавтор) переоценил 30 ответов по рубрике.

| Измерение | Точное совпадение | κ Коэна |
|-----------|-------------------|---------|
| Правильность ответа (0/1) | 73,3 % | 0,49 |
| Валидность решения (0–3) | 53,3 % | **0,74** (взвешенная) / 0,59 (линейная) |
| Тип ошибки (6 классов) | 56,7 % | 0,44 |

Средняя абсолютная разница по валидности: **0,53** на шкале 0–3. Согласие по валидности (главный показатель) — **существенное**. В расхождениях автоматический судья был чуть **строже** (чаще ставил более низкую валидность).

### 2. Вторая модель (Claude Opus 4.8) — подтверждение

Вторая независимая модель оценила ту же подвыборку. Она совпала с человеком-экспертом **почти идеально** (взвешенная κ = 0,97 по валидности; 96,7 % точного совпадения по правильности ответа). Поскольку человек и независимая модель другого вендора сходятся, расхождения судьи с человеком отражают **настоящие пограничные случаи**, а не случайную ошибку человека.

### 3. Что вскрыли расхождения

Большинство расхождений — это ±1 по валидности или метка типа ошибки. Два расхождения вскрыли **ошибки в ключе эталонных ответов**, где модель была права, а судья штрафовал её по неверному эталону; исправлено в `data/problems/`:

- **DM-12**: верная замкнутая форма aₙ = n·2ⁿ ⇒ a₁₀ = **10240** (в ключе ошибочно было 5120).
- **MS-13**: верная дисперсия **D(α\*) = α²/(n−2)** (вывод о «неэффективности» не меняется).

### Файлы
- `judge_validation_spivak_grades.json` — оценки человека-эксперта (30 ответов).
- `judge_validation_opus_grades.json` — оценки второй модели.
- `judge_validation_30.xlsx` / `judge_validation_30_FILLED.xlsx` — слепой бланк (пустой / заполненный).
- `HUMAN_VALIDATION_PROMPT.md` — инструкция по оцениванию.
