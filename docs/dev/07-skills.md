# Lab 7 — Skills

<div class="lab-meta">
  <span class="time">12 min</span>
  <span>Claude Code</span>
  <span>.claude/skills/</span>
</div>

## The problem

You have a procedure your team follows — how to cut a release, how to add a
migration, how to wire up a new endpoint. It lives in a wiki page nobody opens,
or in `CLAUDE.md` where it's eating context on every single session including
the ones that will never cut a release.

A **skill** is a procedure that loads only when it's relevant.

!!! note "Slash commands are skills now"
    `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both
    produce `/deploy`. Existing command files keep working, and the skill wins
    on a name collision. Write new ones as skills — you get a directory for
    supporting files, and Claude can invoke it on its own when relevant.

## Do this

**Create the directory before you start Claude** — a top-level skills directory
that didn't exist at session start needs a restart to be noticed.

```bash
mkdir -p .claude/skills/summarize-changes
```

`.claude/skills/summarize-changes/SKILL.md`:

```markdown title="SKILL.md"
---
description: Summarises uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---

## Current changes

!`git diff HEAD`

## Instructions

Summarise the changes above in two or three bullets, then list any
risks: missing error handling, hardcoded values, tests that need
updating, behaviour changes not covered by a test.

If the diff is empty, say so and stop.
```

Start Claude and run it:

```text
/summarize-changes
```

## The line that makes this powerful

```markdown
!`git diff HEAD`
```

That's **dynamic context injection**. Claude Code runs the command and
substitutes the output *before Claude sees the skill*. The skill isn't
instructions about how to go and get the diff — the diff is already there.

This is the difference between a skill and a saved prompt, and it's what makes
skills worth writing for engineering work. Anything you can get from a shell
command can be baked in: `!`git log --oneline -20``, `!`kubectl get pods``,
`!`cat package.json``.

## Where they live

| Scope | Path |
|---|---|
| Personal, all projects | `~/.claude/skills/<name>/SKILL.md` |
| Project, committed | `.claude/skills/<name>/SKILL.md` |

**The command name comes from the directory name**, not the frontmatter. Commit
project skills — that's how a procedure becomes the team's rather than yours.

## Frontmatter worth knowing

```yaml
---
description: What it does and when to use it. Claude reads this to decide.
disable-model-invocation: true    # only you can run it, never Claude
allowed-tools: Bash(npm test *), Read, Edit
model: opus
context: fork                     # run in a subagent, keep my context clean
---
```

`disable-model-invocation: true` is the important one for anything with side
effects — `/deploy`, `/release`, `/commit`. You don't want Claude deciding your
code looks ready to ship.

## Skill, rule, or hook?

| You want | Use |
|---|---|
| A fact, always relevant | `CLAUDE.md` |
| A fact, only for some paths | `.claude/rules/` with `paths:` |
| A **procedure** with steps | A skill |
| Must happen every time, no exceptions | A hook (Lab 8) |

The signal to extract a skill: **a section of `CLAUDE.md` has grown into a
procedure rather than a fact.**

<div class="yours" markdown>
**Now on your own repo.** Write the skill for the thing you explain to every
new joiner. Release process, migration checklist, how to add a feature flag,
what to do when the integration tests hang.

Use at least one `!` command in it. The skill that already knows the current
state of the repo is a different class of tool from the one that has to go
looking.
</div>

!!! tip "Editing takes effect immediately"
    Changes to an existing `SKILL.md` are picked up without restarting. Only
    *creating* a top-level skills directory that wasn't there at launch needs
    a restart.

!!! warning "Gotcha"
    Skills in `~/.claude/skills/` are yours and yours alone. They aren't
    available in Cowork or in cloud sessions, which load skills from your
    Claude account instead. If a skill mysteriously "doesn't exist", check
    which surface you're on.

---

**Go deeper:** [Skills](https://code.claude.com/docs/en/skills) ·
[agentskills.io](https://agentskills.io)

**Next:** [Lab 8 — Subagents and hooks](08-subagents-and-hooks.md)
