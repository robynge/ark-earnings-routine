# ARK Earnings Routine — script library

Helper scripts and templates for the daily ARK earnings-call analysis pipeline.

This repo no longer fetches data itself — it is consumed by:
- **`robynge/ark-routine`** — owns holdings (`refresh-csvs.yml`) and earnings
  data fetch + transcript PDF rendering (`fetch-earnings.yml` + `scripts/run_earnings.py`).
  That workflow `git clone`s this repo into `.ear/` to use the scripts below.
- **Cloud routine `earnings`** (claude.ai/code/routines) — clones this repo for
  the briefing template, analysis prompt, and HTML-to-PDF renderer; reads
  pre-fetched data from `ark-routine/earnings/`.

## Layout

```
scripts/
├── parse_holdings.py        # 14 ARK CSVs → ticker→funds universe JSON
├── find_today_calls.py      # universe + ET date → today's ARK calls (transcript_ready)
├── fetch_transcript.py      # one (ticker, year, quarter) → level-2 speakers JSON
├── render_transcript.py     # speakers JSON + meta → Helvetica/ARK transcript PDF
├── render_html_to_pdf.py    # generic HTML → PDF (used for briefings)
└── briefing_template.html   # briefing template; Claude fills the {{...}} placeholders
prompts/
└── analysis.md              # analysis methodology (verbatim-quote rules, banned words, output skeleton)
requirements.txt
```

## What was removed and why

- `.github/workflows/daily_holdings.yml` — replaced by `ark-routine`'s `refresh-csvs.yml`
- `data/LATEST/` (holdings CSVs + universe.json + _fetched_at.json) — `ark-routine` is the live source now
- `scripts/fetch_holdings.py` — no longer called by anything

## Local testing

```
pip install -r requirements.txt
# WeasyPrint needs Pango/Cairo system libs:
# macOS:  brew install pango cairo gdk-pixbuf libffi
# linux:  apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b
```
