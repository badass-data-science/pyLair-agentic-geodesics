"""Report house-style issues in book Markdown files (see ../AGENTS.md).

Usage: python3 tools/style_check.py [FILE ...]   (default: every chapter and appendix)

Reports, per file: running-prose paragraphs over 130 words; counts of filler
intensifiers and em dashes per 1,000 words; "our heroine" in lower case;
"Secret Lab" / "Powers That Be" without the trademark glyph; bare "heat"
not preceded by "Interpol". Code blocks are skipped. Nothing is changed.
"""
import glob
import os
import re
import sys

BOOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILLERS = ["actually", "genuinely", "exactly", "really", "precisely", "honestly", "literally", "simply"]


def prose_lines(text):
    in_code = False
    for n, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            yield n, line


def check(path):
    text = open(path, encoding="utf-8").read()
    lines = list(prose_lines(text))
    prose = "\n".join(l for _, l in lines)
    prose_nocode = re.sub(r"`[^`]*`", "", prose)
    words = len(prose_nocode.split()) or 1
    out = []
    for n, line in lines:
        if line.startswith(("#", ">", "|", "**[", "- ", "* ", "1.")):
            continue
        w = len(line.split())
        if w > 130:
            out.append(f"  line {n}: paragraph of {w} words")
    counts = {f: len(re.findall(rf"\b{f}\b", prose_nocode, re.I)) for f in FILLERS}
    dashes = prose_nocode.count("—")
    out.append(f"  {words} words; em dashes {dashes} ({dashes * 1000 / words:.1f}/1k); fillers: "
               + ", ".join(f"{k} {v}" for k, v in counts.items() if v))
    for n, line in lines:
        l = re.sub(r"`[^`]*`", "", line)
        if re.search(r"\bour heroine\b", l) and "Heroine" not in l.replace("our heroine", ""):
            out.append(f"  line {n}: lower-case 'our heroine'")
        elif re.search(r"\bour heroine\b", l):
            out.append(f"  line {n}: lower-case 'our heroine'")
        if re.search(r"Secret Lab(?!(™|'s™|&trade;))", l):
            out.append(f"  line {n}: 'Secret Lab' without ™")
        if re.search(r"Powers That Be(?!™)", l):
            out.append(f"  line {n}: 'Powers That Be' without ™")
        if re.search(r"(?<!Interpol )\bheat\b", l, re.I) and "Interpol" in l:
            out.append(f"  line {n}: bare 'heat' near Interpol")
    print(os.path.relpath(path, BOOK))
    print("\n".join(out))


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(BOOK, "chapter-*.md")) + glob.glob(os.path.join(BOOK, "appendix-*.md")))
    for f in files:
        check(f)


if __name__ == "__main__":
    main()
