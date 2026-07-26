# Lab 9 — The month-end pack, as a script you rerun

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Terminal</span>
  <span>File: month_end.py</span>
</div>

## The problem

Lab 8 produced one report from one query. Month-end isn't one report. It's the
same report, for a different period, with the same six checks, every single
month — and the thing that makes it eat a Tuesday is that the period changes
and nothing else does.

That's the shape of problem Python is actually for.

## Before you start

- [ ] Lab 8 done and `ar-report.xlsx` opened
- [ ] Virtual environment active

## Do this

### 1. Parameterise the period

The whole lab is this idea. Instead of editing the query every month, leave a
gap in it and pass the period in:

```python
SUMMARY = text("""
    SELECT d.dept_name ...
    WHERE b.period = :period
    ...
""")

pd.read_sql(SUMMARY, cnx, params={"period": period})
```

`:period` is a placeholder. The driver fills it in safely. What you must never
do is build the string yourself:

```python
# Don't.
f"WHERE period = '{period}'"
```

That works until a value contains an apostrophe — `O'Brien` in a customer name
is enough — at which point the query breaks or, worse, does something you
didn't ask for. Placeholders handle quoting for you and cannot be tricked.

### 2. Run it

Download [`month_end.py`](../files/db/month_end.py).

```python title="month_end.py"
import getpass
import os
import sys

import pandas as pd
from sqlalchemy import create_engine, text

PASSWORD = os.environ.get("MYSQL_PASSWORD") or getpass.getpass("MySQL password: ")
engine = create_engine(f"mysql+mysqlconnector://root:{PASSWORD}@127.0.0.1/northwind")

SUMMARY = text("""
    SELECT d.dept_name                   AS department,
           SUM(b.budget)                 AS budget,
           SUM(b.actual)                 AS actual,
           SUM(b.actual) - SUM(b.budget) AS variance
    FROM budget_actual b
    JOIN departments  d ON d.dept_id = b.dept_id
    WHERE b.period = :period
    GROUP BY d.dept_name
    ORDER BY variance DESC
""")

DETAIL = text("""
    SELECT d.dept_name    AS department,
           a.account_name AS account,
           b.budget, b.actual,
           b.actual - b.budget AS variance
    FROM budget_actual b
    JOIN departments d ON d.dept_id    = b.dept_id
    JOIN accounts    a ON a.account_id = b.account_id
    WHERE b.period = :period
    ORDER BY variance DESC
""")

CONTROL = text("""
    SELECT COUNT(*)              AS lines_,
           ROUND(SUM(budget), 2) AS budget,
           ROUND(SUM(actual), 2) AS actual
    FROM budget_actual WHERE period = :period
""")


def build_pack(period):
    with engine.connect() as cnx:
        summary = pd.read_sql(SUMMARY, cnx, params={"period": period})
        detail = pd.read_sql(DETAIL, cnx, params={"period": period})
        control = pd.read_sql(CONTROL, cnx, params={"period": period}).iloc[0]

    if control["lines_"] == 0:
        raise SystemExit(f"No data for {period}. Nothing written.")

    # Tie out before writing. Round: pandas read DECIMAL back as float.
    assert len(detail) == control["lines_"], "detail row count does not tie"
    assert round(detail["actual"].sum(), 2) == float(control["actual"]), \
        "detail actuals do not tie to the control total"
    assert round(summary["actual"].sum(), 2) == float(control["actual"]), \
        "summary actuals do not tie to the control total"

    summary["pct"] = (summary["variance"] / summary["budget"] * 100).round(1)
    top = detail.head(5)

    out = f"month-end-{period}.xlsx"
    with pd.ExcelWriter(out, engine="openpyxl") as xl:
        summary.to_excel(xl, sheet_name="Summary", index=False)
        top.to_excel(xl, sheet_name="Top 5 variances", index=False)
        detail.to_excel(xl, sheet_name="Detail", index=False)

    variance = round(control["actual"] - control["budget"], 2)
    print(f"{period}: {int(control['lines_'])} lines, "
          f"budget {control['budget']:>12,.2f}, "
          f"actual {control['actual']:>12,.2f}, "
          f"variance {variance:>11,.2f}  ->  {out}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        periods = sys.argv[1:]
    else:
        with engine.connect() as cnx:
            periods = pd.read_sql(
                "SELECT DISTINCT period FROM budget_actual ORDER BY period", cnx
            )["period"].tolist()
    for p in periods:
        build_pack(p)
```

```bash
python month_end.py 2026-06
python month_end.py
```

The first builds June. The second builds every period in the database, because
no argument means "all of them".

### 3. Break it on purpose

```bash
python month_end.py 2026-07
```

There is no July. You get a message and no file, rather than an empty
spreadsheet that looks like a zero-spend month.

Now break the check itself. Change one figure in the database:

```sql
UPDATE budget_actual SET actual = actual + 1000 WHERE id = 1;
```

Rerun `python month_end.py 2026-04`. It still works — the control total came
from the same table, so it moved too. That's worth understanding: **a control
total only proves internal consistency**. To prove the number is *right* you
have to tie back to something outside the database, which is why the figures
in Lab 2 were checked against the CSV.

Put it back:

```sql
UPDATE budget_actual SET actual = actual - 1000 WHERE id = 1;
```

## What good looks like

```text
2026-04: 43 lines, budget   523,900.00, actual   519,481.77, variance   -4,418.23  ->  month-end-2026-04.xlsx
2026-05: 43 lines, budget   523,900.00, actual   527,482.17, variance    3,582.17  ->  month-end-2026-05.xlsx
2026-06: 43 lines, budget   523,900.00, actual   559,846.11, variance   35,946.11  ->  month-end-2026-06.xlsx
```

Three files, three sheets each, about a second. And the story is right there in
the third column: April and May were fine, June was 6.9% over on its own.

June's **Top 5 variances** sheet:

| Department | Account | Budget | Actual | Variance |
|---|---|---|---|---|
| Engineering | Contract Labor | 14,900 | 46,190.00 | +31,290.00 |
| G&A | Professional Fees | 2,100 | 9,240.00 | +7,140.00 |
| Marketing | Marketing Programs | 7,300 | 8,220.48 | +920.48 |
| Sales | Contract Labor | 9,300 | 10,207.60 | +907.60 |
| G&A | Contract Labor | 6,500 | 7,146.68 | +646.68 |

The top two are 38,430 of a 35,946 overspend. Everything else nets off. That's
the sentence the memo opens with, and you now get it for free, monthly.

!!! example prompt "Copy this prompt"

    ```text
    Here's a Python script that builds a monthly variance pack from
    MySQL:

    [paste month_end.py]

    Add a fourth sheet called "Commentary" containing one row per
    variance over 5,000 or over 20% of budget, whichever catches more,
    with columns: department, account, variance, percent, and an
    empty "Explanation" column for me to fill in.

    Sort it by absolute variance, biggest first, so favourable
    variances that are large enough to matter also appear.

    Don't change the existing sheets or the assertions. Show me the
    whole file.
    ```

<div class="yours" markdown>
**Now with your own close.** Pick the single most repetitive thing in your
month-end. Not the hardest — the most repetitive.

Write the query. Wrap it in this script. Parameterise the period. Add the
tie-out. Run it for last month and reconcile the output to the pack you
produced by hand.

When they agree, you have replaced a recurring afternoon with a command. When
they disagree, you have found something, which is also a good day.
</div>

!!! warning "Gotcha"
    `params={"period": period}` with `text()` around the query is the pair.
    Use `text()` and forget the params and you get an error about a missing
    bind parameter; use plain string SQL with `params` and the placeholder
    syntax differs by driver. Keep them together.

!!! tip "Where the script lives"
    Put it in a folder with the `.venv`, and add a one-line README saying what
    it does, which database it reads and who to ask. Six months from now that
    file is the difference between a tool and a mystery.

---

**Go deeper:** [SQLAlchemy textual SQL and bound parameters](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#sending-parameters) ·
[pandas.ExcelWriter](https://pandas.pydata.org/docs/reference/api/pandas.ExcelWriter.html)

**Next:** [Lab 10 — SQL or Python?](10-sql-or-python.md)
