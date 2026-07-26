# Data Track

Ten labs for people who live in spreadsheets and have hit the ceiling. Six on
MySQL and four on Python, the last of which is about knowing which of the two
to reach for.

No programming background assumed. You will use a terminal, and that's fine —
by Lab 3 it's just a box you type questions into.

## Why these are one track and not two

Python is only interesting here because there's a database behind it. Every
Python lab connects to the database you build in Labs 1 and 2, and Lab 9 queries
the tables you normalise in Lab 5. Run them in order the first time.

## Before you start

- A laptop you can install software on. Both parts need admin rights for the
  installers — if your machine is locked down, get that sorted first.
- The [sample data](../sample-data.md), unzipped into a folder you can find.
- About 2 GB of disk. MySQL and Python together are not small.
- A Claude account. Every lab uses Claude to write, explain or check
  something — the [chat interface](https://claude.ai) is enough, no Cowork
  and no desktop app required.

!!! note "This track doesn't need Claude Pro"
    Unlike the finance track, nothing here depends on Cowork, file creation or
    scheduled tasks. The free plan will get you through it, though you'll hit
    limits faster.

## Part one — the database

Getting MySQL onto your machine and getting answers out of it.

| | Lab | What you'll be able to do |
|---|---|---|
| 1 | [Get a database running on your laptop](01-install-mysql.md) | Install MySQL, connect to it, prove it works |
| 2 | [Get your finance data into it](02-load-the-data.md) | Run a SQL script, import a CSV, tie the totals out |
| 3 | [Ask the database your first question](03-first-queries.md) | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT` |
| 4 | [Totals and subtotals without a pivot table](04-group-and-total.md) | `GROUP BY`, `SUM`, `HAVING` — and find a duplicate payment |
| 5 | [Why the customer name isn't stored 34 times](05-one-table-is-not-enough.md) | Tables, keys, joins, and what "relational" actually means |
| 6 | [The query that looks right and isn't](06-queries-that-lie.md) | Catch the three ways a clean-looking query gives a wrong total |

## Part two — Python

The database answers questions. Python is how you turn an answer into
something you can send someone, every month, without doing it by hand.

| | Lab | What you'll be able to do |
|---|---|---|
| 7 | [Get Python talking to the database](07-install-python.md) | Install Python, make a virtual environment, run a query from code |
| 8 | [Turn a query into a spreadsheet](08-query-to-spreadsheet.md) | pandas, SQLAlchemy, a formatted `.xlsx`, and a tie-out that fails loudly |
| 9 | [The month-end pack, as a script you rerun](09-month-end-script.md) | One command, three months, three files |
| 10 | [SQL or Python?](10-sql-or-python.md) | Stop guessing which tool the job wants |

---

!!! tip "If you only have forty minutes"
    Labs 2, 4 and 6. Loading data, aggregating it, and learning how a query
    lies to you is the useful core. Everything else builds on those three.

    You'll need Lab 1 done first, which is why it isn't on the list — an
    install isn't learning.

!!! quote "How to use these"
    Type the SQL rather than pasting it, at least in Labs 3 and 4. It's four
    extra minutes and it's the difference between recognising syntax and being
    able to write it. Paste the longer scripts.

## One idea underneath all ten

A spreadsheet stores answers. A database stores facts and computes answers on
demand.

That sounds like a distinction without a difference until the fact changes.
In a spreadsheet, a corrected customer name has to be found and fixed in every
row it appears in, and the one you miss is the one that shows up in the board
pack. In a database it's stored once, so there's nothing to miss.

Everything in Part one is a consequence of that: keys exist so a fact has one
home, joins exist so you can still see it from everywhere, and Lab 6 is what
happens when a fact has no home at all.
