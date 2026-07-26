# Lab 9 — Teach Claude your house style

<div class="lab-meta">
  <span class="time">10 min</span>
  <span>Skills</span>
  <span>Bring 2–3 of your own documents</span>
</div>

## The problem

Lab 8's skill knows your *procedure*. It doesn't know that your team writes
"FY26" not "FY2026", puts the period in the subject line, never uses the word
"leverage", and always rounds to thousands in board material but to dollars in
management reports.

Those rules exist. They're mostly in one person's head, and every new hire
learns them by getting corrected for six months.

## The trick

Don't try to write the rules down from memory — you'll miss most of them.
Give Claude finished examples and have it extract the rules.

## Before you start

- [ ] Two or three documents your team produced and was happy with — memos,
      board commentary, management reports. Redact anything sensitive first.

!!! tip "If you can't use real documents"
    Use the memo you generated in Lab 7 plus one you edit by hand to look the
    way you'd want it. Two contrasting versions is enough for the exercise.

## Do this

1. New chat. Attach your examples.
2. Paste this:

!!! example prompt "Copy this prompt"

    ```text
    Attached are documents my team wrote. I want to capture our house
    style so future documents match without me having to edit them.

    Read them and infer our conventions. Cover:
    - Structure: what sections, in what order, how long
    - Tone and register: formality, how direct, first person or not
    - Number formatting: rounding, currency, negatives, percentages,
      how periods are written
    - Vocabulary: terms we use, terms we clearly avoid
    - Anything else consistent across all of them

    Give me the list as specific, checkable rules. "Professional tone"
    is not a rule. "Never opens a paragraph with 'Additionally'" is.

    Then flag any place the documents contradict each other, so I can
    decide which is right.
    ```

3. Read the list. **Correct it** — it will get some wrong, and the
   contradictions it flags are usually genuinely unresolved in your team.
4. Then:

!!! example prompt "Copy this prompt"

    ```text
    Good. Turn the corrected list into a skill called house-style.

    The description should make Claude apply it whenever it writes
    anything I'd send to someone else - memos, commentary, emails,
    board material - but not when it's just answering me in chat.
    Under 200 characters.
    ```

5. Upload it: **Customize → Skills → Add**.

## What good looks like

The rules should be specific enough that you could hand them to a contractor.
Vague output here means your examples were too few or too different from each
other — three similar documents beats six unrelated ones.

Test it by asking for something new and seeing whether it comes out sounding
like your team wrote it. Then combine: ask for a variance memo and watch both
skills apply — the procedure from Lab 8, the voice from this one.

<div class="yours" markdown>
**Keep correcting it.** The first version will be about 70% right. When you
edit its output, notice *what* you changed, and add that as a rule.

Three or four rounds of this and the editing mostly stops. That's the actual
return on the exercise, and it takes a few weeks rather than one afternoon.
</div>

!!! warning "Gotcha"
    Keep house style and procedure in **separate** skills. Bundle them and
    you've got one skill that only fires for variance memos, when the style
    rules should apply to everything you write.

---

**Next:** [Lab 10 — Monday morning, before you're in](10-scheduled-tasks.md)
