# ARK Earnings Routine — helper scripts

Companion repository for the daily ARK earnings-call analysis routine running on Claude Code.

## Layout

```
scripts/
├── parse_holdings.py        # CSVs → ticker→funds JSON
├── find_today_calls.py      # universe.json + earningscall calendar → today's matches
├── fetch_transcript.py      # one (ticker, year, quarter) → speakers JSON
├── render_transcript.py     # speakers JSON + meta → styled transcript PDF (Helvetica/ARK design)
├── render_html_to_pdf.py    # generic HTML → PDF (used for briefings & digests)
└── briefing_template.html   # Helvetica-styled briefing template; Claude fills placeholders
prompts/
└── analysis.md              # the OPTIMIZED_PROMPT (Bridgewater-lens + media discipline)
requirements.txt
```

## Usage from a Claude Code routine

The routine clones this repo and runs scripts from Bash. The routine itself does:
1. Drive MCP read of today's ARK Holdings CSVs → /tmp
2. `python scripts/parse_holdings.py /tmp/*.csv > /tmp/universe.json`
3. `python scripts/find_today_calls.py /tmp/universe.json > /tmp/today_calls.json`
4. For each match: fetch_transcript → render_transcript → analysis (Claude) → render_html_to_pdf
5. Drive MCP upload of all PDFs

`EARNINGSCALL_API_KEY` env required for steps 3-4.

## Local testing

```
pip install -r requirements.txt
# requires Pango/Cairo system libs for weasyprint:
# macOS:  brew install pango cairo gdk-pixbuf libffi
# linux:  apt-get install -y libpango-1.0-0 libpangoft2-1.0-0
```
