# Lab 7 — Variances into a memo

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Cowork</span>
  <span>File: budget-vs-actual-q2-fy26.csv</span>
</div>

## The problem

You have the variance analysis. What you're actually asked for is four
paragraphs your CFO can put in front of a board, written in a register that
isn't spreadsheet.

The gap between "I know what happened" and "I've written it up" is where most
of the month-end evening goes.

## Before you start

- [ ] [`budget-vs-actual-q2-fy26.csv`](../files/budget-vs-actual-q2-fy26.csv) in your folder
- [ ] Cowork open, folder connected

## Do this

!!! example prompt "Copy this prompt"

    ```text
    budget-vs-actual-q2-fy26.csv has Q2 opex by month, department and
    account.

    Write me a variance memo as q2-variance-memo.docx, addressed to the
    CFO, from the controller. Structure:

    - One opening paragraph: total budget, total actual, variance in
      dollars and percent, and a one-sentence verdict
    - A short table of the drivers that explain the variance
    - One paragraph per driver: what it is, how much, and the most
      likely explanation given this is a mid-size distribution business
    - A closing section headed "To confirm before this is final"
      listing what I need to check with department heads

    Rules:
    - Under one page
    - Plain professional English. No filler, no "it is important to
      note", no restating the numbers in prose after the table
    - Where you're inferring a cause rather than reading it from the
      data, mark the sentence with [inferred]
    - Favourable variances get one sentence total, not a paragraph each

    Before you write it, show me the driver table and let me confirm
    the numbers.
    ```

Check the table it shows you, *then* let it write.

## What good looks like

The numbers should come out here:

| | Budget | Actual | Variance |
|---|---|---|---|
| **Total Q2 opex** | 1,571,700 | 1,606,810 | **+35,110 (+2.2%)** |

Three drivers, all of which should be in its table:

| Month | Department | Account | Variance |
|---|---|---|---|
| Jun | Engineering | Contract Labor | +31,290 (+210%) |
| Jun | G&A | Professional Fees | +7,140 (+340%) |
| May | Marketing | Marketing Programs | +6,570 (+90%) |

Partly offset by underspend in Sales contract labour (April, −6,696) and
Operations travel (June, −3,510).

The interesting line for the memo: **those three drivers total 44,999 — more
than the entire 35,110 overspend.** Everything else in the business came in
under. That's a much better opening sentence than "opex was 2.2% over."

The `[inferred]` markers should be on the causal claims. There is nothing in
this file that says *why* Engineering contract labour tripled — Claude will
suggest something plausible, and it should be honest that it's guessing.

!!! tip "Confirm the table before the prose"
    That one instruction — *show me the table first, then write* — is worth
    keeping in every prompt like this. If the numbers are wrong, you find out
    before you've read a page of well-written commentary built on them. Wrong
    numbers in fluent prose are much harder to spot than wrong numbers in a
    table.

## Want a deck instead?

Same prompt, different last line:

!!! example prompt "Deck variant"

    ```text
    Same analysis, but give me q2-variance.pptx instead: a title slide,
    one slide with the driver table, one slide per driver with the
    number as the headline and three bullets under it, and a final
    slide of open questions. No clip art, no gradient backgrounds.
    ```

<div class="yours" markdown>
**Now with your own numbers.** Your real budget-to-actual, your real reporting
line.

Then do the thing that makes this stick: **paste in last quarter's memo** that
you wrote by hand and say *"match this tone and structure."* The output goes
from generically competent to recognisably yours, and that's the version
people will accept.

Hold on to whichever prompt works. You're going to turn it into a skill in the
next lab.
</div>

!!! warning "Gotcha"
    Claude will write confident causal explanations if you let it. "The
    increase reflects accelerated hiring to support the platform migration" is
    a sentence about a platform migration that may not exist. The `[inferred]`
    convention exists so you can see the seams — don't drop it just because
    the output looks cleaner without it.

---

**Next:** [Lab 8 — Your first skill](08-your-first-skill.md)
