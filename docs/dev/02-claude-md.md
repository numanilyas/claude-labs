# Lab 2 — Project memory

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Claude Code</span>
  <span>CLAUDE.md · rules</span>
</div>

## The problem

Every session starts from nothing. Without project memory you re-explain the
build command, the test runner, the fact that `legacy/` is frozen, and the
import convention — every single time.

`CLAUDE.md` is where that lives. It loads automatically at session start.

## Do this

```bash
cd ~/your-repo
claude
```

```text
/init
```

That generates a starter `CLAUDE.md` from what Claude can infer. **Read it
critically** — it's a first draft written by something that has only just met
your codebase. Delete the parts that are obvious from the file tree.

Then improve it by hand. Aim for something like:

```markdown title="CLAUDE.md"
# Project

Payments service. Go, Postgres, deployed to ECS.

## Commands

- Build: `make build`
- Test: `make test` (unit), `make test-integration` (needs docker compose up)
- Lint: `make lint` — CI fails on any warning
- Single test: `go test ./internal/ledger -run TestName`

## Conventions

- Errors wrap with `fmt.Errorf("context: %w", err)`. Never `errors.New`
  at a call site.
- All money is `decimal.Decimal`. Never float64. This has bitten us.
- Database access only through `internal/store`. No raw SQL in handlers.

## Do not touch

- `internal/legacy/` — frozen, being deleted in Q4. Don't refactor it,
  don't fix its lint warnings.
- `migrations/` — additive only, never edit an applied migration.

## Gotchas

- Integration tests need `docker compose up -d` first or they fail with
  a confusing connection error.
- `make build` is required before `make test-integration`; the test
  binary reads the built artifact.
```

## The load order

All of these are read and concatenated, broadest to most specific:

| Scope | Path |
|---|---|
| User, all projects | `~/.claude/CLAUDE.md` |
| Project, committed | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Project, personal | `./CLAUDE.local.md` — gitignore it |

Claude also walks *up* from your working directory, and pulls in a
subdirectory's `CLAUDE.md` on demand when it reads files there. Big monorepo:
put a small one at the root and specific ones in each service.

Verify what actually loaded:

```text
/context
```

Look under **Memory files**. This is how you find out that the `CLAUDE.md` you
thought was loading isn't.

## Keep it short

**Under 200 lines.** This is the rule people ignore and then wonder why Claude
stopped following their conventions.

Everything in `CLAUDE.md` is in the context window for the entire session, and
a long file dilutes itself — instruction 40 gets less attention than
instruction 4. If yours is growing, split it:

| The thing you want | Where it goes |
|---|---|
| A fact, always relevant | `CLAUDE.md` |
| A fact, relevant only to some paths | `.claude/rules/` with `paths:` frontmatter |
| A **procedure** with steps | A skill (Lab 7) |
| Something that must happen every time, no exceptions | A hook (Lab 8) |

Path-scoped rules look like this:

```markdown title=".claude/rules/api.md"
---
paths:
  - "internal/api/**/*.go"
---

- Every handler validates input before touching the store layer.
- Return `problem+json` on error, never a bare string.
```

That only enters the context when Claude is working in `internal/api/`.

<div class="yours" markdown>
**Now on your own repo.** Run `/init`, then cut the generated file in half.

Then do the thing that actually populates it: **for the next week, every time
you correct Claude about a project convention, add that correction as a line.**
Corrections you've had to make twice are exactly the content that belongs
here — and nothing else is.
</div>

!!! tip "The maintenance signal"
    When you catch yourself explaining the same thing in a third session, it
    belongs in `CLAUDE.md`. When `CLAUDE.md` is over 200 lines and Claude is
    dropping rules, the longest section belongs in a skill or a rule file.

---

**Go deeper:** [Memory](https://code.claude.com/docs/en/memory)

**Next:** [Lab 3 — Explore, plan, implement](03-explore-plan-implement.md)
