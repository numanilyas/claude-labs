# Lab 11 — Verify before you send

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Chat</span>
  <span>File: budget-vs-actual-q2-fy26.csv</span>
</div>

## The problem

Everything up to here made you faster. This lab is the one that keeps the speed
from costing you.

Claude is confident in the same tone whether it's right or wrong. That's not a
flaw you can prompt away — it's a property you have to build a habit around.
In finance the cost of a plausible wrong number is not "a bit of rework". It's
a restated report.

## Exercise 1 — watch it happen

Attach `budget-vs-actual-q2-fy26.csv` to a new chat and ask:

!!! example prompt "Copy this prompt"

    ```text
    How did the Logistics department perform against budget in Q2?
    ```

There is no Logistics department in that file. The departments are Sales,
Marketing, Operations, Engineering, G&A and Customer Success.

**What should happen:** Claude tells you there's no such department and lists
what's actually there.

**What sometimes happens:** it finds the nearest thing — Operations — and
answers about that without flagging the substitution clearly. Or it hedges in a
way that's easy to skim past.

Either way, notice how *little* the answer's tone told you about which one you
got. That's the entire lesson.

## Exercise 2 — the three moves

Ask a real question, then run all three checks. They take ninety seconds
together.

!!! example prompt "Move 1 — show the source"

    ```text
    Show me the exact rows from the file behind that number, and tell
    me how many rows you read in total.
    ```

If it can't produce them, the number isn't real. This catches the most
dangerous failure — a figure that was inferred rather than computed.

!!! example prompt "Move 2 — re-derive independently"

    ```text
    Recompute that a different way, without referring to your previous
    answer, and tell me if the two results differ.
    ```

Two independent derivations agreeing is meaningfully stronger evidence than one
derivation asserted twice.

!!! example prompt "Move 3 — tie to something you already know"

    ```text
    What's the total of the Actual column across all 129 rows? I'll
    check that against my own figure.
    ```

You know the file has 129 rows and the actuals total 1,606,810.05. In real
life you always have *something* you already know — a trial balance total, a
headcount, last month's closing. Tie to it.

## Build it into the prompt

Better than checking afterwards is asking for the checks up front. Add this
block to anything that produces numbers you'll act on:

!!! example prompt "The tie-out block — keep this one"

    ```text
    Before you give me the answer:
    - Compute with code, not estimation
    - State the number of rows you processed and any you excluded, and
      why
    - Reconcile your totals back to the source file totals and show me
      both figures
    - End with a section headed "What I could not verify" listing
      anything you assumed, inferred, or worked around

    If that last section would be empty, say so explicitly rather than
    omitting the heading.
    ```

That last instruction matters. An empty section is a claim. A missing section
is silence, and silence reads as "nothing to report" when it might mean "I
forgot to check."

## What good looks like

A habit, not an output. By the end of this lab you should find yourself
uncomfortable sending a Claude-derived number that you haven't tied to
something.

<div class="yours" markdown>
**Now on something real.** Take a number Claude produced for you this week and
run the three moves on it.

If you find an error, that's the lab working. If you don't, you've spent ninety
seconds buying the right to say "yes, I checked" when someone asks.
</div>

!!! danger "The rule"
    **If you can't verify it, don't send it.** Not "don't send it without a
    caveat" — don't send it. A caveat transfers the risk to a reader who
    trusts you more than you trusted the output.

!!! tip "Where errors actually cluster"
    Not in the arithmetic — code doesn't make addition mistakes. They cluster
    in **interpretation**: which rows counted as "Q2", whether a blank meant
    zero or unknown, whether "Ops" and "Operations" got merged, which sign
    convention applied. Ask *"what did you have to decide in order to answer
    this?"* — it's the highest-yield verification question there is.

---

**Next:** [Lab 12 — What not to paste into Claude](12-what-not-to-paste.md)
