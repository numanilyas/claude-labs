# Lab 10 — SQL or Python?

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Terminal</span>
  <span>Mostly thinking</span>
</div>

## The problem

You now have two tools that can both produce a total. Reach for the wrong one
and nothing breaks — you just end up with something slow, or fragile, or
subtly wrong in the second decimal place.

There's a rule that gets it right nearly every time, and it isn't about which
language you prefer.

## Before you start

- [ ] Labs 1 to 9 done — this one is a decision, and the decision only makes
      sense once you've used both tools badly at least once
- [ ] A list, on paper, of the data jobs you actually do in a month

## Do this

### 1. Learn the rule

**Reduce in SQL. Shape and deliver in Python.**

The database is sitting next to the data. Filtering, joining, grouping and
summing four million rows is what it was built for, and it does it without
sending you four million rows. Python is on the other end of a wire with all
of that in memory.

So: get the data down to the smallest correct answer inside the query. Then
use Python for everything that happens to the answer afterwards.

### 2. Learn where each one wins

| Job | Tool | Why |
|---|---|---|
| Filter, join, group, sum | **SQL** | The database does it where the data is. Sending 4m rows to Python to add them up is the slowest possible way. |
| Money arithmetic | **SQL** | `DECIMAL` is exact. Lab 8 showed pandas turning 1,096,352.29 into 1096352.2899999998. |
| One number for an email | **SQL** | It's one line. Don't write a script. |
| Ad-hoc question at 4pm | **SQL** | Faster to type than to set up. |
| Excel output, formatting | **Python** | SQL has no concept of a bold header. |
| The same report, twelve times | **Python** | A loop and a parameter. Lab 9. |
| Combining MySQL with a CSV, an API, a PDF | **Python** | SQL can only see its own tables. |
| Anything conditional — "if it fails, don't send it" | **Python** | SQL has no `if this then stop`. |
| Charts | **Python** | Or Excel. Not SQL. |
| Sending, saving, scheduling | **Python** | SQL returns rows and goes back to sleep. |

### 3. Learn the tell

If you catch yourself pulling a big result into pandas and then filtering or
grouping it there, that work belonged in the query. Every time.

```python
# Slow, and gets slower every month.
df = pd.read_sql("SELECT * FROM budget_actual_raw", cnx)
june = df[df["month"] == "2026-06"]
by_dept = june.groupby("department")["actual"].sum()
```

```python
# The database does the work and hands you six rows.
df = pd.read_sql("""
    SELECT department, SUM(actual) AS actual
    FROM budget_actual_raw
    WHERE month = '2026-06'
    GROUP BY department
""", cnx)
```

Same answer. On 129 rows both are instant. On a real ledger the first one is
the difference between a script that runs in two seconds and one you start and
go for coffee.

### 4. Sort these five

Decide, before reading on, which tool each one wants.

1. "What's total AR over 90 days?"
2. "Send the aging pack to the three account managers, each with only their
   own customers, on the first working day of the month."
3. "Which customers are over their credit limit?"
4. "Does our AR ledger agree to the aging report the bank has?"
5. "Chart the last 24 months of opex by department."

??? note "Open after you've decided"

    1. **SQL.** One query, one number. Writing a script for this is a way of
       avoiding writing the query.
    2. **Python** — wrapping a SQL query. The filtering per manager is `WHERE
       account_manager = :manager`; the looping, the three files and the
       sending are Python. This is Lab 9 with names instead of months.
    3. **SQL.** You wrote it in Lab 5. It's a `JOIN`, a `GROUP BY` and a
       `HAVING`.
    4. **Python.** Two sources, one of them not in your database. SQL cannot
       see the bank's file.
    5. **Python**, with the aggregation in SQL. `GROUP BY period, dept_id`
       gives you 24 × 6 rows; the chart is matplotlib or Excel. Do not pull
       two years of transactions to chart six lines.

    The pattern in 2, 4 and 5: **the query is still the core**. Python is the
    wrapper. If your Python is doing arithmetic on money, look again at
    whether the query should have done it.

## What good looks like

Two of the five — 1 and 3 — are a single SQL query and nothing else. The other
three are Python **wrapping** a SQL query, and in none of them is Python doing
arithmetic on money.

If you put 2, 4 or 5 down as "pure Python", you were thinking about the
deliverable rather than the data. If you put any of them down as "pure SQL",
you were thinking about the data and forgetting that somebody has to receive
it.

## The third option

For a genuine one-off — a question you'll ask once and never again — the right
answer is sometimes neither. Export the query result and open it in Excel.
Nobody gets promoted for automating something that happens once.

The moment to write the script is the *second* time somebody asks.

!!! example prompt "Copy this prompt"

    ```text
    I do this task every month by hand:

    [describe it - where the data comes from, what you do to it, what
    you produce, who gets it]

    I have MySQL 8.4 and Python with pandas available.

    Tell me:
    1. Which parts of this should be a SQL query and which should be
       Python, and why for each
    2. Which parts should stay manual, if any, and why
    3. What could go wrong if this ran unattended, and what check
       would catch each one

    Be blunt about anything that isn't worth automating.
    ```

<div class="yours" markdown>
**Now write your list.** Take the ten things you do most often with data.
Against each one put SQL, Python, or Excel.

Then look at the SQL column. Those are the ones you can start doing better
this week, because you already know how.

Look at the Python column. Pick the one that costs you the most hours a year
and build it with Lab 9's script as the skeleton.

Ignore the Excel column. It's fine.
</div>

!!! warning "Gotcha"
    The rule is about *where the work happens*, not about which language the
    file is written in. A Python script that runs one well-shaped query is
    following it. A Python script that pulls a table and reimplements
    `GROUP BY` in pandas is breaking it, no matter how tidy the code looks.

## What you've got now

Ten labs ago a database was something you raised a ticket for. You can now
install one, load a file into it, ask it questions, spot when its answers are
lying to you, and wrap the whole thing in a script that refuses to produce a
file when the numbers don't tie.

That last part is the one that matters. Every technique here can produce a
wrong number confidently and quickly. What makes it safe to use at work is the
control total, run every time, on a number that came from outside the system.

!!! danger "Before you point any of this at production"
    Everything in this track ran against a local database with fictional data.
    Read-only credentials against a real system, a copy of the data rather
    than the system itself, and someone else's eyes on the query before its
    output goes anywhere. The finance track's
    [Verify before you send](../finance/11-verify-before-you-send.md) applies
    here word for word.

---

**Go deeper:** [MySQL 8.4 reference manual](https://dev.mysql.com/doc/refman/8.4/en/) ·
[pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html)

**Next:** back to the [track index](index.md), or the
[prompt library](../prompt-library.md) for everything in one place.
