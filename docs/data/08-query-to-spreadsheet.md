# Lab 8 — Turn a query into a spreadsheet

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Terminal</span>
  <span>File: ar_report.py</span>
</div>

## The problem

Nobody wants a query result. They want an AR report with a summary tab and a
detail tab, in a file they can open.

Getting from one to the other by hand — run query, copy grid, paste into
Excel, format, repeat for the second tab — takes fifteen minutes and gets done
wrong roughly once a quarter. It's also the single most automatable thing in
the finance calendar.

## Before you start

- [ ] Lab 7 done and `first_query.py` ran
- [ ] Virtual environment active — your prompt starts with `(.venv)`

## Do this

### 1. Install three more packages

```bash
pip install pandas sqlalchemy openpyxl
```

- **pandas** holds query results as a table you can reshape
- **SQLAlchemy** is what pandas wants a connection to look like
- **openpyxl** is what writes the `.xlsx`

### 2. Why SQLAlchemy is in that list

Hand pandas your `mysql.connector` connection directly and it works, but says:

```text
UserWarning: pandas only supports SQLAlchemy connectable (engine/connection)
or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are
not tested. Please consider using SQLAlchemy.
```

"Not tested" is doing a lot of work in that sentence. Wrap the connection in a
SQLAlchemy engine and the warning goes away:

```python
engine = create_engine("mysql+mysqlconnector://root:PASSWORD@127.0.0.1/northwind")
```

Same driver underneath. One line.

### 3. Build the report

Download [`ar_report.py`](../files/db/ar_report.py) and run it.

```python title="ar_report.py"
import getpass
import os

import pandas as pd
from sqlalchemy import create_engine

PASSWORD = os.environ.get("MYSQL_PASSWORD") or getpass.getpass("MySQL password: ")

engine = create_engine(f"mysql+mysqlconnector://root:{PASSWORD}@127.0.0.1/northwind")

BY_CUSTOMER = """
    SELECT c.customer_name     AS customer,
           c.account_manager   AS manager,
           c.credit_limit      AS credit_limit,
           COUNT(i.invoice_no) AS open_invoices,
           SUM(i.amount)       AS owed
    FROM customers c
    JOIN invoices  i ON i.customer_id = c.customer_id
    GROUP BY c.customer_name, c.account_manager, c.credit_limit
    ORDER BY owed DESC
"""

DETAIL = """
    SELECT i.invoice_no, i.invoice_date, i.due_date, i.days_past_due,
           i.aging_bucket, i.amount,
           COALESCE(c.customer_name, '*** NO CUSTOMER RECORD ***') AS customer
    FROM invoices i
    LEFT JOIN customers c ON c.customer_id = i.customer_id
    ORDER BY i.days_past_due DESC, i.amount DESC
"""

# The control total, computed in SQL where DECIMAL arithmetic is exact.
CONTROL = "SELECT ROUND(SUM(amount), 2) FROM invoices"

with engine.connect() as cnx:
    by_customer = pd.read_sql(BY_CUSTOMER, cnx)
    detail = pd.read_sql(DETAIL, cnx)
    control = float(pd.read_sql(CONTROL, cnx).iloc[0, 0])

# Tie the report back to the source before writing anything.
# round() is not optional - pandas turned DECIMAL into float on the way in.
detail_total = round(detail["amount"].sum(), 2)
assert detail_total == control, f"detail does not tie: {detail_total} vs {control}"
print(f"Detail ties to {detail_total:,.2f} across {len(detail)} invoices")

customer_total = round(by_customer["owed"].sum(), 2)
print(f"By-customer total is {customer_total:,.2f}, "
      f"which is {round(control - customer_total, 2):,.2f} light. Lab 6 explains why.")

by_customer["over_limit_by"] = (by_customer["owed"]
                                - by_customer["credit_limit"]).clip(lower=0).round(2)

with pd.ExcelWriter("ar-report.xlsx", engine="openpyxl") as xl:
    by_customer.to_excel(xl, sheet_name="By customer", index=False)
    detail.to_excel(xl, sheet_name="Detail", index=False)

print("Wrote ar-report.xlsx")
```

```bash
python ar_report.py
```

## What good looks like

```text
Detail ties to 1,096,352.29 across 34 invoices
By-customer total is 1,074,341.36, which is 22,010.93 light. Lab 6 explains why.
Wrote ar-report.xlsx
```

Open `ar-report.xlsx`. Two sheets. On **Detail**, sorted by days past due, the
second row is `*** NO CUSTOMER RECORD ***` — Lab 6's orphan invoice, now
impossible to miss because the `LEFT JOIN` and the `COALESCE` were written to
surface it rather than swallow it.

**By customer** starts:

| Customer | Manager | Credit limit | Open invoices | Owed | Over limit by |
|---|---|---|---|---|---|
| Dunmore Wholesale | M. Okafor | 150,000 | 5 | 221,230.18 | 71,230.18 |
| Ironwood Partners | S. K. Rao | 100,000 | 6 | 122,398.43 | 22,398.43 |
| Copperfield & Sons | M. Okafor | 100,000 | 3 | 115,141.15 | 15,141.15 |

## The bit accountants need to read twice

Try this in Python:

```python
print(repr(detail["amount"].sum()))
```

```text
np.float64(1096352.2899999998)
```

MySQL stored those amounts as `DECIMAL`, which is exact. pandas read them in
as **floating point**, which is not — it's binary approximation, and it cannot
represent 0.29 precisely any more than decimal can represent a third.

The gap is far too small to have a name in money — it's in the tenth decimal
place. That isn't the problem. The problem is that `detail_total == control`
was `False` until the `round(..., 2)` went in, so your tie-out would have
failed on data that was perfectly fine.

Two rules follow, and they're most of Lab 10:

1. **Do money arithmetic in SQL.** `SUM`, `ROUND` and the variance calculation
   belong in the query, where `DECIMAL` is exact.
2. **If you must add money in pandas, round explicitly** before comparing
   anything to anything.

## Making it your report

!!! example prompt "Copy this prompt"

    ```text
    Here's a Python script that runs two MySQL queries and writes
    them to an Excel file with pandas:

    [paste ar_report.py]

    Change it so the output actually looks like a finance deliverable:
    - Currency format with thousands separators on the money columns
    - Dates as dd/mm/yyyy
    - Bold header row, frozen top row, columns wide enough to read
    - A totals row at the bottom of each sheet

    Use openpyxl. Keep the tie-out assertion exactly where it is and
    explain any change you make to it.

    Show me the whole file, not a diff.
    ```

"Keep the tie-out exactly where it is" is deliberate. Ask for a rewrite and
the check is the first thing that quietly gets dropped.

<div class="yours" markdown>
**Now build the report you produce by hand.** Pick the one you rebuild every
month — the aging, the accruals schedule, the cost-centre pack.

Write its query first and get it right in SQL. Then wrap it in this script:
same shape, your query, your filename. Then add the tie-out, and make it an
`assert` rather than a `print` so a bad month stops the script instead of
producing a file.

The first one takes an afternoon. The second one takes twenty minutes.
</div>

!!! warning "Gotcha"
    `ModuleNotFoundError: No module named 'openpyxl'` at the `to_excel` line,
    not at the top of the script. pandas only looks for the Excel writer when
    it's about to write. `pip install openpyxl` — and check your virtual
    environment is active, because installing it into the wrong one is the
    usual cause.

!!! danger "An assertion is not a comment"
    `assert detail_total == control` stops the script dead when it fails. That
    is the feature. A report that refuses to be produced is annoying for ten
    minutes; a report that's produced wrong is annoying for a quarter.

---

**Go deeper:** [pandas.read_sql](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html) ·
[SQLAlchemy engines](https://docs.sqlalchemy.org/en/20/core/engines.html)

**Next:** [Lab 9 — The month-end pack, as a script you rerun](09-month-end-script.md)
