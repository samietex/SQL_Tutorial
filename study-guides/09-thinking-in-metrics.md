# Study Guide 09: Thinking in Metrics

Companion to [`09-thinking-in-metrics.ipynb`](<../09-thinking-in-metrics.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Analyst, Analytics Engineer, Data Engineer | Take-home, case interview ("how would you measure..."), technical screen |

## Concept recap

A **metric** is a number with a definition: what's measured, over which rows, for what period. A business question like "who are our best customers?" leaves decisions open, and a query makes each of them, on purpose or not:

| Decision | The question to settle |
| --- | --- |
| Grain | What one row of the answer is (one customer, not one order) |
| Measure | Total spent, order count, average order, share of credit used |
| Who counts | Is a customer with no orders included? |
| Period | All time, this quarter? Can the data even tell? |
| Ties | Do tied rows share a rank, or does a rule break the tie? |

On four customers, "best" has four correct answers: Bola by total spent, Ada and Bola tied by order count, Chidi by average order, Ada by share of credit used. On AdventureWorks, the biggest spender, the biggest average order, and the two most frequent customers are four different customers.

Two traps change metrics without an error. **Integer division** truncates: 170 / 200 is 0 in SQLite, PostgreSQL, and SQL Server (MySQL returns a decimal), and the online share of AdventureWorks orders comes out as 0 instead of 0.88. **`LIMIT 1` on a tie** names one winner arbitrarily; `RANK()` keeps every tied row.

## Key syntax cheat sheet

```sql
-- Definition first, kept with the query
-- Best customers: total order amount, all time,
-- every customer included (no orders counts as 0), tied totals share a rank.
WITH customer_totals AS (
    SELECT
        c.customer_name,
        COALESCE(SUM(o.amount), 0) AS total_spent
    FROM customers AS c
    LEFT JOIN orders AS o
        ON o.customer_id = c.customer_id
    GROUP BY
        c.customer_id,
        c.customer_name
)
SELECT
    customer_name,
    total_spent,
    RANK() OVER (ORDER BY total_spent DESC) AS spend_rank
FROM customer_totals;

-- A share that doesn't truncate
ROUND(100.0 * total_spent / credit_limit, 1)
```

## Gotchas and common mistakes

- Answering "best customers" without saying which measure, period, and population the answer uses.
- A `LEFT JOIN` that keeps a customer with no orders, followed by an `AVG` that skips them anyway because their total is `NULL`. Only `COALESCE` counts them as 0, and 136.67 becomes 102.5.
- Dividing two whole numbers.
- `LIMIT 1` or `TOP 1` when a tie for first is possible.
- Confusing average order value (per order) with the average of each customer's average (per customer). On the lesson data they're 82.0 and 91.67; on AdventureWorks, about 3,916 and 1,678, the gap going the other way.
- Labelling a column vaguely. `avg_spend_per_ordering_customer` is clumsy and can't be misread.

## Interview questions and model answers

**Q1 (case interview): "How would you find our best customers?"**
Model answer: "I'd first ask what the answer is for, because that decides the measure: revenue for a thank-you campaign, order frequency for a loyalty programme, share of credit for a risk review. Then I'd confirm the period, whether customers with no orders count, and how to handle ties, write that as a one-sentence definition, and only then write the query, with the definition as a comment."

**Q2: "Two dashboards show different numbers for average spend per customer. How do you investigate?"**
Model answer: "Compare the definitions before the SQL: who's in the denominator, what period, which orders count, whether missing values are skipped or counted as zero. A classic cause is one including customers who never ordered and the other not."

**Q3: "Why does this percentage query return 0 for most rows?"**
Model answer: "Both sides of the division are integers, so the engine does integer division and truncates. Multiplying by `1.0` or `100.0` first makes it a decimal division, and the result then stops depending on which engine runs it."

**Q4: "Who's our most frequent customer?" (with a tie)**
Model answer: "I'd rank with `RANK()` and return everyone at rank 1, so a tie is visible. If the business needs one name, I'd agree a tie-breaking rule and put it in the `ORDER BY`, rather than let `LIMIT 1` pick arbitrarily."

## Extra practice

- Rank customers by order count with `RANK()` and `DENSE_RANK()`, and explain where and why they differ.
- Show each customer's share of all revenue, including Dami at 0, and check the shares add to 100.
- On AdventureWorks, find the best customer of 2013 and compare them with the all-time leader.
- Write a one-sentence definition for "active customer" and list every decision it makes.
