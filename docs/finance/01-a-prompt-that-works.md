# Lab 1 — A prompt that works

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Chat</span>
  <span>No files needed</span>
</div>

## The problem

Most disappointing answers from Claude are disappointing because the question
was under-specified, and the person asking didn't notice — they had all the
context in their head and forgot they hadn't said any of it out loud.

You're going to feel this directly rather than take my word for it.

## Do this

Open a **new chat**. Paste the bad version first.

!!! example prompt "Prompt A — the one everybody types"

    ```text
    Can you help me analyse our expenses?
    ```

Read what comes back. It'll be generic, or it'll ask you five questions.
Neither is useless, but neither is the answer.

Now start **another new chat** — a fresh one, so the first attempt isn't
influencing it — and paste this.

!!! example prompt "Prompt B — the same question, specified"

    ```text
    You're helping a financial controller at a mid-size distribution
    company. We closed Q2 and operating expenses came in 8% over budget.

    Our budget-to-actual by department shows Engineering contract labour
    at 310% of budget, G&A professional fees at 440% of budget, and
    Marketing programmes at 190% in May only. Everything else is within
    a few points either way.

    Draft the variance commentary section of our quarterly management
    report. Six to eight sentences. Lead with the largest driver. For
    each variance, state the amount, name the most likely cause given
    what a distribution business looks like, and say what I should go
    confirm before this is final.

    Do not speculate beyond what the numbers support. Where you're
    guessing at a cause, say so explicitly.
    ```

## What good looks like

Prompt B should give you something you could paste into a document and edit,
rather than something you'd have to rewrite. It should also refuse to invent
causes it can't support — you asked it to flag guesses, and it should.

Compare the two outputs side by side. The model didn't get smarter between
them. You just stopped making it guess.

## The four things prompt B has

Not a formula to memorise, but notice what's there:

**Who you are and what the situation is.** "Financial controller", "closed Q2",
"8% over". Claude writes differently for a controller than for a CFO's board
deck.

**The actual numbers.** Prompt A asked Claude to analyse expenses without
showing it any. This happens constantly.

**What you want back, and how much of it.** "Six to eight sentences", "lead
with the largest driver". Without a length, you get whatever length it feels
like.

**What not to do.** "Don't speculate", "flag your guesses". Constraints are
the highest-value line in most prompts and the one people leave out.

<div class="yours" markdown>
**Now with your own work.** Think of something you asked Claude recently that
came back mediocre. Rewrite it with those four pieces and run it again.

If nothing comes to mind: take the last email you had to write twice, and
write the prompt that would have produced the second version directly.
</div>

!!! warning "Gotcha"
    Long prompts aren't automatically better. A specific two-line prompt beats
    a vague ten-line one. What you're adding is *information Claude doesn't
    have*, not words.

!!! tip "The lazy shortcut that works"
    When you can't be bothered writing all that, try: *"Before you answer, ask
    me any questions you need to give a good answer."* It'll usually ask three
    sharp ones, and you've offloaded the specification work onto the thing
    that knows what's missing.

---

**Go deeper:** [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)

**Next:** [Lab 2 — Give Claude your data](02-give-claude-your-data.md)
