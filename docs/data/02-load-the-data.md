# Lab 2 — Get your finance data into it

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Terminal + Workbench</span>
  <span>Files: northwind-setup.sql + budget CSV</span>
</div>

## The problem

An empty database is no use to anyone. There are two ways data gets into one,
and you'll use both constantly: **running a script somebody gave you**, and
**importing a file you exported from somewhere else**.

This lab does both, and then ties the result back to a number you already know
so you can be sure nothing fell out on the way in.

## Before you start

- [ ] Lab 1 done — `mysql -u root -p` gets you a prompt
- [ ] [`northwind-setup.sql`](../files/db/northwind-setup.sql) downloaded into your `claude-labs` folder
- [ ] [`budget-vs-actual-q2-fy26.csv`](../files/budget-vs-actual-q2-fy26.csv) in the same folder

## Do this

### 1. Run the setup script

This creates the database and the tables, and fills three of them. Open a
terminal **in your `claude-labs` folder**, then:

```bash
mysql -u root -p
```

At the `mysql>` prompt:

```sql
SOURCE northwind-setup.sql
```

=== "macOS"

    If you started the terminal somewhere else, give the full path:

    ```sql
    SOURCE /Users/you/claude-labs/northwind-setup.sql
    ```

=== "Windows"

    Backslashes need escaping, so use forward slashes instead — MySQL accepts
    them on Windows:

    ```sql
    SOURCE C:/Users/you/claude-labs/northwind-setup.sql
    ```

    Paths with spaces go in double quotes.

### 2. Look at what you got

```sql
USE northwind;
SHOW TABLES;
SELECT * FROM customers;
```

Four tables. Three have data in them; `budget_actual_raw` is empty on purpose,
and you're about to fill it.

### 3. Import the CSV

=== "MySQL Workbench (easier)"

    1. Open Workbench and connect to your local server
    2. In the **Schemas** panel on the left, expand **northwind** → **Tables**
    3. Right-click **budget_actual_raw** → **Table Data Import Wizard**
    4. Browse to `budget-vs-actual-q2-fy26.csv`
    5. Choose **Use existing table**, leave the column mapping alone — the
       names already match — and run it

=== "Command line (faster)"

    `LOAD DATA LOCAL INFILE` is switched off at both ends by default, so
    there are three commands, not one.

    In the client you already have open:

    ```sql
    SET GLOBAL local_infile = 1;
    ```

    Then `exit`, and reconnect with the client flag:

    ```bash
    mysql --local-infile=1 -u root -p northwind
    ```

    ```sql
    LOAD DATA LOCAL INFILE 'budget-vs-actual-q2-fy26.csv'
    INTO TABLE budget_actual_raw
    FIELDS TERMINATED BY ',' ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES
    (month, department, account, budget, actual);
    ```

Use the wizard the first time so you can see what's happening. Use
`LOAD DATA` when the file is big — the wizard has a long-standing reputation
for crawling on large files, and your real extracts will be large.

### 4. Prove nothing fell out

Never trust a load you haven't tied out.

```sql
SELECT COUNT(*)    AS rows_loaded,
       SUM(budget) AS budget,
       SUM(actual) AS actual
FROM budget_actual_raw;
```

## What good looks like

The setup script finishes by printing its own row counts:

| status | customers | invoices | gl_entries |
|---|---|---|---|
| northwind is ready | 10 | 34 | 30 |

And the import ties to the figures the finance track already uses:

| | |
|---|---|
| Rows loaded | **129** |
| Total budget | **1,571,700.00** |
| Total actual | **1,606,810.05** |

If you got 130 rows, the header came in as data. If you got 128, a line was
dropped. If the totals are out, a column mapped to the wrong field. Either
way, empty the table and do it again — `TRUNCATE TABLE budget_actual_raw;`
gets you back to a clean start.

## Loading your own file

The awkward part of a real import is never the import. It's the fifteen
minutes of working out what type each column should be. Hand that to Claude.

!!! example prompt "Copy this prompt"

    ```text
    I want to load a CSV into MySQL 8.4. Here are the header row and
    the first five data rows:

    [paste them]

    Give me:
    1. A CREATE TABLE statement with sensible column types and
       lengths. Use DECIMAL for anything that is money - tell me the
       precision and scale you chose and why.
    2. The LOAD DATA LOCAL INFILE statement to match.
    3. A short list of what will break if the file has blank cells,
       dates in a different format, or thousands separators in the
       numbers.

    Explain the type choices in one line each. Assume I know
    accounting and not databases.
    ```

Then read the types before you run it. If Claude gave a money column `FLOAT`,
change it to `DECIMAL(12,2)` — Lab 8 shows what floats do to a control total.

<div class="yours" markdown>
**Now with your own extract.** Take a real CSV export — a trial balance, an AR
aging, a transaction dump — and get it into a table of its own with the prompt
above.

Then run the tie-out from step 4 against it. Row count and the total of the
one column you care about. If they don't match the source file, you have found
something out about your data, which is the point.
</div>

!!! warning "Gotcha"
    ```text
    ERROR 3948 (42000): Loading local data is disabled; this must be
    enabled on both the client and server sides
    ```

    Exactly what it says: `SET GLOBAL local_infile = 1;` on the server **and**
    `--local-infile=1` on the client. Doing one without the other gets you the
    identical message, which is why people go round twice.

!!! tip "Windows line endings"
    A CSV saved on Windows ends its lines with `\r\n`. If your last column
    comes in with a stray character on the end, change
    `LINES TERMINATED BY '\n'` to `LINES TERMINATED BY '\r\n'`.

---

**Go deeper:** [LOAD DATA statement](https://dev.mysql.com/doc/refman/8.4/en/load-data.html) ·
[Workbench data import](https://dev.mysql.com/doc/workbench/en/wb-admin-export-import-table.html)

**Next:** [Lab 3 — Ask the database your first question](03-first-queries.md)
