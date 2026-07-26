# Lab 7 — Get Python talking to the database

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Terminal</span>
  <span>File: first_query.py</span>
</div>

## The problem

SQL answers questions. It won't email the answer, won't format it, won't loop
over twelve months, and won't stop halfway through because a control total
didn't tie.

Python does those. Not because it's better at data — it isn't, and Lab 10 is
about exactly that — but because it's the thing that sits around the query and
turns an answer into a process.

## Before you start

- [ ] Lab 2 done — Python needs a database to talk to
- [ ] Your MySQL root password
- [ ] A terminal open in your `claude-labs` folder

## Do this

### 1. Install Python

Get 3.14 or later from [python.org/downloads](https://www.python.org/downloads/).

=== "macOS"

    Run the installer. It puts `python3` and `pip3` on your PATH for you.

    One extra step people skip: open **Applications → Python 3.14** and
    double-click **Install Certificates.command**. Without it, `pip install`
    fails later with an SSL certificate error that looks like a network
    problem and isn't.

    ```bash
    python3 --version
    ```

=== "Windows"

    On the **first** installer screen, tick the box that adds Python to your
    PATH before clicking Install. It's easy to miss and annoying to fix
    afterwards.

    ```powershell
    python --version
    ```

    If that says "Python was not found", the box wasn't ticked. Re-run the
    installer and choose Modify.

### 2. Make a virtual environment

A virtual environment is a folder holding the packages for one project, so
installing something for this work can't break something else. Make one per
project, always.

=== "macOS"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

=== "Windows PowerShell"

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

=== "Windows cmd"

    ```bat
    python -m venv .venv
    .venv\Scripts\activate.bat
    ```

Your prompt now starts with `(.venv)`. That's how you know it's on. `deactivate`
turns it off.

### 3. Install the driver

```bash
pip install mysql-connector-python
```

That's Oracle's official MySQL driver. It works with MySQL 8's default
authentication without anything extra, which is the main reason to start with
it rather than the alternatives.

### 4. Run a query from code

Download [`first_query.py`](../files/db/first_query.py) into your folder, or
type it out — it's short enough to be worth typing once.

```python title="first_query.py"
import getpass
import os

import mysql.connector

PASSWORD = os.environ.get("MYSQL_PASSWORD") or getpass.getpass("MySQL password: ")

cnx = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=PASSWORD,
    database="northwind",
)

QUERY = """
    SELECT aging_bucket,
           COUNT(*)    AS invoices,
           SUM(amount) AS total
    FROM invoices
    GROUP BY aging_bucket
    ORDER BY total DESC
"""

with cnx.cursor() as cur:
    cur.execute(QUERY)
    print(f"{'Bucket':<10}{'Invoices':>10}{'Total':>16}")
    for bucket, invoices, total in cur.fetchall():
        print(f"{bucket:<10}{invoices:>10}{total:>16,.2f}")

    cur.execute("SELECT COUNT(*), SUM(amount) FROM invoices")
    n, grand = cur.fetchone()
    print(f"{'TOTAL':<10}{n:>10}{grand:>16,.2f}")

cnx.close()
```

```bash
python first_query.py
```

## What good looks like

```text
Bucket      Invoices           Total
Current           19      665,109.08
31-60              9      255,969.98
90+                4      116,829.32
61-90              2       58,443.91
TOTAL             34    1,096,352.29
```

Same numbers as Lab 4, because it's the same query. All Python did was ask.
That's worth noticing before Lab 8 makes it look like more than it is.

## Reading the code

Four things are happening, and they're the same four every time you do this:

| Line | What it's for |
|---|---|
| `connect(...)` | Open a connection. Host, user, password, database. |
| `cnx.cursor()` | A cursor is the thing you send a query through and read results back from. |
| `cur.execute(QUERY)` | Send it. |
| `cur.fetchall()` | Pull the rows back, as a list of tuples. |

The `getpass` line keeps your password out of the file. Set `MYSQL_PASSWORD`
as an environment variable and it won't even prompt.

## When it goes wrong

!!! example prompt "Copy this prompt"

    ```text
    I'm running Python 3.14 on [macOS / Windows] with
    mysql-connector-python against a local MySQL 8.4 server.

    My script:
    [paste it]

    The error, in full:
    [paste it, including the traceback]

    Explain what the error means in plain English first, then tell me
    the fix. If the fix is a command, say what it will change on my
    machine before I run it.
    ```

<div class="yours" markdown>
**Now point it at your own table.** Change `database=` and swap the query for
one of yours from Lab 3.

Then do the thing that makes this worth having: put a `print()` of your
control total at the top, and don't look at the rest of the output until the
control total is right. That habit, established now, is what stops a script
from quietly producing wrong numbers for six months.
</div>

!!! warning "PowerShell won't run the activate script"
    ```text
    ... cannot be loaded because running scripts is disabled on this system.
    ```

    Windows blocks local scripts by default. This fixes it for your account
    only and doesn't need admin:

    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

!!! note "The `py` launcher"
    Older Windows guides tell you to run `py script.py`. From Python 3.14 the
    old launcher has been superseded by the Python Install Manager, so what
    `py` is and where it comes from depends on how you installed. Inside an
    active virtual environment `python script.py` is unambiguous — use that.

!!! danger "Don't put the password in the file"
    A script with a live password in it gets emailed, committed, and copied
    onto a shared drive. `getpass` prompts for it; an environment variable
    keeps it out of the file entirely. Either is fine. Typing it into line 6
    is not.

---

**Go deeper:** [MySQL Connector/Python guide](https://dev.mysql.com/doc/connector-python/en/) ·
[Python venv](https://docs.python.org/3/library/venv.html)

**Next:** [Lab 8 — Turn a query into a spreadsheet](08-query-to-spreadsheet.md)
