# Study Guide 06: Window Functions, Part 1

Companion to [`06-window-functions-part-1.ipynb`](<../06-window-functions-part-1.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Analytics Engineer, Data Engineer, Data Analyst | Technical screen (live coding), take-home |

## Concept recap

A **window function** calculates across a set of related rows and attaches the result to every row, instead of collapsing them the way `GROUP BY` does: five orders in, five rows out, each with its customer's total. `OVER (...)` defines the window: `PARTITION BY` decides which rows belong together, and `ORDER BY` decides their sequence.

The three families: **ranking** (`ROW_NUMBER()`, and `RANK()` from `09`), **offset** (`LAG()` and `LEAD()`, which pull a value from the previous or next row), and **aggregate** (`SUM()` or `AVG()` with `OVER`).

Window functions are calculated after `WHERE`, so they can only appear in the `SELECT` list and `ORDER BY`. To filter on one, compute it in an inner query and filter in the outer one. `WHERE` also decides which rows the window can see, so filtering before a `LAG()` can make the first remaining row's previous value `NULL`.

## Key syntax cheat sheet

```sql
-- Group total on every row
SELECT
    order_id,
    customer_id,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id) AS customer_total
FROM orders;

-- Top one per group: rank inside, filter outside
SELECT
    customer_id,
    order_id,
    amount
FROM (
    SELECT
        customer_id,
        order_id,
        amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY amount DESC
        ) AS rn
    FROM orders
) AS ranked
WHERE rn = 1;

-- Change from the previous row
SELECT
    customer_id,
    order_id,
    amount - LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_id) AS change_from_prev
FROM orders;
```

## Gotchas and common mistakes

- Forgetting `PARTITION BY`, so `LAG()` reads across customers: Bola's first order shows Ada's last amount as "previous". No error, plausible result.
- Filtering on a window alias in the same query's `WHERE`, which errors in SQLite and SQL Server alike.
- Treating the `NULL` from `LAG()` on a partition's first row as 0. Arithmetic with it gives `NULL`; decide explicitly with `COALESCE` or `LAG(amount, 1, 0)`, which mean different things.
- Ranking with `ROW_NUMBER()` when two rows can tie on the `ORDER BY`. Add a tie-breaker, or use `RANK()`.
- Dividing by a windowed sum without `100.0` or `1.0`, which truncates every share to 0 on integer columns.

## Interview questions and model answers

**Q1: "What's the difference between GROUP BY and a window function?"**
Model answer: "`GROUP BY` collapses each group to one row. A window function computes over the group but keeps every row and attaches the result, so I can show each order next to its customer's total, or its share of it."

**Q2 (very common): "Return each customer's largest order."**
Model answer: the ranked derived table above. "`ROW_NUMBER()` partitioned by customer and ordered by amount descending numbers each customer's orders, and the outer query keeps `rn = 1`. If two orders can tie and both should appear, I'd use `RANK()` instead, and if only one should, I'd add a tie-breaker to the `ORDER BY`."

**Q3: "Why can't you put ROW_NUMBER() in a WHERE clause?"**
Model answer: "Window functions are calculated after `WHERE` has chosen the rows, so the value doesn't exist when `WHERE` runs. I compute it in a CTE or derived table and filter one level up."

**Q4: "Calculate month-over-month change in sales."**
Model answer: "Aggregate sales by month in a CTE, then `sales - LAG(sales) OVER (ORDER BY month)`. No `PARTITION BY`, because the months form one sequence. If I only want to show one year, I compute `LAG` over all months first and filter afterwards, or the first month of the year loses its previous month."

## Extra practice

- Show each order's percentage of its customer's total, and check Bola's two orders add to 100.
- On AdventureWorks, return each salesperson's single largest order (17 rows), and explain where the `WHERE SalesPersonID IS NOT NULL` must go and why.
- Recreate the missing-`PARTITION BY` mistake on purpose, then explain the wrong value in Bola's first row out loud.
