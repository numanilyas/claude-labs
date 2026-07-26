# Lab 3 — Ask the database your first question

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Terminal or Workbench</span>
  <span>Database: northwind</span>
</div>

## The problem

You know what you want: the five biggest open invoices, everything over 90
days, the ones due this week. In a spreadsheet that's sort, filter, sort
again, and a nagging feeling you left a filter on.

SQL is the sentence version of that. Four words get you most of the way, and
they're the same four words every time.

## Before you start

- [ ] Lab 2 done and the tie-out figures matched
- [ ] Connected: `mysql -u root -p` then `USE northwind;`

## Do this

Type these rather than pasting them. It's four minutes and it's the difference
between recognising SQL and writing it.

### 1. Everything, then a bit less

```sql
SELECT * FROM invoices;
```

34 rows. `*` means every column. Now ask for less:

```sql
SELECT invoice_no, invoice_date, amount FROM invoices;
```

### 2. Only the rows you want

```sql
SELECT invoice_no, amount, aging_bucket
FROM invoices
WHERE aging_bucket = '90+';
```

`WHERE` is your filter row. Text goes in single quotes; numbers don't.

```sql
SELECT invoice_no, amount FROM invoices WHERE amount > 50000;
SELECT invoice_no, due_date FROM invoices WHERE due_date < '2026-06-30';
```

### 3. In an order that helps

```sql
SELECT invoice_no, invoice_date, amount
FROM invoices
ORDER BY amount DESC
LIMIT 5;
```

`DESC` is largest first, `ASC` (the default) smallest first. `LIMIT 5` stops
after five rows — get in the habit of it, because one day you'll run
`SELECT *` against four million rows and wish you had.

### 4. The one you'll run every time

```sql
SELECT COUNT(*) AS invoices, SUM(amount) AS total FROM invoices;
```

`COUNT(*)` counts rows, `SUM()` adds a column, and `AS` renames the output
column so the result is readable. This is the control total. Run it before you
believe anything else.

## What good looks like

| Query | Answer |
|---|---|
| `COUNT(*)` on invoices | **34** |
| `SUM(amount)` on invoices | **1,096,352.29** |
| Count of `aging_bucket = '90+'` | **4** |
| Sum of those four | **116,829.32** |

And the top five by amount:

| Invoice | Date | Amount |
|---|---|---|
| INV-4387 | 2026-06-18 | 58,785.79 |
| INV-4397 | 2026-05-21 | 58,179.54 |
| INV-4406 | 2026-06-05 | 57,507.26 |
| INV-4462 | 2026-02-10 | 55,699.51 |
| INV-4435 | 2026-06-18 | 55,638.15 |

Those are the same figures as the [AR aging file](../sample-data.md) in the
finance track, because it's the same data. That's a useful habit in itself:
when you move data somewhere new, check it against a number you already know.

## Getting Claude to write the SQL

You will not remember the syntax for date arithmetic. Nobody does. What
matters is being able to read what comes back and tell whether it answers the
question you asked.

!!! example prompt "Copy this prompt"

    ```text
    MySQL 8.4. I have a table called invoices with these columns:

    invoice_no, customer_id, invoice_date, due_date, amount,
    days_past_due, aging_bucket

    Write me a query that lists every invoice that was due more than
    60 days ago and is for more than 20,000, largest first.

    Then explain the query line by line in plain English, and tell me
    one way it could give me a misleading answer.
    ```

Run it. Then check the row count against a query you write yourself with just
one of the two conditions — the answer must be smaller than either.

!!! tip "Ask for the explanation every time"
    A query you can't read is a number you can't defend. "Explain it line by
    line" costs Claude nothing and turns each answer into a small lesson.
    Drop it once you no longer need it.

<div class="yours" markdown>
**Now against your own table.** Use the table you loaded at the end of Lab 2.

Write three queries without help: a count of all rows, a sum of your main
amount column, and the ten largest rows. Compare the first two against the
source file.

If they don't match, stop and find out why before going any further. A
reporting layer built on a bad load is worse than no reporting layer, because
it looks fine.
</div>

!!! warning "Gotcha"
    Forgetting the semicolon leaves you at a `->` prompt, which looks like the
    terminal has hung. It hasn't — it's waiting for you to finish the
    sentence. Type `;` and press enter.

!!! warning "`SELECT *` on a real table"
    On this data it's 34 rows. On your GL extract it's four million, and it
    will print all of them. Put `LIMIT 20` on the end while you're exploring.

---

**Go deeper:** [SELECT syntax](https://dev.mysql.com/doc/refman/8.4/en/select.html) ·
[MySQL tutorial: retrieving information](https://dev.mysql.com/doc/refman/8.4/en/retrieving-data.html)

**Next:** [Lab 4 — Totals and subtotals without a pivot table](04-group-and-total.md)
