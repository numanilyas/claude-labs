# Lab 1 — Setup and first session

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Claude Code</span>
  <span>Bring a repo</span>
</div>

## Install

=== "macOS / Linux / WSL"

    ```bash
    curl -fsSL https://claude.ai/install.sh | bash
    ```

=== "Windows PowerShell"

    ```powershell
    irm https://claude.ai/install.ps1 | iex
    ```

=== "Homebrew"

    ```bash
    brew install --cask claude-code
    ```

The native installer auto-updates in the background. Homebrew and WinGet
installs don't — you'll run `claude update` yourself.

```bash
claude --version
```

## First session

```bash
unset ANTHROPIC_API_KEY     # do this before the first login
cd ~/your-repo
claude
```

A browser opens; sign in with your Pro account. That's the auth done — Claude
Code runs against your subscription, and its usage shares the same allowance as
the Claude app.

## Do this

Start with questions rather than edits. It's the fastest way to find out
whether it understands your codebase, and it costs nothing if it doesn't.

!!! example prompt "Copy this prompt"

    ```text
    Give me a tour of this repository. What does it do, what are the
    main components, how do they talk to each other, and where does a
    request enter the system?

    Then tell me three things that would surprise a new engineer
    joining this codebase.
    ```

That last question is the good one. It surfaces the load-bearing weirdness that
isn't in any README.

Follow up with the things you'd ask a senior colleague:

```text
How does logging work here?
Why does this call foo() instead of bar() on line 333?
What's the test story? What's covered and what obviously isn't?
```

## Four commands to learn now

```text
/usage      your plan bars, and the 24h / 7d breakdown
/model      which model this session uses - and the source of truth
            for what your account can select
/clear      wipe the conversation, keep the session
/context    what's actually loaded right now, and what it costs
```

`/clear` is the one to build a habit around. Starting an unrelated task in a
context full of the last task is the single most common way sessions go bad.

!!! tip "On usage limits"
    Published prompt-count figures for Pro are stale and model availability
    shifts. Don't take a number from a blog post — run `/usage` for your
    actual position and `/model` for what you can select. Those are live.

## Permission modes

<kbd>Shift</kbd>+<kbd>Tab</kbd> cycles between them. Watch the status bar.

| Mode | What it does |
|---|---|
| **Manual** (config name: `default`) | Asks before each edit or command |
| **acceptEdits** | Auto-approves file edits in the working directory — **and also `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`** |
| **plan** | Read-only. Explores and proposes, cannot edit. |

!!! warning "`acceptEdits` covers more than edits"
    That list includes `rm`. It's a reasonable mode to work in, but know what
    you've agreed to before you leave it on in a directory that matters.

Plan mode is Lab 3 and it's the one that changes how you work.

<div class="yours" markdown>
**Now on your own repo.** Ask the tour question about a part of your codebase
you've been avoiding. The bit with no tests and one original author who left.

Then run `/context` and look at what a session actually costs you. Knowing
what's in the window is most of knowing why an answer was mediocre.
</div>

!!! warning "Gotcha"
    Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repo has an
    `AGENTS.md` from another tool, bridge it with a one-line `CLAUDE.md`
    containing `@AGENTS.md` rather than maintaining two files.

---

**Go deeper:** [Claude Code overview](https://code.claude.com/docs/en/overview) ·
[CLI reference](https://code.claude.com/docs/en/cli-reference)

**Next:** [Lab 2 — Project memory](02-claude-md.md)
