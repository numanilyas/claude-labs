# Lab 4 — Totals and subtotals without a pivot table

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Terminal or Workbench</span>
  <span>Database: northwind</span>
</div>

## The problem

A pivot table is a `GROUP BY` with a mouse. It's a good tool right up to the
point where you want the same subtotals next month, or the source has more
rows than Excel will hold, or somebody asks how you got the number and the
honest answer is "I dragged Department into Rows".

`GROUP BY` is the same operation written down, which means it can be rerun,
reviewed and pasted into an email.

## Before you start

- [ ] Labs 2 and 3 done
- [ ] `USE northwind;`

## Do this

### 1. Subtotals

```sql
SELECT aging_bucket,
       COUNT(*)    AS invoices,
       SUM(amount) AS total
FROM invoices
GROUP BY aging_bucket
ORDER BY total DESC;
```

Read it as: one output row per distinct `aging_bucket`, and for each of them
count the rows and add up the amounts. Everything you select must either be in
the `GROUP BY` or be wrapped in a function like `SUM` or `COUNT`.

### 2. The variance report

```sql
SELECT department,
       SUM(budget)               AS budget,
       SUM(actual)               AS actual,
       SUM(actual) - SUM(budget) AS variance,
       ROUND((SUM(actual) - SUM(budget)) / SUM(budget) * 100, 1) AS pct
FROM budget_actual_raw
GROUP BY department
ORDER BY variance DESC;
```

That's the Q2 opex variance by department, and it took eight lines.

### 3. The control total

```sql
SELECT COUNT(*)                  AS lines_,
       SUM(budget)               AS budget,
       SUM(actual)               AS actual,
       SUM(actual) - SUM(budget) AS variance
FROM budget_actual_raw;
```

Drop the `GROUP BY` and you get the grand total. The department subtotals must
add to this. Check it once so you know the query is doing what you think.

### 4. Now find something

`HAVING` filters the groups after they're formed, the way `WHERE` filters rows
before. It's how you find things that happened more than once — which, in a
cash ledger, is how you find a payment that went out twice.

```sql
SELECT reference,
       COUNT(*)    AS times_posted,
       SUM(credit) AS total
FROM gl_entries
WHERE credit IS NOT NULL
GROUP BY reference
HAVING COUNT(*) > 1;
```

Two rows come back. Only one of them is a problem. Work out which before you
read the next section.

## What good looks like

**Aging:**

| Bucket | Invoices | Total |
|---|---|---|
| Current | 19 | 665,109.08 |
| 31-60 | 9 | 255,969.98 |
| 90+ | 4 | 116,829.32 |
| 61-90 | 2 | 58,443.91 |

**Variance by department:**

| Department | Budget | Actual | Variance | % |
|---|---|---|---|---|
| Engineering | 423,900.00 | 454,717.21 | +30,817.21 | +7.3 |
| G&A | 185,400.00 | 193,758.97 | +8,358.97 | +4.5 |
| Marketing | 167,400.00 | 175,358.87 | +7,958.87 | +4.8 |
| Customer Success | 172,500.00 | 173,827.34 | +1,327.34 | +0.8 |
| Operations | 357,600.00 | 351,380.59 | −6,219.41 | −1.7 |
| Sales | 264,900.00 | 257,767.07 | −7,132.93 | −2.7 |

Grand total **1,571,700.00** budget against **1,606,810.05** actual, so
**+35,110.05**, or +2.2%. Same figures as the finance track's variance memo —
different tool, same answer, which is how you know both are right.

??? note "The duplicate — open after you've tried"

    | Reference | Times posted | Total |
    |---|---|---|
    | CHK10476 | 2 | 28,400.00 |
    | ACH | 3 | 283,980.00 |

    **ACH is fine.** Three separate ACH movements — two payroll runs and a
    corporate card settlement — that all carry the same generic reference.
    Nothing is wrong; the reference just isn't unique.

    **CHK10476 is not fine.** One cheque number, two postings, 14,200.00 each.
    It's the annual Orion Software licence, entered twice — the second entry's
    memo even says "re-posted". Cash in the ledger is 14,200.00 lower than it
    should be.

    This is the same duplicate the [bank reconciliation
    lab](../finance/06-reconciliation.md) turns up by matching a statement
    line by line. Here it took one query and no statement at all.

    The lesson isn't that the query found it. It's that the query returned
    **two** rows and only one was a finding. A tool that flags duplicates will
    flag legitimate ones too, and deciding which is which is the part that
    still needs you.

## Ask for the query, then read it

!!! example prompt "Copy this prompt"

    ```text
    MySQL 8.4. Table budget_actual_raw has these columns:
    month (like '2026-06'), department, account, budget, actual.

    Write one query that gives me the ten worst overspends at the
    month/department/account level, with budget, actual, the dollar
    variance and the percentage variance, worst first.

    Exclude any line where the budget is zero, and tell me why that
    exclusion is there.

    Then, separately, give me a query I can run to prove your first
    query didn't drop any rows it shouldn't have.
    ```

That last paragraph is the one worth stealing. Asking for the check alongside
the answer costs you nothing and gets you something you can actually hand to a
reviewer.

<div class="yours" markdown>
**Now on your own data.** Take the table you loaded in Lab 2 and write the
subtotal you produce most often by hand — by cost centre, by vendor, by month.

Then run the `HAVING COUNT(*) > 1` pattern against whatever ought to be unique
in your data: invoice numbers, cheque numbers, journal references, employee
IDs. It takes thirty seconds and it is remarkable how often something comes
back.
</div>

!!! warning "Gotcha"
    ```text
    ERROR 1055 (42000): Expression #1 of SELECT list is not in GROUP BY
    clause and contains nonaggregated column ... which is not functionally
    dependent on columns in GROUP BY clause
    ```

    You selected a column that isn't in the `GROUP BY` and isn't wrapped in
    `SUM`/`COUNT`/`MAX`. MySQL is refusing to guess which of the many values
    in that group you meant. Either add the column to the `GROUP BY` or
    aggregate it.

!!! danger "`HAVING` is not `WHERE`"
    `WHERE` runs before grouping and filters rows. `HAVING` runs after and
    filters groups. Putting a row condition in `HAVING` still works and is
    slower; putting a group condition in `WHERE` is an error. If you're
    filtering on a `SUM` or a `COUNT`, it's `HAVING`.

---

**Go deeper:** [Aggregate functions](https://dev.mysql.com/doc/refman/8.4/en/aggregate-functions.html) ·
[GROUP BY handling](https://dev.mysql.com/doc/refman/8.4/en/group-by-handling.html)

**Next:** [Lab 5 — Why the customer name isn't stored 34 times](05-one-table-is-not-enough.md)
