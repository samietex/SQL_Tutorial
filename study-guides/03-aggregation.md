# Study Guide 03: Aggregation (GROUP BY, HAVING, COUNT, SUM, AVG)

Companion to [`03-aggregation.ipynb`](<../03-aggregation.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Analyst, Analytics Engineer, Data Engineer | Technical screen (live coding), take-home |

## Concept recap

`GROUP BY` buckets rows that share a value and runs each aggregate once per bucket, so the **grain** of the result changes: seven order rows become three customer rows. Every column in the `SELECT` must either be in the `GROUP BY` or inside an aggregate.

The aggregates treat `NULL` differently, and the differences decide answers:

| Expression | What it counts or computes | David's two completed orders (150 and `NULL`) |
| --- | --- | --- |
| `COUNT(*)` | Rows | 2 |
| `COUNT(total)` | Rows where `total` isn't `NULL` | 1 |
| `SUM(total)` | Sum of the non-`NULL` values | 150 |
| `AVG(total)` | Average of the non-`NULL` values | 150, not 75 |

If every value in a group is `NULL`, `SUM` and `AVG` return `NULL`, while `COUNT(column)` returns 0.

`WHERE` filters rows before grouping; `HAVING` filters groups after. A condition that uses an aggregate belongs in `HAVING`, and putting it in `WHERE` is an error.

## Key syntax cheat sheet

```sql
SELECT
    customer_name,
    COUNT(*) AS order_count,
    COUNT(total) AS known_totals,
    SUM(total) AS recorded_spend,
    AVG(total) AS average_known_total
FROM lesson_orders
WHERE status = 'completed'
GROUP BY
    customer_name
HAVING SUM(total) > 200
ORDER BY
    customer_name;

-- A data-quality check: groups with at least one missing value
SELECT
    customer_name
FROM lesson_orders
GROUP BY
    customer_name
HAVING COUNT(*) > COUNT(total);
```

## Gotchas and common mistakes

- Using `COUNT(*)` when the question was about rows with a value, or `COUNT(column)` when it was about all rows.
- Reading an `AVG` without checking how many values it used. `NULL`s are skipped without a word.
- Putting an aggregate in `WHERE`.
- Adding a column to the `SELECT` that isn't grouped or aggregated. SQLite returns a value from an arbitrary row (a "bare column"), older MySQL did the same silently, and SQL Server and PostgreSQL reject it.
- Averaging a whole-number column on SQL Server: `AVG(OrderQty)` returns 2 where the true average is about 2.27. Multiply by `1.0` first.
- Averaging values recorded in different units. AdventureWorks stores some product weights in grams and some in pounds, so one `AVG(Weight)` mixes them.
- Expecting a group to appear when `WHERE` removed all its rows. No rows left means no group, not a zero.

## Interview questions and model answers

**Q1: "What's the difference between WHERE and HAVING?"**
Model answer: "`WHERE` filters individual rows before they're grouped, so it can't use an aggregate. `HAVING` filters the groups after the aggregates are calculated, so it can. If a condition is about a single row, I put it in `WHERE`, which also means fewer rows get grouped."

**Q2: "What's the difference between COUNT(*), COUNT(column), and COUNT(DISTINCT column)?"**
Model answer: "`COUNT(*)` counts rows, `COUNT(column)` counts rows where that column isn't `NULL`, and `COUNT(DISTINCT column)` counts different non-`NULL` values. On AdventureWorks orders they give 31,465, 3,806, and 17 for the salesperson column: orders, orders sold by staff, and salespeople. Three different questions."

**Q3 (live coding): "Which customers have spent more than $200 on completed orders?"**
Model answer:
```sql
SELECT
    customer_name,
    SUM(total) AS recorded_spend
FROM lesson_orders
WHERE status = 'completed'
GROUP BY
    customer_name
HAVING SUM(total) > 200;
```
"Then I'd flag that `SUM` ignores missing totals, so a customer with an unrecorded order might really qualify, and name the column `recorded_spend` so nobody reads it as complete."

**Q4: "Why might AVG give a different answer from SUM divided by COUNT(*)?"**
Model answer: "`AVG` divides by the number of non-`NULL` values, while `COUNT(*)` counts every row, including rows with a `NULL`. For David, `AVG` is 150 and `SUM / COUNT(*)` is 75. Which is right depends on whether a missing value means 'unknown' or 'zero', and that's a business question before it's a SQL one."

## Extra practice

- On AdventureWorks, find the customers who've placed 25 or more orders, most orders first, with a tie-breaker so the order is stable (14 customers).
- Group `Production.Product` by `WeightUnitMeasureCode` and explain, from the result, why a single average weight across all products is meaningless.
- Write a query that lists every customer with the number of cancelled orders, and explain why David is missing and what it would take to show him with 0.
