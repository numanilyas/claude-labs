# Lab 8 — Your first skill

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Skills</span>
  <span>Builds on Lab 7</span>
</div>

## The problem

Lab 7's prompt was good. It was also 200 words, and next month you'll have lost
it, and the month after that a colleague will write a worse one from memory.

A **skill** is that prompt, saved, with a description telling Claude when to
use it. You stop writing the prompt; you just ask for a variance memo and the
procedure comes with it.

Think of it as a documented procedure rather than a clever prompt. That's
genuinely all it is.

## Route A — let Claude build it (recommended)

Easiest, and you don't need to know the file format.

1. Start a **new chat** (not Cowork).
2. Paste this:

!!! example prompt "Copy this prompt"

    ```text
    I want to create a skill that writes our monthly variance memo.

    Here's the procedure it should follow: [paste the prompt you used
    in Lab 7 here]

    Ask me anything you need about our conventions, then build the
    skill. Keep the description under 200 characters and make sure it
    describes when to use the skill, not just what it does.
    ```

3. Answer its questions. It'll ask about your reporting line, materiality,
   tone — the things you'd tell a new hire.
4. It produces a skill file. Download it.
5. Go to **Customize → Skills** in the sidebar (on some builds:
   **Settings → Capabilities → Skills**), click **Add**, and upload it.

## Route B — write it yourself

Worth doing once, so the format isn't mysterious. Create a folder called
`variance-memo` containing one file, `SKILL.md`:

```markdown title="SKILL.md"
---
name: variance-memo
description: Writes a monthly or quarterly variance memo from a budget-to-actual file. Use for variance commentary, budget vs actual analysis, or management report commentary.
---

# Variance memo

## When this applies

The user has a budget-to-actual file and wants written commentary,
not just analysis.

## Procedure

1. Read the file with code. Never estimate figures.
2. Compute variance as actual minus budget. On expense lines a
   positive variance is unfavourable.
3. Identify drivers by dollar amount, not percentage. Stop when the
   remaining variances are individually immaterial.
4. **Show the driver table and stop.** Wait for the user to confirm
   the numbers before writing prose.
5. Write the memo as a .docx:
   - Opening paragraph: total budget, total actual, variance in
     dollars and percent, one-sentence verdict
   - Driver table
   - One paragraph per driver
   - Closing section: "To confirm before this is final"
6. Favourable variances get one sentence in total.

## House rules

- Under one page.
- Plain professional English. No filler phrases, no restating the
  table in prose.
- Mark any inferred cause with [inferred]. Never assert a cause the
  data does not support.
- If the file has fewer rows than expected or contains blanks in
  Budget or Actual, say so before analysing.
```

Zip the **folder** — `variance-memo.zip` should contain a `variance-memo/`
folder with `SKILL.md` inside it, not a loose `SKILL.md` at the top level.
That's the single most common mistake, and it fails silently.

Then upload it the same way: **Customize → Skills → Add**.

## Test it

New chat. Attach `budget-vs-actual-q2-fy26.csv` and say something that doesn't
mention the skill at all:

!!! example prompt "Copy this prompt"

    ```text
    Can you write up the variance commentary for Q2 from this?
    ```

## What good looks like

Claude should reach for the skill on its own, because your *description* matched
what you asked for. You should see it mention using the skill as it works.

And it should stop after the driver table and wait for you — because step 4 said
so. If it blows straight through to the memo, your procedure isn't being
followed closely enough; make step 4 more emphatic.

!!! tip "The description is the whole ballgame"
    Claude decides whether to use a skill by reading its description and
    nothing else. `description: Variance memo skill` will almost never fire.
    Describe **when to use it**, using the words you'd actually say:
    "variance commentary", "budget vs actual", "management report".

    The 200-character cap applies to skills uploaded to Claude on the web.
    Skills written for Claude Code have a much larger allowance — don't carry
    the tight limit across if you write one there.

<div class="yours" markdown>
**Now with your own procedure.** Pick something you do more than twice a
quarter and that has rules other people get wrong. Good candidates:

- Month-end close checklist
- Commission calculation, with all its exceptions
- The way your team formats a customer-facing statement
- New vendor onboarding checks

Build it from a prompt that already worked, not from scratch. Skills written
in the abstract tend to describe a process nobody follows.
</div>

!!! warning "Gotcha"
    On a Pro plan, skills are **yours alone**. There's no org-wide sharing —
    each colleague uploads their own copy. So share the *file*, not a link, and
    decide now who owns the master version, or you'll have five drifting
    variants by November.

!!! warning "Skills don't travel"
    A skill uploaded to Claude on the web is not automatically available
    everywhere else. If it doesn't fire where you expected, check you're on the
    surface you uploaded it to.

---

**Go deeper:** [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

**Next:** [Lab 9 — Teach Claude your house style](09-house-style-skill.md)
