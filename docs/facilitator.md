---
hide:
  - navigation
---

# Facilitator notes

Answer keys and expected outputs. Don't hand this to participants before
they've tried.

!!! note "Claude's output will vary"
    The *numbers* below are fixed — they come from the data and are checkable.
    The wording, structure and framing of Claude's responses will differ every
    run. Judge on the figures, not on how closely the prose matches.

## Lab 4 — Messy P&L

Expected findings from the two checks:

- **Subtotals foot.** Every subtotal equals the sum of its components. If
  Claude reports a discrepancy here, it's parsed something wrong — most likely
  it read a parenthesised value as positive.
- **One duplicate row.** A second `Total Operating Expenses` row near the
  bottom, with no Q2 total in column F. It would double-count if you summed
  the column.

Formatting problems it should have handled: junk rows 1–5, split header rows
6–7, empty column C, parenthesised negatives, `224800.00 ` stored as text with
a trailing space, `$94,200` with a currency symbol, `  sales commissions `
with a trailing space, footer notes below the data.

## Lab 5 — Invoices

| Vendor | Invoice | Date | Terms | PO | Total |
|---|---|---|---|---|---|
| Cascade Logistics | CL-77412 | 2026-06-24 | Net 15 | — | 16,845.00 |
| Orion Software Ltd | ORN-INV-20260612 | 2026-06-12 | Due on receipt | PO-8855 | 17,040.00 |
| Meridian Staffing | MS-2026-06-B | 2026-06-23 | Net 7 | PO-8861 | 27,596.00 |
| Kestrel Legal LLP | KL-9920-06 | 2026-06-27 | Net 30 | — | 34,042.50 |
| Pacific Materials Supply | PMS-2026-3391 | 2026-06-16 | Net 30 | PO-8849 | 69,760.00 |
| | | | | **Total** | **165,283.50** |

Orion is the only one with tax: subtotal 14,200.00, VAT at 20% = 2,840.00.

Notes column should flag: no PO on Cascade and Kestrel; tax on Orion; Net 7 on
Meridian as unusually short; "due on receipt" on Orion.

## Lab 6 — Bank reconciliation

**The headline figures**

| | |
|---|---|
| Opening balance, both sides | 742,800.00 |
| Bank closing balance | 409,975.30 |
| Book closing balance | 404,768.00 |
| Difference | 5,207.30 |
| **Adjusted balance, both sides** | **415,735.30** |

**The eight items**

| # | Item | Amount | Side | Treatment |
|---|---|---|---|---|
| 1 | Deposit in transit — Fairlight Mercantile, INV-4502, 30 Jun | 12,400.00 | Book only | Add to bank |
| 2 | Outstanding cheque #10485 — Kestrel Legal | 4,750.00 | Book only | Deduct from bank |
| 3 | Outstanding cheque #10486 — Delta Freight | 1,890.00 | Book only | Deduct from bank |
| 4 | Interest credit, 30 Jun | 142.30 | Bank only | Add to book |
| 5 | Monthly service charge, 30 Jun | 85.00 | Bank only | Deduct from book |
| 6 | Returned item NSF — Eastvale Distribution, 21 Jun | 3,200.00 | Bank only | Deduct from book |
| 7 | Duplicate posting — cheque #10476 Orion, JE-2610 and JE-2611 | 14,200.00 | Book error | Add back to book |
| 8 | Transposition — cheque #10478 Summit, bank 1,542.00 vs book 1,452.00 | 90.00 | Book error | Deduct from book |

**Proof**

```text
Bank   409,975.30 + 12,400.00 - 4,750.00 - 1,890.00            = 415,735.30
Book   404,768.00 + 142.30 - 85.00 - 3,200.00 + 14,200.00 - 90 = 415,735.30
```

Items 1–3 are timing and need no entry. Items 4–8 all need a journal entry.

**What to draw out.** Item 6 is a live receivable that came back and nobody was
chasing. Item 7 made cash look 14,200 worse than it was. Item 8 is the one
people miss by eye, because 90 dollars looks like nothing — and it's exactly
the size of error a transposition produces.

## Lab 7 — Variance memo

| | Budget | Actual | Variance |
|---|---|---|---|
| Total Q2 opex | 1,571,700.00 | 1,606,810.05 | +35,110.05 (+2.2%) |

Drivers:

| Month | Department | Account | Budget | Actual | Variance |
|---|---|---|---|---|---|
| Jun | Engineering | Contract Labor | 14,900 | 46,190 | +31,290 (+210%) |
| Jun | G&A | Professional Fees | 2,100 | 9,240 | +7,140 (+340%) |
| May | Marketing | Marketing Programs | 7,300 | 13,870 | +6,570 (+90%) |

Largest favourable: Sales contract labour April (−6,696), Operations travel
June (−3,510).

**The point to land:** those three drivers total 44,999 against a net overspend
of 35,110. Everything else came in under budget. "Three lines explain more than
the entire variance" is a far better opening than "opex was 2.2% over" — and
noticing that is the difference between analysis and reporting.

## Lab 11 — The trap

The file has no **Logistics** department. Departments are Sales, Marketing,
Operations, Engineering, G&A, Customer Success.

Good behaviour: Claude says there's no such department and lists what exists.
Less good: it silently answers about Operations, or hedges in a way that's easy
to skim past.

Either outcome teaches the lesson — the tone of the answer told you nothing
about which one you got. If the room gets the good behaviour, point out that
they only know that *because they knew the answer*.

Checkable totals for the tie-out exercise: **129 rows**, actuals total
**1,606,810.05**.

## Timing, observed

| Lab | Realistic |
|---|---|
| 1–3 | 10 min each, faster if the room is confident |
| 4 | 15–20 — first Cowork run, expect setup friction |
| 5 | 10 |
| 6 | 15–25 — let them struggle, it's worth it |
| 7 | 12 |
| 8 | 15–20 — first skill, expect zip-structure mistakes |
| 9 | 10, plus however long they argue about house style |
| 10 | 10 |
| 11–12 | 10 each, mostly discussion |

Labs 4 and 6 always overrun. Plan for it by cutting 9 rather than rushing them.
