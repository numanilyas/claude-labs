---
hide:
  - navigation
---

# Sample data

Everything here is invented. **Northwind Trading Co.** doesn't exist, Meridian
Commerce Bank doesn't exist, and none of the vendors or customers are real
companies. Use it freely.

The files are also deliberately imperfect. A clean file teaches you nothing —
the whole point is to practise on data that fights back.

[:octicons-download-24: Download everything (one zip)](files/claude-labs-sample-data.zip){ .md-button .md-button--primary }

Unzip it into a folder called `claude-labs` somewhere you can find it. You'll
connect that folder to Cowork in Lab 4.

## The files

<div class="dl" markdown>

### [messy-pl-q2-fy26.xlsx](files/messy-pl-q2-fy26.xlsx)

Q2 P&L, as exported by a system that hates you. Used in **Lab 4**.

What's wrong with it, deliberately:

- Four rows of junk above the real header
- The header split across two rows
- An entirely empty phantom column in the middle
- Negative numbers stored as text in parentheses: `(48,200)`
- One row stored as text with a trailing space: `224800.00 `
- One row with a currency symbol baked into the value: `$94,200`
- Inconsistent account labels — trailing spaces, mixed case
- A duplicated `Total Operating Expenses` row pasted in near the bottom
- Explanatory notes below the data that would break any import

The subtotals do all foot correctly. The duplicate row is the trap.

---

### [bank-statement-june-2026.pdf](files/bank-statement-june-2026.pdf) + [general-ledger-june-2026.csv](files/general-ledger-june-2026.csv)

June 2026, same cash account, two sources that don't agree. Used in **Lab 6**.

| | |
|---|---|
| Opening balance, both sides | 742,800.00 |
| Bank closing balance | 409,975.30 |
| Book closing balance | 404,768.00 |
| **Adjusted balance, both sides** | **415,735.30** |

There are eight reconciling items and they're findable. The full list is in
the [facilitator notes](facilitator.md) — don't read it before you've tried.

---

### [invoices.zip](files/invoices.zip)

Five vendor invoices as PDFs, five different layouts. Used in **Lab 5**.
Grand total **165,283.50**.

Between them they cover: an international supplier with VAT, two invoices with
no PO number, one with unusually short terms, and three different billing bases
(per hour, per shipment, per lot).

!!! note "These don't tie to the bank and ledger"
    The invoice pack shares vendor names with the June cash data because it's
    the same fictional company, but the amounts aren't meant to reconcile to
    June payments. Don't send anyone hunting for a match that isn't there.

---

### [budget-vs-actual-q2-fy26.csv](files/budget-vs-actual-q2-fy26.csv)

129 rows. Q2 opex by month, department and account. Used in **Labs 2, 3, 7
and 11**.

| | |
|---|---|
| Total budget | 1,571,700.00 |
| Total actual | 1,606,810.05 |
| Variance | +35,110.05 (+2.2%) |

Three planted drivers explain more than the whole overspend, offset by
underspend elsewhere. Departments are Sales, Marketing, Operations,
Engineering, G&A and Customer Success — note there is **no Logistics
department**, which is the trap in Lab 11.

---

### [ar-aging-june-2026.csv](files/ar-aging-june-2026.csv)

34 open invoices across 10 customers, aged at 30 June 2026. Total
**1,096,352.29**, of which **116,829.32** is over 90 days. Spare data for
Lab 10 and for your own experiments.

</div>

## Regenerating it

The data is produced by `build_data.py` in the repository root. If you want
different numbers, a different company name, or more transactions:

```bash
pip install openpyxl reportlab
python build_data.py
```

The script asserts that the bank reconciliation balances before it writes
anything, so it fails loudly rather than shipping a broken exercise.
