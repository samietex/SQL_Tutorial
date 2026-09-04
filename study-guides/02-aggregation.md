# Study Guide 02 — Aggregation (GROUP BY, HAVING, COUNT/SUM/AVG)

Companion to [`02 - Aggregation (GROUP BY, HAVING, COUNT-SUM-AVG).ipynb`](<../02 - Aggregation (GROUP BY, HAVING, COUNT-SUM-AVG).ipynb>).

| Tracks | Interview format |
|---|---|
| Data Analyst · Analytics Engineer · Data Engineer | Technical screen (live coding), take-home |

## Concept recap

`GROUP BY` collapses every row sharing a value in some column into a single summary row. `COUNT(*)` counts rows per group, `SUM()` totals a numeric column per group, `AVG()` averages it. `HAVING` filters those summary rows the way `WHERE` filters individual rows, the difference is *when* each one runs: `WHERE` runs before grouping, on raw rows; `HAVING` runs after grouping, on the aggregated result. That's why `WHERE SUM(TotalDue) > 50000` fails, there's no `SUM(TotalDue)` value to filter on yet at the point `WHERE` executes, only `HAVING` runs late enough to see it.

## Key syntax cheat sheet

```sql
SELECT
    CustomerID,
    SUM(TotalDue) AS "Total Spent",
    AVG(TotalDue) AS "Average Order Value",
    COUNT(*) AS "Number of Orders"
FROM Sales.SalesOrderHeader
GROUP BY CustomerID
HAVING SUM(TotalDue) > 50000
ORDER BY "Total Spent" DESC;
```

Order that actually runs: `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY`.

## Gotchas & common mistakes

- Writing `WHERE SUM(TotalDue) > 50000` instead of `HAVING`, this is the single most common `GROUP BY` mistake and a near-guaranteed interview question.
- Selecting a non-aggregated column that isn't in the `GROUP BY` list. SQL Server (like most engines outside older MySQL defaults) errors on this, because it's genuinely ambiguous which row's value to show.
- Forgetting that `HAVING` can filter on *any* aggregate, not just the one used to build the summary, `HAVING COUNT(*) > 5` is just as valid as `HAVING SUM(...) > 50000`.

## Interview questions & model answers

**Q1: "What's the difference between `WHERE` and `HAVING`, and why do both exist?"**
Model answer: "`WHERE` filters individual rows before grouping happens. `HAVING` filters the grouped/aggregated rows after `GROUP BY` runs. You need `HAVING` specifically because an aggregate like `SUM(TotalDue)` doesn't exist as a value until the rows are already grouped, `WHERE` runs too early to see it."

**Q2 (live coding): "Find every customer whose total spend across all orders exceeds $50,000."**
Model answer:
```sql
SELECT CustomerID, SUM(TotalDue) AS "Total Spent"
FROM Sales.SalesOrderHeader
GROUP BY CustomerID
HAVING SUM(TotalDue) > 50000
ORDER BY "Total Spent" DESC;
```

**Q3: "Can you filter on `COUNT(*)` in the same query where you're also computing a `SUM`?"**
Model answer: "Yes, `HAVING` isn't tied to one aggregate. `HAVING COUNT(*) > 10 AND SUM(TotalDue) > 50000` filters on both at once, since both are computed at the same point in execution, after grouping, before the final `SELECT`."

**Q4: "Why does SQL Server error if I `SELECT` a column that's not in my `GROUP BY` and isn't wrapped in an aggregate?"**
Model answer: "Because it's ambiguous. Once rows are collapsed into one row per group, there's no single correct value left for a column that varies within the group, SQL Server refuses to guess, rather than silently picking an arbitrary row's value like some engines will under looser settings."

## Extra practice

- Extend the notebook's query to also return `COUNT(*)`, then add a second `HAVING` condition requiring more than 3 orders *and* over $50,000 spent.
- Find the customers in the *bottom* 10 by total spend instead of a fixed threshold, think about what changes: `ORDER BY ... ASC` plus a row-limiting clause, not `HAVING`.
