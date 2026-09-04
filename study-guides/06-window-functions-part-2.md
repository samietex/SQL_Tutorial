# Study Guide 06 — Window Functions, Part 2

Companion to [`06 - Window Functions, Part 2.ipynb`](<../06 - Window Functions, Part 2.ipynb>).

| Tracks | Interview format |
|---|---|
| Data Engineer · Analytics Engineer (heavy, senior-level differentiator) | Technical screen, whiteboard, take-home |

## Concept recap

Every window function runs over a **frame**, the specific rows within the current partition it actually looks at. With `ORDER BY` inside `OVER(...)` and no frame stated, SQL Server defaults to `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, everything from the start of the partition through the current row, which is exactly what makes a running total (`05`) a *running* total. `ROWS BETWEEN` names a different, explicit frame, for example `1 PRECEDING AND 1 FOLLOWING` for a moving average centered on the current row.

`NTILE(n)` divides a partition's rows, in `ORDER BY` order, into `n` roughly equal buckets numbered 1 through n, the tool behind "top quartile" / "bottom decile" reporting. `PERCENT_RANK()` (`(rank - 1) / (rows - 1)`, always 0 at the bottom, 1 at the top) and `CUME_DIST()` (`rows at or below this value / total rows`, never 0 at the bottom since a row always counts itself) both express relative standing as 0–1 without picking a bucket count up front, but they are **not interchangeable numbers**.

The frame trap: `LAST_VALUE()` looks like it should mirror `FIRST_VALUE()`, but under the *default* frame (`RANGE ... CURRENT ROW`), every row's frame ends at itself, so `LAST_VALUE()` just returns the current row's own value, every time, silently, with no error. The fix is the same tool as the moving average, `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, widened to the entire partition instead of a few neighboring rows.

## Key syntax cheat sheet

```sql
-- Moving average: explicit frame, not the default
AVG(TotalDue) OVER (PARTITION BY CustomerID ORDER BY OrderDate
                     ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)

-- Quartile buckets
NTILE(4) OVER (ORDER BY "Total Spent" DESC)

-- Relative standing
PERCENT_RANK() OVER (ORDER BY "Total Spent")
CUME_DIST()    OVER (ORDER BY "Total Spent")

-- LAST_VALUE, fixed: widen the frame to the whole partition
LAST_VALUE(TotalDue) OVER (PARTITION BY CustomerID ORDER BY OrderDate
                            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

## Gotchas & common mistakes

- **The `LAST_VALUE()` frame trap.** This is the single most-cited SQL Server window function gotcha, and a strong signal in an interview: candidates who've hit it explain the default `RANGE ... CURRENT ROW` frame unprompted; candidates who haven't usually just say "that's weird" and move on.
- Assuming `PERCENT_RANK()` and `CUME_DIST()` are the same percentile measure. They agree at neither the exact top nor bottom in general, `PERCENT_RANK()`'s lowest row is always exactly 0, `CUME_DIST()`'s never is.
- Forgetting that `NTILE()` doesn't leave a leftover partial bucket, if the row count doesn't divide evenly, the earliest buckets absorb the extra rows so every bucket stays within one row of the others.

## Interview questions & model answers

**Q1 (senior-level differentiator): "You used `LAST_VALUE()` in a query and the result looks wrong, every row seems to just repeat its own value back. What's going on?"**
Model answer: "It's almost certainly the default window frame. With `ORDER BY` and no explicit `ROWS`/`RANGE` clause, SQL Server defaults to `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, so every row's frame stops at itself, and `LAST_VALUE()` returns the current row's own value every time. The fix is `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, which widens the frame to the whole partition, so `LAST_VALUE()` can actually see the true last row."

**Q2: "How would you split customers into spending quartiles in SQL?"**
Model answer: `NTILE(4) OVER (ORDER BY total_spent DESC)` on a pre-aggregated per-customer total, "quartile 1 ends up as the top spenders because I ordered descending; if I wanted quartile 1 to be the *lowest* spenders instead, I'd just order ascending."

**Q3: "What's the difference between `PERCENT_RANK()` and `CUME_DIST()`?"**
Model answer: "Both range 0 to 1 and both express relative standing, but the formulas differ. `PERCENT_RANK()` is `(rank - 1) / (n - 1)`, so the single lowest row is always exactly 0 and the single highest is always exactly 1. `CUME_DIST()` is 'rows at or below this value divided by total rows', so the lowest row is never exactly 0, it's always at least counting itself, and any row tied for the maximum is exactly 1. I'd reach for `PERCENT_RANK()` when I want a clean 0-to-1 spread, and `CUME_DIST()` when I actually care about ties and 'what fraction of rows are at or below me.'"

**Q4: "Write a 3-period moving average of order totals per customer."**
Model answer:
```sql
AVG(TotalDue) OVER (PARTITION BY CustomerID ORDER BY OrderDate
                     ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS "3-Order Moving Average"
```
"This includes the current row plus its immediate neighbor on each side, up to 3 rows. The first and last order in each customer's history only have one neighbor available, not two, so their average is over 2 rows, not 3, that's expected, not a bug."

## Extra practice

- Compute both `PERCENT_RANK()` and `CUME_DIST()` on the same ordered column and manually verify, for the lowest and highest row, exactly why the two values differ.
- Deliberately break `LAST_VALUE()` by omitting the `ROWS BETWEEN`, confirm it returns the current row's own value every time, then fix it, do this from memory before checking the notebook.
