# Lab 4 — Code review

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Claude Code</span>
  <span>Bring a branch with changes</span>
</div>

## The problem

Claude reviewing code Claude just wrote is a weak check. It's biased toward its
own choices in the same way you are toward yours, and for the same reason: it
already decided this was the right approach.

The fix is structural, not a better prompt — **fresh context**.

## Do this

On a branch with real changes ahead of `main`:

```text
/code-review
```

That reviews commits ahead of upstream plus anything uncommitted. You can also
target it:

```text
/code-review main...my-feature
/code-review internal/ledger/posting.go
/code-review 1432
```

Useful flags:

| | |
|---|---|
| `--fix` | Applies the findings instead of just reporting |
| `--comment` | Posts inline comments on a GitHub PR |

Non-interactive, for a script or a git hook:

```bash
claude -p '/code-review'
```

## The writer/reviewer split

The pattern that actually works, and the reason it works is context isolation:

1. **Session A** implements the change.
2. **Session B**, started fresh, reviews it.

Session B hasn't spent an hour justifying these decisions to itself. It reads
the diff the way a colleague would.

For a review with real teeth, ask for refutation rather than assessment:

!!! example prompt "Copy this prompt — in a fresh session"

    ```text
    Review the diff on this branch against what it claims to do in the
    PR description.

    Look for: behaviour changes that aren't covered by a test, error
    paths that swallow failures, assumptions about input that aren't
    validated, and anything that changes semantics for existing
    callers.

    Report gaps, not style preferences. If you find nothing
    substantive, say so plainly rather than padding the list.
    ```

That final sentence is doing real work. **A reviewer prompted to find problems
will find some, whether or not they exist.** Without permission to come back
empty, you get a list of invented nits, and then you go and "fix" them.

## What good looks like

Findings you'd have been glad a colleague caught, and no more than that. If
every review returns eight items of equal weight, the prompt is generating
findings rather than discovering them.

Chasing every finding leads to over-engineering. Read the list, take the two
that matter, discard the rest without guilt.

<div class="yours" markdown>
**Now on your own branch.** Run `/code-review` on something you're about to
open a PR for.

Then run the refutation prompt in a fresh session and compare. Notice which
one found the thing that actually mattered — in my experience it's usually the
second, and the gap is the whole argument for fresh context.
</div>

!!! warning "Gotcha"
    `/code-review --fix` runs in the background and its edits land **outside
    the checkpoint system**, so `/rewind` won't undo them. Commit first, and
    review the resulting diff with git rather than trusting it.

---

**Go deeper:** [Code review](https://code.claude.com/docs/en/code-review)

**Next:** [Lab 5 — Tests and debugging](05-tests-and-debugging.md)
