# Lab 6 — The query that looks right and isn't

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Terminal or Workbench</span>
  <span>Database: northwind</span>
</div>

## The problem

A wrong query doesn't crash. It returns a tidy table of plausible numbers,
formats nicely, and gets pasted into a board pack.

This is the whole risk of moving from spreadsheets to SQL. In a spreadsheet
you can see the rows. In SQL you see the answer, and the answer looks the same
whether it used all your data or most of it.

Three ways it happens. All three are in this database right now.

## Before you start

- [ ] Labs 2 to 5 done
- [ ] `USE northwind;`

## Do this

### 1. The one that costs you money

Two reasonable-looking queries for the same thing — total open receivables.

```sql
SELECT SUM(i.amount) AS total
FROM invoices i
JOIN customers c ON c.customer_id = i.customer_id;
```

```sql
SELECT SUM(amount) AS total FROM invoices;
```

Run both. They disagree.

Now find out why:

```sql
SELECT i.invoice_no, i.amount, i.aging_bucket
FROM invoices i
LEFT JOIN customers c ON c.customer_id = i.customer_id
WHERE c.customer_id IS NULL;
```

A plain `JOIN` — properly, an `INNER JOIN` — only keeps rows that match on
**both** sides. One invoice has no customer record, so the first query
silently dropped it. `LEFT JOIN` keeps every row from the left-hand table
whether it matched or not, which is what makes it useful for finding the gaps.

Check what else that quietly changed:

```sql
SELECT SUM(i.amount) AS over_90_days
FROM invoices i
JOIN customers c ON c.customer_id = i.customer_id
WHERE i.aging_bucket = '90+';
```

The missing invoice is in the 90+ bucket. So the aging report — the one that
drives collections — was understating your worst bucket by 19%.

### 2. The one that hides in a filter

```sql
SELECT COUNT(*) FROM customers WHERE region IS NULL;
SELECT COUNT(*) FROM customers WHERE region IS NULL OR region = '';
```

Different answers. `NULL` means "no value". An empty string means "a value,
which happens to be nothing". They are not the same thing and no filter
catches both unless you write it to.

Two customers were never given a region. A third has one that's blank. Any
data-quality report built on `IS NULL` alone finds two of the three and
reports a clean bill of health on the one it missed.

```sql
SELECT COUNT(*) AS all_customers, COUNT(region) AS with_a_region
FROM customers;
```

`COUNT(*)` counts rows. `COUNT(column)` counts rows where that column isn't
`NULL`. The empty string counts as a value, so even this disagrees with both
queries above.

### 3. The one you'll do to yourself

```sql
SELECT COALESCE(NULLIF(region, ''), '(not set)') AS region,
       COUNT(*) AS customers
FROM customers
GROUP BY COALESCE(NULLIF(region, ''), '(not set)')
ORDER BY region;
```

`NULLIF(region, '')` turns the empty string into `NULL`; `COALESCE` turns any
`NULL` into a label you can see. The result is a regional breakdown where the
rows with no region are *visible* rather than quietly absent.

Compare it with the naive version:

```sql
SELECT region, COUNT(*) FROM customers GROUP BY region;
```

The naive one gives six rows: your four regions, a `NULL` row, and a row whose
region column is simply blank. Three customers with no usable region, split
across two lines, both easy to skim past. The first version puts all three on
one labelled row you can't miss.

## What good looks like

| Query | Answer |
|---|---|
| `SUM(amount)` on invoices | **1,096,352.29** |
| Same, via `JOIN customers` | **1,074,341.36** |
| The difference | **22,010.93** |
| The orphan | **INV-4391**, 22,010.93, bucket 90+ |
| 90+ total, all invoices | **116,829.32** |
| 90+ total, via `JOIN` | **94,818.39** |
| `region IS NULL` | **2** |
| `region IS NULL OR region = ''` | **3** |
| `COUNT(*)` / `COUNT(region)` | **10** / **8** |

Run Lab 5's exposure query again without the `HAVING` line and look at
Brightwater Industries: 75,142.15. They actually owe 97,153.08 — the missing
22,010.93 is theirs, so their exposure is reported 23% too low.

It doesn't change a decision here, because their limit is 150,000 either way.
That's the uncomfortable part. The same silent 22,010.93 lands on the aging
report, where it takes 19% off the oldest bucket, and on a customer's exposure,
where this time it happened not to matter. Nothing in the output tells you
which case you're in.

## The habit that catches all three

One control total, computed the simplest possible way, checked against every
aggregate you build. In this database that's
`SELECT COUNT(*), SUM(amount) FROM invoices;` — no joins, no filters, no
grouping.

If your report doesn't tie to it, you have a finding: either your query is
wrong or your data has a hole in it. Both are worth knowing before somebody
else finds out.

!!! example prompt "Copy this prompt"

    ```text
    Review this MySQL query. It's going into a report that finance
    will send out, so I need to know how it could be wrong, not
    whether it runs.

    [paste your query]

    The tables are:
    [paste the output of SHOW CREATE TABLE for each one]

    Tell me specifically:
    - Could any JOIN drop rows? Which, and what would that do to the
      totals?
    - Does any filter behave differently on NULL or empty values?
    - Could any join produce more rows than it started with and
      inflate a SUM?
    - What single query should I run as a control total to prove this
      one is complete?

    Don't rewrite it yet. Just tell me what's at risk.
    ```

!!! danger "Claude cannot see your data"
    It can read your query and your schema and tell you what *could* go wrong.
    It cannot tell you whether it *did* — that needs the control total, and
    the control total needs you to run it.

    Treat a review as a list of things to check, never as a clean bill of
    health.

<div class="yours" markdown>
**Now on a query you already rely on.** Find one — a saved report, something
in your BI tool, a query somebody handed you when they left.

Run it. Then run the count-and-sum control total against the base table with
no joins and no filters. Compare.

If they differ, work out whether the difference is deliberate. Sometimes it
is. The dangerous case is when nobody knew there was a difference at all.
</div>

!!! warning "Gotcha"
    `NULL = NULL` is not true. It isn't false either — it's `NULL`. That's why
    `WHERE region = NULL` returns nothing at all rather than an error, and
    why it must be `IS NULL`. This catches everyone once.

---

**Go deeper:** [Working with NULL values](https://dev.mysql.com/doc/refman/8.4/en/working-with-null.html) ·
[JOIN clause](https://dev.mysql.com/doc/refman/8.4/en/join.html)

**Next:** [Lab 7 — Get Python talking to the database](07-install-python.md)
