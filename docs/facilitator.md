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

## Finance Track

### Lab 4 — Messy P&L

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

### Lab 5 — Invoices

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

### Lab 6 — Bank reconciliation

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

### Lab 7 — Variance memo

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

**The point to land:** those three drivers total 45,000 against a net overspend
of 35,110. Everything else came in under budget. "Three lines explain more than
the entire variance" is a far better opening than "opex was 2.2% over" — and
noticing that is the difference between analysis and reporting.

### Lab 11 — The trap

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

## Data Track

### Lab 2 — the load

| | |
|---|---|
| Setup script prints | `northwind is ready  10  34  30` |
| Rows imported into `budget_actual_raw` | **129** |
| Total budget | **1,571,700.00** |
| Total actual | **1,606,810.05** |

128 rows means the header was skipped twice or a line was dropped. 130 means
the header came in as data. Totals out by a round-ish amount usually means a
column mapped to the wrong field in the Workbench wizard.

### Lab 3 — first queries

`COUNT(*)` 34, `SUM(amount)` 1,096,352.29. The `90+` bucket is 4 invoices
totalling 116,829.32. Top five by amount: INV-4387, INV-4397, INV-4406,
INV-4462, INV-4435.

### Lab 4 — grouping

Aging: Current 19 / 665,109.08; 31-60 9 / 255,969.98; 90+ 4 / 116,829.32;
61-90 2 / 58,443.91.

Departmental variance ties to the finance track's Lab 7 exactly —
1,571,700.00 against 1,606,810.05, +35,110.05, +2.2%.

**The `HAVING` exercise returns two rows and only one is a finding.**

| Reference | Times | Total | Verdict |
|---|---|---|---|
| CHK10476 | 2 | 28,400.00 | The duplicate. Orion Software licence posted twice, 14,200.00 each. |
| ACH | 3 | 283,980.00 | Fine. Two payrolls and a card settlement sharing a generic reference. |

Draw this out — most rooms report both as duplicates. The point is that a
duplicate-detector produces candidates, not findings.

### Lab 5 — normalising

Six departments, eight accounts, 129 rows in `budget_actual`, totals unchanged
from Lab 2. If the row count falls, a join found no match; that's the Lab 6
lesson arriving early and it's worth stopping on.

Over credit limit, exactly three:

| Customer | Limit | Owed | Over by |
|---|---|---|---|
| Dunmore Wholesale | 150,000.00 | 221,230.18 | 71,230.18 |
| Ironwood Partners | 100,000.00 | 122,398.43 | 22,398.43 |
| Copperfield & Sons | 100,000.00 | 115,141.15 | 15,141.15 |

### Lab 6 — the three traps

| Check | Answer |
|---|---|
| `SUM(amount)` on invoices | 1,096,352.29 |
| Same via `JOIN customers` | 1,074,341.36 |
| Difference | 22,010.93 — invoice **INV-4391**, bucket 90+ |
| 90+ all invoices / via `JOIN` | 116,829.32 / 94,818.39 |
| `region IS NULL` | 2 |
| `region IS NULL OR region = ''` | 3 |
| `COUNT(*)` / `COUNT(region)` | 10 / 8 |

**What to land.** The join query is not wrong in any way a reviewer would spot.
It reads correctly, runs without warning, and returns a well-formed number that
is 2% light — and the 2% is concentrated entirely in the oldest bucket, which
is the one that drives collections. Run Lab 5's exposure query without its
`HAVING` line and Brightwater Industries shows 75,142.15 against a true
97,153.08 — 23% light. It changes no decision there, because their limit is
150,000 either way, and that's the point worth making: the same silent gap
mattered on one report and not on the other, and nothing in either output
said which.

If somebody asks "so should we always use LEFT JOIN" — no. The fix is the
control total, not a blanket rule.

### Labs 7–9 — Python

Lab 7 output is the Lab 4 aging table plus a TOTAL line of 34 /
1,096,352.29.

Lab 8 prints:

```text
Detail ties to 1,096,352.29 across 34 invoices
By-customer total is 1,074,341.36, which is 22,010.93 light. Lab 6 explains why.
```

The float demonstration is real and reproducible:
`detail["amount"].sum()` is `1096352.2899999998`. Have someone run it. The
assertion fails without the `round(..., 2)`, on data that is entirely correct.
This is the moment the "do money arithmetic in SQL" rule stops being advice.

Lab 9 output:

```text
2026-04: 43 lines, budget   523,900.00, actual   519,481.77, variance   -4,418.23
2026-05: 43 lines, budget   523,900.00, actual   527,482.17, variance    3,582.17
2026-06: 43 lines, budget   523,900.00, actual   559,846.11, variance   35,946.11
```

June's top two variances (Engineering contract labour +31,290, G&A
professional fees +7,140) total 38,430 against a 35,946 monthly overspend —
the same "two lines explain more than the whole variance" point the finance
track makes from the CSV.

### Lab 10 — the sorting exercise

1 SQL · 2 Python wrapping SQL · 3 SQL · 4 Python · 5 Python with the
aggregation in SQL.

The disagreement worth having is 2 and 5, where people split on whether "it
uses Python" means "it's a Python job". It doesn't — the query is still the
core in both.

## Timing, observed

### Finance track

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

### Data track

| Lab | Realistic |
|---|---|
| 1 | 20–30 — installs, and someone's laptop will fight back |
| 2 | 15–25 — PATH and `local_infile` are where the time goes |
| 3–4 | 12 each if they type rather than paste, which they should |
| 5 | 20 — the concepts land slower than the syntax |
| 6 | 15–20, and it's the one to protect |
| 7 | 20 — second round of installs |
| 8–9 | 15 each |
| 10 | 10, mostly discussion |

Run the two install labs as pre-work if you possibly can. An hour of a
session spent watching downloads is an hour nobody learns anything. If they
must be done live, have the download links open before people arrive.
