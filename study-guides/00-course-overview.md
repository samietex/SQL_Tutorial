# Study Guide 00 — Course Overview

Companion to [`00 - Course Overview.ipynb`](<../00 - Course Overview.ipynb>).

| Tracks | Interview format |
|---|---|
| Data Analyst · Analytics Engineer · Data Engineer | Technical screen (rapport / background questions) |

## Concept recap

This notebook is setup, not SQL itself, but it makes one point worth internalizing before you touch a single query: **the SQL you're learning here is ANSI-standard SQL**, not a SQL Server party trick. `SELECT`, `WHERE`, `JOIN`, `GROUP BY`, CTEs, and window functions all work the same way on MySQL, PostgreSQL, Snowflake, or anywhere else. SQL Server is just the one real engine this repo installs so you have somewhere to actually run queries, not three.

The exception, flagged explicitly in the notebook, is the handful of places SQL Server does its own thing: mostly around changing data and table structure, in `08a`/`08b`. `ALTER COLUMN`, `USE`, and default-constraint syntax are SQL Server phrasing; other engines spell the same ideas differently.

The other practical point: viewing a `.ipynb` on GitHub shows a **preview** only, text and whatever output was already saved. Nothing executes until you open it somewhere connected to a real database.

## Key syntax cheat sheet

There's no new syntax in this notebook, it's the map for everything that follows. The one line worth memorizing: **portable SQL vs. engine-specific SQL** is a real distinction interviewers probe for, especially if the job posting names a different database than whatever you learned on.

## Gotchas & common mistakes

- Assuming a SQL skill learned on one engine "doesn't count" for a job posting a different one. It transfers almost entirely; only DDL syntax specifics change.
- Confusing "I read the notebook" with "I ran the notebook." A GitHub preview is not proof you can execute a query against a live database, and interviewers can tell the difference fast in a live technical screen.

## Interview questions & model answers

**Q1: "We use PostgreSQL (or MySQL, or Snowflake) here, not SQL Server. Is that going to be a problem for you?"**
Model answer: "No, the core language is the same set of ANSI SQL clauses, `SELECT`, `WHERE`, `JOIN`, `GROUP BY`, CTEs, window functions, they all behave identically across engines. The differences I'd expect to hit are mostly on the DDL side, like `ALTER COLUMN` syntax or default-value syntax, which I already know varies engine to engine because I ran into it directly comparing SQL Server, MySQL, and PostgreSQL. I'd expect to be productive within a day or two of adjusting to the specific dialect."

**Q2: "What are the three sub-languages of SQL, and where does a `SELECT` statement fit?"**
Model answer: "DDL (Data Definition Language) for structure, `CREATE`/`ALTER`/`DROP`; DML (Data Manipulation Language) for changing data, `INSERT`/`UPDATE`/`DELETE`; and DQL (Data Query Language), which is really just `SELECT` and its clauses, for reading data back out. `SELECT` is DQL."

**Q3: "How do you verify a query actually did what you think it did, beyond it running without an error?"**
Model answer: "I run it against real data, not just review the syntax. A query can be syntactically valid and semantically wrong, wrong join grain, wrong aggregate, off-by-one in a window frame, so I check row counts before and after, spot-check a few rows by hand, and compare against a known-good number when one exists."

## Extra practice

- Take any query from `01` or `02` and rewrite it in PostgreSQL syntax from memory, then check yourself against the Postgres docs. Note exactly what changed and what didn't.
- Write one sentence, out loud, explaining the difference between DDL, DML, and DQL, without looking at this guide. This is a genuinely common opening SQL interview question, and it's the kind of thing you either have cold or fumble under pressure.
