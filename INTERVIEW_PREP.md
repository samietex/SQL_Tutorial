# Interview and Job-Readiness Prep

This repo doesn't target a certification; it targets a job. This file is the track-by-track map for using it that way: what gets asked in interviews for Data Analyst, Analytics Engineer, and Data Engineer roles, which notebooks and study guides matter most for each, and how to study the guides so the material holds up under interview pressure rather than only on a re-read.

## How to use the study guides

Each notebook has a matching file in [`study-guides/`](study-guides/). Don't read them side by side on a first pass, which turns into passive re-reading and doesn't build recall the way retrieval does. Instead:

1. **First pass:** work the notebook top to bottom, running every cell and changing queries to see what happens, including the AdventureWorks section (in Colab or on your own machine).
2. **Second pass:** close the notebook, open the study guide, and answer the interview questions *before* reading the model answers. Say your answer out loud or write it down; producing an answer builds recall, and recognizing a correct one doesn't.
3. **Gap check:** compare your answer with the model answer. Where you were vague, long-winded, or wrong is what to re-drill, not the whole notebook.
4. **Spaced repetition:** before starting a new notebook, skim the "Gotchas and common mistakes" of the previous one or two guides. It's the cheapest way to stop earlier material fading before a real interview.

Most model answers are written to be spoken in 30 to 90 seconds, roughly the length of a live technical-screen answer. Practise saying them, not just thinking them.

## Track by track: what to prioritize

Every notebook is fair game for every track, since SQL is SQL, but interviewers weight topics differently by role, and knowing that ahead of time is most of the advantage.

### Data Analyst

Interviews lean on `SELECT`, `WHERE`, and `ORDER BY` fluency, `GROUP BY` reporting logic, and join correctness, usually as live coding against a schema you've never seen, sometimes as a take-home asking for a specific business answer from raw tables.

| Priority | Notebooks | Guides |
| --- | --- | --- |
| Highest | 02, 03, 04, 09 | [02](study-guides/02-sql-basics.md), [03](study-guides/03-aggregation.md), [04](study-guides/04-joins.md), [09](study-guides/09-thinking-in-metrics.md) |
| High | 05, 06 | [05](study-guides/05-subqueries-to-ctes.md), [06](study-guides/06-window-functions-part-1.md) |
| Useful | 01, 07, 08a, 08b, Appendix A | [01](study-guides/01-what-is-a-database.md), [07](study-guides/07-window-functions-part-2.md), [08a](study-guides/08a-changing-data-part-1.md), [08b](study-guides/08b-changing-data-part-2.md), [A](study-guides/appendix-a-sql-server-reference.md) |

The [capstone](<capstone-online-store-analysis.ipynb>) matters for every track, because "walk me through a project" comes up in nearly every interview loop, whatever the role; its [study guide](study-guides/capstone-online-store-analysis.md) has model answers.

What to over-prepare: `WHERE` against `HAVING` (03), the "customers with no orders" anti-join (04), explaining a join-grain miscount out loud without being asked to code it (04), and turning a vague question like "who are our best customers?" into a definition before writing anything (09). The last two test judgment rather than syntax, which is why interviewers like them.

### Analytics Engineer

Interviews add CTEs, window functions, and readability on top of the analyst core, often as a take-home you defend afterwards: "why did you structure it this way?", not only "does it run?"

| Priority | Notebooks | Guides |
| --- | --- | --- |
| Highest | 03, 04, 05, 06, 09 | [03](study-guides/03-aggregation.md), [04](study-guides/04-joins.md), [05](study-guides/05-subqueries-to-ctes.md), [06](study-guides/06-window-functions-part-1.md), [09](study-guides/09-thinking-in-metrics.md) |
| High | 07, 08b | [07](study-guides/07-window-functions-part-2.md), [08b](study-guides/08b-changing-data-part-2.md) |
| Useful | 01, 02, 08a | [01](study-guides/01-what-is-a-database.md), [02](study-guides/02-sql-basics.md), [08a](study-guides/08a-changing-data-part-1.md) |

What to over-prepare: CTEs against nested subqueries for readability (05), the `ROW_NUMBER()` top-one-per-group pattern and its tie problem (06), and writing a metric definition down before the SQL so two dashboards can't disagree (09). Analytics engineering is largely the job of making definitions consistent, and `09` is the preview.

### Data Engineer

Interviews go deepest on window frames, safe changes to data, and schema design: the parts of SQL that touch pipeline correctness and production risk directly.

| Priority | Notebooks | Guides |
| --- | --- | --- |
| Highest | 06, 07, 08a, 08b | [06](study-guides/06-window-functions-part-1.md), [07](study-guides/07-window-functions-part-2.md), [08a](study-guides/08a-changing-data-part-1.md), [08b](study-guides/08b-changing-data-part-2.md) |
| High | 03, 04, 05 | [03](study-guides/03-aggregation.md), [04](study-guides/04-joins.md), [05](study-guides/05-subqueries-to-ctes.md) |
| Useful | 01, 02, 09, Appendix A | [01](study-guides/01-what-is-a-database.md), [02](study-guides/02-sql-basics.md), [09](study-guides/09-thinking-in-metrics.md), [A](study-guides/appendix-a-sql-server-reference.md) |

What to over-prepare: the `LAST_VALUE()` frame trap and running totals over tied values (07), "what do you check before an `UPDATE` or `DELETE` in production?" (08a), adding a `NOT NULL` column or a constraint to a table that already has rows (08b), and recursive CTEs for hierarchies (05).

## Interview format cheat sheet

- **Technical screen** (live, 30 to 45 minutes, in a shared editor): expect fluency with `02` to `06`, explained out loud as you type. Speed and correctness both count, but a narrated answer with a small slip usually beats a silent correct one, because the interviewer is scoring how you think.
- **Take-home** (hours to a few days): expect a messier dataset and an open-ended question. This is where readable CTEs (05), join-grain awareness (04), written metric definitions (09), and safe-change habits (08a) get judged, not only the final number.
- **Whiteboard or no editor** (rarer, still common for senior roles): expect window functions (06, 07) and schema design (08b) described in plain language before any syntax, like what a frame is or why a foreign key exists.
- **Case interview** ("how would you measure X?"): expect `09`'s questions before any SQL: what one row is, what's measured, who counts, over what period, and how ties are handled.

## Building a portfolio project from this material

Passing an interview and having something to point to in one are different things. The [capstone](<capstone-online-store-analysis.ipynb>) is a worked example of the second; to build your own:

- **Chain the notebooks into one analysis.** Pick a real question against AdventureWorks (top customers by lifetime value, which territories grew fastest, which products are bought together) and answer it with the sequence the capstone follows: a written definition (09), checks on the data (02, 03), joins to assemble it (04), CTEs to name each step (05), window functions to rank or trend it (06, 07), and an aggregated summary (03), ending in a short write-up with its caveats.
- **Write down why, not just what.** Note in comments why each step uses a `LEFT JOIN` rather than an `INNER JOIN`, or a `ROWS` frame rather than the default. Being able to defend a choice is what a review conversation is built to surface.
- **Show the safe-change habit.** Pair each `UPDATE` or `DELETE` with the `SELECT` you ran first, and run it inside a transaction. It's a small thing that signals real production experience.
- **Say the interview answers out loud.** Every question in `study-guides/` is answerable in 30 to 90 seconds, spoken, which is the format a technical screen takes.

## After this repo

The [Course Overview](<00-course-overview.ipynb>) and the [reading version of this curriculum](https://aaboutdata.substack.com/p/start-here-from-beginner-to-job-ready) cover where the roadmap goes next. This repo covers standard SQL on SQLite and SQL Server; it doesn't go into query performance tuning, execution plans, indexing strategy, or engine-specific extensions like JSON functions, PL/pgSQL, or T-SQL stored procedures, which senior data engineering interviews sometimes probe. Treat those as the next layer once you can explain the fundamentals here without hesitating.
