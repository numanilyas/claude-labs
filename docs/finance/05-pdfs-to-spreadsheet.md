# Lab 5 — Five PDFs into one spreadsheet

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Cowork</span>
  <span>Files: invoices/ (5 PDFs)</span>
</div>

## The problem

Five vendor invoices, five different layouts. One is from a UK supplier and
carries VAT. Two have no PO number. One bills in hours, one bills in lots, one
bills per shipment. You need them in a single schedule with consistent columns.

Doing this by hand is twenty minutes of retyping and one transposition error
you won't find until the vendor calls.

## Before you start

- [ ] Download [`invoices.zip`](../files/invoices.zip) and unzip it into your
      `claude-labs` folder, so you have a `claude-labs/invoices/` folder with
      five PDFs
- [ ] Cowork open, folder connected

## Do this

!!! example prompt "Copy this prompt"

    ```text
    The invoices folder has five vendor invoices as PDFs, all in
    different formats.

    Build me an AP schedule as accounts-payable-schedule.xlsx with one
    row per invoice and these columns: Vendor, Invoice Number, Invoice
    Date, Terms, Due Date, PO Number, Currency, Subtotal, Tax, Total.

    Rules:
    - If a field isn't on the invoice, leave the cell empty and don't
      guess
    - Add a Notes column flagging anything I should look at: missing PO,
      tax charged, terms shorter than net 30, anything unusual
    - Sort by due date, soonest first
    - Add a total row using a real SUM formula

    Then tell me the grand total and confirm each invoice's Subtotal
    plus Tax equals its Total. If any invoice doesn't foot, say which.
    ```

## What good looks like

Five rows plus a total. Check these against your output:

| Vendor | Invoice | Total |
|---|---|---|
| Cascade Logistics | CL-77412 | 16,845.00 |
| Orion Software Ltd | ORN-INV-20260612 | 17,040.00 |
| Meridian Staffing | MS-2026-06-B | 27,596.00 |
| Kestrel Legal LLP | KL-9920-06 | 34,042.50 |
| Pacific Materials Supply | PMS-2026-3391 | 69,760.00 |
| | **Grand total** | **165,283.50** |

The Notes column should have flagged:

- **Cascade Logistics** and **Kestrel Legal** — no PO number
- **Orion Software** — the only invoice with tax (20% VAT, £/GBP supplier), and
  terms of "due on receipt"
- **Meridian Staffing** — Net 7, unusually short

Every invoice should foot. If Claude says one doesn't, check it by hand before
you believe it — that's the correct instinct and it's what Lab 11 is about.

!!! tip "Why the total row matters"
    Asking for "a real SUM formula, not a hardcoded number" is a small phrase
    with a large effect. A hardcoded total is right once. A formula stays right
    when you add a sixth invoice.

<div class="yours" markdown>
**Now with your own documents.** Drop a folder of real invoices, receipts,
statements, or remittance advices somewhere Cowork can see and run the same
shape of prompt.

The two clauses worth keeping every time:

- *"If a field isn't there, leave it empty and don't guess"* — otherwise you
  get plausible invented PO numbers
- *"Add a Notes column flagging anything I should look at"* — this is where
  the value is. Extraction is table stakes; the exceptions are the work.
</div>

!!! warning "Gotcha"
    Scanned or photographed invoices are much harder than digital PDFs. If your
    real ones are scans, expect to spot-check every figure rather than a sample.
    Say *"these are scans, flag anything you're less than confident about"* and
    it will tell you where to look.

---

**Next:** [Lab 6 — Reconcile a bank statement](06-reconciliation.md)
