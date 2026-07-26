# Lab 3 — Explore, plan, implement

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Claude Code</span>
  <span>Plan mode</span>
</div>

## The problem

The default failure mode is: you describe a feature, Claude starts editing
immediately, and forty files later you discover it misunderstood the
architecture in the first thirty seconds. Now you're reviewing a large wrong
diff instead of a small right one.

Plan mode fixes this by making Claude read before it writes.

## The loop

**Explore → Plan → Implement → Commit.** Four phases, and the first two happen
before a single file changes.

## Do this

Pick a real change in your repo — something you'd estimate at an hour or two.
Not a one-liner.

### 1. Explore

Enter plan mode: <kbd>Shift</kbd>+<kbd>Tab</kbd> until the status bar reads
`⏸ plan mode on`. Claude can now read and run exploration commands, but cannot
edit.

!!! example prompt "Copy this prompt"

    ```text
    Read the code involved in [the area you're changing] and explain
    how it currently works. Don't propose anything yet - I want to
    know you understand it before we talk about changes.
    ```

Read the answer properly. **If it's wrong here, stop and correct it.** This is
the cheapest possible moment to fix a misunderstanding, and it's the moment
almost everyone skips.

### 2. Plan

Still in plan mode:

!!! example prompt "Copy this prompt"

    ```text
    I want to [describe the change]. What files need to change, in what
    order, and what could break? Call out anything you're uncertain
    about rather than picking an approach and moving on.

    Give me a plan, not code.
    ```

Press <kbd>Ctrl</kbd>+<kbd>G</kbd> to open the plan in your editor and change
it directly. Editing the plan is much faster than arguing with the model about
it in chat.

### 3. Implement

Approve the plan to exit plan mode. Then:

!!! example prompt "Copy this prompt"

    ```text
    Implement the plan. Write tests for the new behaviour, run the test
    suite, and fix any failures. Show me the test output rather than
    telling me it passes.
    ```

That last clause matters. **Give Claude a way to check its own work and it will
use it; leave it without one and "looks done" is the only signal it has** — and
you become the verification loop.

### 4. Commit

```text
commit with a descriptive message and open a PR
```

## What good looks like

A diff you can review in one sitting, that does what the plan said, with tests
that ran in front of you.

Compare it against how the same change goes without plan mode. Do it once —
the difference is more convincing than any explanation.

## When to skip the plan

**If you could describe the diff in one sentence, skip it.** Plan mode on
"rename this variable" is pure overhead. The loop earns its keep on changes
that touch several files or where you're not certain of the approach yourself.

## Escalating how hard Claude checks itself

Four levels, cheapest first:

1. **In the prompt** — "run the tests after implementing"
2. **Across the session** — `/goal <condition>` re-checks after every turn
3. **A deterministic gate** — a `Stop` hook that blocks until your script
   passes (Lab 8)
4. **A second opinion** — a reviewer subagent with fresh context (Lab 4)

Start at 1. Escalate when 1 isn't holding.

<div class="yours" markdown>
**Now on your own work.** Run your next real feature through all four phases.

The specific discipline to build: **do not leave phase 1 until Claude's
description of the current code matches your mental model.** Every expensive
session I've seen went wrong there and nowhere else.
</div>

!!! tip "Session hygiene"
    - <kbd>Esc</kbd> stops generation without losing context
    - <kbd>Esc</kbd> <kbd>Esc</kbd> or `/rewind` restores conversation, code, or both
    - `/clear` between unrelated tasks — free, and the highest-leverage habit here
    - After two failed corrections, `/clear` and rewrite the prompt. A third
      correction almost never works.

!!! warning "Gotcha"
    Checkpoints only track Claude's own file-editing tools. Anything changed by
    a shell command it ran isn't covered, so `/rewind` won't undo it. Commit
    before anything ambitious — checkpoints are not a git replacement.

---

**Go deeper:** [Best practices](https://code.claude.com/docs/en/best-practices) ·
[Permission modes](https://code.claude.com/docs/en/permission-modes)

**Next:** [Lab 4 — Code review](04-code-review.md)
