# Study Guide 01: What Is a Database

Companion to [`01-what-is-a-database.ipynb`](<../01-what-is-a-database.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Analyst, Analytics Engineer, Data Engineer | Conversational screen, the opening minutes of a technical screen |

## Concept recap

A **table** is a stricter spreadsheet: every row has the same columns, and every column holds one kind of value. Rows have no built-in position, so a row is identified by its values, usually a **primary key** like `customer_id` that no two rows share. A missing value is `NULL`, which means unknown, not zero and not empty text.

A **database** is a set of tables connected through shared columns. The shop in the notebook keeps customers and orders in separate tables, with each order holding only a `customer_id`, so that every fact is stored once: Ada's credit limit lives on one row, and changing it can't leave two orders disagreeing about it. The cost is that a question about both tables needs a **join**, which `04` teaches. The formal name for "store each fact once" is **normalization**.

**SQL** is declarative: you describe the answer you want, and the database works out the steps. It's shared across engines like SQLite, PostgreSQL, MySQL, and SQL Server, each with its own **dialect**.

The habit to carry forward: before querying any table, ask what one row represents and what each column means.

## Vocabulary cheat sheet

| Term | Meaning |
| --- | --- |
| Row | One instance of the thing the table stores (one customer, one order) |
| Column | One fact about every row, with one type |
| Primary key | A column whose value identifies exactly one row |
| Foreign key | A column that points at another table's primary key (`orders.customer_id`) |
| `NULL` | A missing, unknown value |
| Grain | What one row represents |
| Schema | A named group of tables, like a folder (`Sales`, `Production` in AdventureWorks) |
| Many-to-many | Two tables linked through a third that holds pairs of IDs (members, classes, sign-ups) |

## Gotchas and common mistakes

- Putting everything in one wide table because it's easier to read. A fact written on several rows can be updated on some of them and not others, and the table ends up disagreeing with itself, which is what happened to Ada's limit in the notebook.
- Assuming rows come back in the order they were inserted. Without `ORDER BY`, the order is undefined.
- Treating `NULL` as zero. A missing order total is unknown, and `02` and `03` show it changing answers.
- Describing a table by its contents ("it has names and emails") instead of its grain ("one row per member signed up for one class").

## Interview questions and model answers

**Q1: "What's the difference between a database and a spreadsheet?"**
Model answer: "A spreadsheet lets you put anything in any cell and identifies rows by position. A database table enforces one type per column and identifies rows by a key, which lets software work with millions of rows safely. And a database splits data across related tables, connected by keys, so each fact is stored once instead of copied everywhere it's needed."

**Q2: "Why would you store customers and orders in separate tables?"**
Model answer: "So each fact lives in one place. If every order row carried the customer's credit limit, raising that limit would mean updating every one of their orders, and missing one leaves two different limits for the same customer. A customer with no orders would also have nowhere to live. Separate tables, connected by a customer ID, avoid both problems; the trade-off is that combining them needs a join."

**Q3: "What is a primary key, and what's a foreign key?"**
Model answer: "A primary key uniquely identifies a row in its own table, like `customer_id` in `customers`. A foreign key is a column in another table that refers to it, like `customer_id` in `orders`, and when it's declared as a constraint the database refuses an order that points at a customer who doesn't exist."

**Q4: "What does NULL mean?"**
Model answer: "That a value is missing or unknown. It isn't zero and it isn't empty text, and most comparisons with it come out unknown rather than true or false, which is why you test for it with `IS NULL`."

## Extra practice

- Pick any spreadsheet you use (a budget, a reading list, a team rota) and say what one row represents. Then list which facts repeat across rows, and sketch the separate tables you'd split it into, with the IDs that would connect them.
- From the notebook's AdventureWorks section, explain in one sentence each what one row of `Sales.Customer` and one row of `Sales.SalesOrderHeader` represent, and which column connects them.
