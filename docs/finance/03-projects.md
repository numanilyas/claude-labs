# Lab 3 — Stop repeating yourself

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Chat</span>
  <span>Projects</span>
</div>

## The problem

By your fourth chat you will have explained your chart of accounts, your fiscal
calendar, and the fact that "Ops" and "Operations" are the same department,
four times. A **Project** is where you say that once.

A Project is a folder of chats that share a knowledge base and a set of
instructions. Every chat inside it starts already knowing your context.

## Do this

1. In the left sidebar, go to **Projects** → **New project**.
2. Name it `FY26 Close`. (Claude doesn't read the name — it's for you.)
3. Click **Set project instructions** and paste the block below. Edit the parts
   in square brackets to match your actual situation, or leave them as-is for
   the lab.
4. Save.
5. Add the [`budget-vs-actual-q2-fy26.csv`](../files/budget-vs-actual-q2-fy26.csv)
   to **Project knowledge** using the **+** on the right.

!!! example prompt "Copy this into project instructions"

    ```text
    You are supporting the finance team at a mid-size distribution
    company. Our fiscal year runs [January to December]. We report in
    [USD]. Amounts in files are [in whole dollars unless a column header
    says otherwise].

    Departments: Sales, Marketing, Operations, Engineering, G&A,
    Customer Success. Source systems are inconsistent about naming —
    treat "Ops" and "Operations" as the same department, and ignore
    differences in capitalisation and trailing spaces in any department
    or account name.

    House conventions:
    - Negative numbers may appear in parentheses. Treat (1,234) as -1234.
    - "Variance" means actual minus budget. Positive variance on an
      expense line is unfavourable.
    - Materiality threshold for commentary is [$25,000] or [10%],
      whichever is larger.

    When you analyse anything:
    - Compute with code rather than estimating, and give exact figures.
    - State what you could not verify, in a separate short section at
      the end, rather than quietly leaving it out.
    - Never invent a cause for a variance. If a cause isn't in the data
      I gave you, say what you'd need to check.
    ```

Now start a chat **inside the project** and ask:

!!! example prompt "Copy this prompt"

    ```text
    Which departments are over budget for Q2, and by how much? Apply
    our materiality threshold.
    ```

## What good looks like

Notice what you didn't have to say: no explanation of what a variance is, no
warning about the parentheses, no threshold. It applied all of it.

Compare that to Lab 2, where you specified everything inline.

## The one rule people get wrong

**Chats inside a Project do not see each other.** If you work something out in
Monday's chat, Tuesday's chat knows nothing about it. Only the *project
knowledge* and the *instructions* are shared.

So when a chat produces something you'll need again — a mapping table, a set of
agreed definitions, last quarter's commentary — you have to put it into project
knowledge deliberately. It doesn't happen on its own.

<div class="yours" markdown>
**Now with your own context.** Build a project for something you do repeatedly.
Put into the instructions the three things you're most tired of explaining.

Good candidates for project knowledge: your chart of accounts, the last two
board decks (so it matches your tone), your close checklist, a glossary of
internal abbreviations nobody outside your team would know.
</div>

!!! warning "Gotcha"
    Project knowledge is not a filing cabinet. Everything in it competes for
    Claude's attention. Five well-chosen documents beat fifty, and a stale
    document is worse than no document — it will get used.

---

**Go deeper:** [What are Projects?](https://support.claude.com/en/articles/9517075-what-are-projects)

**Next:** [Lab 4 — Clean up an export nobody documented](04-messy-excel.md)
