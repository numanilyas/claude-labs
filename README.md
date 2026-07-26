# Claude Labs

Short, hands-on labs for getting real work done with Claude. Two tracks:

- **Finance track** — 12 labs, ~2 hours, aimed at accounting and finance staff on a Claude Pro plan
- **Developer track** — 10 labs, aimed at working software engineers

Every lab is one page, about ten minutes, and ends with the participant running
the same thing on their own file. All practice data is synthetic.

---

## Publish it (about 10 minutes)

### 1. Put it on GitHub

```bash
cd claude-labs
git init
git add .
git commit -m "Claude Labs curriculum"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/claude-labs.git
git push -u origin main
```

If you don't have a repo yet, create an empty one at
<https://github.com/new> named `claude-labs`. Do **not** initialise it with a
README — you already have one.

### 2. Turn on Pages

On GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

That's the whole setup. The included workflow (`.github/workflows/deploy.yml`)
builds and publishes on every push to `main`.

> **Free GitHub accounts can only serve Pages from public repos.** If this repo
> must stay private you need a paid GitHub plan, or serve the built `site/`
> folder some other way.

### 3. Fix the three placeholder URLs

Open `mkdocs.yml` and replace `CHANGE-ME` with your GitHub username in:

- `site_url`
- `repo_url`
- `extra.social[0].link`

Your site lands at `https://YOUR-USERNAME.github.io/claude-labs/`.

Watch the first build under the repo's **Actions** tab. It takes about a minute.

---

## Edit it locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Live-reloading preview at <http://127.0.0.1:8000>.

To publish a change: edit the markdown, commit, push. The site rebuilds itself.

---

## Regenerate the sample data

The practice files in `docs/files/` are produced by `build_data.py`. You only
need this if you want to change the numbers, add transactions, or rebrand the
fictional company.

```bash
pip install openpyxl reportlab
python build_data.py
```

The script asserts that the bank reconciliation actually balances, so it will
fail loudly rather than ship a broken exercise.

---

## Layout

```
docs/
  index.md                 landing page
  start-here.md            15-minute setup, do this before lab 1
  how-to-run-a-session.md  for whoever is teaching
  finance/                 12 labs
  dev/                     10 labs
  cheatsheet.md            one-page reference
  prompt-library.md        every prompt in the curriculum, in one place
  sample-data.md           download index + what's wrong with each file
  facilitator.md           answer keys
  files/                   the synthetic data pack
build_data.py              regenerates docs/files/
mkdocs.yml                 site config and navigation
```

To add a lab: drop a markdown file in `docs/finance/` or `docs/dev/`, then add
it to the `nav:` block in `mkdocs.yml`. The build runs with `--strict`, so a
broken internal link fails the deploy instead of shipping quietly.
