# Lab 6 — Reconcile a bank statement

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Cowork</span>
  <span>Files: bank statement PDF + GL CSV</span>
</div>

## The problem

A bank statement in PDF and a cash ledger in CSV. They don't agree. Somewhere
in there are a deposit that hasn't cleared, cheques nobody's cashed, fees the
bank took without asking, a customer payment that bounced, an entry someone
posted twice, and a transposed figure.

Finding those by eye takes an hour and you'll miss the transposition, because
90 dollars looks like nothing.

## Before you start

- [ ] [`bank-statement-june-2026.pdf`](../files/bank-statement-june-2026.pdf) in your folder
- [ ] [`general-ledger-june-2026.csv`](../files/general-ledger-june-2026.csv) in your folder
- [ ] Cowork open, folder connected

## Do this

!!! example prompt "Copy this prompt"

    ```text
    Two files in the folder: bank-statement-june-2026.pdf and
    general-ledger-june-2026.csv. Both cover June 2026 for the same
    cash account. Opening balance at 1 June was 742,800.00 on both
    sides.

    Do a bank reconciliation and give me reconciliation-june-2026.xlsx
    with four tabs:

    1. Summary - the classic format. Bank closing balance, plus deposits
       in transit, less outstanding cheques, to get adjusted bank
       balance. Then book closing balance, adjusted for items the bank
       knows about and we don't, plus any errors on our side, to get
       adjusted book balance. The two adjusted figures must agree.
    2. Matched - transactions that tie on both sides
    3. Exceptions - every unmatched or mismatched item, one per row,
       with which side it's on, the amount, and what you think it is
    4. Source data - both files as you parsed them, so I can audit you

    Match on amount, date and reference, and allow a few days of
    timing difference. Watch for the same item posted twice on one
    side, and for amounts that are close but not equal.

    When you're done, tell me in plain English what each reconciling
    item is and what I need to do about it.
    ```

## What good looks like

The headline figures, so you can check yourself:

| | |
|---|---|
| Bank closing balance | 409,975.30 |
| Book (GL) closing balance | 404,768.00 |
| Unreconciled difference | 5,207.30 |
| **Adjusted balance, both sides** | **415,735.30** |

If your adjusted figures don't both land on **415,735.30**, the reconciliation
isn't finished. That's the whole test.

There are **eight** reconciling items. Try to get all eight before you open
this.

??? note "The eight items — open after you've tried"

    **Timing — nothing wrong, just hasn't happened yet**

    1. **Deposit in transit, 12,400.00.** Fairlight Mercantile, INV-4502,
       booked 30 June, hits the bank in July. *Add to the bank side.*
    2. **Outstanding cheque #10485, 4,750.00.** Kestrel Legal.
       *Deduct from the bank side.*
    3. **Outstanding cheque #10486, 1,890.00.** Delta Freight Services.
       *Deduct from the bank side.*

    **The bank knows something we don't**

    4. **Interest credit, 142.30.** Never posted. *Add to the book side.*
    5. **Monthly service charge, 85.00.** Never posted. *Deduct from the
       book side.*
    6. **Returned item — NSF, 3,200.00.** Eastvale Distribution's payment
       bounced on 21 June. *Deduct from the book side.* This one isn't
       housekeeping — it's a live receivable that's come back, and
       somebody needs to chase it.

    **We made mistakes**

    7. **Duplicate posting, 14,200.00.** Cheque #10476 to Orion Software
       is in the ledger twice, JE-2610 and JE-2611, the second flagged
       "re-posted". Cash is understated. *Add back to the book side.*
    8. **Transposition, 90.00.** Cheque #10478 to Summit Office Supply
       cleared the bank at 1,542.00; the ledger says 1,452.00.
       *Deduct 90.00 from the book side.*

    Four of these need a journal entry (4, 5, 6, 7, 8 — five, in fact).
    Three are pure timing and need nothing but a note.

## The part that matters

Look at what the exercise actually surfaced. A bounced customer payment for
3,200 that nobody was chasing, and a 14,200 duplicate that made cash look worse
than it was. Neither is a reconciliation problem. Both are business problems
that the reconciliation happened to catch.

That's the argument for doing this monthly rather than quarterly, and it's the
argument for automating it — which is Lab 10.

<div class="yours" markdown>
**Now with your own accounts.** Same prompt, your statement and your ledger.
Start with a small account — petty cash, a card account, a subsidiary's bank —
before you point it at the main operating account.

Keep the **Source data** tab. It's the difference between a tool you can defend
in an audit and a black box that produced a number.
</div>

!!! warning "Gotcha"
    Claude will occasionally match two items that a human wouldn't, especially
    where amounts repeat — recurring rent, identical payroll runs. The
    Exceptions tab is where you look, but the Matched tab is where the quiet
    errors hide. Scan it once.

!!! danger "Don't skip the tie-out"
    If the two adjusted balances agree, the reconciliation is arithmetically
    complete. That is *not* the same as correct — both sides can agree on a
    wrong classification. Read the exception list yourself. Every time.

---

**Next:** [Lab 7 — Variances into a memo](07-variance-memo.md)
