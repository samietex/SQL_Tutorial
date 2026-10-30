# Study Guide 07: Window Functions, Part 2 (frames)

Companion to [`07-window-functions-part-2.ipynb`](<../07-window-functions-part-2.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Engineer, Analytics Engineer, Data Analyst | Technical screen (live coding), whiteboard, take-home |

## Concept recap

An aggregate used as a window function reads a **frame**: the slice of its partition read for each row. With no `ORDER BY` inside `OVER`, every row is a peer and the frame is the whole partition. With `ORDER BY` and no frame written, the default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which includes the current row's **peers**, the rows tied with it.

That default causes two silent mistakes. A running total ordered by a column with ties jumps straight past the tied rows: ordered by `customer_id`, both of Ada's orders show 100, and on AdventureWorks every one of the 43 orders on the first day shows the whole day's total. And `LAST_VALUE()` returns the current row, because the default frame ends there; it needs `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

`ROWS` counts individual rows, which suits moving windows but needs a unique ordering. Moving windows have short frames at the edges, so the first rows average fewer values. `NTILE(n)` splits rows into `n` buckets, larger ones first, and can split ties across buckets; `PERCENT_RANK()` is the share of *other* rows below a row, and `CUME_DIST()` the share of *all* rows at or below it. `ROW_NUMBER()`, `LAG()`, `LEAD()`, `NTILE()`, `PERCENT_RANK()`, and `CUME_DIST()` ignore the frame.

## Key syntax cheat sheet

```sql
-- A running total with a unique ordering and an explicit frame
SUM(amount) OVER (
    ORDER BY
        customer_id,
        order_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

-- A trailing moving average, with a count of rows in the frame
AVG(amount) OVER (ORDER BY order_id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
COUNT(*) OVER (ORDER BY order_id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- The last value in the whole partition
LAST_VALUE(amount) OVER (
    PARTITION BY customer_id
    ORDER BY order_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

SQL Server allows `RANGE` only with `UNBOUNDED PRECEDING`, `CURRENT ROW`, and `UNBOUNDED FOLLOWING`; for a sliding window there, use `ROWS`.

## Gotchas and common mistakes

- Relying on the default frame for a running total when the `ORDER BY` column can tie.
- Switching to `ROWS` without a tie-breaker: the order of tied rows is still undefined, so the result can change between runs.
- `LAST_VALUE()` with the default frame.
- Charting the first rows of a moving average as if they averaged a full window.
- Treating a seven-row window as seven days when some days are missing or doubled.
- Using `NTILE()` when identical values must land in the same bucket.

## Interview questions and model answers

**Q1 (senior differentiator): "Why does LAST_VALUE() return the current row's value?"**
Model answer: "Because with `ORDER BY` in the window and no frame written, the frame runs from the start of the partition to the current row, so the last row of the frame is the current row. Widening the frame to `UNBOUNDED FOLLOWING` fixes it."

**Q2: "What's the difference between ROWS and RANGE?"**
Model answer: "`ROWS` counts physical rows. `RANGE` works on values, so `CURRENT ROW` includes every row tied with the current one. They only differ when the `ORDER BY` has ties, which is why a running total by date can jump by a whole day at once under the default `RANGE` frame."

**Q3 (live coding): "Write a 7-day moving average of daily sales."**
Model answer: "`AVG(sales) OVER (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`, with a `COUNT(*)` over the same frame so I can flag the first six days. I'd also check there's exactly one row per day first, filling missing days, since `ROWS` counts rows, not days."

**Q4: "PERCENT_RANK or CUME_DIST?"**
Model answer: "`PERCENT_RANK` is the share of other rows ranked below this one, so the lowest is always 0; `CUME_DIST` is the share of all rows at or below it, so the lowest is never 0. On four customers, the same customer is at 0.33 by one and 0.5 by the other, so I'd pick the one that matches how the report will word it."

## Extra practice

- Run the running total ordered by `customer_id` with the default frame and with `ROWS`, and explain each column's first row.
- Write a centered moving average (one row before and one after) and say which rows have short frames.
- On AdventureWorks, split customers into spending quartiles and find the value that appears in two quartiles.
