# Study Guide 01 — SQL Basics (SELECT, WHERE, ORDER BY)

Companion to [`01 - SQL Basics (SELECT, WHERE, ORDER BY).ipynb`](<../01 - SQL Basics (SELECT, WHERE, ORDER BY).ipynb>).

| Tracks | Interview format |
|---|---|
| Data Analyst · Analytics Engineer · Data Engineer | Technical screen (live coding) |

## Concept recap

`SELECT` picks columns, `WHERE` filters rows, `ORDER BY` sorts the result. Column aliases (`AS "Department"`) make output readable. `IN (...)` replaces a chain of `OR` conditions for matching against a list of values. `COUNT(DISTINCT column)` counts unique values rather than every row.

The one idea worth over-learning here: SQL Server doesn't run a query in the order you *write* it. `FROM` and `WHERE` run first, `SELECT` picks columns next, and `ORDER BY` runs last. That's why a column alias created in `SELECT` isn't visible to `WHERE`, at the point `WHERE` runs, that alias doesn't exist yet.

## Key syntax cheat sheet

```sql
SELECT col1, col2 AS "Readable Name"
FROM Schema.Table
WHERE col3 = 'value'          -- or: col3 IN ('a', 'b', 'c')
ORDER BY col1 ASC;             -- ASC is the default, DESC reverses it

SELECT COUNT(DISTINCT col) AS "Distinct Count"
FROM Schema.Table;
```

## Gotchas & common mistakes

- Trying to filter or sort on a `SELECT`-defined alias inside the same query's `WHERE` clause, it silently fails or errors because `WHERE` runs before `SELECT` in logical execution order, not textual order.
- Chaining `OR col = 'a' OR col = 'b' OR col = 'c'` when `IN ('a', 'b', 'c')` says the same thing more clearly, this is a small thing interviewers notice in a live-coding screen.
- Forgetting `DISTINCT` when a question asks for unique values and getting a row count instead of a distinct-value count.

## Interview questions & model answers

**Q1: "Why can't I reference a column alias I just created in `SELECT` inside the `WHERE` clause of that same query?"**
Model answer: "Because of SQL's logical order of execution, `FROM` and `WHERE` run before `SELECT` does. By the time `WHERE` is evaluated, the alias from `SELECT` doesn't exist yet. If I need to filter on a computed value, I either repeat the expression in `WHERE`, or wrap the query in a CTE and filter in the outer query, where the alias does exist."

**Q2: "Write a query to find every distinct job title in an employee table, and how many there are."**
Model answer, live-coded:
```sql
SELECT DISTINCT JobTitle FROM HumanResources.Employee;

SELECT COUNT(DISTINCT JobTitle) AS "Distinct Job Titles"
FROM HumanResources.Employee;
```
"The first gives me the list, the second gives me the count, `COUNT(DISTINCT ...)` doesn't double-count repeated titles."

**Q3: "What's the practical difference between `WHERE col IN ('a','b','c')` and three `OR` conditions?"**
Model answer: "Functionally identical, same result, same execution plan in virtually every engine. `IN` is just more readable once you're past two or three values, and it's less error-prone to maintain, adding a fourth value is one more item in a list instead of one more `OR col = ...` clause to copy-paste correctly."

## Extra practice

- Against `Sales.Customer`, write a query that returns every customer in a specific `TerritoryID`, sorted by `AccountNumber`. Then try to sort by a column alias you invent in the same `SELECT`, and explain out loud why it errors.
- Rewrite the `HumanResources.Employee` `JobTitle IN (...)` query from the notebook as three `OR` conditions, then back again, until the equivalence feels automatic.
