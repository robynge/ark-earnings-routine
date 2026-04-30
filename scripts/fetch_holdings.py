#!/usr/bin/env python3
"""Fetch all 14 ARK ETF holdings CSVs directly from ark-funds.com.

Usage:
    python fetch_holdings.py OUT_DIR
"""
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ETFS = [
    ("ARKK",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv"),
    ("ARKG",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_GENOMIC_REVOLUTION_ETF_ARKG_HOLDINGS.csv"),
    ("ARKQ",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_AUTONOMOUS_TECH._&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv"),
    ("ARKW",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv"),
    ("ARKB",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_21SHARES_BITCOIN_ETF_ARKB_HOLDINGS.csv"),
    ("ARKVX", "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_VENTURE_FUND_ARKVX_HOLDINGS.csv"),
    ("ARKX",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv"),
    ("ARKF",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv"),
    ("IZRL",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS.csv"),
    ("PRNT",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv"),
    ("ARKD",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_DIET_Q1_BUFFER_ETF_ARKD_HOLDINGS.csv"),
    ("ARKT",  "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_DIET_Q4_BUFFER_ETF_ARKT_HOLDINGS.csv"),
    ("ARKUX", "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_VENTURE_FUND_ARKUX_HOLDINGS.csv"),
    ("ARKSX", "https://assets.ark-funds.com/fund-documents/funds-etf-csv/ARK_VENTURE_FUND_ARKSX_HOLDINGS.csv"),
]


def fetch(out_dir, etf, url):
    req = urllib.request.Request(url, headers={"User-Agent": "ark-earnings-routine/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    p = out_dir / f"{etf}.csv"
    p.write_bytes(data)
    return etf, len(data)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: fetch_holdings.py OUT_DIR")
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch, out, etf, url): etf for etf, url in ETFS}
        for fut in as_completed(futs):
            etf = futs[fut]
            try:
                e, sz = fut.result()
                print(f"  {e}: {sz:,} bytes")
                n += 1
            except Exception as ex:
                print(f"  {etf}: FAILED {ex}", file=sys.stderr)
    print(f"fetched {n}/{len(ETFS)} CSVs to {out}")


if __name__ == "__main__":
    main()
