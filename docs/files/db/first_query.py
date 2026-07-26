"""Claude Labs - Data Track, Lab 7. Ask MySQL a question from Python."""

import getpass
import os

import mysql.connector

PASSWORD = os.environ.get("MYSQL_PASSWORD") or getpass.getpass("MySQL password: ")

cnx = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=PASSWORD,
    database="northwind",
)

QUERY = """
    SELECT aging_bucket,
           COUNT(*)    AS invoices,
           SUM(amount) AS total
    FROM invoices
    GROUP BY aging_bucket
    ORDER BY total DESC
"""

with cnx.cursor() as cur:
    cur.execute(QUERY)
    print(f"{'Bucket':<10}{'Invoices':>10}{'Total':>16}")
    for bucket, invoices, total in cur.fetchall():
        print(f"{bucket:<10}{invoices:>10}{total:>16,.2f}")

    cur.execute("SELECT COUNT(*), SUM(amount) FROM invoices")
    n, grand = cur.fetchone()
    print(f"{'TOTAL':<10}{n:>10}{grand:>16,.2f}")

cnx.close()
