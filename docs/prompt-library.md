---
hide:
  - navigation
---

# Prompt library

Every prompt from the curriculum, in one place, so you don't have to go back
through the labs to find one. Copy button on the right of each block.

Square brackets mean *replace this*.

---

## Analysis

!!! example prompt "Variance analysis from a budget file"

    ```text
    Attached is our [period] budget-to-actual by department and account.

    Find the five largest unfavourable variances by dollar amount, not
    by percentage. For each one give me: department, account, month,
    budget, actual, dollar variance, and percent variance.

    Then tell me which are likely one-off and which look like a
    run-rate problem that will repeat, and say what in the data makes
    you think so.

    Show me the table first, then the commentary.
    ```

!!! example prompt "The tie-out block — add to anything that produces numbers"

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

---

## Cleaning and extraction

!!! example prompt "Clean a hostile export"

    ```text
    In the connected folder there's [filename]. It's a [what it is]
    and it's a mess.

    Produce a clean version called [output name] that I can pivot and
    chart against:

    - Drop junk rows above the header and notes below the data, but
      tell me what was in them before you throw them away
    - Build one proper header row
    - Every number must be a real number: strip currency symbols,
      convert text-stored numbers, convert parenthesised values to
      negatives
    - Drop empty columns
    - Normalise labels: trim whitespace, consistent case

    Two things to check and report, don't fix silently:
    1. Whether subtotals equal the sum of their components
    2. Whether any row appears twice

    Give me the numbers you found for both.
    ```

!!! example prompt "PDFs into a schedule"

    ```text
    The [folder] has [n] [document type] as PDFs, all in different
    formats.

    Build me [output].xlsx with one row per document and these columns:
    [list them].

    Rules:
    - If a field isn't on the document, leave the cell empty and don't
      guess
    - Add a Notes column flagging anything I should look at
    - Sort by [field]
    - Add a total row using a real SUM formula

    Then tell me the grand total and confirm each document's components
    sum to its total. If any doesn't foot, say which.
    ```

!!! example prompt "Reconcile two sources"

    ```text
    Two files: [source A] and [source B]. Both cover [period] for the
    same [account]. Opening balance was [amount] on both sides.

    Reconcile them and give me [output].xlsx with four tabs:

    1. Summary - the classic format, adjusting both sides to a common
       figure. The two adjusted figures must agree.
    2. Matched - items that tie on both sides
    3. Exceptions - every unmatched or mismatched item, one per row,
       with which side it's on, the amount, and what you think it is
    4. Source data - both files as you parsed them, so I can audit you

    Match on amount, date and reference, allowing a few days of timing
    difference. Watch for the same item posted twice on one side, and
    for amounts that are close but not equal.

    Then tell me in plain English what each reconciling item is and
    what I need to do about it.
    ```

---

## Writing

!!! example prompt "Variance memo"

    ```text
    [File] has [period] opex by month, department and account.

    Write me a variance memo as [output].docx, addressed to [reader],
    from [you]. Structure:

    - One opening paragraph: total budget, total actual, variance in
      dollars and percent, one-sentence verdict
    - A short table of the drivers that explain the variance
    - One paragraph per driver: what it is, how much, most likely
      explanation given this is a [business type]
    - A closing section headed "To confirm before this is final"

    Rules:
    - Under one page
    - Plain professional English. No filler, no restating the numbers
      in prose after the table
    - Where you're inferring a cause rather than reading it from the
      data, mark the sentence with [inferred]
    - Favourable variances get one sentence total

    Before you write it, show me the driver table and let me confirm
    the numbers.
    ```

!!! example prompt "Extract your house style from examples"

    ```text
    Attached are documents my team wrote. I want to capture our house
    style so future documents match without me having to edit them.

    Read them and infer our conventions. Cover:
    - Structure: what sections, in what order, how long
    - Tone and register
    - Number formatting: rounding, currency, negatives, percentages,
      how periods are written
    - Vocabulary: terms we use, terms we clearly avoid

    Give me the list as specific, checkable rules. "Professional tone"
    is not a rule. "Never opens a paragraph with 'Additionally'" is.

    Then flag any place the documents contradict each other, so I can
    decide which is right.
    ```

---

## Verification

!!! example prompt "Show the source"

    ```text
    Show me the exact rows from the file behind that number, and tell
    me how many rows you read in total.
    ```

!!! example prompt "Re-derive independently"

    ```text
    Recompute that a different way, without referring to your previous
    answer, and tell me if the two results differ.
    ```

!!! example prompt "What did you have to decide?"

    ```text
    What did you have to decide or assume in order to answer that?
    List every judgement call, including ones you think are obvious.
    ```

---

## Claude Code

!!! example prompt "Repository tour"

    ```text
    Give me a tour of this repository. What does it do, what are the
    main components, how do they talk to each other, and where does a
    request enter the system?

    Then tell me three things that would surprise a new engineer
    joining this codebase.
    ```

!!! example prompt "Explore, before any planning"

    ```text
    Read the code involved in [area] and explain how it currently
    works. Don't propose anything yet - I want to know you understand
    it before we talk about changes.
    ```

!!! example prompt "Plan"

    ```text
    I want to [change]. What files need to change, in what order, and
    what could break? Call out anything you're uncertain about rather
    than picking an approach and moving on.

    Give me a plan, not code.
    ```

!!! example prompt "Implement"

    ```text
    Implement the plan. Write tests for the new behaviour, run the test
    suite, and fix any failures. Show me the test output rather than
    telling me it passes.
    ```

!!! example prompt "Adversarial review — run in a fresh session"

    ```text
    Review the diff on this branch against what it claims to do.

    Look for: behaviour changes that aren't covered by a test, error
    paths that swallow failures, assumptions about input that aren't
    validated, and anything that changes semantics for existing
    callers.

    Report gaps, not style preferences. If you find nothing
    substantive, say so plainly rather than padding the list.
    ```

!!! example prompt "Reproduce before fixing"

    ```text
    Users report that [symptom] after [condition]. Check [area],
    especially [suspicion].

    Write a failing test that reproduces the issue first. Show me it
    failing. Then fix it and show me it passing.

    Address the root cause. Don't suppress the error or add a
    defensive check that hides it.
    ```

!!! example prompt "Find the test gaps that matter"

    ```text
    Find functions in [package] that aren't covered by tests. Rank them
    by how much damage a silent failure would do, not by line count.
    ```
