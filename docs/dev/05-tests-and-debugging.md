# Lab 5 — Tests and debugging

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Claude Code</span>
  <span>Bring a real bug if you have one</span>
</div>

## Part 1 — Tests

Claude reads your existing test files and matches the style, framework and
assertion patterns already there. You get less value from explaining your
conventions than from pointing at a file that demonstrates them.

### Find the gaps first

!!! example prompt "Copy this prompt"

    ```text
    Find functions in internal/ledger that aren't covered by tests.
    Rank them by how much damage a silent failure would do, not by
    line count.
    ```

That ranking clause turns a coverage report into a work list.

### Then write them

!!! example prompt "Copy this prompt"

    ```text
    Add tests for [the top one]. Match the style and framework in the
    existing tests in that package.

    Cover the edge cases, not just the happy path - specifically the
    boundary conditions and the error paths. Avoid mocks where a real
    value will do.

    Run them and show me the output.
    ```

**Be specific about what you're testing for.** "Write tests for foo.py" gets
you a happy-path test. "Write a test for foo.py covering the case where the
user is logged out, avoid mocks" gets you the test you wanted.

### TDD, if that's your thing

It works well here, because the tests become the verification signal:

1. Fresh session: *"Write failing tests for [behaviour]. Don't implement it."*
2. Commit the tests.
3. Fresh session: *"Make these tests pass. Don't modify the tests."*

That last instruction is not optional. Without it, a stuck model will
eventually edit the test.

## Part 2 — Debugging

### Reproduce before you fix

The single highest-value prompt in this lab:

!!! example prompt "Copy this prompt"

    ```text
    Users report that [symptom] after [condition]. Check [the area],
    especially [your suspicion].

    Write a failing test that reproduces the issue first. Show me it
    failing. Then fix it and show me it passing.

    Address the root cause. Don't suppress the error or add a
    defensive check that hides it.
    ```

A fix without a reproduction is a guess that happened to make the symptom go
away. The failing test is what turns it into a fix — and it stays in the suite
afterwards.

### Give it the trace

Paste the actual stack trace and the command that produces it. Claude debugging
from your paraphrase of an error is Claude debugging with one hand tied.

```text
/debug
```

turns on debug logging mid-session and analyses the session log — useful when
the problem is with the Claude Code session itself rather than your code.

## What good looks like

For tests: a diff you'd approve, in the style of the surrounding tests, that
fails if you break the behaviour it claims to cover. Verify that last part —
break the code deliberately and check the test goes red.

For bugs: a failing test, then a passing test, then a fix whose diff you
understand.

<div class="yours" markdown>
**Now on your own code.** Take the most recent bug you fixed by hand and run it
through the reproduce-first prompt. See whether Claude finds the same root cause
you did.

If it finds a different one, that's worth ten minutes of your attention.
</div>

!!! warning "Gotcha"
    A model that can't make a test pass will sometimes make the test easier
    instead. `git diff` the test files before you commit, every time. This is
    not paranoia — it's a well-known failure mode with a trivially cheap check.

---

**Go deeper:** [Common workflows](https://code.claude.com/docs/en/common-workflows)

**Next:** [Lab 6 — Big refactors](06-big-refactors.md)
