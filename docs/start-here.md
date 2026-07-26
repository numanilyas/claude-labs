# Start here

<div class="lab-meta">
  <span class="time">15 min, once</span>
  <span>Setup</span>
</div>

Do this before Lab 1. Most of the "it didn't work for me" moments in these labs
trace back to one of these four things.

## 1. Check your plan

Open Claude, click your name in the bottom left → **Settings** → look for your
plan.

You need **Pro** or higher. On the free plan, file creation is limited, Cowork
isn't available, and roughly half of this curriculum won't run.

## 2. Turn on code execution

This is the big one. Without it Claude can describe a spreadsheet to you but
can't hand you one.

1. **Settings → Capabilities**
2. Turn on **Code execution and file creation**

!!! warning "If you don't see it"
    Some builds label this section differently, and on a managed work account
    an administrator may control it. If the toggle is missing or greyed out,
    that's an org policy — ask whoever runs your Claude account.

While you're in Settings, look at **Settings → Usage**. Get familiar with where
it is. Cowork burns through your allowance considerably faster than chatting
does, and it's better to know that now than halfway through Lab 6.

## 3. Install the desktop app

Download it from [claude.com/download](https://claude.com/download). macOS and
Windows.

You need this for the Cowork labs (4 through 7, plus 10). Cowork is rolling out
to the web and mobile, but the desktop app is the surface where everything in
this curriculum works today, including connecting a local folder.

Sign in with the same account.

## 4. Make a practice folder

Create a folder somewhere obvious — Desktop is fine — called
`claude-labs`. Download the sample data into it.

[:octicons-download-24: Get the sample data](sample-data.md){ .md-button .md-button--primary }

You'll connect this folder to Cowork in Lab 4 and keep using it throughout.

---

## Check that it worked

Open Claude, start a new chat, and paste this:

!!! example prompt "Copy this prompt"

    ```text
    Create a small Excel file called setup-check.xlsx with two columns,
    Month and Revenue, and three rows of made-up data. Add a fourth row
    that totals the Revenue column using a real SUM formula, not a
    hardcoded number.
    ```

**You should get** a downloadable `.xlsx` file. Open it and click on the total
cell — the formula bar should show `=SUM(B2:B4)` or similar.

If you got a description of a spreadsheet instead of an actual file, step 2
didn't take. Go back and check the toggle.

---

## Two things worth knowing before you start

**Claude's memory doesn't follow you into Cowork.** What Claude picks up about
you in ordinary chat doesn't carry into a Cowork session. If you've told Claude
in chat how your company reports revenue, you'll need to tell it again in
Cowork, or put it somewhere Cowork reads. Lab 3 covers where.

**Everything runs in a sandbox with a file size ceiling.** Once code execution
is involved, the practical limit is about 30 MB per file. A full-year GL export
will hit that. Lab 12 covers what to do about it.

---

**Next:** [Finance Track → Lab 1](finance/01-a-prompt-that-works.md) or
[Developer Track → Lab 1](dev/01-setup.md)
