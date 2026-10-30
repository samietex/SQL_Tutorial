# Study Guide 04: JOINs (INNER vs LEFT, and grain)

Companion to [`04-joins.ipynb`](<../04-joins.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Analyst, Analytics Engineer, Data Engineer | Technical screen (live coding), take-home |

## Concept recap

A join tests pairs of rows against the `ON` condition and combines each matching pair into one result row. `INNER JOIN` keeps only matched pairs; `LEFT JOIN` also keeps every left-hand row that found no match, with `NULL` in the right-hand columns. A join without a useful condition pairs every row with every row (a cross join: 4 customers and 3 orders make 12 rows).

The higher-stakes idea is **grain**. Join customers to their orders and the result has one row per order, so a customer-level value like a credit limit is repeated once per order. In the notebook, summing credit limits after the join gives 900 instead of 800, and `SUM(DISTINCT)` gives 600, which is also wrong because two customers share a limit of 200. The fix is to aggregate to the grain you want before joining, or to sum the right column at the right grain.

Two quieter traps: a `WHERE` condition on the right-hand table turns a `LEFT JOIN` back into an inner one, because unmatched rows have `NULL` there and fail the condition; and `COUNT(*)` counts an unmatched row as 1, so counting zeros needs `COUNT(right_table.key)`.

## Key syntax cheat sheet

```sql
-- Every customer, with their orders if any
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id;

-- Anti-join: customers with no orders
SELECT
    c.customer_id,
    c.customer_name
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Count per customer, keeping zeros
SELECT
    c.customer_name,
    COUNT(o.order_id) AS orders
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.customer_name;

-- Filter the right-hand table in ON, not WHERE, to keep unmatched rows
SELECT
    c.customer_name,
    COUNT(o.order_id) AS big_orders
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
   AND o.amount >= 60
GROUP BY
    c.customer_id,
    c.customer_name;
```

## Gotchas and common mistakes

- Summing a parent-level column after a one-to-many join, which counts it once per child row.
- Trusting `SUM(DISTINCT)` to undo duplication; it removes equal values, not repeated rows.
- Putting a right-hand filter in `WHERE` after a `LEFT JOIN`. On AdventureWorks, filtering 2014 orders that way keeps 10,354 customers instead of all 19,820.
- `COUNT(*)` after a `LEFT JOIN`, which reports 1 for a customer with no orders.
- Joining on the wrong columns, like `customer_id = order_id`. It runs, and returns nonsense or nothing.
- Treating two numbers that agree as proof. In AdventureWorks, an inner join to `Person.Person` loses exactly as many customers (701) as never ordered, by coincidence.

## Interview questions and model answers

**Q1 (extremely common): "Find every customer who has never placed an order."**
Model answer: the anti-join above. "The `LEFT JOIN` keeps every customer, and `WHERE o.order_id IS NULL` keeps only those whose order columns came back empty. I test a column that can't be `NULL` in a real match, like the order's primary key. `NOT EXISTS` with a correlated subquery is an equally good answer."

**Q2: "My revenue total doubled after I joined orders to order lines. Why?"**
Model answer: "The join changed the grain from one row per order to one row per order line, so each order's total is repeated once per line. I'd either sum the line amounts instead, or aggregate the lines to one row per order before joining."

**Q3: "When would you use INNER JOIN instead of LEFT JOIN?"**
Model answer: "When unmatched rows aren't part of the answer, like revenue by customer, where a customer with no orders contributes nothing. When the unmatched rows matter, like 'all customers and their order counts, including zero', it's a `LEFT JOIN`, and I check that nothing in `WHERE` removes them again."

**Q4: "What's wrong with this query?" (a LEFT JOIN with `WHERE o.amount >= 60`)**
Model answer: "The `WHERE` condition is on the right-hand table, so customers without a matching order have `NULL` there and get filtered out, making it an inner join. Moving the condition into `ON` keeps them."

## Extra practice

- Before and after a join, count the rows, and explain which table multiplied them.
- On AdventureWorks, find how many products have never been sold (238), then list the first ten.
- Explain, without code, why `SUM(DISTINCT credit_limit)` gives 600 on the lesson data.
