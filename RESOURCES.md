# Resources

The best places to learn SQL beyond this course, chosen for depth and accuracy rather than popularity. Every notebook already ends with a "Go deeper" list for its own topic; this page covers the whole subject, and the next steps after it.

You don't need all of these. A good plan is one practice site you return to every week, one book you read alongside the notebooks, and the official documentation for whichever database your work or study uses.

## Free courses

| Resource | Best for |
| --- | --- |
| [CS50's Introduction to Databases with SQL](https://cs50.harvard.edu/sql/), Harvard | A full university course, with lectures and problem sets, from tables to database design and scaling |
| [SQLBolt](https://sqlbolt.com/) | Short interactive lessons in the browser, a gentle first week |
| [Select Star SQL](https://selectstarsql.com/) | An interactive book built on one real dataset, closer to real analysis than most beginner courses |
| [Khan Academy: Intro to SQL](https://www.khanacademy.org/computing/computer-programming/sql) | Video plus exercises, for anyone who learns best by watching first |
| [Microsoft Learn: Get started querying with Transact-SQL](https://learn.microsoft.com/en-us/training/paths/get-started-querying-with-transact-sql/) | A free learning path for SQL Server specifically, useful if your workplace runs it |

## Practice

Reading SQL and writing it are different skills, and only practice builds the second one.

| Resource | Best for |
| --- | --- |
| [SQLZoo](https://sqlzoo.net/) | Quick drills on each topic, checked in the browser |
| [PostgreSQL Exercises](https://pgexercises.com/) | One realistic schema, with exercises that get properly hard by the end |
| [DataLemur](https://datalemur.com/) | Interview questions from real companies, with a free SQL tutorial alongside |
| [StrataScratch](https://www.stratascratch.com/) | A large bank of interview questions from named companies, many free |
| [LeetCode: SQL 50](https://leetcode.com/studyplan/top-sql-50/) | A fixed set of fifty interview-style problems, a good test of readiness |
| [HackerRank SQL](https://www.hackerrank.com/domains/sql) | Graded problems by topic and difficulty, often used for screening tests |
| [SQL Murder Mystery](https://mystery.knightlab.com/) | A detective story solved with queries, a good break from drills that still makes you think |

## Books

| Book | Best for |
| --- | --- |
| [Learning SQL](https://www.oreilly.com/library/view/learning-sql-3rd-edition/9781492057604/), Alan Beaulieu | A clear, complete first book, covering the same ground as this course and more |
| [Practical SQL](https://nostarch.com/practical-sql-2nd-edition), Anthony DeBarros | Learning SQL by analysing real public datasets on PostgreSQL |
| [SQL for Data Analysis](https://www.oreilly.com/library/view/sql-for-data/9781492088776/), Cathy Tanimura | The analysis techniques that come after the basics: time series, cohorts, experiments, and text |
| [T-SQL Fundamentals](https://www.microsoftpressstore.com/store/t-sql-fundamentals-9780138102104), Itzik Ben-Gan | The deepest account of how SQL Server thinks, including the logical query processing order |
| [SQL Antipatterns, Volume 1](https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/), Bill Karwin | Common design and query mistakes, why people make them, and what to do instead |
| [SQL Performance Explained](https://sql-performance-explained.com/), Markus Winand | How indexes work and why queries get slow, for when correctness is no longer the only question; most of it is free online as [Use The Index, Luke](https://use-the-index-luke.com/) |

## Official documentation

Learn to read the documentation of the database you use. It's the final word when a tutorial and the engine disagree, and every notebook in this course quotes it for exactly that reason.

- [SQLite](https://www.sqlite.org/lang.html), the engine behind every `%%sql` cell
- [SQL Server (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/language-reference), the engine behind every `%%tsql` cell
- [PostgreSQL](https://www.postgresql.org/docs/current/), whose [tutorial](https://www.postgresql.org/docs/current/tutorial.html) is one of the best free introductions to SQL there is
- [MySQL](https://dev.mysql.com/doc/refman/8.4/en/)

## Explainers worth reading

- **[SQL queries don't start with SELECT](https://jvns.ca/blog/2019/10/03/sql-queries-don-t-start-with-select/)**, Julia Evans. The order a query actually runs in, in one short page with a diagram.
- **[Modern SQL](https://modern-sql.com/)**, Markus Winand. What standard SQL can do beyond the basics, and which engines support each feature.
- **[Say NO to Venn Diagrams When Explaining JOINs](https://blog.jooq.org/say-no-to-venn-diagrams-when-explaining-joins/)**, Lukas Eder. The reason `04` explains joins as pairs of rows rather than overlapping circles.

## Tools

- **[DB Fiddle](https://www.db-fiddle.com/)** and **[dbfiddle.uk](https://dbfiddle.uk/)** run a query on several database engines in the browser, which is the quickest way to check how PostgreSQL, MySQL, or SQL Server treats something.
- **[DuckDB](https://duckdb.org/)** runs SQL directly on CSV and Parquet files on your own computer, with nothing to set up, and is fast enough for millions of rows.
- **[DBeaver Community](https://dbeaver.io/)** is a free desktop client that connects to almost any database.
- **[SQL Server Management Studio](https://learn.microsoft.com/en-us/ssms/install/install)** is the standard SQL Server client on Windows.

## Datasets for your own project

The [capstone](<capstone-online-store-analysis.ipynb>) ends by asking you to answer a question of your own. These are good places to find the data:

- **[AdventureWorks](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure)**, which you already have set up, and which has far more to explore than the course used.
- **[Maven Analytics Data Playground](https://mavenanalytics.io/data-playground)**, free business datasets, each with a description of its tables.
- **[Kaggle Datasets](https://www.kaggle.com/datasets)**, thousands of public datasets; check how each was collected before trusting it.
- **[NYC Open Data](https://opendata.cityofnewyork.us/)**, real city data, large and messy in the way real data is.

## After SQL, by track

The [Start Here roadmap](https://aaboutdata.substack.com/p/start-here-from-beginner-to-job-ready) sets out each track in full. For the first step beyond SQL on each:

- **Data Analytics:** [SQL for Data Analysis](https://www.oreilly.com/library/view/sql-for-data/9781492088776/), above, then a visualisation tool such as [Power BI](https://learn.microsoft.com/en-us/training/powerplatform/power-bi) or [Tableau Public](https://public.tableau.com/app/learn/how-to-videos).
- **Analytics Engineering:** [dbt Learn](https://learn.getdbt.com/catalog), free courses on turning SQL into tested, documented data models, and [Kimball's dimensional modeling techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/) for how those models are usually shaped.
- **Data Engineering:** [Designing Data-Intensive Applications](https://dataintensive.net/), Martin Kleppmann, for how the systems that store and move data work, and [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/), Joe Reis and Matt Housley, for the shape of the job.

---

Know a resource that belongs here, or found a broken link? Please [open an issue](https://github.com/samietex/SQL_Tutorial/issues).
