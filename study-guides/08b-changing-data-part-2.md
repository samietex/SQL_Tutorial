# Study Guide 08b: Changing Data, Part 2 (CREATE TABLE, constraints, ALTER TABLE)

Companion to [`08b-changing-data-part-2.ipynb`](<../08b-changing-data-part-2.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Engineer, Analytics Engineer | Technical screen, whiteboard (schema design), take-home |

## Concept recap

`CREATE TABLE` defines each column as a name, a type, and optional rules, and the database enforces those rules on every write. The constraints you'll use most:

| Constraint | Rule |
| --- | --- |
| `NOT NULL` | The column must have a value |
| `PRIMARY KEY` | Unique and not null; identifies the row |
| `UNIQUE` | No two rows share a value (`NULL`s are treated differently by different engines) |
| `CHECK (condition)` | Rejects rows where the condition is false |
| `DEFAULT value` | Filled in when an `INSERT` leaves the column out |
| `REFERENCES parent (key)` | A foreign key: the value must exist in the parent table |

Engines differ in ways that matter. SQLite enforces foreign keys only after `PRAGMA foreign_keys = ON;`, set per connection and ignored inside an open transaction; SQL Server always enforces them. SQLite stores a value's type per value unless the table is `STRICT`, so it accepts a credit limit of `'Efe'`; SQL Server's columns have fixed types. SQLite and PostgreSQL allow many `NULL`s in a `UNIQUE` column, while SQL Server allows one.

`ALTER TABLE` changes a table that has rows. A new `NOT NULL` column needs a `DEFAULT` for the existing rows. SQLite can add, drop, and rename columns but must rebuild a table to change a type or add a constraint; SQL Server has `ALTER COLUMN` and `ADD CONSTRAINT`, and checks a new constraint against every existing row.

## Key syntax cheat sheet

```sql
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders (order_id),
    amount INTEGER NOT NULL CHECK (amount > 0),
    method TEXT NOT NULL DEFAULT 'card' CHECK (method IN ('card', 'cash', 'transfer')),
    reference TEXT UNIQUE
);

ALTER TABLE customers
ADD COLUMN signup_year INTEGER NOT NULL DEFAULT 2026;

-- SQL Server only
ALTER TABLE customers
ALTER COLUMN credit_limit DECIMAL(10, 2) NOT NULL;

ALTER TABLE customers
ADD CONSTRAINT credit_limit_positive CHECK (credit_limit > 0);
```

## Gotchas and common mistakes

- Declaring a foreign key in SQLite and forgetting the pragma, so it isn't enforced.
- `INSERT INTO t VALUES (...)` without a column list: adding a column later breaks it loudly, and a swapped value order can be accepted quietly.
- Adding a `NOT NULL` column with no `DEFAULT` to a table with rows.
- Assuming `UNIQUE` means "always present"; it needs `NOT NULL` too.
- Adding a constraint that existing rows violate, which SQL Server refuses.
- Never testing a rule. A typo in a `CHECK` can make it accept everything; test each rule with a row that should fail.

## Interview questions and model answers

**Q1: "What's the difference between a primary key and a unique constraint?"**
Model answer: "Both forbid duplicates. A primary key also forbids `NULL`, identifies the row, and there's one per table; a table can have several unique constraints, and depending on the engine they allow one or many `NULL`s."

**Q2: "How would you add a NOT NULL column to a table that already has millions of rows?"**
Model answer: "Give it a `DEFAULT` so the existing rows get a value, or add it as nullable, backfill it in batches, and then add the `NOT NULL` constraint. On a big table I'd check how the engine applies the change, since some rewrite the whole table and lock it, and test on a copy first."

**Q3: "What does a foreign key protect you from?"**
Model answer: "Orphans: child rows pointing at parents that don't exist, either from inserting a bad reference or deleting a parent that still has children. Without one, reports that join to the parent silently drop rows that reports without the join still count."

**Q4: "Why name the columns in an INSERT?"**
Model answer: "So the statement says which value goes where. Without the list, values must fill every column in table order, so adding a column breaks the insert, and swapping two values can put a name in a number column on an engine that doesn't enforce types."

## Extra practice

- Design a `products` table with a required unique name, a positive price, and a stock flag defaulting to 1, then write one failing insert per rule.
- Predict which of four inserts into `payments` succeed, as in the notebook's exercise 2, before running them.
- On AdventureWorks, find which table the most foreign keys point at (`Production.Product`, with 14), and explain what that means for deleting a product.
