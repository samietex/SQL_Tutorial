# SQL Server Basics Tutorial

![](./SQL%20Tutorial%20Cover.png)

This is for people new to databases, or who know a little SQL and want a solid grounding in SQL Server specifically. Work through the notebooks in order and by the end you'll be able to query, filter, join, and aggregate data with T-SQL, and manage database structure with DDL and DML statements.

## Getting Started

To get started, work through this [notebook](/SQL%20Notebook1.ipynb). It introduces SQL and covers downloading SQL Server and SQL Server Management Studio.

Work through the notebooks in this order:

| Notebook Name                  | Description                                        | Link                                            |
|--------------------------------|----------------------------------------------------|-------------------------------------------------|
| Introduction to SQL            | Introduction to SQL queries and basic concepts    | [Notebook](/SQL%20Notebook1.ipynb) |
| SQL Data Definition (ALTER command)          | Use the ALTER command to change the structure of a database          | [Notebook](/DDL_ALTER.ipynb) |
| SQL Data Manipulation          | The basics of data manipulation with SQL            | [Notebook](/DML.ipynb)   |
| SQL Data Querying    | All the basic commands and concepts for querying databases         | [Notebook](/DQL.ipynb) |

### Prerequisites

- **SQL Server**: Make sure you have SQL Server installed. You can download the free SQL Server Express Edition for practice.

### Installation

1. Install SQL Server Express Edition.
2. Open SQL Server Management Studio (SSMS).

## Core Concepts

### 1. SQL Basics

- SQL (Structured Query Language) is used to manage and manipulate relational databases.
- Start constructing your `SELECT` statement to retrieve data from SQL Server.
- Filter out unwanted data using the `WHERE` clause.
- Order your result set using the `ORDER BY` clause.

### 2. Joins

- Understand different types of joins:
  - `INNER JOIN`
  - `LEFT OUTER JOIN`
  - `RIGHT OUTER JOIN`
  - `FULL OUTER JOIN`
- Retrieve data from multiple tables using joins.

### 3. Aggregates and Grouping

- Use aggregate functions like `SUM`, `AVG`, `COUNT`, etc.
- Group and summarize data using the `GROUP BY` clause.
- Apply filters to grouped data with the `HAVING` clause.

## Contributing

Contributions are welcome. If you'd like to improve existing content or add new tutorials:

1. Fork this repository.
2. Create a new branch for your changes.
3. Make your modifications (add or edit Markdown files).
4. Submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
