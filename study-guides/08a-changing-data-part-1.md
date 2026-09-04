# Study Guide 08a — Changing Data, Part 1 (INSERT, UPDATE, DELETE)

Companion to [`08a - Changing Data, Part 1 - INSERT, UPDATE, DELETE.ipynb`](<../08a - Changing Data, Part 1 - INSERT, UPDATE, DELETE.ipynb>).

| Tracks | Interview format |
|---|---|
| Data Engineer (heavy) · Analytics Engineer · Data Analyst | Technical screen, take-home |

## Concept recap

`INSERT INTO table VALUES (...)` adds rows. `UPDATE table SET col = value WHERE condition` modifies existing rows matching the condition. `DELETE FROM table WHERE condition` removes matching rows. All three are Data Manipulation Language (DML), changing data, not structure, that's `08b`'s territory.

Every `UPDATE` and `DELETE` example in the notebook filters on a specific `WHERE Book_ID = 100`, that's not incidental. `USE database_name` works the same way in SQL Server and MySQL to switch the active database, PostgreSQL has no `USE` statement at all, you connect to a specific database directly instead.

## Key syntax cheat sheet

```sql
INSERT INTO Books
VALUES (100, 'Song of Ice and Fire', 'George RR Martins', 5000, 10, 'Fiction');

UPDATE Books
SET Genre = 'Non-Fiction'
WHERE Book_ID = 100;

DELETE FROM Books
WHERE Book_ID = 100;
```

## Gotchas & common mistakes

- **Running `UPDATE` or `DELETE` without a `WHERE` clause.** Without it, both statements apply to *every row in the table*, not just the one you meant. This is one of the most common, and most costly, real-world SQL mistakes, and interviewers ask about it directly because it separates people who've internalized the danger from people who haven't.
- Assuming `DELETE` and `TRUNCATE` are interchangeable. They're related but not the same tool, `DELETE` is row-by-row DML and can be filtered with `WHERE` and rolled back inside a transaction; `TRUNCATE` is a DDL-adjacent operation that removes all rows at once and behaves differently around logging, triggers, and identity columns depending on the engine, worth reading up on before you need it.
- Forgetting that `USE` isn't portable, code that switches databases with `USE` won't run unchanged against PostgreSQL.

## Interview questions & model answers

**Q1 (a genuinely common safety-culture question): "What's the first thing you check before running an `UPDATE` or `DELETE` in production?"**
Model answer: "That there's a `WHERE` clause, and that I've run the equivalent `SELECT` with the same `WHERE` clause first to see exactly which rows it would touch, before I let the `UPDATE`/`DELETE` run. An `UPDATE`/`DELETE` with no `WHERE`, or a `WHERE` that's broader than intended, applies to every matching row in the table, and that's the kind of mistake that's expensive to walk back."

**Q2: "Write an `UPDATE` statement that changes a book's genre, and explain what happens if you drop the `WHERE` clause."**
Model answer:
```sql
UPDATE Books SET Genre = 'Non-Fiction' WHERE Book_ID = 100;
```
"Without `WHERE Book_ID = 100`, this sets *every* row's `Genre` to `'Non-Fiction'`, not just book 100's. The `WHERE` clause is what scopes the change to the specific row I mean."

**Q3: "Is `USE database_name` something you can rely on across database engines?"**
Model answer: "No, it works in SQL Server and MySQL, but PostgreSQL doesn't have a `USE` statement, you connect to a specific database directly at connection time instead of switching mid-session. It's a small but real portability gap worth knowing before assuming a script will run unchanged on a different engine."

## Extra practice

- Write the `INSERT`/`UPDATE`/`DELETE` sequence for the Employees table exercise in the notebook, then deliberately remove the `WHERE` clause from the `UPDATE` and predict, before running it, exactly how many rows would be affected.
- Look up how `DELETE FROM table WHERE ...` differs from `TRUNCATE TABLE table` on transaction logging and identity/auto-increment columns, this is a common follow-up question once `DELETE` comes up.
