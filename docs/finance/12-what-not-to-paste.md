# Lab 12 — What not to paste into Claude

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Judgment</span>
  <span>No files needed</span>
</div>

## The problem

Eleven labs taught you to put your data into Claude. This one is about which
data, and it's the lab most likely to matter to somebody other than you.

!!! danger "Read this first"
    **Your organisation's policy is the actual answer.** Nothing on this page
    overrides it. If your company has rules about where financial data,
    customer information, or employee records may go, those rules govern —
    including the possibility that the answer is "none of this, on a personal
    account."

    If you don't know whether a policy exists, that's the first thing to go
    find out. Ask before you paste, not after.

## The thing about a Pro account

A Pro subscription is a **personal** plan. That has consequences people don't
always think through:

- It isn't administered by your company. No admin controls it, no admin can
  audit it, and no admin can retrieve or delete what's in it.
- Cowork activity in particular isn't captured in the audit and export tooling
  that business plans have.
- If you leave, your chat history leaves with you — including whatever company
  data is in it.

None of that means "never use it for work." It means the appropriate ceiling
for a personal account is lower than for a company-administered one, and your
employer may have opinions you haven't asked for yet.

## A workable sorting rule

Not a policy — a starting point for the conversation with whoever writes the
policy.

| | Examples | Reasonable on a personal Pro account? |
|---|---|---|
| **Fine** | Public filings, published data, your own templates, synthetic data like this curriculum's | Yes |
| **Think** | Internal management reports, budgets, aggregated actuals, anonymised vendor data | Usually — check your policy |
| **Don't, without explicit sign-off** | Named customer records, employee salaries, bank account and card numbers, anything under NDA, unreleased results of a public company, personal data of identifiable people | No |

The unreleased-results one catches people out. If you work for a listed company
and the quarter isn't announced, those numbers are material non-public
information and the rules around them are not about AI at all.

## Three practical moves

**Aggregate before you share.** You rarely need row-level customer data to
answer the question. A department-level summary usually gets the same analysis
with none of the exposure. Do the aggregation locally, share the aggregate.

**Substitute identifiers.** Replace customer names with `CUST-001`, `CUST-002`
and keep the mapping in a file on your machine. The analysis is identical;
Claude never sees a name. This takes about a minute in Excel and solves most
of the "think" row above.

**Use incognito for the one-offs.** For a genuinely sensitive question you need
answered once, an incognito chat isn't saved to your history and isn't used to
build Claude's memory of you. Look for the ghost icon. Useful, but it is not a
substitute for policy — the data still goes to the service.

## The practical limits, while we're here

Worth knowing so you design around them instead of discovering them at 6pm:

| | |
|---|---|
| File size, once code execution is involved | about **30 MB** |
| Files per chat | up to **20** |
| PDF pages | up to **1,000** — but see below |
| Project knowledge | **30 MB** per file |

**The PDF one is a cliff, not a limit.** A PDF of **100 pages or fewer** gets
both text and visual analysis — layout, tables, charts. From **101 pages
onwards, the whole document is text-only** and no visual elements are read at
all. It doesn't analyse the first hundred and give up; it switches mode for
the entire file.

That matters for the kind of work in Labs 5 and 6. A 300-page statement pack
uploaded whole will have its tables read as a stream of text with no sense of
column structure. **Split it into chunks of 100 pages or fewer** and you get
meaningfully better extraction.

A full-year GL export will also blow past 30 MB. Split it by period or by
account, or aggregate before you upload — which is the same advice as above,
for a different reason.

<div class="yours" markdown>
**Do this today.** Find out what your organisation's actual policy is on
putting company data into AI tools, and whether a personal Claude account is
covered by it.

If there isn't one, you're now one of the people best placed to say what it
should look like — you've spent two hours learning exactly what these tools do
with a file.
</div>

---

## You've finished the finance track

Twelve labs. What you can now do that you couldn't this morning:

- Write a prompt that gets a usable answer first time
- Hand Claude a file and get exact, checkable figures back
- Set up a Project so you stop re-explaining your business
- Clean a hostile export, extract a stack of PDFs, and reconcile two sources
- Turn analysis into a memo somebody will read
- Save a working procedure as a skill, and your house style as another
- Schedule the recurring noticing
- Verify a number before you stake your name on it

**The part that actually matters now** is doing it on your own work. The
technique doesn't stick from the sample data — it sticks the third time you
use it on something real and it saves you an afternoon.

Pick one thing you do every month. Do it with Claude next month. That's it.

---

**Where to go next**

- [The cheat sheet](../cheatsheet.md) — one page, print it
- [The prompt library](../prompt-library.md) — every prompt from the curriculum
- [Developer track](../dev/index.md) — if you write code too
