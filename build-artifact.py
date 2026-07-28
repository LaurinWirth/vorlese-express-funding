#!/usr/bin/env python3
"""Erzeugt artifact.html aus index.html.

index.html ist die lokale Vollversion (im Browser per Doppelklick nutzbar).
Der Artifact-Host liefert doctype/html/head/body selbst, deshalb wird der
Dokumentrahmen entfernt. Zusätzlich werden data-theme-Overrides eingefügt,
damit der Theme-Umschalter des Viewers die prefers-color-scheme-Regel
in beide Richtungen überstimmt.

Nach jeder Änderung an index.html:  python3 build-artifact.py
Danach in Claude Code artifact.html erneut veröffentlichen (gleiche URL).
"""

import io
import sys

LIGHT = """    --paper:#fbf8f3; --paper-2:#fffdfa; --ink:#20201d; --ink-2:#55534c; --ink-3:#8a8779;
    --line:#e4ded2; --accent:#bf5133; --accent-soft:#fbeee9; --teal:#2c6b68; --teal-soft:#e6f1f0;
    --gold:#b98526; --gold-soft:#fbf1dc; --red:#a33a3a; --red-soft:#f9e9e9;
    --shadow:0 1px 2px rgba(40,30,10,.05), 0 8px 24px -12px rgba(40,30,10,.16);"""

DARK = """    --paper:#16161a; --paper-2:#1d1d22; --ink:#eceae4; --ink-2:#a9a69d; --ink-3:#75726a;
    --line:#302f36; --accent:#e78163; --accent-soft:#2e211c; --teal:#6fbdb7; --teal-soft:#172a29;
    --gold:#d9a94f; --gold-soft:#2a2317; --red:#e08282; --red-soft:#2d1c1c;
    --shadow:0 1px 2px rgba(0,0,0,.3), 0 8px 24px -12px rgba(0,0,0,.6);"""

ANCHOR = "  *{box-sizing:border-box}"


def main() -> int:
    src = io.open("index.html", encoding="utf-8").read()

    body = src[src.index("<style>"):src.index("</body>")]
    body = body.replace("</head>\n<body>\n", "").replace("</head>\n<body>", "")

    if body.count(ANCHOR) != 1:
        print("Anker im CSS nicht eindeutig gefunden — index.html geändert?", file=sys.stderr)
        return 1

    override = (
        '  /* Theme-Umschalter des Viewers muss die Media Query in beide Richtungen schlagen */\n'
        f'  :root[data-theme="light"]{{\n{LIGHT}\n  }}\n'
        f'  :root[data-theme="dark"]{{\n{DARK}\n  }}\n'
    )
    body = body.replace(ANCHOR, override + ANCHOR)

    io.open("artifact.html", "w", encoding="utf-8").write(body)
    print(f"artifact.html geschrieben ({body.count(chr(10)) + 1} Zeilen)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
