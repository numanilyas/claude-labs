# Lab 9 — Write an MCP server

<div class="lab-meta">
  <span class="time">20 min</span>
  <span>MCP</span>
  <span>Python 3.10+</span>
</div>

## The problem

Claude can read your files and run your commands. It cannot query your staging
database, hit your internal service, or reach your ticketing system.

**MCP** is the protocol for giving it those. Writing a server is much less work
than the acronym suggests — the whole thing below is about forty lines.

## Adding an existing server first

Before writing one, know how to install one:

```bash
# remote, over HTTP
claude mcp add --transport http notion https://mcp.notion.com/mcp

# local, a subprocess
claude mcp add --env AIRTABLE_API_KEY=your-key --transport stdio airtable \
  -- npx -y airtable-mcp-server

claude mcp list
```

!!! danger "The `--` is mandatory"
    Everything after `--` is the server's own command line. Leave it out and
    Claude Code parses the server's flags as its own, with confusing results.

    Second trap: `--env` takes multiple `KEY=value` pairs, so the **server name
    must not come directly after it** — the CLI reads the name as another pair
    and rejects it. Put another option in between, or put `--env` first, as in
    the example above.

### Scopes

```bash
claude mcp add -s project ...   # writes .mcp.json, commit it, whole team gets it
claude mcp add -s user ...      # all your projects, just you
claude mcp add ...              # default: local, this project, just you
```

Project scope is how you give a team a shared toolset. Note that a freshly
cloned repo requires someone to accept the trust dialog before its servers
start — that's deliberate, since a repo could otherwise ship a server that runs
on checkout.

## Build one

Two tools that Claude genuinely can't do well on its own: who actually owns a
file, and what's been churning lately.

```bash
uv init repo-insight && cd repo-insight
uv add "mcp[cli]"
```

```python title="server.py"
import collections
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("repo-insight")


def _git(*args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd,
        capture_output=True, text=True, check=True,
    ).stdout


@mcp.tool()
def who_owns(path: str, repo: str = ".") -> str:
    """Find who wrote most of a file, by surviving lines of code.

    Args:
        path: File path relative to the repository root
        repo: Path to the git repository
    """
    out = _git("blame", "--line-porcelain", path, cwd=repo)
    authors = collections.Counter(
        line[len("author "):]
        for line in out.splitlines()
        if line.startswith("author ")
    )
    total = sum(authors.values()) or 1
    return "\n".join(
        f"{a}: {n} lines ({n / total:.0%})"
        for a, n in authors.most_common(5)
    )


@mcp.tool()
def recent_churn(days: int = 30, repo: str = ".") -> str:
    """List the files changed most often recently. High churn often
    means a design problem or an area under active rework.

    Args:
        days: How many days back to look
        repo: Path to the git repository
    """
    out = _git("log", f"--since={days} days ago",
               "--name-only", "--pretty=format:", cwd=repo)
    files = collections.Counter(l for l in out.splitlines() if l.strip())
    return "\n".join(f"{n:3d}  {f}" for f, n in files.most_common(15)) \
        or "No changes in that window."


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

That's the whole server. **FastMCP derives the tool schema from your type hints
and docstring** — the docstring isn't documentation, it's what Claude reads to
decide whether to call the tool. Write it accordingly.

Wire it up:

```bash
claude mcp add --transport stdio repo-insight \
  -- uv --directory /absolute/path/to/repo-insight run server.py
```

Then, in a repo:

!!! example prompt "Copy this prompt"

    ```text
    Who should review a change to internal/ledger/posting.go, and what
    files have been churning most this month? Use the repo-insight
    tools.
    ```

## What good looks like

`/mcp` shows `repo-insight` connected with two tools. Claude calls them and
gets real answers about your actual repository.

!!! danger "The mistake everyone makes once"
    **On stdio transport, never write to stdout.** A stray `print()` corrupts
    the JSON-RPC stream and the server dies with an unhelpful error.

    ```python
    import sys
    print("debugging", file=sys.stderr)   # fine
    print("debugging")                     # breaks everything
    ```

    Use `logging`, or stderr. On HTTP transport stdout is harmless.

## stdio or HTTP?

| | stdio | HTTP |
|---|---|---|
| Runs | Local subprocess | Anywhere reachable |
| Auth | Environment variables | OAuth 2.0 |
| Use for | Local tools, your machine's state | Shared team services |

Start with stdio. Move to HTTP when more than one person needs it.

<div class="yours" markdown>
**Now on your own stack.** Write a server exposing the one thing you always
have to go and look up by hand: staging deploy status, feature flag state, the
schema of a table, the last five errors in your log aggregator.

Keep it to two or three tools. A server with twenty tools puts twenty tool
descriptions in every session's context — the cost is real and constant.
</div>

!!! tip "CLIs beat MCP servers, when they exist"
    If there's already a good CLI — `gh`, `aws`, `kubectl`, `sentry-cli` —
    install it and let Claude run it. That's more context-efficient than an
    MCP server, because nothing is loaded until it's used. Write a server when
    there's no CLI, or when you need to constrain what's callable.

---

**Go deeper:** [MCP in Claude Code](https://code.claude.com/docs/en/mcp) ·
[Build a server](https://modelcontextprotocol.io/docs/develop/build-server)

**Next:** [Lab 10 — Agent SDK](10-agent-sdk.md)
