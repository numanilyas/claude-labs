"""Claude Labs - Data Track, Lab 9. The month-end variance pack, as a script.

    python month_end.py 2026-06
    python month_end.py            # every period in the database
"""

import getpass
import os
import sys

import pandas as pd
from sqlalchemy import create_engine, text

PASSWORD = os.environ.get("MYSQL_PASSWORD") or getpass.getpass("MySQL password: ")
engine = create_engine(f"mysql+mysqlconnector://root:{PASSWORD}@127.0.0.1/northwind")

SUMMARY = text("""
    SELECT d.dept_name                        AS department,
           SUM(b.budget)                      AS budget,
           SUM(b.actual)                      AS actual,
           SUM(b.actual) - SUM(b.budget)      AS variance
    FROM budget_actual b
    JOIN departments  d ON d.dept_id = b.dept_id
    WHERE b.period = :period
    GROUP BY d.dept_name
    ORDER BY variance DESC
""")

DETAIL = text("""
    SELECT d.dept_name   AS department,
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
    SELECT COUNT(*)                       AS lines_,
           ROUND(SUM(budget), 2)          AS budget,
           ROUND(SUM(actual), 2)          AS actual
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
