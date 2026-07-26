# Lab 2 — Give Claude your data

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Chat</span>
  <span>File: budget-vs-actual-q2-fy26.csv</span>
</div>

## The problem

Lab 1 made you type numbers into the prompt by hand. Nobody's doing that with
a 400-row budget file. This lab is about handing Claude the file itself — and
about the one habit that separates people who trust the output from people who
shouldn't.

## Before you start

- [ ] Download [`budget-vs-actual-q2-fy26.csv`](../files/budget-vs-actual-q2-fy26.csv)
- [ ] Open a new chat

## Do this

1. Click the **paperclip** (or **+**) in the message box and attach the CSV.
2. Paste the prompt below.
3. Read the output, then do the follow-up. The follow-up is the actual lab.

!!! example prompt "Copy this prompt"

    ```text
    Attached is our Q2 budget-to-actual by department and account.

    Find the five largest unfavourable variances by dollar amount, not
    by percentage. For each one give me: department, account, month,
    budget, actual, dollar variance, and percent variance.

    Then tell me which of the five are likely to be one-off and which
    look like a run-rate problem that will repeat in Q3, and say what
    in the data makes you think so.

    Show me the table first, then the commentary.
    ```

Now the part people skip:

!!! example prompt "Follow-up — always do this"

    ```text
    Show me the exact rows from the file behind the top three variances,
    and tell me the total number of rows you read.
    ```

## What good looks like

A table of five variances where the dollar amounts actually reconcile to the
file, followed by commentary that distinguishes a one-time legal bill from a
contractor run-rate that's going to show up again.

The follow-up should return real rows you can go check. If Claude can't produce
the underlying rows, or the row count looks wrong, the analysis above it is
not trustworthy — and you've found that out in ten seconds rather than in a
meeting.

!!! tip "Dollars, not percentages"
    Notice the prompt said "by dollar amount, not by percentage". Ask for
    percentage variances and the top of your list will be a £400 line that
    doubled. Sorting by dollars is almost always what you actually meant.

## Paste, or attach?

| | Use it when |
|---|---|
| **Paste into the message** | Under ~50 rows, or you want Claude to see it exactly as formatted. Fastest for a quick question. |
| **Attach the file** | Anything bigger, anything with structure, anything you'd have to reformat to paste. Also: Claude can process the file with code rather than reading it, which is more reliable on big files. |

Attaching is the default. Paste is the exception.

<div class="yours" markdown>
**Now with your own file.** Take a real export — a trial balance, an aging, a
commission schedule — and ask Claude the question you'd normally answer with a
pivot table.

Then run the follow-up prompt. Every time. Make it a reflex: **ask for the
rows behind the number.**
</div>

!!! warning "Gotcha"
    Big files get summarised unless you ask for precision. If your file is
    thousands of rows and the answer comes back suspiciously round, say
    *"process this with code and give me exact figures, don't estimate."*
    That pushes Claude to actually compute rather than read and infer.

---

**Go deeper:** [Uploading files to Claude](https://support.claude.com/en/articles/8241126-upload-files-to-claude)

**Next:** [Lab 3 — Stop repeating yourself](03-projects.md)
