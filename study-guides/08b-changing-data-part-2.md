# Study Guide 08b — Changing Data, Part 2 (CREATE & ALTER TABLE)

Companion to [`08b - Changing Data, Part 2 - CREATE & ALTER TABLE.ipynb`](<../08b - Changing Data, Part 2 - CREATE & ALTER TABLE.ipynb>).

| Tracks | Interview format |
|---|---|
| Data Engineer (heavy, schema design) · Analytics Engineer | Technical screen, whiteboard, take-home |

## Concept recap

`ALTER TABLE` changes an existing table's structure: `ADD column`, `DROP COLUMN`, `ALTER COLUMN` to change a type, and adding or dropping named constraints, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `UNIQUE`, `DEFAULT`. A `PRIMARY KEY` enforces both uniqueness and non-nullability for a column, and a column generally needs `NOT NULL` set before it can become one. A `FOREIGN KEY` constraint ties a column's values back to a valid value in another table's column, enforcing referential integrity, break it and the database itself rejects rows that don't have a matching parent. `CHECK` enforces a condition on every row (`CHECK (Age > 18)`), `UNIQUE` enforces no duplicates without requiring the column be the primary key, `DEFAULT` supplies a fallback value when `INSERT` doesn't specify one.

Changing a column's data type is flagged explicitly as risky, it can cause data loss or fail outright if the existing data doesn't fit the new type.

The syntax for several of these operations genuinely differs by engine, this is one of the few places in the whole repo where "SQL Server does its own thing" instead of everything being portable ANSI SQL:

| Operation | SQL Server | MySQL | PostgreSQL |
|---|---|---|---|
| Change a column's type | `ALTER COLUMN col TYPE` | `MODIFY COLUMN col TYPE` | `ALTER COLUMN col TYPE ...` |
| Set a default | `ADD CONSTRAINT ... DEFAULT 'x' FOR col` | inline or `ALTER col SET DEFAULT 'x'` | `ALTER COLUMN col SET DEFAULT 'x'` |
| Switch active database | `USE db` | `USE db` | not supported, connect directly |

## Key syntax cheat sheet

```sql
ALTER TABLE Employees ADD Gender VARCHAR(255);
ALTER TABLE Employees DROP COLUMN Gender;
ALTER TABLE Employees ALTER COLUMN Employee_ID INT NOT NULL;

ALTER TABLE Employees ADD CONSTRAINT PK_ID PRIMARY KEY (Employee_ID);
ALTER TABLE Employees ADD CONSTRAINT FK_Department_ID
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID);
ALTER TABLE Employees ADD CONSTRAINT CK_Age CHECK (Age > 18);
ALTER TABLE Employees ADD CONSTRAINT UQ_Employee_Name UNIQUE (Employee_Name);
ALTER TABLE Departments ADD CONSTRAINT DF_Department_Name DEFAULT 'Finance' FOR Department_Name;
```

## Gotchas & common mistakes

- Trying to make a column a `PRIMARY KEY` while it still allows `NULL`, it needs `NOT NULL` first, exactly the two-step sequence the notebook walks through on `Department_ID`.
- Changing a column's type in place on a table with existing data that doesn't fit the new type, without checking first, this is a production incident waiting to happen, not just a syntax exercise.
- Assuming `ALTER COLUMN` syntax is portable, it's SQL Server's specific keyword; MySQL and PostgreSQL both phrase the same operation differently.
- Dropping a `FOREIGN KEY` and not recreating it, silently losing referential integrity between two tables that are supposed to stay in sync.

## Interview questions & model answers

**Q1: "Walk me through adding a foreign key relationship between two existing tables that don't currently have one."**
Model answer: "First, the column has to exist, `ALTER TABLE Employees ADD Department_ID INT`, if it doesn't already. Then I add the constraint itself: `ALTER TABLE Employees ADD CONSTRAINT FK_Department_ID FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID)`. From that point, SQL Server enforces that every `Department_ID` value in `Employees` has to exist in `Departments`, inserts or updates that violate it get rejected."

**Q2: "What's the difference between a `PRIMARY KEY` and a `UNIQUE` constraint?"**
Model answer: "Both enforce no duplicate values, but a `PRIMARY KEY` also disallows `NULL` and a table can only have one, it's the canonical identity of each row. A `UNIQUE` constraint allows `NULL` (in most engines, one or more `NULL`s are allowed since `NULL` isn't considered equal to itself), and a table can have several `UNIQUE` constraints on different columns."

**Q3: "You need to change a column's type in a production table. What do you check before running the `ALTER`?"**
Model answer: "Whether the existing data actually fits the new type without truncation or conversion errors, on a large table this can also lock it for the duration, so I'd check size and consider running it in a maintenance window or testing it against a copy first. The notebook's own caution is right: altering a type can cause data loss if the new type can't accommodate what's already there, so I verify before I run it, not after."

**Q4: "Is `ALTER TABLE ... ALTER COLUMN` something you can copy-paste into a MySQL or Postgres script unchanged?"**
Model answer: "No. MySQL uses `MODIFY COLUMN` for the same operation, PostgreSQL keeps `ALTER COLUMN` but a different clause structure (`ALTER COLUMN col TYPE ...`). It's one of the few genuinely engine-specific corners of otherwise-portable SQL, worth double-checking docs before assuming it just works elsewhere."

## Extra practice

- Design a two-table schema (like `Employees`/`Departments`) from scratch: write the `CREATE TABLE` statements, then add a primary key, foreign key, check, unique, and default constraint entirely with `ALTER TABLE` afterward, don't put them inline at creation, to practice the "modify an existing table" scenario a take-home is more likely to actually ask for.
- Look up how your foreign-key error would read differently in Postgres vs. SQL Server if you tried to insert a row violating referential integrity, interviewers sometimes ask what an error actually looks like, not just what causes it.
