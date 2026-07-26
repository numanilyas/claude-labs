# Lab 5 — Why the customer name isn't stored 34 times

<div class="lab-meta">
  <span class="time">15 min</span>
  <span>Terminal or Workbench</span>
  <span>Database: northwind</span>
</div>

## The problem

Look at what you imported in Lab 2:

```sql
SELECT department, COUNT(*) FROM budget_actual_raw GROUP BY department;
```

Six department names, 129 rows. "Marketing" is written out 24 separate times.
That's what a spreadsheet is: one wide sheet where every fact is repeated on
every row it applies to.

It works until the day Marketing is renamed to Growth. Now you have 24 places
to change and one you'll miss, and next quarter's report shows both a
Marketing and a Growth line, and nobody can tell whether that's a restatement
or a mistake.

Storing a fact once, in one place, is the whole idea. Everything else —
tables, keys, joins — is machinery for making that practical.

## Before you start

- [ ] Labs 2 to 4 done
- [ ] `USE northwind;`

## Do this

### 1. Give each fact one home

Run these together. Two tables, each created and then filled from the
distinct values already sitting in your flat import.

```sql
CREATE TABLE departments (
  dept_id   INT AUTO_INCREMENT PRIMARY KEY,
  dept_name VARCHAR(40) NOT NULL UNIQUE
);

INSERT INTO departments (dept_name)
SELECT DISTINCT department FROM budget_actual_raw ORDER BY department;

CREATE TABLE accounts (
  account_id   INT AUTO_INCREMENT PRIMARY KEY,
  account_name VARCHAR(60) NOT NULL UNIQUE
);

INSERT INTO accounts (account_name)
SELECT DISTINCT account FROM budget_actual_raw ORDER BY account;
```

`PRIMARY KEY` means "this column identifies the row, and no two rows share a
value". `UNIQUE` on the name means you cannot accidentally create Marketing
twice. Those two constraints are most of what a database gives you that a
spreadsheet doesn't.

### 2. Point at them instead of repeating them

```sql
CREATE TABLE budget_actual (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  period     CHAR(7)       NOT NULL,
  dept_id    INT           NOT NULL,
  account_id INT           NOT NULL,
  budget     DECIMAL(12,2) NOT NULL,
  actual     DECIMAL(12,2) NOT NULL,
  FOREIGN KEY (dept_id)    REFERENCES departments (dept_id),
  FOREIGN KEY (account_id) REFERENCES accounts (account_id)
);

INSERT INTO budget_actual (period, dept_id, account_id, budget, actual)
SELECT r.month, d.dept_id, a.account_id, r.budget, r.actual
FROM budget_actual_raw r
JOIN departments d ON d.dept_name    = r.department
JOIN accounts    a ON a.account_name = r.account;
```

A **foreign key** is a promise the database enforces: `dept_id` must be a real
department. Try to insert a budget line for department 99 and it refuses. That
promise is why the rename problem goes away — the name lives in exactly one
row of `departments`, and everything else points at its ID.

### 3. Put it back together with a JOIN

The names are gone from the numbers table, which is the point, and also
inconvenient. `JOIN` is how you get them back:

```sql
SELECT d.dept_name,
       a.account_name,
       SUM(b.budget)                 AS budget,
       SUM(b.actual)                 AS actual,
       SUM(b.actual) - SUM(b.budget) AS variance
FROM budget_actual b
JOIN departments d ON d.dept_id    = b.dept_id
JOIN accounts    a ON a.account_id = b.account_id
GROUP BY d.dept_name, a.account_name
ORDER BY variance DESC
LIMIT 5;
```

Read `JOIN departments d ON d.dept_id = b.dept_id` as: for each budget row,
go and fetch the department row with the matching ID. `b`, `d` and `a` are
just short names so you don't type the full table name every time.

### 4. Tie it out

You just moved 129 rows through two joins. Prove nothing changed:

```sql
SELECT COUNT(*) AS rows_, SUM(budget) AS budget, SUM(actual) AS actual
FROM budget_actual;
```

### 5. Now the one you'd actually be asked for

`customers` and `invoices` were already built this way. Same pattern:

```sql
SELECT c.customer_name,
       c.credit_limit,
       COUNT(i.invoice_no)         AS open_invoices,
       SUM(i.amount)               AS owed,
       SUM(i.amount) - c.credit_limit AS over_by
FROM customers c
JOIN invoices  i ON i.customer_id = c.customer_id
GROUP BY c.customer_name, c.credit_limit
HAVING SUM(i.amount) > c.credit_limit
ORDER BY over_by DESC;
```

Who's over their credit limit. One query, and it's right every time you run
it.

## What good looks like

After step 4:

| | |
|---|---|
| Departments | **6** |
| Accounts | **8** |
| Rows in `budget_actual` | **129** |
| Total budget | **1,571,700.00** |
| Total actual | **1,606,810.05** |

Identical to Lab 2. If the row count dropped, a join found no match and
silently threw the row away — which is Lab 6, and it's the single most
common way people lose money in a database.

Step 5 gives exactly three customers:

| Customer | Credit limit | Owed | Over by |
|---|---|---|---|
| Dunmore Wholesale | 150,000.00 | 221,230.18 | 71,230.18 |
| Ironwood Partners | 100,000.00 | 122,398.43 | 22,398.43 |
| Copperfield & Sons | 100,000.00 | 115,141.15 | 15,141.15 |

## The three-sentence version of "relational"

Facts about one kind of thing live in one table, one row each. Rows carry an
ID so other tables can refer to them without copying them. `JOIN` follows
those references at query time.

That's it. The rest is detail you can pick up when you need it.

!!! example prompt "Copy this prompt"

    ```text
    I'm an accountant learning MySQL. Here is a flat spreadsheet
    export - header row plus five sample rows:

    [paste them]

    Show me how you'd split this into proper tables. For each one:
    the CREATE TABLE statement, what its primary key is and why, and
    which columns become foreign keys.

    Then give me the JOIN that puts it back together so the result
    looks like my original spreadsheet, and a query that proves the
    row count and column totals are unchanged.

    Be honest about anything in my data that makes this awkward.
    ```

That last line earns its place. Real exports have a column that means two
different things depending on the row, and you want to be told.

<div class="yours" markdown>
**Now with your own export.** Take the flat file you loaded in Lab 2 and run
the prompt above against its header and a few rows.

You probably won't rebuild your warehouse this afternoon. That isn't the
point. The point is being able to look at a schema someone shows you and know
what the arrows mean — which is most of what "talking to the data team"
requires.
</div>

!!! warning "Gotcha"
    `budget_actual_raw` is still sitting there with the department names in it.
    It's now a *copy*, and copies drift — rename a department in one and the
    other doesn't know. In a real system you'd load into a staging table,
    normalise, and drop the staging table. Leave it for now; Lab 9's script
    reads the normalised tables, not this one.

!!! tip "Watch a foreign key do its job"
    ```sql
    INSERT INTO budget_actual (period, dept_id, account_id, budget, actual)
    VALUES ('2026-07', 99, 1, 100, 100);
    ```

    It's refused. Department 99 doesn't exist, so the row can't be created.
    That's the database keeping your data honest without you writing any
    validation.

---

**Go deeper:** [JOIN syntax](https://dev.mysql.com/doc/refman/8.4/en/join.html) ·
[Foreign key constraints](https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html)

**Next:** [Lab 6 — The query that looks right and isn't](06-queries-that-lie.md)
