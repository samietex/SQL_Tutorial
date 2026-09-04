# Interview & Job-Readiness Prep

This repo doesn't target a certification, it targets a job. This file is the track-by-track map for using it that way: what actually gets asked in interviews for Data Analyst, Analytics Engineer, and Data Engineer roles, which notebooks and companion guides matter most for each, and how to study the guides so the material sticks under interview pressure rather than just on a re-read.

## How to actually use the companion guides

Each notebook in this repo has a matching file in [`study-guides/`](study-guides/). Don't read them side by side on your first pass, that turns into passive re-reading, which doesn't build recall the way retrieval does. Instead:

1. **First pass:** work the notebook itself top to bottom, actually running the SQL against your own AdventureWorks2022 install, not just reading it.
2. **Second pass:** close the notebook, open the study guide, and try to answer the interview questions *before* reading the model answers. Say your answer out loud or write it down, producing an answer is what builds recall, recognizing a correct one when you see it doesn't.
3. **Gap check:** compare your answer to the model answer. Where you were vague, too long-winded, or just wrong, that's your signal for what to re-drill, not the whole notebook again.
4. **Spaced repetition:** before starting a new notebook, skim the "Gotchas & common mistakes" section of the previous one or two guides. This is the cheapest way to keep earlier material from decaying before an actual interview.

Most model answers in these guides are written to be spoken in 30-90 seconds, that's roughly the real format of a live technical-screen answer. Practice saying them, not just thinking them.

## Track-by-track: what to prioritize

Every notebook is fair game for any of the three tracks, SQL is SQL. But interviewers weight topics differently depending on the role, and knowing that ahead of time is most of the advantage.

### Data Analyst

Interviews lean heavily on `SELECT`/`WHERE`/`ORDER BY` fluency, `GROUP BY` reporting logic, and `JOIN` correctness, usually as live coding against a schema you've never seen before, sometimes as a take-home asking for a specific business answer from raw tables.

| Priority | Notebook | Guide |
|---|---|---|
| Highest | 01, 02, 03 | [01](study-guides/01-sql-basics.md), [02](study-guides/02-aggregation.md), [03](study-guides/03-joins.md) |
| High | 04, 05 | [04](study-guides/04-subqueries-to-ctes.md), [05](study-guides/05-window-functions-part-1.md) |
| Useful, less common | 06, 08a, 08b, Appendix A | [06](study-guides/06-window-functions-part-2.md), [08a](study-guides/08a-changing-data-part-1.md), [08b](study-guides/08b-changing-data-part-2.md), [Appendix A](study-guides/appendix-a-sql-overview.md) |

What to over-prepare: the `WHERE` vs `HAVING` distinction (02), the anti-join "customers with no orders" pattern (03), and explaining a join-grain miscount out loud without being asked to code it (03), that last one is a favorite because it tests judgment, not just syntax recall.

### Analytics Engineer

Interviews add CTEs, window functions, and code readability/maintainability on top of the analyst core, often as a take-home you have to defend afterward: "why did you structure it this way," not just "does it run."

| Priority | Notebook | Guide |
|---|---|---|
| Highest | 02, 03, 04, 05 | [02](study-guides/02-aggregation.md), [03](study-guides/03-joins.md), [04](study-guides/04-subqueries-to-ctes.md), [05](study-guides/05-window-functions-part-1.md) |
| High | 06 | [06](study-guides/06-window-functions-part-2.md) |
| Useful | 01, 08a, 08b | [01](study-guides/01-sql-basics.md), [08a](study-guides/08a-changing-data-part-1.md), [08b](study-guides/08b-changing-data-part-2.md) |

What to over-prepare: CTE-vs-nested-subquery readability tradeoffs (04), the `ROW_NUMBER()` greatest-n-per-group pattern (05), and being able to explain *why* you'd reach for a CTE vs a temp table in a specific scenario (04), that's a judgment question, and judgment is exactly what a take-home review is scoring.

### Data Engineer

Interviews go deepest on window function frames, DML safety, and DDL/schema design, the parts of SQL that touch pipeline correctness and production risk directly, not just reporting correctness.

| Priority | Notebook | Guide |
|---|---|---|
| Highest | 05, 06, 08a, 08b | [05](study-guides/05-window-functions-part-1.md), [06](study-guides/06-window-functions-part-2.md), [08a](study-guides/08a-changing-data-part-1.md), [08b](study-guides/08b-changing-data-part-2.md) |
| High | 02, 03, 04 | [02](study-guides/02-aggregation.md), [03](study-guides/03-joins.md), [04](study-guides/04-subqueries-to-ctes.md) |
| Useful | 01, Appendix A | [01](study-guides/01-sql-basics.md), [Appendix A](study-guides/appendix-a-sql-overview.md) |

What to over-prepare: the `LAST_VALUE()` frame trap (06), it's a genuine senior/mid differentiator question; "what's the first thing you check before an `UPDATE`/`DELETE` in production" (08a); and walking through adding a foreign key constraint to an existing table without breaking existing rows (08b).

## Interview format cheat sheet

- **Technical screen** (live, 30-45 min, shared editor or whiteboard tool): expect notebooks 01-05 syntax fluency, explained out loud while you type. Speed and correctness both count, but a wrong-but-narrated answer usually beats a right-but-silent one, interviewers are scoring how you think, not just the final query.
- **Take-home** (async, hours to a few days): expect a real, messier dataset and an open-ended business question. This is where CTE readability (04), join-grain awareness (03), and DML safety habits (08a) actually get evaluated, not just whether the final number is correct.
- **Whiteboard / no-editor** (increasingly rare, still shows up for senior DE/AE roles): expect window functions (05, 06) and schema design (08b) drawn out conceptually before syntax matters, be ready to describe a `PARTITION BY`/frame or a foreign-key relationship in plain language first.

## Building a portfolio project from this material

Passing an interview and having something to point to in one are different things. To turn this repo into an actual portfolio artifact:

- **Chain notebooks into one real analysis.** Right now each notebook is a standalone concept demo. Pick a real question against AdventureWorks2022 (top customers by lifetime value, month-over-month order trends, which product categories have declining repeat purchase rates) and answer it using the *sequence* this repo teaches: joins to assemble the data (03), CTEs to name each step (04), window functions to rank or trend it (05, 06), aggregated into a final summary (02). That sequence, visibly used together, is what a take-home is actually testing.
- **Write down the query plan, not just the query.** For any non-trivial query, note in a comment or a short doc why you chose a `LEFT JOIN` over an `INNER JOIN`, or a CTE over a temp table, at that specific step. Being able to defend a choice, not just produce a working query, is the difference a live interview is built to surface.
- **Practice the DML safety habit publicly.** Show a `SELECT` with the exact `WHERE` clause run *before* the `UPDATE`/`DELETE` it corresponds to, as a paired example, in a README or a notebook cell. It's a small thing that signals real production experience.
- **Say the interview answers out loud, not just in your head.** Every question in every `study-guides/` file is written to be answerable in 30-90 seconds, spoken. That's the actual format a technical screen takes, rehearsing the words matters as much as knowing the answer.

## After this repo

The [Course Overview](<00 - Course Overview.ipynb>) and the [reading version of this curriculum](https://aaboutdata.substack.com/p/start-here-from-beginner-to-job-ready) cover where the roadmap goes next. This repo's own ceiling is standard SQL against a single relational engine, it doesn't cover query performance tuning, execution plans, indexing strategy in depth, or engine-specific extensions (JSON functions, PL/pgSQL, T-SQL stored procedures) that senior DE interviews sometimes probe. Treat those as the next layer once the fundamentals here are solid enough to explain without hesitation.
