# Lab 1 — Get a database running on your laptop

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Terminal</span>
  <span>Nothing to open yet</span>
</div>

## The problem

The extract is 400,000 rows. Excel opens it in ninety seconds, recalculates in
four minutes, and crashes when you pivot it. Someone says "put it in a
database" and the conversation ends there, because a database sounds like a
thing you have to raise a ticket for.

It isn't. MySQL is free, it installs on a laptop in about a quarter of an
hour, and it will hold that extract without noticing.

## Before you start

- [ ] Admin rights on your machine — the installer needs them
- [ ] About 15 minutes, most of which is the download
- [ ] Somewhere to write down a password you must not lose

## Do this

### 1. Download MySQL Community Server 8.4 LTS

Go to [dev.mysql.com/downloads/mysql](https://dev.mysql.com/downloads/mysql/)
and pick **8.4** — not 9.x. 8.4 is the long-term support release: premier
support runs to 2029 and extended support to 2032. The 9.x series changes
behaviour every quarter, which is the last thing you want underneath a
month-end process.

=== "macOS"

    Choose macOS in the OS dropdown, then the DMG matching your chip — the
    listings are labelled ARM for Apple Silicon and x86 for Intel. Check
    **About This Mac** if you're not sure which you have.

=== "Windows"

    Use the [MySQL Installer for Windows](https://dev.mysql.com/downloads/installer/).
    It's a single MSI that installs the server and can install Workbench at
    the same time.

=== "Homebrew (macOS)"

    If you already have Homebrew, skip the download entirely:

    ```bash
    brew install mysql@8.4
    brew services start mysql@8.4
    ```

    Homebrew installs MySQL **with no root password set**. Connect with
    `mysql -u root` and no password, then run `mysql_secure_installation` to
    set one. Skip to step 3.

### 2. Run the installer

Both installers make you set a **root password**. Write it down somewhere you
will still have it in six months. There is a recovery procedure and you do not
want to be learning it at 6pm on a reporting day.

=== "macOS"

    Take the installer's defaults for password encryption. It also installs a
    **MySQL** pane in System Settings (System Preferences on older macOS),
    which is where you start and stop the server. Leave the "start at startup"
    option on unless you have a reason not to.

=== "Windows"

    Accept the default of running MySQL **as a Windows service** starting
    automatically. That means it's running whenever your machine is, and you
    never think about it again.

### 3. Put `mysql` on your PATH

Neither installer does this for you. This is the step that causes most of the
"I installed it and nothing works" messages.

=== "macOS"

    ```bash
    echo 'export PATH="/usr/local/mysql/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

=== "Windows"

    Search the Start menu for **environment variables** and open the system
    environment variables editor. Find **Path** under System variables, edit
    it, and add a new entry:

    ```text
    C:\Program Files\MySQL\MySQL Server 8.4\bin
    ```

    Close and reopen your terminal afterwards. It won't pick up the change in
    a window that was already open.

### 4. Connect

```bash
mysql -u root -p
```

It asks for the password from step 2. Nothing echoes as you type — that's
normal, not a frozen terminal. You should land at a `mysql>` prompt.

```sql
SELECT VERSION();
SHOW DATABASES;
```

Type `exit` to leave.

### 5. Install MySQL Workbench

[dev.mysql.com/downloads/workbench](https://dev.mysql.com/downloads/workbench/)
— on Windows the MySQL Installer will have offered it already.

Workbench is a window with a query box, a results grid and a list of your
tables down the side. You don't need it for anything in this track, but seeing
your tables in a list makes the first few labs considerably less abstract, and
Lab 2 uses its CSV import wizard.

## What good looks like

```text
mysql> SELECT VERSION();
+-----------+
| VERSION() |
+-----------+
| 8.4.x     |
+-----------+
1 row in set (0.00 sec)
```

`SHOW DATABASES;` lists four: `information_schema`, `mysql`,
`performance_schema`, `sys`. Those are MySQL's own bookkeeping. Yours comes in
Lab 2.

## When it goes wrong

It will, and the error text is usually the whole answer. Give it to Claude
rather than to a search engine — a search engine gives you six people with a
superficially similar problem, and Claude will at least ask what you ran.

!!! example prompt "Copy this prompt"

    ```text
    I'm installing MySQL 8.4 on [macOS / Windows] and I'm stuck.

    What I ran:
    [paste the exact command]

    What I got back:
    [paste the exact error, all of it]

    I'm new to this, so tell me what the error actually means before
    you tell me what to type, and explain anything you want me to run
    before I run it.
    ```

That last sentence matters. You are about to be handed commands that change
your machine's configuration, and "I don't know what that did" is not a
position you want to be in on your own laptop.

<div class="yours" markdown>
**Now find out what you're actually up against.** Before Lab 2, look at the
biggest file you regularly wrestle with — the GL extract, the transaction
dump, the thing that makes Excel think. Check how many rows it has and how
many columns.

Keep that number in mind. Everything in this track is aimed at it.
</div>

!!! warning "Gotcha"
    `command not found: mysql` or `'mysql' is not recognized` after a
    successful install means step 3 didn't take. On Windows, the most common
    cause is a terminal window you opened before editing the PATH. Close it
    and open a new one.

!!! danger "The root password"
    Losing it means stopping the server, restarting it in a mode that skips
    authentication, and resetting the password by hand. It's recoverable and
    it's tedious. Write it down now.

---

**Go deeper:** [Installing MySQL on macOS](https://dev.mysql.com/doc/refman/8.4/en/macos-installation-pkg.html) ·
[Installing MySQL on Windows](https://dev.mysql.com/doc/refman/8.4/en/windows-installation.html)

**Next:** [Lab 2 — Get your finance data into it](02-load-the-data.md)
