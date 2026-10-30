# Study Guide 02: SQL Basics (SELECT, WHERE, ORDER BY)

Companion to [`02-sql-basics.ipynb`](<../02-sql-basics.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Analyst, Analytics Engineer, Data Engineer | Technical screen (live coding), take-home |

## Concept recap

`SELECT` chooses columns, `WHERE` chooses rows, and `ORDER BY` sorts what's left. The database runs them in a different order from the one you write them in: `FROM`, then `WHERE`, then `SELECT`, then `ORDER BY`. That's why `ORDER BY` can use a column alias and standard SQL's `WHERE` can't (SQLite allows it; SQL Server and PostgreSQL don't).

`WHERE` keeps a row only when its condition is **true**. A comparison with `NULL` is neither true nor false but **unknown**, so a row with a missing value drops out of `total > 100` and out of `total <= 100`. In the notebook, those two filters return three orders each from a table of seven, and David's order 5 is in neither. Missing values are found with `IS NULL`, never `= NULL`, which silently returns no rows.

`AND` binds more tightly than `OR`, so `A OR B AND C` means `A OR (B AND C)`. Parentheses, or `IN` for a list of values, say what you meant. Without `ORDER BY`, row order is undefined, and engines disagree about where `NULL`s sort: SQLite and SQL Server put them first in ascending order, PostgreSQL last.

## Key syntax cheat sheet

```sql
-- Columns, rows, and order
SELECT
    order_id,
    customer_name,
    total
FROM lesson_orders
WHERE status = 'completed'
  AND total > 100
ORDER BY
    total DESC;

-- Finding missing values
SELECT
    order_id
FROM lesson_orders
WHERE total IS NULL;

-- A list of values, with no AND/OR precedence to get wrong
SELECT
    order_id
FROM lesson_orders
WHERE customer_name IN ('Maria', 'Amina')
  AND total > 100;

-- Checking the actual values before filtering on text
SELECT DISTINCT status
FROM lesson_orders;
```

On SQL Server, `SELECT TOP 5 ...` takes the first rows, where SQLite writes `LIMIT 5` at the end.

## Gotchas and common mistakes

- Writing `= NULL` or `<> NULL`. Both return nothing, without an error.
- Assuming a filter and its opposite cover every row. They miss every row where the column is `NULL`; on AdventureWorks, `SalesPersonID = 279` and `SalesPersonID <> 279` together miss 27,659 of 31,465 orders.
- Mixing `AND` and `OR` without parentheses.
- Typing a text value from memory. `'Completed'` doesn't match `'completed'` in SQLite, but it does in a case-insensitive SQL Server database, so the same query can behave differently on two engines.
- Relying on row order without `ORDER BY`.

## Interview questions and model answers

**Q1 (live coding): "Return completed orders over $100, largest first."**
Model answer:
```sql
SELECT
    order_id,
    customer_name,
    total
FROM lesson_orders
WHERE status = 'completed'
  AND total > 100
ORDER BY
    total DESC;
```
"I'd also mention that any completed order with a missing total won't appear, since `total > 100` is unknown for it, and ask whether the business wants those flagged."

**Q2: "Why does `WHERE column = NULL` return nothing?"**
Model answer: "Because `NULL` means unknown, and comparing anything to unknown gives unknown, not true. `WHERE` only keeps rows where the condition is true. The right test is `IS NULL`, which always returns true or false."

**Q3: "Can you use a column alias in a WHERE clause?"**
Model answer: "Not in standard SQL. `WHERE` is evaluated before `SELECT`, so the alias doesn't exist yet. `ORDER BY` runs after `SELECT`, so it can use the alias. SQLite happens to accept an alias in `WHERE`, but SQL Server and PostgreSQL reject it, so I repeat the expression in `WHERE` to keep the query portable."

**Q4: "What does this return: `WHERE name = 'Maria' OR name = 'Amina' AND total > 100`?"**
Model answer: "Every Maria order, plus Amina's orders over 100, because `AND` binds first. If the intent was Maria's or Amina's orders over 100, it needs parentheses around the `OR`, or `name IN ('Maria', 'Amina') AND total > 100`."

**Q5: "How would you find the rows a filter left out?"**
Model answer: "Count the filter, count its opposite, and compare with the total. If they don't add up, the gap is usually `NULL`s, which I'd confirm with `IS NULL`."

## Extra practice

- On AdventureWorks, `Production.Product` has 504 products. Count the black ones, the ones that aren't black, and the ones with no color, and confirm the three counts add up to 504 (the notebook's stretch exercise).
- Rewrite an `IN` list as `OR` conditions and back again, adding the parentheses each time, until the equivalence feels automatic.
- Write a query that sorts completed orders by total, smallest first, with missing totals at the end, once with `NULLS LAST` in SQLite and once with a `CASE` expression for SQL Server.
