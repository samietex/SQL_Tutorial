# Study Guide: Capstone, The Online Store

Companion to [`capstone-online-store-analysis.ipynb`](<../capstone-online-store-analysis.ipynb>).

| Tracks | Interview format |
| --- | --- |
| Data Analyst, Analytics Engineer, Data Engineer | "Walk me through a project", take-home, case interview |

## Concept recap

The capstone answers an open business question on AdventureWorks in the order an analyst works: write the definitions down, learn the grain of each table, check the data, analyse, save the results, and write up the answer with its caveats. Each step catches a different way of being wrong without an error:

| Step | What it caught |
| --- | --- |
| Definitions | "Revenue" could mean `SubTotal` or `TotalDue`; "came back" could mean ever or within a window |
| Date range | 2011 and 2014 are partial years, so comparing them with full years is unfair |
| First and last months | May 2011 holds one day; June 2014 has no bike sales and a 97.5 percent revenue drop |
| Lines against orders | Every order's lines add up to its `SubTotal`, so line-level revenue can be trusted |
| `NULL` check | 209 products have no subcategory, but none was ever sold, so the category join loses nothing |
| Join grain | Joining orders to lines and summing `SubTotal` doubled online revenue, from $29.4 to $59.2 million |
| Censoring | "Ever came back" made 2012 customers look 94 percent loyal and 2014 customers 7 percent |

The two findings: on 30 May 2013 the online store added accessories, clothing, and cheaper bikes, so orders roughly tripled while the average order fell to about a third, and revenue then grew to almost three times the previous year's. And among customers who first ordered between June and November 2013, those whose first order had no bike came back within 180 days six times as often as bike buyers, 20.4 percent against 3.4.

## Key syntax cheat sheet

```sql
-- Month buckets on SQL Server
DATEFROMPARTS(YEAR(OrderDate), MONTH(OrderDate), 1)

-- Month-over-month change and a three-month moving average
100.0 * (revenue - LAG(revenue) OVER (ORDER BY month_start))
    / LAG(revenue) OVER (ORDER BY month_start)
AVG(revenue) OVER (
    ORDER BY month_start
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)

-- Count orders, not lines, after joining to order lines
COUNT(DISTINCT CASE WHEN category = 'Bikes' THEN SalesOrderID END)

-- A fair repeat rate: same window for everyone
SUM(CASE WHEN second_order_date <= DATEADD(day, 180, first_order_date) THEN 1 ELSE 0 END)
```

## Gotchas and common mistakes

- Drawing a trend through the first and last periods without checking whether they're complete.
- Summing an order-level column after joining to order lines.
- Comparing "ever came back" across groups that have been watched for different lengths of time.
- Changing the group of customers between the columns you're comparing, such as a longer date range for a shorter window.
- Dropping suspicious data without saying so. Mark it, exclude it on purpose, and name it in the caveats.
- Writing "customers without a bike come back because..." when the analysis only shows that they do.

## Interview questions and model answers

**Q1: "Walk me through a project you've done."**
Model answer: "I analysed an online store's sales to answer two questions from its head of sales: how the store had done month by month, and whether first-time customers came back. I wrote the definitions down first, then checked the data, which turned up an incomplete final month I excluded. The main change was a range expansion in May 2013: orders tripled, the average order fell to about a third, and revenue almost tripled over the next year. For repeat customers, I used a fixed 180-day window and found people whose first order had no bike came back six times as often as bike buyers. I wrote it up with the definitions and caveats, including one data pattern I couldn't explain."

**Q2: "How did you know you could trust the data?"**
Model answer: "I checked it before analysing. I looked at the date range and found partial first and last years; I looked at the first and last months, and the last one had lost almost all its revenue and every bike sale, so I treated it as incomplete. I reconciled order lines against order totals, and checked that the join to product categories didn't drop any sold products because of `NULL`s."

**Q3: "Why did you use a fixed window to measure repeat purchases?"**
Model answer: "Because recent customers haven't had as long to come back. Measured as 'ever came back', older customers looked over 90 percent loyal and the newest under 10, which mostly measured time. Giving everyone the same 180 days, and only including customers whose whole window fell inside reliable data, made the groups comparable. I also reran it at 30 and 90 days to check the conclusion didn't depend on the window."

**Q4: "What would you do next, or differently?"**
Model answer: "I'd take the data questions to whoever owns the data: why the last month looks incomplete, and why nobody placed a second order before the range expanded. Then I'd look at what the returning customers bought, and whether the pattern holds for later groups of customers once they've had six months of data."

**Q5: "Your query summed revenue and the number came out twice as big as the finance report. What happened?"**
Model answer: "Most likely a join changed the grain. If orders are joined to order lines, each order appears once per line, so summing an order-level total counts it several times. I'd check the row count against the number of orders, and either sum a line-level amount or aggregate the lines before joining."

## Extra practice

- Answer one of the "Make it yours" questions from section 10 of the notebook, following the same steps, and write it up in under 300 words.
- Rerun the repeat-rate comparison for customers who first ordered between December 2013 and February 2014 with a 90-day window, and compare it with the June to November result.
- Explain, in under a minute and out loud, why "ever came back" favours older customers.
