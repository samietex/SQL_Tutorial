# Study Guide: Appendix A, SQL Server Reference

Companion to [`appendix-a-sql-server-reference.ipynb`](<../appendix-a-sql-server-reference.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Analyst, Analytics Engineer, Data Engineer | Technical screen, especially for roles that name a specific database |

## Concept recap

Most of SQL is shared across engines: `SELECT`, `WHERE`, `JOIN`, `GROUP BY`, CTEs, and window functions behave the same almost everywhere. The differences sit in details, and the dangerous ones change an answer without an error: whole-number averages and division, text comparison and collation, a scalar subquery returning several rows, whether foreign keys are enforced, and how `NULL` is treated by `UNIQUE` or by joining text with `+`. The appendix's side-by-side table lists every difference the course met, with the notebook that shows it.

On an unfamiliar database, the first move is to explore it: `INFORMATION_SCHEMA.TABLES` and `INFORMATION_SCHEMA.COLUMNS` (standard SQL, so they work on PostgreSQL and MySQL too) list tables, columns, types, and nullability, and SQL Server's `sys.foreign_keys` shows how tables connect.

## Key syntax cheat sheet

| Task | SQLite | SQL Server |
| --- | --- | --- |
| First rows | `LIMIT 5` | `SELECT TOP 5` |
| Paging | `LIMIT 5 OFFSET 10` | `ORDER BY ... OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY` |
| Join text | `a \|\| b` | `a + b`, `CONCAT`, `CONCAT_WS` |
| First non-null | `COALESCE` | `COALESCE` or `ISNULL` |
| Today | `date('now')` | `CAST(GETDATE() AS DATE)` |
| Rows changed | `changes()` | `@@ROWCOUNT` |
| Temporary table | `CREATE TEMP TABLE` | `#name` |

```sql
-- What's in this table?
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'Sales'
  AND TABLE_NAME = 'SalesOrderHeader'
ORDER BY
    ORDINAL_POSITION;
```

## Gotchas and common mistakes

- Joining text with `+` when a part can be `NULL`: the whole result is `NULL`. `CONCAT_WS` skips `NULL` parts.
- Reading `DATEDIFF(year, ...)` as full years; it counts boundaries crossed.
- Filtering dates with `BETWEEN` on a column that carries times, which misses the last day after midnight.
- Using `FLOAT` for money.
- Running `DROP` without a backup or a check of what depends on the object.

## Interview questions and model answers

**Q1: "You learned SQL on one database and this job uses another. What would you watch for?"**
Model answer: "The core is the same, so I'd focus on the details that change answers silently: integer division and averages, how text compares, how `NULL`s sort, what happens with ambiguous `GROUP BY` columns or multi-row subqueries, and whether constraints like foreign keys are enforced. And row-limiting syntax, `LIMIT` against `TOP`."

**Q2: "How do you get to know a database you've never seen?"**
Model answer: "List the schemas and tables from `INFORMATION_SCHEMA`, read the columns, types, and nullability of the ones that matter, look at the foreign keys to see how they connect, and then, for each table, work out what one row represents before I query it."

**Q3: "Why might a VARCHAR column not be enough?"**
Model answer: "`VARCHAR` may not store characters outside the database's code page; `NVARCHAR` stores Unicode, which names in many languages need. On SQL Server, Unicode literals are written with an `N` prefix."

## Extra practice

- Pick one AdventureWorks table you haven't used and describe its grain, its key, and which columns can be `NULL`, using only `INFORMATION_SCHEMA` queries.
- Rewrite three queries from earlier notebooks so they run on SQL Server instead of SQLite.
- Build a full name from `Person.Person` three ways and explain each result for a person with no middle name.
