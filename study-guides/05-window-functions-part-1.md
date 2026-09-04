# Study Guide 05 — Window Functions, Part 1

Companion to [`05 - Window Functions, Part 1.ipynb`](<../05 - Window Functions, Part 1.ipynb>).

| Tracks | Interview format |
|---|---|
| Data Engineer · Analytics Engineer (heavy) · Data Analyst | Technical screen, whiteboard |

## Concept recap

`GROUP BY` collapses rows into one summary row per group, you lose the detail rows. A window function (`... OVER (PARTITION BY ... ORDER BY ...)`) computes something across a group of rows *without* collapsing them, every original row stays, with the aggregate sitting alongside it as a new column.

`ROW_NUMBER()` assigns a sequential number within each `PARTITION BY` group, the standard tool for "keep only the most recent row per group" (filter to `"Order Rank" = 1`). `LAG()`/`LEAD()` look at a neighboring row, previous or next, within the same partition, without a self-join. `SUM() OVER (PARTITION BY ... ORDER BY ...)` with no explicit frame produces a running total, because the default frame is "everything from the start of the partition up to the current row" (the frame clause itself is `06`'s subject).

Window functions run after `WHERE`/`GROUP BY` but before `ORDER BY` in SQL Server's actual execution order, so a window function's alias can't be referenced in that same query's `WHERE` clause, wrap it in a CTE first and filter in the outer query.

## Key syntax cheat sheet

```sql
-- Most recent row per group ("greatest-n-per-group")
WITH numbered_orders AS (
    SELECT CustomerID, SalesOrderID, OrderDate,
           ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderDate DESC) AS "Order Rank"
    FROM Sales.SalesOrderHeader
)
SELECT CustomerID, SalesOrderID, OrderDate FROM numbered_orders WHERE "Order Rank" = 1;

-- Compare to the previous row
SELECT CustomerID, OrderDate, TotalDue,
       LAG(TotalDue) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS "Previous Order Total"
FROM Sales.SalesOrderHeader;

-- Running total
SELECT CustomerID, OrderDate, TotalDue,
       SUM(TotalDue) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS "Running Total"
FROM Sales.SalesOrderHeader;
```

## Gotchas & common mistakes

- Reaching for `GROUP BY` when the actual goal is "rank/compare rows but keep every row", that's a window function, `GROUP BY` throws the detail away.
- Forgetting `PARTITION BY` and getting one ranking across the *entire* table instead of one ranking per group, `PARTITION BY` is what makes it reset per customer (or whatever the grouping is) rather than run globally.
- Trying to filter directly on a window function's result in the same query's `WHERE` clause, it isn't visible there yet at that point in execution; wrap it in a CTE.
- Expecting `LAG()` to return `0` instead of `NULL` for the first row in a partition, there is no previous row, so `NULL` is correct, not a bug.

## Interview questions & model answers

**Q1 (one of the most common SQL interview questions at any level): "How would you get only the most recent order per customer?"**
Model answer:
```sql
WITH numbered AS (
    SELECT CustomerID, SalesOrderID, OrderDate,
           ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderDate DESC) AS rn
    FROM Sales.SalesOrderHeader
)
SELECT CustomerID, SalesOrderID, OrderDate FROM numbered WHERE rn = 1;
```
"`ROW_NUMBER()` restarts at 1 for every new `CustomerID` because of the `PARTITION BY`, and `ORDER BY OrderDate DESC` puts the newest order first within each customer, so `rn = 1` is always their latest order. This is the general 'greatest-n-per-group' pattern, it works the same way for 'top 3 per category' by changing the filter to `rn <= 3`."

**Q2: "What's the actual difference between `GROUP BY` and a window function?"**
Model answer: "`GROUP BY` reduces N rows to one row per group, you lose row-level detail. A window function computes the same kind of aggregate but keeps every row, the aggregate just becomes an extra column alongside the original data. I use `GROUP BY` when I only need the summary; I use a window function when I need the summary *and* the detail together, like showing a running total next to each individual transaction."

**Q3: "How would you compute a running total per customer in SQL?"**
Model answer: `SUM(TotalDue) OVER (PARTITION BY CustomerID ORDER BY OrderDate)`, "no explicit frame needed here, the default frame for an ordered window is 'start of partition through the current row', which is exactly the definition of a running total."

**Q4: "Why would `WHERE row_num = 1` fail if `row_num` is a `ROW_NUMBER()` alias defined in the same `SELECT`?"**
Model answer: "Execution order, window functions run after `WHERE` but before `ORDER BY`. At the point `WHERE` executes, that alias doesn't exist yet. The fix is to compute it in a CTE or subquery, then filter in the outer query where it's already resolved."

## Extra practice

- Modify the `LAG()` example to also include `LEAD()`, comparing each order to both its previous *and* next order in the same query.
- Change the "most recent order per customer" pattern to "3 most recent orders per customer" and explain out loud exactly what changes in the `WHERE` clause.
