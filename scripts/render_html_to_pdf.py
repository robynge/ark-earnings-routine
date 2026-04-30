#!/usr/bin/env python3
"""Render an HTML file to a styled PDF via WeasyPrint.

Generic renderer used for briefings and digests. Claude generates the HTML
(with our standard CSS injected by inject_css.py or inline), this script
just runs WeasyPrint.

Usage:
    python render_html_to_pdf.py INPUT.html OUT.pdf
"""
import sys
from weasyprint import HTML

if len(sys.argv) != 3:
    sys.exit("usage: render_html_to_pdf.py INPUT.html OUT.pdf")

inp, out = sys.argv[1:3]
HTML(filename=inp).write_pdf(out)
print(f"PDF written: {out}")
