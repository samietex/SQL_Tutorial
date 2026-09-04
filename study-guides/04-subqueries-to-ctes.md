# Study Guide 04 — Subqueries to CTEs

Companion to [`04 - Subqueries to CTEs.ipynb`](<../04 - Subqueries to CTEs.ipynb>).

| Tracks | Interview format |
|---|---|
| Analytics Engineer · Data Engineer (heavy) · Data Analyst | Take-home / code review, technical screen |

## Concept recap

A Common Table Expression (`WITH name AS (...)`) names an intermediate query result so the main query can reference it like a table. Multiple CTEs stack under one `WITH`, separated by commas, each one able to reference the ones defined before it. The output is identical to writing the same logic as nested subqueries, the difference is entirely readability: nested subqueries read inside-out, from the deepest one first; a stack of CTEs reads top to bottom, in the order the logic actually happens.

Two things not to do: you cannot nest a `WITH` inside another CTE's definition, every CTE in a query lives under a single `WITH`, listed in sequence. And a CTE isn't materialized by default, reference the same CTE more than once in a query and SQL Server may recompute it each time. When an expensive intermediate result needs to be reused or indexed, a temp table (`SELECT ... INTO #staging`) is the more predictable tool.

## Key syntax cheat sheet

```sql
WITH high_value_customers AS (
    SELECT CustomerID, SUM(TotalDue) AS "Total Spent"
    FROM Sales.SalesOrderHeader
    GROUP BY CustomerID
    HAVING SUM(TotalDue) > 50000
),
customer_summary AS (
    SELECT c.CustomerID, c.AccountNumber, hvc."Total Spent"
    FROM Sales.Customer c
    INNER JOIN high_value_customers hvc ON c.CustomerID = hvc.CustomerID
)
SELECT * FROM customer_summary ORDER BY "Total Spent" DESC;
```

## Gotchas & common mistakes

- Trying to nest a `WITH` inside another CTE's body, list every CTE under one `WITH`, in order, instead.
- Assuming a CTE is cached/materialized the way a temp table is, referencing it multiple times in one query can mean SQL Server evaluates it multiple times.
- Reaching for a deeply nested subquery in an interview when a CTE would say the same thing far more legibly, readability is part of what's being evaluated in a take-home, not just correctness.

## Interview questions & model answers

**Q1: "What's a CTE, and why prefer one over a nested subquery?"**
Model answer: "A CTE is a named, temporary result set defined with `WITH`, that the rest of the query can reference like a table. It produces the same result and the same execution plan as an equivalent nested subquery, the value is entirely readability and maintainability: a stack of CTEs reads top to bottom in the order the logic runs, where a nested subquery has to be read inside-out."

**Q2: "When would you reach for a temp table instead of a CTE?"**
Model answer: "When I need to reference the same intermediate result multiple times in a query and want it computed once, not re-evaluated per reference, or when I want to index an intermediate result because it's large and expensive to recompute. A CTE is my default for readability; a temp table is what I reach for once re-evaluation or performance becomes an actual, measured problem, not a hypothetical one."

**Q3: "Can a CTE reference itself?"**
Model answer: "Yes, a recursive CTE, useful for hierarchical data like an org chart or a folder tree. I haven't gone deep on the syntax yet, but I understand the base case / recursive case structure conceptually and know where to go deepen that if the role needs it." *(Honest answer if you haven't studied recursive CTEs yet, this notebook explicitly flags them as a deeper topic worth reading up on separately.)*

**Q4 (take-home style): "Refactor this deeply nested subquery into readable CTEs."**
Model approach: name each logical step as its own CTE in the order it needs to happen, verify each CTE's output alone before chaining the next one on top, exactly the way `high_value_customers` is proven out before `customer_summary` joins on top of it.

## Extra practice

- Take the nested-subquery version of the high-value-customers query from the notebook and convert it back into stacked CTEs from memory, then compare against the original.
- Add a third CTE to the stack, on top of `customer_summary`, that ranks those customers by spend (a preview of `05 - Window Functions, Part 1`, `ROW_NUMBER()` over `customer_summary`).
