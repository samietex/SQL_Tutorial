# SQL Tutorial

![](./SQL%20Tutorial%20Cover.png)

A hands-on companion to the *All About Data & More* SQL curriculum. This is for people new to databases, or who know a little SQL and want a solid grounding in SQL Server specifically. Work through the notebooks in order and by the end you'll be able to query, filter, aggregate, and eventually join and window-function your way through real data, plus manage database structure with DDL and DML statements.

## Getting Started

**Already comfortable with git, VS Code, and SQL Server?** Clone the repo, open it in VS Code with the mssql extension installed, restore AdventureWorks2022, and start with [`01 - SQL Basics`](<01 - SQL Basics (SELECT, WHERE, ORDER BY).ipynb>). Everything below is for anyone who isn't, worth a read even if you're experienced, since it's specific to this repo, not a generic git tutorial. The full version of this lives in [`00 - Course Overview.ipynb`](<00 - Course Overview.ipynb>), read that first if you're new here.

### What you're actually looking at

Every file ending in `.ipynb` is a Jupyter notebook: a document that mixes explanation with actual SQL code you can run one step at a time and see the real result underneath it. That's the whole point of this repo, you don't just read about `SELECT`, you run it yourself.

### Reading vs. running

Viewing this on github.com shows you a **preview**. GitHub can display a notebook's text and whatever results were already saved in it, but it can't execute anything, there's no database behind the page. To actually run a query, you need to open the notebook somewhere connected to a real SQL Server, on your own computer.

### 1. Get the code onto your computer

```
git clone https://github.com/samietex/SQL_Tutorial.git
```
Never used git? Click the green **Code** button on this page, then **Download ZIP**, and unzip it somewhere on your computer.

### 2. Install SQL Server and load the practice data

- Install [SQL Server Express Edition](https://www.microsoft.com/en-us/sql-server/sql-server-downloads), it's free.
- Install [SQL Server Management Studio (SSMS)](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms), the tool you'll use to load the sample database below.
- Download and restore the **AdventureWorks2022** sample database, most of these notebooks query it, and it doesn't come with SQL Server automatically. Official instructions: [Install and configure AdventureWorks](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure). You want the OLTP `.bak` file, restored as `AdventureWorks2022`.

### 3. Install a tool that can actually run the notebooks

These notebooks use a SQL kernel, they need an app that can connect a `.ipynb` file to a real SQL Server and run its cells.

- Install [Visual Studio Code](https://code.visualstudio.com/), it's free.
- Inside VS Code, install the **SQL Server (mssql)** extension by Microsoft.
- Open this repo's folder in VS Code, then open a notebook.
- The first time you run a cell, VS Code asks you to pick a kernel, choose the SQL kernel and connect it to your local SQL Server instance.
- Run a cell with `Shift+Enter`. A cell that queries data shows its result as a table right underneath it, a real result from your own database.

Azure Data Studio works too, it has the same SQL Notebooks feature built in.

## Course Agenda

| # | Type | Module |
|---|------|--------|
| 1 | Newsletter Only | What is a Database, and Why SQL (conceptual, no notebook, see the newsletter) |
| 2 | Hands-On | [01 - SQL Basics (SELECT, WHERE, ORDER BY)](<01 - SQL Basics (SELECT, WHERE, ORDER BY).ipynb>) |
| 3 | Hands-On | [02 - Aggregation (GROUP BY, HAVING, COUNT/SUM/AVG)](<02 - Aggregation (GROUP BY, HAVING, COUNT-SUM-AVG).ipynb>) |
| 4 | Hands-On | [03 - JOINs (INNER vs LEFT)](<03 - JOINs (INNER vs LEFT).ipynb>) |
| 5 | Hands-On | [04 - Subqueries to CTEs](<04 - Subqueries to CTEs.ipynb>) |
| 6 | Hands-On | [05 - Window Functions, Part 1](<05 - Window Functions, Part 1.ipynb>) |
| 7 | Coming Soon | Window Functions, Part 2 |
| 8a | Hands-On | [08a - Changing Data, Part 1 (INSERT, UPDATE, DELETE)](<08a - Changing Data, Part 1 - INSERT, UPDATE, DELETE.ipynb>) |
| 8b | Reference | [08b - Changing Data, Part 2 (CREATE & ALTER TABLE)](<08b - Changing Data, Part 2 - CREATE & ALTER TABLE.ipynb>) |
| 9 | Newsletter Only | Thinking in Metrics (conceptual, no notebook, see the newsletter) |
| App A | Reference | [Appendix A - SQL Overview & Getting Started](<Appendix A - SQL Overview & Getting Started.ipynb>) |

Only Window Functions, Part 2 is still **Coming Soon**. See the full reasoning behind the sequence at [All About Data & More](https://aaboutdata.substack.com/p/start-here-from-beginner-to-job-ready).

## Contributing

Contributions are welcome. If you'd like to improve existing content or add new tutorials:

1. Fork this repository.
2. Create a new branch for your changes.
3. Make your modifications (add or edit notebooks or Markdown files).
4. Submit a pull request.

## License

This project is licensed under the MIT License, see the LICENSE file for details.
