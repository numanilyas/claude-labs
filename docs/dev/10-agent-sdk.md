# Lab 10 — Agent SDK

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Agent SDK</span>
  <span>Needs an API key</span>
</div>

!!! danger "This lab is not covered by your Pro subscription"
    The Agent SDK cannot authenticate against a Claude.ai plan — Anthropic
    doesn't permit subscription auth for third-party agents. You need an API
    key from the [Console](https://platform.claude.com), billed separately.

    A few dollars covers the exercise. If you'd rather not, read it anyway —
    knowing where the boundary sits is most of the value.

## The problem

Labs 1–9 were you, at a terminal, driving. Sometimes the thing you want is
Claude Code running *inside your own program*: triaging incoming issues,
processing a queue, reviewing PRs on a schedule.

The **Agent SDK** is Claude Code as a library. Same tools, same agent loop,
same context management — no terminal.

## Set up

=== "TypeScript"

    ```bash
    npm init -y && npm pkg set type=module
    npm install @anthropic-ai/claude-agent-sdk
    npm install --save-dev tsx
    export ANTHROPIC_API_KEY=sk-ant-...
    ```

=== "Python"

    ```bash
    uv init && uv add claude-agent-sdk
    export ANTHROPIC_API_KEY=sk-ant-...
    ```

Both SDKs bundle their own Claude Code binary. You don't need Claude Code
installed separately.

## Do this

=== "TypeScript"

    ```typescript title="agent.ts"
    import { query } from "@anthropic-ai/claude-agent-sdk";

    for await (const message of query({
      prompt: "Find any TODO comments in src/ and summarise what they " +
              "suggest is unfinished. Group by theme, not by file.",
      options: { allowedTools: ["Read", "Grep", "Glob"] }
    })) {
      if ("result" in message) console.log(message.result);
    }
    ```

    ```bash
    npx tsx agent.ts
    ```

=== "Python"

    ```python title="agent.py"
    import asyncio
    from claude_agent_sdk import query, ClaudeAgentOptions


    async def main():
        async for message in query(
            prompt=(
                "Find any TODO comments in src/ and summarise what they "
                "suggest is unfinished. Group by theme, not by file."
            ),
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Grep", "Glob"],
            ),
        ):
            if hasattr(message, "result"):
                print(message.result)


    asyncio.run(main())
    ```

    ```bash
    uv run agent.py
    ```

Note `allowedTools` — read-only here. That's the right default for anything
running unattended.

## Which of the three do you want?

| | You write | Use when |
|---|---|---|
| **Messages API** (`anthropic`) | The whole tool loop yourself | You want full control, or you're not doing agentic work at all |
| **Tool Runner** (`tool_runner`) | Your tools; it runs the loop | You want the loop handled but not a filesystem agent |
| **Agent SDK** | A prompt | You want Claude Code's behaviour, programmatically |

The Messages API version of an agent loop looks like this — worth seeing once
so you know what the SDK is doing for you:

```python
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, **params)
```

Versus:

```python
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

## Two API things worth knowing

**Prompt caching.** If you're sending the same large system prompt or codebase
context repeatedly, cache it. Reads cost about a tenth of a normal input token.

The trap: there's a **minimum cacheable prefix**, and below it caching silently
doesn't happen — no error, just a bill. Check
`usage.cache_read_input_tokens` on the response to confirm it's working, rather
than assuming.

**Batch API.** 50% off, 24-hour window, up to 100,000 requests. If your work
isn't interactive — nightly analysis, bulk classification, backfills — this is
free money you're otherwise not taking.

<div class="yours" markdown>
**Now build something small.** The best first project is a thing you currently
do by hand on a schedule:

- Triage new GitHub issues and apply labels
- Summarise yesterday's error logs into a digest
- Check every PR for a missing changelog entry

Keep `allowedTools` read-only for the first version. Add write access only once
you've watched it behave for a week.
</div>

---

## You've finished the developer track

Ten labs. The through-line, one more time: **a fresh context beats a long one**.
Skills load on demand, subagents summarise instead of dumping, plan mode reads
before it writes, `/clear` is free.

The habits worth keeping from all ten:

- Plan before implementing, and don't leave explore until the description
  matches your model of the code
- Review in a fresh session, never the one that wrote the code
- Reproduce with a failing test before fixing
- `git diff` the test files before committing
- When "it usually does it" isn't good enough, that's a hook

---

**Go deeper:** [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) ·
[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

**Back to:** [Developer track](index.md) · [Finance track](../finance/index.md)
