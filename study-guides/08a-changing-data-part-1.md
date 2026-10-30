# Study Guide 08a: Changing Data, Part 1 (INSERT, UPDATE, DELETE)

Companion to [`08a-changing-data-part-1.ipynb`](<../08a-changing-data-part-1.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Engineer, Analytics Engineer, Data Analyst | Technical screen, behavioral ("tell me about a time..."), take-home |

## Concept recap

`SELECT` reads and leaves the table alone; `INSERT`, `UPDATE`, and `DELETE` (DML) change rows, report how many they changed, and are permanent once committed. `CREATE TABLE` and `ALTER TABLE` (DDL) change structure, covered in `08b`.

`UPDATE` and `DELETE` without a `WHERE` change every row. A `WHERE` that matches nothing changes zero rows without an error. Each statement sees the table the previous one left behind, so the order of writes matters. A transaction (`BEGIN` in SQLite, `BEGIN TRANSACTION` in SQL Server) holds changes until `COMMIT` or throws them away with `ROLLBACK`, which makes it the safe way to try a change.

Deleting a row that other rows point to leaves **orphans** unless a foreign key forbids it: deleting Chidi leaves order 105 behind, so an `INNER JOIN` report drops 140 of revenue that a plain `SUM` still counts.

## Key syntax cheat sheet

```sql
-- Name the columns
INSERT INTO customers (
    customer_id,
    customer_name,
    credit_limit
)
VALUES (5, 'Efe', 150);

-- Check the WHERE with a SELECT, then update the same rows
SELECT
    customer_id,
    credit_limit
FROM customers
WHERE customer_id = 2;

UPDATE customers
SET credit_limit = credit_limit + 50
WHERE customer_id = 2;

-- Try a risky change safely
BEGIN;
DELETE FROM orders
WHERE amount < 50;
SELECT COUNT(*) FROM orders;
ROLLBACK;

-- Find orphans
SELECT
    o.order_id
FROM orders AS o
LEFT JOIN customers AS c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

Rows changed by the last statement: `SELECT changes();` in SQLite, `SELECT @@ROWCOUNT;` in SQL Server.

## Gotchas and common mistakes

- `UPDATE` or `DELETE` without a `WHERE`.
- Not reading the row count afterwards: zero rows and every row are both silent.
- `WHERE column = NULL` in an update, which changes nothing.
- Assuming an earlier write didn't affect a later one. In the notebook, a 10 percent discount on 2014 orders pushed 293 more orders under $5, so the next `DELETE` removed 530 rows instead of 237.
- Deleting a parent row without checking what points to it.
- Running a large change without a backup or a transaction.

## Interview questions and model answers

**Q1 (very common for DE roles): "What do you do before running an UPDATE or DELETE in production?"**
Model answer: "Run the same `WHERE` as a `SELECT` and check the row count matches what I expect. Make sure there's a backup, or copy the affected rows first. Run the change inside a transaction, check the reported count and a sample of the result, and only then commit. And check what references the rows I'm deleting."

**Q2: "What happens if you leave out the WHERE in an UPDATE?"**
Model answer: "Every row is updated, with no warning, because it's valid SQL. Inside a transaction I could roll it back; after a commit I'd need a backup."

**Q3: "What's a transaction?"**
Model answer: "A group of statements that succeed or fail together. Changes inside it aren't permanent until `COMMIT`, and `ROLLBACK` undoes all of them, which is what makes a multi-step change safe and lets you check a change before keeping it."

**Q4: "What's an orphaned row, and how do you prevent it?"**
Model answer: "A child row whose parent is gone, like an order for a deleted customer. It makes reports disagree depending on whether they join to the parent. A foreign key constraint prevents it by refusing the delete, or by deleting or nulling the children if it's declared with an `ON DELETE` action."

## Extra practice

- Predict the final `orders` table after the notebook's three-statement transaction, then run it, then swap the `UPDATE` and `DELETE` and predict again.
- Write a raise for every customer who's ordered, using a subquery in the `WHERE`, and say why `credit_limit * 1.1` gives untidy numbers.
- On AdventureWorks, copy products with a price into a temporary table and lower prices for products with no color inside a transaction (59 rows), then explain why `WHERE Color = NULL` would change nothing.
