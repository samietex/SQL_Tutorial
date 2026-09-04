# Study Guide 03 — JOINs (INNER vs LEFT)

Companion to [`03 - JOINs (INNER vs LEFT).ipynb`](<../03 - JOINs (INNER vs LEFT).ipynb>).

| Tracks | Interview format |
|---|---|
| Data Analyst · Analytics Engineer · Data Engineer | Technical screen (live coding), take-home |

## Concept recap

`INNER JOIN` returns a row only when both sides match, non-matching rows on either side vanish silently. `LEFT JOIN` keeps every row from the left table regardless of a match, filling unmatched right-side columns with `NULL`. `LEFT JOIN ... WHERE right.key IS NULL` is the standard "find things with no match" pattern, an anti-join.

The higher-stakes idea: joining changes your row **grain**. `Sales.Customer` is one row per customer; join it to `Sales.SalesOrderHeader` and the result is one row per *order*, a customer with five orders now appears five times. `COUNT(*)` after that join counts orders, not customers, a mismatch that quietly inflates reports if you don't re-`GROUP BY` back to the grain you actually want.

## Key syntax cheat sheet

```sql
-- INNER JOIN: only matching rows on both sides
SELECT c.CustomerID, s.SalesOrderID
FROM Sales.Customer c
INNER JOIN Sales.SalesOrderHeader s ON c.CustomerID = s.CustomerID;

-- LEFT JOIN + IS NULL: the anti-join pattern, "customers with no orders"
SELECT c.CustomerID
FROM Sales.Customer c
LEFT JOIN Sales.SalesOrderHeader s ON c.CustomerID = s.CustomerID
WHERE s.SalesOrderID IS NULL;

-- Re-establishing per-customer grain after a join
SELECT c.CustomerID, COUNT(s.SalesOrderID) AS "Order Count"
FROM Sales.Customer c
INNER JOIN Sales.SalesOrderHeader s ON c.CustomerID = s.CustomerID
GROUP BY c.CustomerID;
```

## Gotchas & common mistakes

- Running `COUNT(*)` right after a one-to-many join and reporting it as a count of the "one" side, it's actually counting the "many" side.
- Using `WHERE s.CustomerID IS NULL` (a column pulled from the *left* table's join key when both sides happen to share a name) instead of a column that's genuinely only populated by the right table, checking the wrong column can silently return zero rows even when unmatched rows exist.
- Reaching for `INNER JOIN` by habit when the question actually wants "all of X, whether or not Y exists", that's a `LEFT JOIN` question, not an `INNER JOIN` question.

## Interview questions & model answers

**Q1 (live coding, extremely common): "Write a query to find every customer who has never placed an order."**
Model answer:
```sql
SELECT c.CustomerID, c.AccountNumber
FROM Sales.Customer c
LEFT JOIN Sales.SalesOrderHeader s ON c.CustomerID = s.CustomerID
WHERE s.SalesOrderID IS NULL;
```
"`LEFT JOIN` keeps every customer, even ones with no matching order, and fills the order columns with `NULL` when there's no match. Filtering `WHERE s.SalesOrderID IS NULL` keeps only the customers where that never happened, an anti-join."

**Q2: "My revenue total doubled after I joined the orders table to the line items table. What happened?"**
Model answer: "The join changed my row grain. An orders table is one row per order; a line items table is one row per line item, several per order. Joining them multiplies each order row by however many line items it has, so summing a per-order total after that join double- (or N-times-) counts it. The fix is to either aggregate the line items down to one row per order *before* joining, or sum the right column at the right grain after."

**Q3: "When would you use `INNER JOIN` instead of `LEFT JOIN`?"**
Model answer: "When I specifically want to exclude rows with no match, when 'no order' isn't a case I want to see at all, just customers who've actually ordered something. `LEFT JOIN` is for when the unmatched case itself is part of the answer, like finding customers with zero orders."

## Extra practice

- Take the notebook's grain example and run `SELECT COUNT(*)` both before and after the `GROUP BY` is added back, confirm out loud why the two numbers differ and which one actually answers "how many customers have orders."
- Write the anti-join pattern from memory against a different pair of tables (for example, employees with no assigned department, if such a relationship exists in your schema) without looking at the example first.
