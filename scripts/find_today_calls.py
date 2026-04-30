#!/usr/bin/env python3
"""Find today's earnings calls that are in the ARK universe AND transcript_ready.

Reads earningscall API key from EARNINGSCALL_API_KEY env or first arg.

Usage:
    python find_today_calls.py UNIVERSE.json > today_calls.json
"""
import json
import os
import sys
from datetime import date

import earningscall
from earningscall import get_calendar, get_company

if len(sys.argv) != 2:
    sys.exit("usage: find_today_calls.py UNIVERSE.json > today_calls.json")

api_key = os.environ.get("EARNINGSCALL_API_KEY")
if not api_key:
    sys.exit("EARNINGSCALL_API_KEY env required")
earningscall.api_key = api_key

universe = json.loads(open(sys.argv[1]).read())
ark_tickers_upper = {t.upper() for t in universe.keys()}

today = date.today()
cal = list(get_calendar(today))

matches = []
for c in cal:
    if not getattr(c, "transcript_ready", False):
        continue
    name = (c.company_name or "").strip()
    co = get_company(name.lower()) if name else None
    # earningscall doesn't expose the resolved ticker on CalendarEvent directly.
    # Resolve by matching company name → company → infer symbol from get_company.
    # If get_company doesn't accept the company name, skip.
    if co is None:
        continue
    # Try to look up symbol via the SDK's _company attribute
    symbol = None
    for attr in ("symbol", "_symbol", "ticker"):
        v = getattr(co, attr, None)
        if isinstance(v, str) and v:
            symbol = v.upper()
            break
    if not symbol:
        # Fall back: try iterating universe and matching company name
        for t, entry in universe.items():
            if (entry.get("company") or "").upper() in name.upper() or name.upper() in (entry.get("company") or "").upper():
                symbol = t.upper()
                break
    if not symbol or symbol not in ark_tickers_upper:
        continue
    matches.append({
        "ticker": symbol,
        "company": str(co),
        "year": c.year,
        "quarter": c.quarter,
        "conference_date": c.conference_date.isoformat() if c.conference_date else None,
        "ark_funds": universe[symbol]["funds"],
    })

json.dump(matches, sys.stdout, indent=2)
