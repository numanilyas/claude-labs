# Lab 10 — Monday morning, before you're in

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Cowork · Scheduled tasks</span>
</div>

## The problem

The reconciliation from Lab 6 and the variance analysis from Lab 7 both have
the same shape: same files, same question, every period. You've automated the
*doing*. The remaining manual step is remembering to do it.

A **scheduled task** is a Cowork task that runs on a timetable and leaves the
result waiting for you.

## Before you start

- [ ] Cowork open
- [ ] The sample files uploaded **to your Claude account** — see the note below

!!! warning "Scheduled tasks can't reach a folder on your computer"
    This is the constraint that shapes the whole lab. Scheduled tasks run
    remotely, on Anthropic's infrastructure, on their own cadence. They work
    with your connectors and with files saved to your Claude account — **not**
    with a folder on your laptop.

    So for this lab, put the sample data somewhere the task can actually see
    it: a Project's knowledge base is the simplest option, or a connected
    service like Google Drive if you have one.

    (The docs are a little inconsistent here — one line suggests a task
    needing local files will run locally instead. Design around the
    restriction rather than betting on the exception.)

## Do this

1. Click **Scheduled** in the Cowork sidebar.
2. Click **New task**.
3. Choose **Set up manually**.
4. Fill it in:

| Field | Value |
|---|---|
| Name | `Monday cash flash` |
| Frequency | Weekly, Monday, 07:00 |
| Approval mode | Manual, for now |

5. For the prompt, paste this:

!!! example prompt "Copy this prompt"

    ```text
    Every Monday, review the ledger and receivables data available to
    you and produce a short cash and exceptions summary for the week
    just ended.

    Give me a single markdown file, under 200 words:

    1. Closing cash per the ledger, and the change from the prior week
    2. Any transaction over 25,000
    3. Any item that appears twice with the same amount, date and
       reference
    4. Any receivable that has gone past 60 days since last week
    5. A one-line "nothing unusual" if none of the above found anything

    If data I'd expect is missing, say so at the top rather than
    working around it silently.

    Do not send this anywhere. Leave the result for me to read.
    ```

6. **Save.**

!!! tip "Create with Claude"
    The other route — **New task → Create with Claude** — has Claude interview
    you and write the schedule itself. Faster if you're not sure what to ask
    for. The manual route is better here because you can see exactly what's
    being saved.

## Test it before you trust it

Don't wait until Monday. Run it once by hand — trigger it, or paste the same
prompt into a normal Cowork task — and read the output.

A scheduled task that produces something subtly wrong every Monday for two
months is worse than no scheduled task, because you'll have stopped reading it
carefully by week three.

## What good looks like

Under 200 words. Genuinely useful or genuinely says "nothing unusual". If it
produces a page and a half of restated data, the prompt needs tightening — a
weekly report you skim is a weekly report you'll eventually ignore.

## What to schedule, and what not to

**Good candidates** — recurring, rule-based, and it's fine if you read the
result an hour later:

- Weekly exception scans, like this one
- Aging deltas: who moved into 60+ this week
- "Has anything in this folder changed since last week"
- Month-end checklist status

**Bad candidates:**

- Anything that sends an email or files something without you reading it first
- Anything where being wrong is expensive and nobody's checking
- Anything needing judgment about a specific situation

The rule: **schedule the noticing, not the deciding.**

<div class="yours" markdown>
**Now with your own routine.** Pick the recurring thing you most often forget
until someone asks. Write the prompt so that a normal week produces one line.

If it produces a page every week, you'll stop reading it, and then it's worse
than nothing.
</div>

!!! danger "The unmonitored-run risk"
    A scheduled task runs when you aren't watching. If it reads documents that
    came from outside your organisation — supplier emails, downloaded
    attachments, anything from the web — instructions hidden in those documents
    can influence what it does. This is a real attack, not a theoretical one.

    Keep scheduled tasks on **manual approval**, pointed at folders you
    control, doing read-and-report work rather than send-and-act work.

!!! tip "The good news about running remotely"
    Because the task runs on Anthropic's infrastructure rather than your
    machine, it fires on schedule whether or not your laptop is open. A 07:00
    Monday task runs at 07:00 Monday, even if you're on a train.

    That's the flip side of not being able to reach your local folder: you
    trade filesystem access for reliability.

!!! warning "Gotcha"
    A scheduled task has the same skills, connectors and tools as an
    interactive one — including the ones you set up in Labs 8 and 9. Worth
    knowing both ways: your house-style skill will apply automatically, and so
    will anything else you've enabled and forgotten about.

---

**Go deeper:** [Schedule recurring tasks in Cowork](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)

**Next:** [Lab 11 — Verify before you send](11-verify-before-you-send.md)
