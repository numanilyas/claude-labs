# Lab 4 — Clean up an export nobody documented

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Cowork</span>
  <span>File: messy-pl-q2-fy26.xlsx</span>
</div>

## The problem

Someone sends you a P&L export. It has four rows of junk above the headers, the
headers are split across two rows, there's an empty phantom column in the
middle, negative numbers are text strings in parentheses, one row is stored as
text with a trailing space, another has a dollar sign baked into the value, and
somebody pasted a duplicate subtotal row near the bottom.

You cannot pivot it. You cannot sum it. You spend forty minutes fixing it by
hand, every month.

This is the lab where Cowork earns its keep.

## Before you start

- [ ] Claude **desktop app** installed and signed in
- [ ] [`messy-pl-q2-fy26.xlsx`](../files/messy-pl-q2-fy26.xlsx) saved in your `claude-labs` folder
- [ ] Open the file in Excel first and look at it, so you know what you're up against

## What Cowork is, in one paragraph

Ordinary chat reads your file and talks about it. **Cowork** gets a working
folder, a sandbox to run code in, and permission to produce files — so it can
open your workbook, write a script to fix it, run the script, check the result,
and hand you a new file. Same Claude, different amount of leash.

## Do this

1. Open the **Claude desktop app**.
2. In the message box, select **Cowork**.
3. Connect your `claude-labs` folder when prompted (or use the folder picker).
4. Leave approvals on **manual** for this first run — you want to watch what it
   does.
5. Paste the prompt.

!!! example prompt "Copy this prompt"

    ```text
    In the connected folder there's a file called messy-pl-q2-fy26.xlsx.
    It's a P&L export and it's a mess.

    Produce a clean version called pl-q2-fy26-clean.xlsx that I can
    pivot and chart against. Specifically:

    - Drop the junk rows above the real header and the notes below the
      data, but tell me what was in them before you throw them away
    - Build one proper header row
    - Every number must be a real number: strip currency symbols,
      convert text-stored numbers, and convert parenthesised values to
      negatives
    - Drop the empty column
    - Normalise the account labels: trim whitespace, consistent case
    - Add a Category column marking each row as Revenue, COGS, Opex,
      Below the line, or Subtotal

    Two things to check and report, don't just fix silently:
    1. Whether the subtotal rows actually equal the sum of their
       components
    2. Whether any row appears twice

    Give me the numbers you found for both.
    ```

## What good looks like

You should get back a workbook with a single clean header row, numeric columns
that sum, and a Category column.

More importantly, the two checks should have found things:

- Every subtotal **does** foot correctly to its components
- There **is** a duplicated row — a stray `Total Operating Expenses` pasted in
  near the bottom, which would have double-counted if you'd summed the column
  naively

If Claude quietly cleaned the file without mentioning the duplicate, you asked
it to check and it didn't — push back: *"You didn't answer question 2. Did any
row appear twice?"* That pushback is a normal part of using this well.

!!! tip "Watch the approvals"
    On manual approval you'll see each step before it runs — read the file,
    write a script, run it, write the output. Watching this once tells you more
    about how Cowork works than any explanation. After that, feel free to speed
    it up.

<div class="yours" markdown>
**Now with your own file.** Take the export you hate most. Point Cowork at it
with the same prompt structure: *what's wrong, what I want back, what to check
and report rather than fix silently.*

That last clause is the one to keep. "Fix it" gets you a clean file. "Fix it
and tell me what you found" gets you a clean file **and** the knowledge that
your March subtotals never footed.
</div>

!!! warning "Gotcha"
    Cowork consumes your usage allowance considerably faster than chatting.
    Check **Settings → Usage** after this lab so you have a feel for the cost.
    Don't leave it running on auto-approve against a folder you care about
    until you trust it.

!!! danger "Before you point this at a real folder"
    Cowork can modify and delete files in a connected folder. Connect a folder
    with a copy of your data in it, not your only copy, until you've built up
    some confidence. Permanent deletion always asks first — but overwriting
    doesn't.

---

**Go deeper:** [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)

**Next:** [Lab 5 — Five PDFs into one spreadsheet](05-pdfs-to-spreadsheet.md)
