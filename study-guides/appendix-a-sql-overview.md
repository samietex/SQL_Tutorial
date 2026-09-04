# Study Guide — Appendix A: SQL Overview & Getting Started

Companion to [`Appendix A - SQL Overview & Getting Started.ipynb`](<../Appendix A - SQL Overview & Getting Started.ipynb>).

| Tracks | Interview format |
|---|---|
| Data Analyst (entry-level screening) · Analytics Engineer · Data Engineer | Technical screen (definitional / conceptual opener) |

## Concept recap

SQL splits into three sub-languages: **DDL** (Data Definition Language, `CREATE`/`ALTER`/`DROP`, structure), **DML** (Data Manipulation Language, `INSERT`/`UPDATE`/`DELETE`, data), and **DQL** (Data Query Language, `SELECT` and its clauses, reading data back out). SQL is both an ANSI and ISO standard, most engines implement the standard core and layer proprietary extensions on top.

`CREATE` makes new objects, databases, tables, indexes. `CREATE INDEX` in particular speeds up retrieval on a column that's frequently searched or joined on. `ALTER` modifies existing objects, add/remove/modify a column, add a constraint. `DROP` permanently deletes an object and its data, this notebook's best-practices list is worth internalizing before you ever run one against anything real: back up first, understand dependencies between objects before dropping one, use transactions when making several related changes, and review the schema periodically as the application evolves.

## Key syntax cheat sheet

```sql
CREATE DATABASE StudentDB;
CREATE TABLE Students (
    StudentID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50)
);
CREATE INDEX idx_lastname ON Students(LastName);

ALTER TABLE Students ADD Email VARCHAR(100);
ALTER TABLE Students ALTER COLUMN Address NVARCHAR(500);
ALTER TABLE Students ADD CONSTRAINT PK_StudentID PRIMARY KEY (StudentID);

DROP TABLE Students;
DROP DATABASE StudentDB;
```

## Gotchas & common mistakes

- Treating `DROP` casually because it "just deletes a table", it deletes the table *and all its data*, permanently, with no undo unless a backup exists.
- Indexing every column "just in case." An index speeds up reads on that column, but every index also slows down writes (`INSERT`/`UPDATE`/`DELETE` now has to maintain the index too) and takes storage, indexing is a trade-off, not a free win.
- Confusing `DELETE` (DML, removes rows, filterable, this repo's `08a`) with `DROP` (DDL, removes the whole object).

## Interview questions & model answers

**Q1 (common opener): "What are the three sub-languages of SQL?"**
Model answer: "DDL for structure, `CREATE`, `ALTER`, `DROP`. DML for data, `INSERT`, `UPDATE`, `DELETE`. And DQL, which in practice is just `SELECT` and its clauses, for reading data back."

**Q2: "What does a database index actually do, and why not add one to every column?"**
Model answer: "An index lets the engine find matching rows without scanning the whole table, it speeds up reads and joins on the indexed column significantly. The trade-off is every index has to be maintained on every write, so more indexes mean slower `INSERT`/`UPDATE`/`DELETE` and more storage used. I'd index columns that are actually searched or joined on frequently, not everything by default."

**Q3: "What would you check before running a `DROP TABLE` in a real environment?"**
Model answer: "That a current backup exists, that I understand what else depends on this table, foreign keys, views, application code, so dropping it doesn't break something else silently, and if I'm making several related structural changes at once, wrapping them in a transaction so a partial failure doesn't leave the schema half-migrated."

**Q4: "What's the difference between `DROP TABLE` and `DELETE FROM table`?"**
Model answer: "`DROP TABLE` is DDL, it removes the table object itself, structure and all data, permanently. `DELETE FROM table` is DML, it removes rows, can be filtered with `WHERE`, and the table structure stays intact afterward, empty or partially emptied, but still there."

## Extra practice

- Write out, from memory, the full `CREATE TABLE` → `ALTER TABLE ADD CONSTRAINT PRIMARY KEY` → `CREATE INDEX` sequence for a table you invent, then compare against the `Students` example.
- Explain out loud, in under a minute, why `DROP` needs more caution in an interview answer than `DELETE` does, this notebook's best-practices list (backup, dependencies, transactions, schema review) is a good structure to hang the answer on.
