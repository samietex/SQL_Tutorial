# Study Guide 05: Subqueries to CTEs

Companion to [`05-subqueries-to-ctes.ipynb`](<../05-subqueries-to-ctes.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Analytics Engineer, Data Engineer, Data Analyst | Take-home (with a review conversation), technical screen |

## Concept recap

A **subquery** is a query inside another. A **scalar subquery** returns one value and can stand anywhere a value goes; a **derived table** is a subquery in `FROM`, given an alias; a **correlated subquery** refers to the outer row and is evaluated once per row; and a **CTE** is a named subquery defined with `WITH` before the main query.

CTEs don't compute anything a subquery can't. What they add is a name: a step defined once and referenced as often as needed, read top to bottom. In the notebook, the nested version of the credit-limit report writes the per-customer total twice; the CTE version writes it once.

The dangerous mistake is an uncorrelated subquery that should have been correlated. `WHERE total_spent > (SELECT credit_limit / 2.0 FROM customers)` returns four rows; SQLite silently uses the first and compares everyone to Ada's half-limit, while SQL Server refuses with "Subquery returned more than 1 value". A **recursive CTE** refers to itself and walks hierarchies of unknown depth.

## Key syntax cheat sheet

```sql
-- Stacked CTEs: one name per step
WITH customer_totals AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COALESCE(SUM(o.amount), 0) AS total_spent
    FROM customers AS c
    LEFT JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY
        c.customer_id,
        c.customer_name
),
ordering_customers AS (
    SELECT
        customer_id,
        total_spent
    FROM customer_totals
    WHERE total_spent > 0
)
SELECT
    customer_name,
    total_spent,
    total_spent > (SELECT AVG(total_spent) FROM ordering_customers) AS above_average
FROM customer_totals;

-- Correlated subquery: evaluated per outer row
SELECT
    e.employee_name,
    (
        SELECT COUNT(*)
        FROM employees AS r
        WHERE r.manager_id = e.employee_id
    ) AS direct_reports
FROM employees AS e;

-- Recursive CTE (write RECURSIVE for SQLite, PostgreSQL, MySQL; omit it on SQL Server)
WITH RECURSIVE org_tree AS (
    SELECT
        employee_id,
        employee_name,
        1 AS depth
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT
        e.employee_id,
        e.employee_name,
        ot.depth + 1
    FROM employees AS e
    INNER JOIN org_tree AS ot
        ON e.manager_id = ot.employee_id
)
SELECT
    employee_name,
    depth
FROM org_tree;
```

## Gotchas and common mistakes

- A scalar subquery that can return more than one row.
- Forgetting to correlate a subquery that should depend on the outer row.
- A second `WITH` keyword instead of a comma between CTEs.
- A derived table without an alias, which SQLite allows and SQL Server rejects.
- `NOT IN` against a subquery that can return `NULL`, which returns no rows; `NOT EXISTS` doesn't have that problem.
- Assuming a CTE runs once. Engines may inline it at each reference; SQLite 3.35.0 and later accept `AS MATERIALIZED` to force one behavior, and SQL Server doesn't support the keyword.

## Interview questions and model answers

**Q1: "What's the difference between a subquery and a CTE?"**
Model answer: "A CTE is a named subquery declared up front with `WITH`. It can be referenced several times and stacked into steps that read top to bottom, which makes long queries much easier to review. It doesn't add new capability, apart from recursion, and some engines inline it, so it isn't automatically faster."

**Q2: "What's a correlated subquery?"**
Model answer: "One that refers to a column from the outer query, so it's evaluated for each outer row. `NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)` is the classic example."

**Q3: "This query runs but the results look wrong. Why?"** (an uncorrelated scalar subquery returning several rows)
Model answer: "The subquery returns more than one row, and SQLite uses the first one silently, so every row is compared to the same arbitrary value. SQL Server would raise an error. The fix is to correlate it to the outer row, or to aggregate it to a single value if one value is really meant."

**Q4: "How would you walk an org chart of unknown depth?"**
Model answer: "A recursive CTE: an anchor query for the top of the tree, `UNION ALL` a query that joins the table to the CTE's previous rows, repeating until nothing new matches. I'd carry a depth counter and, on real data, guard against cycles."

## Extra practice

- Rewrite the nested two-level version of the credit-limit report as stacked CTEs from memory.
- On AdventureWorks, count the components of product 749 at each level of its bill of materials (14, 50, 21, and 4).
- Find customers with no orders three ways: `LEFT JOIN`, `NOT IN`, and `NOT EXISTS`, and say when `NOT IN` would fail.
