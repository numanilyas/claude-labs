# Lab 6 — Big refactors

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Claude Code</span>
  <span>Needs a git repo</span>
</div>

## The problem

"Migrate 200 files from X to Y" in one session is the worst possible shape for
this tool. The context fills, quality degrades, and file 180 gets a worse
treatment than file 3 for no reason other than position.

The answer is always the same: **many small contexts instead of one large one.**
Three ways to get there.

## Option 1 — `/batch`

The built-in approach, and the first thing to reach for.

```text
/batch migrate the handlers in internal/api from gorilla/mux to chi
```

It researches the codebase, decomposes the work into 5–30 independent units,
and shows you a plan. Once you approve, it spawns one background subagent per
unit, each in its own git worktree, each running the tests and opening a PR.

Requires a git repo. Review the decomposition carefully before approving — a
bad split produces units that conflict with each other, and you'll find out
during merge.

## Option 2 — headless fan-out

When you want to control the loop yourself:

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from React class components to hooks. \
Preserve behaviour exactly. Return OK or FAIL with a reason." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

Each iteration is a fresh process with a clean context. File 200 gets the same
treatment as file 1.

**The discipline that makes this work:** run it on two or three files first,
read the diffs properly, refine the prompt based on what went wrong, and only
then run the full set. Everyone learns this by not doing it once.

## Option 3 — worktrees

For a handful of parallel streams you're supervising:

```bash
claude --worktree feature-auth
claude --worktree feature-billing
```

Separate working directories, no stepping on each other. Needs at least one
commit in the repo.

## The incremental alternative

Sometimes the right answer isn't parallelism, it's smaller steps in sequence:

```text
find all usage of the deprecated PaymentGateway API
suggest how to refactor internal/billing to the new interface
refactor internal/billing/charge.go only, keeping behaviour identical
run the billing tests
```

Then the next file. Slower in wall-clock, much easier to review, and you can
stop halfway and ship what you have.

**Rule of thumb:** if the migration is mechanical and verifiable by tests,
parallelise it. If it needs judgment per file, go incremental.

## Do this

Pick something real but bounded in your repo — 10 to 30 files. A deprecated
API, a logging library swap, a lint rule you've been ignoring.

Try `/batch` first. Read the decomposition before approving. Then look at what
came back and ask yourself whether you'd have split it the same way.

## What good looks like

Units that are genuinely independent, each with passing tests. If two units
touched the same file, the decomposition was wrong and that's the thing to
learn from — feed it back: *"units 3 and 7 both modify config.go, re-split so
each file belongs to exactly one unit."*

<div class="yours" markdown>
**Now on your own migration.** The one you've been putting off because it's
boring and touches everything. That's precisely the shape this is good at.

Start with the two-or-three-file trial run. Always. The twenty minutes it costs
saves you reviewing 200 wrong diffs.
</div>

!!! warning "Gotcha"
    Worktrees cost real disk and setup time per agent. For a handful of units
    that's nothing; for a hundred it's noticeable. And a fan-out that opens 30
    PRs is 30 PRs someone has to review — the bottleneck moves, it doesn't
    disappear.

---

**Go deeper:** [Monorepos and large repos](https://code.claude.com/docs/en/large-codebases)

**Next:** [Lab 7 — Skills](07-skills.md)
