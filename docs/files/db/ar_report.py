"""Claude Labs - Data Track, Lab 8. Query -> formatted spreadsheet."""

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
