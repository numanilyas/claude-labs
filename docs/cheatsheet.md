---
hide:
  - navigation
---

# Cheat sheet

One page. Print it, or keep it in a tab.

## The four parts of a prompt that works

1. **Who you are and what the situation is** — role, company type, what just happened
2. **The actual data** — attach it, don't describe it
3. **What you want back** — format, length, structure
4. **What not to do** — the highest-value line, and the one people leave out

Stuck? *"Before you answer, ask me any questions you need to give a good answer."*

## Phrases worth stealing

| Say this | To get |
|---|---|
| "Compute with code, don't estimate" | Exact figures instead of plausible ones |
| "Show me the rows behind that number" | Something you can actually check |
| "Show me the table first, then write" | A chance to catch bad numbers before good prose |
| "Use a real SUM formula, not a hardcoded number" | A spreadsheet that survives the next row |
| "If it isn't there, leave it empty and don't guess" | Blanks instead of invented data |
| "Flag anything I should look at" | The exceptions, which are the actual work |
| "Mark inferences with [inferred]" | Visible seams between fact and guess |
| "End with what you could not verify" | Known unknowns instead of silent ones |
| "If you find nothing substantive, say so" | An empty list instead of invented findings |
| "Report gaps, not style preferences" | A review worth reading |

## Verify before you send

Three moves, ninety seconds:

1. **Show the source** — "show me the exact rows, and how many you read"
2. **Re-derive** — "recompute a different way without referring to your last answer"
3. **Tie out** — to a total you already know

The highest-yield question: **"What did you have to decide in order to answer this?"**
Errors cluster in interpretation, not arithmetic.

!!! danger "The rule"
    If you can't verify it, don't send it.

## Where things go

| | |
|---|---|
| **Chat** | Questions, drafting, analysis of files you attach |
| **Project** | Context you're tired of repeating. Instructions + knowledge, shared by every chat in it |
| **Cowork** | Anything that touches a folder or produces files |
| **Skill** | A procedure you follow more than twice a quarter |
| **Scheduled task** | The recurring noticing — never the deciding |

Two things that catch people:

- **Chats in a Project don't see each other.** Only project knowledge and instructions are shared.
- **Chat memory doesn't reach Cowork.** Tell it again, or put it in the folder.

## Limits

| | |
|---|---|
| File size, with code execution | ~30 MB |
| Files per chat | 20 |
| PDF pages | 1,000 — but **visual** analysis only if the whole PDF is ≤100 pages |
| Project knowledge | 30 MB per file |

Cowork burns allowance much faster than chat. **Settings → Usage.**

---

## Claude Code

```text
/usage      plan bars and 24h/7d breakdown
/model      which model - and the source of truth for what you can pick
/clear      wipe conversation, keep session. Free. Use it constantly.
/context    what's loaded and what it costs
/init       generate a starter CLAUDE.md
/rewind     restore conversation, code, or both
/code-review    review the branch
/batch <x>  decompose a migration and fan out
```

<kbd>Shift</kbd>+<kbd>Tab</kbd> cycles permission modes · <kbd>Ctrl</kbd>+<kbd>G</kbd> edits the plan · <kbd>Esc</kbd> stops without losing context

**Before your first login:** `unset ANTHROPIC_API_KEY`

### The loop

**Explore → Plan → Implement → Commit.** Don't leave explore until Claude's
description of the code matches yours. Skip the plan if you could describe the
diff in one sentence.

### Where things go

| You want | Use |
|---|---|
| A fact, always relevant | `CLAUDE.md` (under 200 lines) |
| A fact, only some paths | `.claude/rules/` with `paths:` |
| A procedure with steps | `.claude/skills/<name>/SKILL.md` |
| Must happen every time | A hook |
| A big search, or an independent review | A subagent |

### Habits

- Review in a **fresh session** — never the one that wrote the code
- Reproduce with a **failing test** before fixing
- `git diff` the **test files** before committing
- After two failed corrections, `/clear` and rewrite the prompt
- Checkpoints don't cover shell-driven changes. Commit first.

## SQL and Python

### The words that do most of the work

```sql
SELECT   which columns
FROM     which table
WHERE    which rows          -- filters rows, before grouping
GROUP BY one output row per  -- everything else must be SUM/COUNT/MAX
HAVING   which groups        -- filters groups, after grouping
ORDER BY DESC / ASC
LIMIT    stop after n
```

### The control total

```sql
SELECT COUNT(*), SUM(amount) FROM your_table;
```

No joins, no filters, no grouping. Run it first. Every aggregate you build
afterwards has to tie back to it, and if it doesn't you have a finding.

### How a query lies

| | Symptom | Catch it with |
|---|---|---|
| `INNER JOIN` drops unmatched rows | Total is quietly light | `LEFT JOIN` + `WHERE right.id IS NULL` |
| `NULL` and `''` aren't the same | A filter finds most of them | `WHERE col IS NULL OR col = ''` |
| `GROUP BY` splits the no-value rows | They scatter across two easy-to-skim lines | `GROUP BY COALESCE(NULLIF(col,''),'(not set)')` |
| A join fans out | Total is quietly heavy | Compare `COUNT(*)` before and after |

The first three are in the Data Track's sample database. `NULL = NULL` is not
true — always `IS NULL`.

### SQL or Python

**Reduce in SQL, shape and deliver in Python.** Filtering, joining, grouping
and all money arithmetic belong in the query — `DECIMAL` is exact and pandas
turns it into a float. Formatting, looping, Excel output, anything touching a
second source, and anything conditional belong in Python.

If you're filtering or grouping a big DataFrame in pandas, that work belonged
in the query.

### Connecting

```python
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://user:pw@127.0.0.1/dbname")
query = text("SELECT ... WHERE period = :period")

with engine.connect() as cnx:
    df = pd.read_sql(query, cnx, params={"period": "2026-06"})
```

`text()` and `params` are a pair — named placeholders don't work without it.
Never build SQL with an f-string.
