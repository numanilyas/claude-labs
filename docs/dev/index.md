# Developer Track

Ten labs for working engineers. Same format as the finance track: ten minutes
each, do it in a real repository, theory links at the bottom.

This assumes you can already use a terminal and git. It does not assume you've
used Claude Code.

## Before you start

- A **Claude Pro** subscription or higher — Claude Code authenticates against
  it directly, no API key needed
- A repository you don't mind Claude touching. A side project is ideal. If you
  only have work code, make a scratch branch.
- macOS, Linux, WSL, or Windows

!!! warning "One thing that will bite you immediately"
    If you have `ANTHROPIC_API_KEY` set in your shell, Claude Code will offer
    to use it *instead of* your Pro subscription, and you'll quietly spend API
    credits. Before your first login:

    ```bash
    unset ANTHROPIC_API_KEY
    ```

## Foundations

| | Lab | What you'll learn |
|---|---|---|
| 1 | [Setup and first session](01-setup.md) | Install, auth against Pro, find your usage |
| 2 | [Project memory](02-claude-md.md) | CLAUDE.md, rules, and why yours will get too long |
| 3 | [Explore, plan, implement](03-explore-plan-implement.md) | The loop that separates good sessions from bad ones |

## Daily driver

| | Lab | What you'll learn |
|---|---|---|
| 4 | [Code review](04-code-review.md) | `/code-review`, and the writer/reviewer split |
| 5 | [Tests and debugging](05-tests-and-debugging.md) | Reproduce first, then fix |
| 6 | [Big refactors](06-big-refactors.md) | `/batch`, worktrees, headless fan-out |

## Extending Claude

| | Lab | What you'll learn |
|---|---|---|
| 7 | [Skills](07-skills.md) | Reusable procedures, and dynamic context injection |
| 8 | [Subagents and hooks](08-subagents-and-hooks.md) | Context isolation, and deterministic gates |
| 9 | [Write an MCP server](09-mcp-server.md) | Your own tools, in about forty lines |
| 10 | [Agent SDK](10-agent-sdk.md) | Claude Code as a library |

!!! note "Lab 10 needs API credits"
    Labs 1–9 run on your Pro subscription. The Agent SDK is explicitly not
    permitted to authenticate against a Claude.ai subscription — it needs an
    API key from the Console. Budget a few dollars, or read that one and skip
    the exercise.

---

!!! tip "If you only have thirty minutes"
    Labs 2, 3, and 7. Project memory, the plan-first loop, and skills are where
    the compounding is. Everything else is easier to pick up on your own.

## One idea underneath all ten

Claude's context window fills up, and quality degrades as it fills. Almost
every technique in this track is a way of *not putting things in the context
window*: skills that load on demand, subagents that summarise instead of
dumping, plan mode that reads before it writes, `/clear` between unrelated
tasks.

If you internalise nothing else: **a fresh context beats a long one**, and
`/clear` is free.
