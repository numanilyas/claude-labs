# Lab 8 — Subagents and hooks

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Claude Code</span>
  <span>.claude/agents/ · settings.json</span>
</div>

Two different tools that people confuse. Subagents manage **context**. Hooks
enforce **determinism**.

---

## Part 1 — Subagents

### The problem

"Search the codebase for every place we handle currency conversion" produces
forty file reads, and all forty are now in your context window competing with
the thing you were actually doing.

A subagent runs that search in **its own context window** and returns only the
answer. The forty file reads never touch your session.

### Do this

```bash
mkdir -p .claude/agents
```

`.claude/agents/security-reviewer.md`:

```markdown title="security-reviewer.md"
---
name: security-reviewer
description: Reviews code for security problems. Use after changes to auth, input handling, or anything touching user data.
tools: Read, Grep, Glob, Bash
model: opus
---

You are a senior security engineer reviewing a diff.

Look for:
- Injection: SQL, command, template
- Authentication and authorisation gaps, especially missing checks
  on new endpoints
- Secrets or credentials in code or config
- Input that reaches a sensitive sink without validation

Give specific line references and a concrete fix for each finding.
Rank by exploitability. If you find nothing substantive, say so
plainly - do not pad the list.
```

Then just ask for it:

```text
Use the security-reviewer subagent on the diff for this branch.
```

Built-ins you already have: **Explore** (read-only search — use it for the
forty-file-read problem) and **Plan** (what plan mode uses).

### The tradeoff

| | Skill | Subagent |
|---|---|---|
| What it is | Instructions injected into a context | A separate agent with its own window |
| Cost | Body stays in your context once loaded | Only the summary comes back |
| Good for | A procedure you want followed | Isolating a big search or an independent review |

Subagents aren't free — spawning one has overhead, and it can't see your
conversation. Use them when the work is genuinely separable.

---

## Part 2 — Hooks

### The problem

You've told Claude four times to run the linter after editing. It does it most
of the time. "Most of the time" isn't a guarantee, and some things need to be.

A hook is a shell command that fires on an event. It always runs. It isn't
asking the model to remember.

### Do this

`.claude/settings.json`:

```json title=".claude/settings.json"
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "make lint",
            "timeout": 60,
            "statusMessage": "Running linter..."
          }
        ]
      }
    ]
  }
}
```

Now the linter runs after every edit, whatever the model intended.

### Blocking

Exit code **2** is the one that matters: it blocks the action and feeds stderr
back to Claude so it can react.

```bash title=".claude/hooks/guard.sh"
#!/usr/bin/env bash
# PreToolUse hook - refuse edits to frozen code.
# Command hooks receive their payload as JSON on stdin, not in an
# environment variable.
payload=$(cat)
path=$(jq -r '.tool_input.file_path // ""' <<< "$payload")

if [[ "$path" == *"internal/legacy/"* ]]; then
  echo "internal/legacy/ is frozen. Don't edit it." >&2
  exit 2
fi
exit 0
```

!!! warning "Read the payload from stdin"
    Hooks get their input as **JSON on stdin**. There is no
    `$CLAUDE_TOOL_INPUT` environment variable — if you write one, it expands
    to empty, your test never matches, the script exits 0, and you'll believe
    you have a guard that blocks nothing. The env vars that *do* exist are
    `CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA` and
    `CLAUDE_EFFORT`.

    Test every hook by deliberately triggering it before you rely on it.

| Exit code | Effect |
|---|---|
| 0 | Success, carry on |
| **2** | **Blocking error** — action denied, stderr goes back to Claude |
| other | Non-blocking, first line of stderr shown |

### The one worth setting up today

A `Stop` hook that blocks the turn from ending until your tests pass. That's
verification level 3 from Lab 3 — a deterministic gate rather than a request.

Build in your own escape hatch — a marker file, an environment variable, a
retry counter the script tracks itself. A gate that can never be satisfied is
a session you have to kill.

```text
/hooks
```

manages them interactively if you'd rather not hand-edit JSON.

<div class="yours" markdown>
**Now on your own repo.** Two things:

1. Write the subagent for the review you always wish someone did. Security,
   accessibility, database migration safety, API compatibility.
2. Write one hook for the rule you're tired of repeating. Formatter on save is
   the obvious first one.

Then notice the difference: the subagent gives an opinion, the hook gives a
guarantee. Reach for a hook whenever "it usually does it" isn't good enough.
</div>

!!! warning "Gotcha"
    Hooks run shell commands automatically, with your permissions, without
    asking. A careless hook is a footgun with a hair trigger — read anything
    you copy from the internet, including from this page.

---

**Go deeper:** [Subagents](https://code.claude.com/docs/en/sub-agents) ·
[Hooks](https://code.claude.com/docs/en/hooks)

**Next:** [Lab 9 — Write an MCP server](09-mcp-server.md)
