"""
assemble_book.py

Concatenates "Agentic Geodesic Lair Design for Supervillains" -- front
matter, all chapters, and the appendices, in reading order -- into one
Markdown file, then (by default) renders it to PDF and EPUB via pandoc.
Internal material (`outline.md`, `README.md`, `AGENTS.md`, `examples/`,
this directory) is never included: only the files `_ordered_source_files()`
names are read.

Adapted from the same script in the series' later volumes (*Systems
Thinking for Supervillains* and *Strategy for Supervillains*), which
replaced the older `examples/assemble_book.py` this book and the first
volume shared. What differs here, and why:

- **Figures are real tool output, not generated art.** The later volumes
  match each `**[IMAGE: ...]**` tag to a PNG by position
  (`chNN-imgM-*.png`). This book's figures are `preview_dome`/`preview_nest`
  renders and plots of real computed data, saved under `examples/images/`
  (and a few from `../blog-posts/`), so each tag names its file
  explicitly:

      **[IMAGE: examples/images/poc-yurt.png | alt-text description]**
      **[CAPTION: reader-facing caption]**

  The path is relative to the book directory. The description becomes the
  figure's alt text (read aloud by screen readers in the EPUB/Kindle
  edition); only the caption prints, as "Figure N.M: caption", numbered
  per chapter in order of appearance.
- **Prose figure references are checked.** `--check-only` (and every full
  build) confirms that every "Figure N.M" mentioned in the prose exists,
  that every chapter cross-reference ("Chapter N") is in range, and that
  every IMAGE path exists.
- **Seven Parts, three appendices, no boxes beyond the series' own.** The
  Prompt / What Comes Back / What It Means convention is ordinary Markdown
  and needs no special handling; Villain's Toolkit / Sketch-It / Debrief
  boxes, if any are added, are kept on one page the same way the later
  volumes do it.
- **Title-page image.** `title-page-image.png` (landscape, 832x624) is not a
  full-bleed cover, so it's placed on the title page under the byline
  (raw LaTeX in the PDF) and used as the EPUB's cover image.

Usage:
    python3 assemble_book.py                  # writes dist/geodesic-lair-book.{md,pdf,epub}
    python3 assemble_book.py --out DIR        # writes to a different directory
    python3 assemble_book.py --skip-pdf       # skip the PDF (still writes EPUB)
    python3 assemble_book.py --skip-epub      # skip the EPUB (still writes PDF)
    python3 assemble_book.py --check-only     # verify images and references, write nothing

The PDF step needs pandoc and a LaTeX engine (xelatex by default) plus the
DejaVu fonts; the EPUB step needs only pandoc. If pandoc is missing, the
script says so and still leaves the Markdown written.
"""

import argparse
import html
import math
import os
import re
import struct
import subprocess
import sys
import zipfile

BOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BOOK_DIR, "examples", "images")
TITLE_PAGE_IMAGE = os.path.join(BOOK_DIR, "title-page-image.png")
OUTPUT_STEM = "geodesic-lair-book"

TITLE = "Agentic Geodesic Lair Design for Supervillains"
SUBTITLE = "Computational Geometry and Agentic AI with pyLair and pyFit"
EDITION = "0th Edition"
AUTHOR = "Lady Napalm"  # the byline, as in the series' later volumes; the copyright line keeps the legal name

# **[IMAGE: path | description]** followed (only whitespace between) by
# **[CAPTION: text]**. Group 1 is the path, group 2 the description,
# group 3 the caption.
IMAGE_TAG_RE = re.compile(r"\*\*\[IMAGE:\s*(.*?)\s*\]\*\*", re.DOTALL)
IMAGE_WITH_CAPTION_RE = re.compile(
    r"\*\*\[IMAGE:\s*([^|\]]+?)\s*\|\s*(.*?)\s*\]\*\*\s*\n\s*\*\*\[CAPTION:\s*(.*?)\s*\]\*\*", re.DOTALL
)
H1_RE = re.compile(r"^# (.+)$", re.MULTILINE)
# "Figure 4.1", "Figures 4.1 and 4.2", "Figure 22.2's" -- every N.M after
# the word, up to the end of a simple list.
FIGURE_REF_RE = re.compile(r"\bFigures?\s+(\d+\.\d+(?:(?:,\s*|,?\s+(?:and|or|through|to)\s+)\d+\.\d+)*)")
CHAPTER_REF_RE = re.compile(r"\bChapters?\s+(\d+(?:(?:,\s*|,?\s+(?:and|or|through|to)\s+|[–-])\d+)*)")
# An old-style hyphenated figure number ("Figure 4-1") left in the prose
# would silently not match the printed "Figure 4.1".
OLD_FIGURE_REF_RE = re.compile(r"\bFigures?\s+\d+-\d+")
# Any Markdown image written directly, bypassing the IMAGE/CAPTION tags.
RAW_IMAGE_RE = re.compile(r"^!\[[^\]]*\]\([^)]+\)", re.MULTILINE)

FRONT_MATTER = [
    "title_page.md",
    "dedication.md",
    "about_the_author.md",
    "about_the_series.md",
    "how_to_use_this_book.md",
    "ai_use_statement.md",
]

# Descriptive half of each Part title only: LaTeX's `book` class numbers
# \part{} itself ("Part I", ...). Keyed by the chapter file that opens it.
PART_OPENERS = {
    "chapter-01-introducing-pylair-pyfit-and-agentic-ai.md": "Meet Your New Design Engineers",
    "chapter-03-picking-a-polyhedron.md": "From Polyhedron to Sphere",
    "chapter-08-squash-and-stretch-ellipsoid-elongation.md": "Shaping the Lair",
    "chapter-12-hub-angles-tangent-deflection-and-spoke-angles.md": "The Bill of Materials",
    "chapter-17-getting-it-out-the-door.md": "Output, Interfaces, and Agentic Use",
    "chapter-19-introducing-pyfit-nesting-as-a-second-geometry-problem.md": "From Panels to Sheets: Nesting with pyFit",
    "chapter-23-prompting-pylair-and-pyfit-like-you-mean-it.md": "Becoming a Better Design Villain",
}
APPENDICES_OPENER_FILE = "appendix-a-glossary.md"

# The LaTeX header and EPUB stylesheet below are copied from *Strategy for
# Supervillains*' assemble_book.py, where each piece's comment records the
# rendering problem it fixed.
_CODE_WRAP_HEADER = (
    # Explicit rather than relying on pandoc's own auto-include-graphicx
    # heuristic (triggered by scanning for `![]()` Markdown image syntax):
    # the title page's cover image is emitted as a raw LaTeX
    # \includegraphics (see _substitute_images()), which that heuristic
    # doesn't see.
    "\\usepackage{graphicx}\n"
    "\\usepackage{fvextra}\n\\fvset{breaklines=true,breakanywhere=true}\n"
    "\\usepackage{seqsplit}\n"
    "\\DeclareRobustCommand{\\texttt}[1]{\\seqsplit{#1}}\n"
    "\\hyphenation{Supervillain Supervillains supervillain supervillains}\n"
    # DejaVu Serif (mainfont, above) has no glyph for U+2713 CHECK MARK --
    # confirmed via fontTools' cmap -- which Chapter 1 and Chapter 20 both
    # use verbatim (the AI report's self-awarded "checkmark badge", a
    # recurring image across both chapters). DejaVu Sans DOES have it, so
    # rather than touching either chapter's prose, redirect just this one
    # character to DejaVu Sans wherever it appears -- transparent to the
    # Markdown source and to EPUB (browsers/e-readers already render the
    # glyph fine; this header is LaTeX/PDF-only).
    "\\usepackage{fontspec}\n\\usepackage{newunicodechar}\n"
    "\\newfontfamily\\checkmarkfont{DejaVu Sans}\n"
    "\\newunicodechar{✓}{{\\checkmarkfont ✓}}\n"
    # Pandoc wraps a standalone `![...](...)` image in a floating LaTeX
    # `figure` environment by default, which can drift onto a later page
    # if it doesn't fit where it occurs in the source -- exactly what
    # happened to the title page's own cover image on the first render.
    # Forcing every figure's placement to `H` (via the `float` package)
    # keeps each of this book's ~50 diagrams pinned right where its
    # surrounding prose actually discusses it.
    "\\usepackage{float}\n\\floatplacement{figure}{H}\n"
    # Pandoc's HTML/EPUB writer has no native figure-numbering counter at
    # all (unlike LaTeX's own, which book.cls would auto-number as
    # "Figure <chapter>.<n>"), so numbering has to be hand-rolled in
    # Python (_substitute_images()) and baked directly into each
    # caption's text identically for both outputs, rather than relying on
    # LaTeX's own counter -- which would otherwise show its OWN
    # "Figure X.Y:" label in front of our hand-rolled one. Suppressing
    # just the label (not the caption styling/spacing) via `caption`'s
    # labelformat=empty leaves our own numbered text as the only prefix.
    "\\usepackage{caption}\n\\captionsetup{labelformat=empty}\n"
    # book.cls defaults to \flushbottom for a twoside document -- every
    # page's text block is stretched (via interline glue) to reach
    # exactly the same bottom margin. Combined with `H`-forced figures
    # immediately above, that stretching turns ugly the moment a figure
    # can't fit on the current page and gets pushed to start a fresh one:
    # whatever short amount of text WAS left on the page it got pushed
    # off of still gets stretched to fill the FULL page height, producing
    # large, unsightly gaps between paragraphs (confirmed by rendering --
    # e.g. Chapter 1 page 24 before this fix). \raggedbottom instead lets
    # a page like that end with genuinely empty space at the bottom
    # margin rather than artificially spread-out text -- the standard
    # fix for exactly this symptom in any LaTeX document with real
    # floats, and worth having globally since nearly every one of this
    # book's ~50 diagrams is `H`-placed the same way.
    "\\raggedbottom\n"
    # Pandoc's \pandocbounded lets an image grow to the full \textheight.
    # The portrait figures sized for Kindle screens (e.g. Figure 18.1,
    # 7x10in) then fill a whole page, and with H placement the text
    # before each one ends on a mostly empty page (eight lines on the
    # page before 18.1, confirmed by rendering). Capping figures at 62%
    # of the text height prints a portrait figure at roughly the size a
    # Kindle shows it (~3.2in wide, so its text keeps save_fig()'s
    # floor) and leaves room for text beside it on the page; landscape
    # figures are under the cap already. Same macro as pandoc's own,
    # one height changed.
    "\\makeatletter\n"
    "\\renewcommand*\\pandocbounded[1]{%\n"
    "  \\sbox\\pandoc@box{#1}%\n"
    "  \\Gscale@div\\@tempa{0.62\\textheight}{\\dimexpr\\ht\\pandoc@box+\\dp\\pandoc@box\\relax}%\n"
    "  \\Gscale@div\\@tempb{\\linewidth}{\\wd\\pandoc@box}%\n"
    "  \\ifdim\\@tempb\\p@<\\@tempa\\p@\\let\\@tempa\\@tempb\\fi%\n"
    "  \\ifdim\\@tempa\\p@<\\p@\\scalebox{\\@tempa}{\\usebox\\pandoc@box}%\n"
    "  \\else\\usebox{\\pandoc@box}%\n"
    "  \\fi%\n"
    "}\n"
    "\\makeatother\n"
    # book.cls's unstarred \chapter updates the running header (via
    # \markboth) automatically; its starred variant \chapter* -- what
    # pandoc emits for every `{-}` unnumbered heading in this book,
    # i.e. literally every chapter -- does NOT, by design. Left alone,
    # every page's running header would freeze on whatever the very
    # last NUMBERED sectioning command set (here: never, so it shows
    # stale "CONTENTS" for the entire rest of the book). Redefining the
    # internal \@schapter to also call \markboth, mirroring what
    # \@chapter already does for the unstarred command, is the standard
    # fix for this well-known book.cls behavior.
    #
    # Passing #1 (the full heading text) straight into \markboth prints
    # the ENTIRE chapter title, all-caps, in the running header -- fine
    # for a short one, but this book's titles carry long colon-subtitles
    # (e.g. "Chapter 9: Time Bombs -- Delays and Why Your Feedback Loop
    # Is Lying to You") that don't fit at this book's narrower 7in trim,
    # overflowing the margin and mashing into the page number. This is
    # the same problem solved the same way in this series' first volume
    # (the Omen book): truncate the heading at its first colon (xstring's
    # \StrBefore) so "Chapter 9: Time Bombs -- ..." becomes just
    # "Chapter 9" in the header -- a colon-less title ("Dedication",
    # "About the Author") is returned unchanged, already short enough.
    # \\noexpandarg: otherwise xstring expands the heading, and an italic
    # title in one (Chapter 26, Appendix E) stops the build.
    "\\usepackage{xstring}\n\\noexpandarg\n"
    "\\newcommand{\\STFSChapterMark}{}\n"
    "\\makeatletter\n"
    "\\def\\@schapter#1{\\if@twocolumn\\@topnewpage[\\@makeschapterhead{#1}]%\n"
    "  \\else\\@makeschapterhead{#1}\\@afterheading\\fi\n"
    "  \\StrBefore{#1}{:}[\\STFSChapterMark]%\n"
    "  \\markboth{\\MakeUppercase{\\STFSChapterMark}}{\\MakeUppercase{\\STFSChapterMark}}}\n"
    "\\makeatother\n"
    # The chapter mark above is short by construction, but on odd pages
    # book.cls's headings style shows the current *section* title instead
    # (\sectionmark -> \markright), uncut. Four of this book's ## headings
    # are long enough that, uppercased and slanted, they fill the whole
    # 5.5in text width and run straight into the page number ("...OF
    # AGENTIC AI31", page 31). Rather than shorten those headings' prose,
    # cap both running heads at the text width minus room for the page
    # number: truncate's \truncate ends an over-long head with an ellipsis
    # at a word boundary. \truncate always sets a box of the full given
    # width, though -- which on even pages pulled the (right-aligned)
    # chapter mark over to sit beside the page number -- so \STFSHead only
    # calls it when the head is actually too wide, and otherwise typesets
    # the head at its natural width. Same layout as book.cls's own twoside
    # headings for every head that fits.
    "\\usepackage{truncate}\n"
    "\\newsavebox{\\STFSHeadBox}\n"
    "\\newcommand{\\STFSHead}[1]{\\sbox{\\STFSHeadBox}{\\slshape #1}%\n"
    "  \\ifdim\\wd\\STFSHeadBox>\\dimexpr\\textwidth-3em\\relax\n"
    "    \\truncate{\\dimexpr\\textwidth-3em\\relax}{\\slshape #1}%\n"
    "  \\else\\usebox{\\STFSHeadBox}\\fi}\n"
    "\\makeatletter\n"
    "\\def\\@evenhead{\\thepage\\hfil\\STFSHead{\\leftmark}}\n"
    "\\def\\@oddhead{\\STFSHead{\\rightmark}\\hfil\\thepage}\n"
    "\\makeatother\n"
    # book.cls's \part writes its ToC entry as bare "\thepart\hspace{1em}
    # title" -- just the roman numeral, e.g. "I  The Villain's Eye: ...",
    # with no "Part" word (that word only appears in the big label on the
    # part's own opening page, via a separate \partname\thepart, in the
    # SAME \@part macro). Copied verbatim from book.cls below, with only
    # that one addcontentsline line changed to also prepend \partname:
    # the table of contents should read "Part I", "Part II", ... rather
    # than just "I", "II", ....
    "\\makeatletter\n"
    "\\def\\@part[#1]#2{%\n"
    "    \\ifnum \\c@secnumdepth >-2\\relax\n"
    "      \\refstepcounter{part}%\n"
    "      \\addcontentsline{toc}{part}{\\partname\\nobreakspace\\thepart\\hspace{1em}#1}%\n"
    "    \\else\n"
    "      \\addcontentsline{toc}{part}{#1}%\n"
    "    \\fi\n"
    "    \\markboth{}{}%\n"
    "    {\\centering\n"
    "     \\interlinepenalty \\@M\n"
    "     \\normalfont\n"
    "     \\ifnum \\c@secnumdepth >-2\\relax\n"
    "       \\huge\\bfseries \\partname\\nobreakspace\\thepart\n"
    "       \\par\n"
    "       \\vskip 20\\p@\n"
    "     \\fi\n"
    "     \\Huge \\bfseries #2\\par}%\n"
    "    \\@endpart}\n"
    "\\makeatother\n"
    # book.cls's three ToC-line macros -- \l@part, \l@chapter (which
    # \@schapter's own \addcontentsline{toc}{chapter}{...} above feeds
    # exactly like an unstarred \chapter would), and \@dottedtocline
    # (which \l@section and \l@subsection are both just thin wrappers
    # around) -- all separate title from page number with glue whose
    # *natural* width is zero and only grows if there's spare room left
    # on the line: a bare \hfil for the first two, a dot-leader box
    # driven by \hfill for the third. Most entries either fit with room
    # to spare (that glue stretches to fill it) or are long enough to
    # wrap onto a second, short line (plenty of slack there too). But
    # three entries in this book land in between -- long enough to fill
    # their line with nothing left over, so the glue's zero natural
    # width means zero space -- confirmed by rendering: Chapter 21's
    # title ("...Trust the Agent153"), Part IV's ("...Modeling
    # Practice121"), and Chapter 18's "Three Biases Worth Naming..."
    # section entry ("...Half the Defense137") all glue their page
    # number directly onto the last word/dot, with no LaTeX overfull
    # warning at all since nothing is technically overflowing.
    # Each macro below is copied verbatim from LaTeX's own source
    # (book.cls / latex.ltx) with only that one zero-minimum glue
    # changed to a rigid 1em floor that can still stretch (\hskip 1em
    # plus 1fil in place of \hfil/\hfill): every already-comfortable
    # entry renders identically (it had far more than 1em of slack
    # anyway), while an entry too tight to fit that floor on one line is
    # forced to wrap to a second line instead -- the same graceful
    # multi-line layout already used by plenty of this book's other,
    # longer titles.
    "\\makeatletter\n"
    "\\renewcommand*{\\l@part}[2]{%\n"
    "  \\ifnum \\c@tocdepth >-2\\relax\n"
    "    \\addpenalty{-\\@highpenalty}%\n"
    "    \\addvspace{2.25em \\@plus\\p@}%\n"
    "    \\setlength\\@tempdima{3em}%\n"
    "    \\begingroup\n"
    "      \\parindent \\z@ \\rightskip \\@pnumwidth\n"
    "      \\parfillskip -\\@pnumwidth\n"
    "      {\\leavevmode\n"
    "       \\large \\bfseries #1\\hskip 1em plus 1fil\n"
    "       \\hb@xt@\\@pnumwidth{\\hss #2\\kern-\\p@\\kern\\p@}}\\par\n"
    "       \\nobreak\n"
    "         \\global\\@nobreaktrue\n"
    "         \\everypar{\\global\\@nobreakfalse\\everypar{}}%\n"
    "    \\endgroup\n"
    "  \\fi}\n"
    "\\renewcommand*{\\l@chapter}[2]{%\n"
    "  \\ifnum \\c@tocdepth >\\m@ne\n"
    "    \\addpenalty{-\\@highpenalty}%\n"
    "    \\vskip 1.0em \\@plus\\p@\n"
    "    \\setlength\\@tempdima{1.5em}%\n"
    "    \\begingroup\n"
    "      \\parindent \\z@ \\rightskip \\@pnumwidth\n"
    "      \\parfillskip -\\@pnumwidth\n"
    "      \\leavevmode \\bfseries\n"
    "      \\advance\\leftskip\\@tempdima\n"
    "      \\hskip -\\leftskip\n"
    "      #1\\nobreak\\hskip 1em plus 1fil\n"
    "      \\nobreak\\hb@xt@\\@pnumwidth{\\hss #2\\kern-\\p@\\kern\\p@}\\par\n"
    "      \\penalty\\@highpenalty\n"
    "    \\endgroup\n"
    "  \\fi}\n"
    "\\renewcommand*{\\@dottedtocline}[5]{%\n"
    "  \\ifnum #1>\\c@tocdepth \\else\n"
    "    \\vskip \\z@ \\@plus.2\\p@\n"
    "    {\\leftskip #2\\relax \\rightskip \\@tocrmarg \\parfillskip -\\rightskip\n"
    "     \\parindent #2\\relax\\@afterindenttrue\n"
    "     \\interlinepenalty\\@M\n"
    "     \\leavevmode\n"
    "     \\@tempdima #3\\relax\n"
    "     \\advance\\leftskip \\@tempdima \\null\\nobreak\\hskip -\\leftskip\n"
    "     {#4}\\nobreak\n"
    "     \\leaders\\hbox{$\\m@th\n"
    "        \\mkern \\@dotsep mu\\hbox{.}\\mkern \\@dotsep\n"
    "        mu$}\\hskip 1em plus 1fil\n"
    "     \\nobreak\n"
    "     \\hb@xt@\\@pnumwidth{\\hfil\\normalfont \\normalcolor #5\\kern-\\p@\\kern\\p@}%\n"
    "     \\par}%\n"
    "  \\fi}\n"
    "\\makeatother\n"
    # Villain's Toolkit / Sketch-It / Debrief boxes are wrapped in this
    # environment by _keep_boxes_together(). A minipage can't break
    # across pages, so a box that doesn't fit at the bottom of a page
    # moves to the next one whole, title and content together (the
    # longest box is ~200 words, well under a page). \addvspace restores
    # the space around the box that the quote's own \topsep gives up
    # inside a minipage.
    "\\newenvironment{stfsbox}"
    "{\\par\\addvspace{\\topsep}\\noindent\\begin{minipage}{\\linewidth}}"
    "{\\end{minipage}\\par\\addvspace{\\topsep}}\n"
)

# EPUB counterpart of stfsbox: appended to pandoc's default EPUB
# stylesheet (render_epub()), asking the reading system not to break a
# page inside a box. Both spellings, since older Kindle and EPUB 2
# readers know only the page-break-* form.
_EPUB_BOX_CSS = (
    "\n/* Villain's Toolkit / Sketch-It / Debrief boxes: keep each on one page */\n"
    "div.stfs-box, div.stfs-box blockquote {\n"
    "  page-break-inside: avoid;\n"
    "  break-inside: avoid;\n"
    "}\n"
    "\n/* About the Author: portrait and text together on one page */\n"
    "div.author-page {\n"
    "  page-break-inside: avoid;\n"
    "  break-inside: avoid;\n"
    "}\n"
    "section#about-the-author h1 {\n"
    "  margin-top: 0;\n"
    "}\n"
    "div.author-page p:first-child {\n"
    "  text-align: center;\n"
    "  margin-top: 0.5em;\n"
    "  margin-bottom: 2em;  /* two blank lines' space before the text */\n"
    "}\n"
    # Smaller than the PDF's 35% (pandoc's inline style, hence !important),
    # which sent the text to the next page on a small screen. Sized in em,
    # not by screen width, so a wide, short screen doesn't enlarge it; the
    # max-width keeps it small on a narrow one. No vh: Kindle support for it
    # can't be relied on.
    "div.author-page img {\n"
    "  width: 6em !important;\n"
    "  max-width: 25%;\n"
    "  height: auto;\n"
    "}\n"
    "\n/* Frontispiece: a screen of its own, centered, scaled to fit */\n"
    "div.frontispiece {\n"
    "  page-break-before: always;\n"
    "  break-before: page;\n"
    "  page-break-after: always;\n"
    "  break-after: page;\n"
    "  text-align: center;\n"
    "}\n"
    "div.frontispiece img {\n"
    "  width: auto !important;\n"
    "  height: auto;\n"
    "  max-width: 100%;\n"
    "  max-height: 95vh;\n"
    "}\n"
    # The EPUB source's headings sit one level deeper than the PDF's inside
    # a Part (_shift_headings()): chapters are h2, sections h3. These give
    # each the look of the level it replaced, from pandoc's own h1/h2/h3
    # rules. h3.unlisted is the title page's subtitle, which isn't shifted.
    "\n/* Chapter and section headings, one level down inside a Part */\n"
    "h2.unnumbered {\n"
    "  margin: 3em 0 0 0;\n"
    "  font-size: 2em;\n"
    "  page-break-before: always;\n"
    "  line-height: 150%;\n"
    "}\n"
    "h3 {\n"
    "  margin: 1.5em 0 0 0;\n"
    "  font-size: 1.5em;\n"
    "  line-height: 135%;\n"
    "}\n"
    "h3.unlisted {\n"
    "  margin: 1.3em 0 0 0;\n"
    "  font-size: 1.3em;\n"
    "}\n"
    "h4 {\n"
    "  margin: 1.3em 0 0 0;\n"
    "  font-size: 1.3em;\n"
    "}\n"
    # pandoc's defaults (display: block, 0.5em side padding) stop a table
    # shrinking to the screen, so a wide one runs off the edge and is cut.
    "\n/* Tables: fit the screen, stay on one page */\n"
    "table {\n"
    "  display: table;\n"
    "  font-size: 0.75em;\n"
    "  page-break-inside: avoid;\n"
    "  break-inside: avoid;\n"
    "}\n"
    "th, td {\n"
    "  padding: 0.25em 0.2em;\n"
    "}\n"
    "\n/* Code: see _epub_code_block() */\n"
    "div.code-block {\n"
    "  margin: 1em 0;\n"
    "  padding-left: 0.6em;\n"
    "  border-left: 2px solid #888888;\n"
    "  text-align: left;\n"
    "}\n"
    "div.code-keep {\n"
    "  page-break-inside: avoid;\n"
    "  break-inside: avoid;\n"
    "}\n"
    "div.code-line {\n"
    "  overflow-wrap: break-word;\n"
    "  word-wrap: break-word;\n"
    "}\n"
    "div.code-line code {\n"
    "  font-family: monospace;\n"
    "  font-size: 100%;\n"
    "}\n"
    "\n/* Figures: image and caption together on one page */\n"
    "figure {\n"
    "  page-break-inside: avoid;\n"
    "  break-inside: avoid;\n"
    "  text-align: center;\n"
    "  margin: 1em 0;\n"
    "}\n"
    "figure img {\n"
    "  page-break-after: avoid;\n"
    "  break-after: avoid;\n"
    "}\n"
    "figcaption {\n"
    "  page-break-before: avoid;\n"
    "  break-before: avoid;\n"
    "  page-break-inside: avoid;\n"
    "  break-inside: avoid;\n"
    "  text-align: left;\n"
    "  font-size: 0.85em;\n"
    "  margin-top: 0.5em;\n"
    "}\n"
    "\n/* Part pages: centered, lower on the page */\n"
    # em here is the heading's own size: much more top margin and a long
    # title runs off a small screen and splits across two pages.
    "h1.part-page {\n"
    "  margin-top: 1.5em;\n"
    "  font-size: 1.6em;\n"
    "  text-align: center;\n"
    "}\n"
)


def _ordered_source_files():
    """Front matter (FRONT_MATTER order), then chapter-01..NN (zero-padded,
    so a filename sort is numeric order), then appendix-a..c."""
    chapters = sorted(
        f for f in os.listdir(BOOK_DIR)
        if f.startswith("chapter-") and f.endswith(".md")
    )
    appendices = sorted(
        f for f in os.listdir(BOOK_DIR)
        if f.startswith("appendix-") and f.endswith(".md")
    )
    return FRONT_MATTER + chapters + appendices


def _chapter_number(filename):
    m = re.match(r"chapter-(\d+)-", filename)
    return int(m.group(1)) if m else None


def _alt_text(description):
    """An IMAGE description as alt text: one line, no Markdown emphasis or
    code marks, with quotes and backslashes escaped for a pandoc
    attribute value."""
    text = re.sub(r"\s+", " ", description).strip()
    text = text.replace("**", "").replace("`", "").replace("*", "")
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _figures_in(content):
    """[(path, description, caption), ...] for every captioned IMAGE tag."""
    return IMAGE_WITH_CAPTION_RE.findall(content)


def _substitute_images(content, filename, out_dir):
    """Replace each IMAGE/CAPTION pair with a Markdown image whose alt text
    is the numbered caption pandoc prints ("Figure N.M: ...") and whose
    explicit `alt` attribute is the description. Paths are rewritten
    relative to out_dir, pandoc's working directory when it renders."""
    if filename == "title_page.md":
        return _with_title_page_image(content, out_dir)

    tags = IMAGE_TAG_RE.findall(content)
    figures = _figures_in(content)
    if len(tags) != len(figures):
        raise ValueError(
            f"{filename}: {len(tags)} **[IMAGE: ...]** tag(s) but only {len(figures)} in the "
            f"form **[IMAGE: path | description]** immediately followed by **[CAPTION: ...]**."
        )
    if not figures:
        return content
    chapter = _chapter_number(filename)
    if chapter is None:
        raise ValueError(f"{filename}: only chapters carry numbered figures")
    counter = {"i": 0}

    def _replace(match):
        counter["i"] += 1
        path, description, caption = match.groups()
        abs_path = os.path.normpath(os.path.join(BOOK_DIR, path))
        if not os.path.isfile(abs_path):
            raise ValueError(f"{filename}: image not found: {path}")
        rel_path = os.path.relpath(abs_path, out_dir)
        caption = re.sub(r"\s+", " ", caption)
        return f'![Figure {chapter}.{counter["i"]}: {caption}]({rel_path}){{alt="{_alt_text(description)}"}}'

    return IMAGE_WITH_CAPTION_RE.sub(_replace, content)


def _with_title_page_image(content, out_dir):
    """The title page's illustration, under the byline (after the first
    paragraph following the subtitle): raw LaTeX in the PDF, so it is never
    a numbered, captioned figure; the EPUB gets it as its cover image
    instead (render_epub())."""
    if not os.path.isfile(TITLE_PAGE_IMAGE):
        return content
    rel_path = os.path.relpath(TITLE_PAGE_IMAGE, out_dir)
    block = (
        "```{=latex}\n\\begin{center}\n"
        f"\\includegraphics[width=0.8\\textwidth,height=0.27\\textheight,keepaspectratio]{{{rel_path}}}\n"
        "\\end{center}\n```"
    )
    lines = content.strip().split("\n")
    # heading, subtitle, blank, byline -> image goes after the byline
    for i, line in enumerate(lines):
        if i > 1 and line.strip().startswith("*") and not line.strip().startswith("**"):
            return "\n".join(lines[: i + 1] + ["", block, ""] + lines[i + 1:])
    return "\n".join(lines[:2] + ["", block, ""] + lines[2:])


def _unnumber_h1(content):
    """Every top-level `# Heading` becomes `# Heading {-}` (unnumbered: the
    heading text already says "Chapter 3: ..."), skipping fenced code
    blocks, where a `# comment` line would otherwise be corrupted."""
    lines = content.split("\n")
    in_code_block = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            m = H1_RE.match(line)
            if m:
                lines[i] = f"# {m.group(1)} {{-}}"
    return "\n".join(lines)


BOX_TITLE_RE = re.compile(r"^> \*\*(Villain's Toolkit|Sketch-It|Debrief) — ")
_BOX_OPEN = "```{=latex}\n\\begin{stfsbox}\n```\n\n::: {.stfs-box}"
_BOX_CLOSE = ":::\n\n```{=latex}\n\\end{stfsbox}\n```"


def _keep_boxes_together(content):
    """Wrap each box blockquote so its title and content share a page: a
    raw-LaTeX stfsbox (unbreakable minipage) for the PDF, a div.stfs-box
    for the EPUB. A box is a run of `>` lines whose first line is a box
    title; fenced code blocks are skipped."""
    lines = content.split("\n")
    out = []
    in_code_block = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
        if not in_code_block and BOX_TITLE_RE.match(line):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            out += ["", _BOX_OPEN, ""] + lines[i:j] + ["", _BOX_CLOSE, ""]
            i = j
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def _delist_title_page_headings(content):
    """Keep the book title (H1) and subtitle (H3) out of the table of
    contents."""
    content = content.replace(f"# {TITLE} {{-}}", f"# {TITLE} {{-.unlisted}}")
    content = content.replace(f"### {SUBTITLE}", f"### {SUBTITLE} {{-.unlisted}}")
    return content


_TOC_MARKER = (
    "```{=latex}\n"
    "{\n"
    "\\setcounter{tocdepth}{0}\n"
    "\\tableofcontents\n"
    "}\n"
    "```"
)


def _part_marker(title, numbered=True):
    """\\part{} (numbered, with secnumdepth bumped locally so "Part N"
    prints) or \\part*{} plus a manual TOC entry for "Appendices"."""
    if numbered:
        return f"```{{=latex}}\n{{\\setcounter{{secnumdepth}}{{0}}\\part{{{title}}}}}\n```"
    return (
        "```{=latex}\n"
        f"\\part*{{{title}}}\n"
        f"\\addcontentsline{{toc}}{{part}}{{{title}}}\n"
        "```"
    )


EPUB_SOURCE_NAME = "_epub-source.md"

# A 6in Kindle's usable screen, and caption metrics at 0.85em, as tuned
# against Calibre renders in the later volumes.
_EPUB_SCREEN_W_IN = 3.3
_EPUB_SCREEN_H_IN = 4.45
_EPUB_CAPTION_CHARS_PER_LINE = 46
_EPUB_CAPTION_LINE_IN = 0.2
_EPUB_FIGURE_SPACING_IN = 0.25
_EPUB_FIGURE_RE = re.compile(r'^!\[(Figure \d+\.\d+: .*)\]\(([^)]+)\)\{alt=', re.MULTILINE)
_ROMAN_NUMERALS = ["I", "II", "III", "IV", "V", "VI", "VII"]


def _epub_part_heading(title, number=None):
    """A real level-1 heading for each Part in the EPUB (pandoc drops raw
    LaTeX there); None means the unnumbered "Appendices" divider."""
    if number is None:
        return f"# {title} {{-.part-page}}"
    return f"# Part {_ROMAN_NUMERALS[number - 1]} — {title} {{-.part-page}}"


_CODE_FENCE_RE = re.compile(r"^```([A-Za-z]*)$")
_CODE_FONT_EM = 0.75
_ALIGNED_FONT_MIN_EM = 0.58
_CODE_BLOCK_PADDING_IN = 0.1
_CODE_KEEP_MAX_LINES = 14
_MONO_ADVANCE_EM = 0.6
_CODE_HANG_EM = 1.2


def _epub_code_line(line, keep_whole):
    """One line of code as its own block, so a wrapped line continues
    indented and doesn't read as a new line of code."""
    text = line.rstrip()
    if not text:
        return '<div class="code-line"><code>&#160;</code></div>'
    indent = len(text) - len(text.lstrip(" "))
    hang = indent * _MONO_ADVANCE_EM + _CODE_HANG_EM
    escaped = html.escape(text, quote=False)
    if keep_whole:
        escaped = escaped.replace(" ", "&#160;")
    else:
        escaped = re.sub(r" {2,}", lambda m: "&#160;" * (len(m.group()) - 1) + " ", escaped)
        escaped = re.sub(r"^ +", lambda m: "&#160;" * len(m.group()), escaped)
    return (
        f'<div class="code-line" style="padding-left: {hang:.2f}em; text-indent: -{hang:.2f}em">'
        f"<code>{escaped}</code></div>"
    )


def _epub_code_block(lines, language):
    """A fenced code block as plain per-line HTML for the EPUB (pandoc's
    syntax colors read poorly on e-ink). JSON and shell output are laid out
    in columns, so they're sized to fit their widest line where they can;
    a block with no language is program output and keeps every space."""
    is_output = not language
    font_em = _CODE_FONT_EM
    if language not in ("python",):
        chars_at_1em = (_EPUB_SCREEN_W_IN - _CODE_BLOCK_PADDING_IN) * 72 / (12 * _MONO_ADVANCE_EM)
        widest = max((len(line.rstrip()) for line in lines), default=1) or 1
        font_em = max(_ALIGNED_FONT_MIN_EM, min(_CODE_FONT_EM, chars_at_1em / widest))
    classes = "code-block code-keep" if len(lines) <= _CODE_KEEP_MAX_LINES else "code-block"
    body = "\n".join(_epub_code_line(line, is_output) for line in lines)
    return f'```{{=html}}\n<div class="{classes}" style="font-size: {font_em:.2f}em">\n{body}\n</div>\n```'


def _plain_code_blocks_for_epub(content):
    """Replace every fenced code block with _epub_code_block()'s HTML; raw
    blocks (```{=latex}) pass through untouched."""
    lines = content.split("\n")
    out = []
    i = 0
    while i < len(lines):
        m = _CODE_FENCE_RE.match(lines[i])
        if m:
            end = lines.index("```", i + 1)
            out.append(_epub_code_block(lines[i + 1:end], m.group(1)))
            i = end + 1
            continue
        if lines[i].startswith("```{="):
            end = lines.index("```", i + 1)
            out.extend(lines[i:end + 1])
            i = end + 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def _png_aspect(path):
    """A PNG's height / width, from its header (1.0 for a non-PNG)."""
    with open(path, "rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        return _jpeg_aspect(path)
    width, height = struct.unpack(">II", header[16:24])
    return height / width


def _jpeg_aspect(path):
    """A JPEG's height / width, from its first SOF marker (1.0 if unknown)."""
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return height / width
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg_len
    return 1.0


def _size_figures_for_screen(content, out_dir):
    """Give each EPUB figure a width that leaves room for its caption on
    one Kindle screen."""
    def _replace(match):
        caption, rel_path = match.group(1), match.group(2)
        lines = math.ceil(len(caption) / _EPUB_CAPTION_CHARS_PER_LINE)
        image_h = _EPUB_SCREEN_H_IN - lines * _EPUB_CAPTION_LINE_IN - _EPUB_FIGURE_SPACING_IN
        width_in = image_h / _png_aspect(os.path.join(out_dir, rel_path))
        width_pct = max(40, min(100, math.floor(width_in / _EPUB_SCREEN_W_IN * 100)))
        return f"![{caption}]({rel_path}){{width={width_pct}% alt="
    return _EPUB_FIGURE_RE.sub(_replace, content)


def _shift_headings(content):
    """Every heading one level deeper (EPUB source only), so chapters nest
    under their Part in the table of contents."""
    lines = content.split("\n")
    in_code_block = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block and re.match(r"^#{1,5} ", line):
            lines[i] = "#" + line
    return "\n".join(lines)


def _expand_numbers(spec):
    """'3, 4 and 6' -> [3, 4, 6]; '8-10' / '8 through 10' -> [8, 9, 10]."""
    nums = []
    tokens = re.split(r"(,\s*|,?\s+(?:and|or)\s+)", spec)
    for tok in tokens:
        tok = tok.strip(" ,")
        if not tok or tok in ("and", "or"):
            continue
        m = re.match(r"^(\d+)\s*(?:[–-]|\s+(?:through|to)\s+)\s*(\d+)$", tok)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            nums.extend(range(a, b + 1) if a <= b else [a, b])
        elif tok.isdigit():
            nums.append(int(tok))
    return nums


def _strip_code(content):
    """Content with fenced code blocks and inline code removed, so a
    reference check reads only prose."""
    content = re.sub(r"^```.*?^```", "", content, flags=re.MULTILINE | re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", content)


def check_only():
    """Verify, without writing anything:
    - every IMAGE tag has the `path | description` form and a CAPTION, and
      its file exists;
    - every "Figure N.M" in the prose names a figure that exists, and no
      old-style "Figure N-M" reference is left;
    - every "Chapter N" reference is in range;
    - no chapter embeds a raw Markdown image that bypasses the tags;
    - images in examples/images/ that no tag uses (reported, not fatal).
    Prints a report; returns True if nothing fatal was found."""
    ok = True
    used = set()
    figures = {}  # chapter -> count
    files = _ordered_source_files()
    max_chapter = max(n for n in (_chapter_number(f) for f in files) if n is not None)
    texts = {}
    for filename in files:
        with open(os.path.join(BOOK_DIR, filename), encoding="utf-8") as f:
            texts[filename] = f.read()
    for filename in files:
        content = texts[filename]
        tags = IMAGE_TAG_RE.findall(content)
        figs = _figures_in(content)
        chapter = _chapter_number(filename)
        if len(tags) != len(figs):
            ok = False
            print(f"BAD      {filename}: {len(tags)} IMAGE tag(s), {len(figs)} well-formed with a CAPTION")
        for path, _, _ in figs:
            abs_path = os.path.normpath(os.path.join(BOOK_DIR, path))
            used.add(abs_path)
            if not os.path.isfile(abs_path):
                ok = False
                print(f"MISSING  {filename}: {path}")
        if figs and chapter is None:
            ok = False
            print(f"BAD      {filename}: figures outside a chapter")
        if chapter is not None:
            figures[chapter] = len(figs)
        if RAW_IMAGE_RE.search(content):
            ok = False
            print(f"RAW      {filename}: Markdown image outside an IMAGE tag")
    for filename in files:
        prose = _strip_code(texts[filename])
        for m in OLD_FIGURE_REF_RE.finditer(prose):
            ok = False
            print(f"OLDREF   {filename}: '{m.group(0)}' (write Figure N.M)")
        for m in FIGURE_REF_RE.finditer(prose):
            for ref in re.findall(r"\d+\.\d+", m.group(1)):
                ch, n = (int(x) for x in ref.split("."))
                if figures.get(ch, 0) < n:
                    ok = False
                    print(f"FIGREF   {filename}: Figure {ref} doesn't exist (Chapter {ch} has {figures.get(ch, 0)})")
        for m in CHAPTER_REF_RE.finditer(prose):
            for n in _expand_numbers(m.group(1)):
                if not 1 <= n <= max_chapter:
                    ok = False
                    print(f"CHREF    {filename}: 'Chapter {n}' is out of range (1-{max_chapter})")
    if os.path.isdir(IMAGE_DIR):
        unused = sorted(f for f in os.listdir(IMAGE_DIR)
                        if os.path.normpath(os.path.join(IMAGE_DIR, f)) not in used)
        if unused:
            print(f"\nNote: images in examples/images/ no IMAGE tag uses: {unused}")
    total = sum(figures.values())
    print(f"\n{total} figures across {sum(1 for v in figures.values() if v)} chapters.")
    print("All checks passed." if ok else "Problems found -- see above.")
    return ok


def assemble(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    parts = []
    epub_parts = []
    part_number = 0
    inside_part = False
    for filename in _ordered_source_files():
        if filename in PART_OPENERS:
            part_number += 1
            inside_part = True
            parts.append(_part_marker(PART_OPENERS[filename], numbered=True))
            epub_parts.append(_epub_part_heading(PART_OPENERS[filename], part_number))
        if filename == APPENDICES_OPENER_FILE:
            parts.append(_part_marker("Appendices", numbered=False))
            epub_parts.append(_epub_part_heading("Appendices"))
        with open(os.path.join(BOOK_DIR, filename), encoding="utf-8") as f:
            content = f.read()
        content = _substitute_images(content, filename, out_dir)
        content = _unnumber_h1(content)
        content = _keep_boxes_together(content)
        if filename == "title_page.md":
            content = _delist_title_page_headings(content)
        parts.append(content.strip())
        epub_content = _plain_code_blocks_for_epub(_size_figures_for_screen(content.strip(), out_dir))
        epub_parts.append(_shift_headings(epub_content) if inside_part else epub_content)
        if filename == "title_page.md":
            # our own \tableofcontents right after the title page (pandoc's
            # --toc would put it ahead of the title page)
            parts.append(_TOC_MARKER)
            epub_parts.append(_TOC_MARKER)

    with open(os.path.join(out_dir, EPUB_SOURCE_NAME), "w", encoding="utf-8") as f:
        f.write("\n\n".join(epub_parts) + "\n")
    md_path = os.path.join(out_dir, f"{OUTPUT_STEM}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(parts) + "\n")
    return md_path


def render_pdf(md_path, out_dir, pdf_engine):
    """Render the PDF with pandoc run from out_dir (image paths are
    relative to it). Returns True on success."""
    pdf_path_abs = os.path.abspath(os.path.join(out_dir, f"{OUTPUT_STEM}.pdf"))
    header_path = os.path.join(out_dir, "_pandoc-header.tex")
    with open(header_path, "w", encoding="utf-8") as f:
        f.write(_CODE_WRAP_HEADER)
    cmd = [
        "pandoc",
        os.path.basename(md_path),
        "-o", pdf_path_abs,
        f"--pdf-engine={pdf_engine}",
        "--top-level-division=chapter",
        "-V", "documentclass=book",
        # 7in x 9.19in, the series' trim size
        "-V", "geometry:paperwidth=7in,paperheight=9.19in,margin=0.75in",
        "-V", "mainfont=DejaVu Serif",
        "-V", "monofont=DejaVu Sans Mono",
        "-M", f"pagetitle={TITLE}",
        "-M", f"author={AUTHOR}",
        "--include-in-header", os.path.basename(header_path),
    ]
    try:
        subprocess.run(cmd, check=True, cwd=os.path.abspath(out_dir))
    except FileNotFoundError:
        print("pandoc not found on PATH -- skipping PDF output. "
              f"The assembled Markdown is still at {md_path}.", file=sys.stderr)
        return False
    except subprocess.CalledProcessError:
        print(f"pandoc exited with an error (see above) -- PDF not written. "
              f"The assembled Markdown is still at {md_path}.", file=sys.stderr)
        return False
    finally:
        os.remove(header_path)
    print(f"Wrote {pdf_path_abs}")
    return True


def _mark_epub_cover_nonlinear(epub_path):
    """Mark the cover page's spine item linear="no", so reading systems
    that show their own cover (Apple Books) don't show it twice. Rewrites
    the zip with the original ZipInfo entries, keeping `mimetype` first and
    uncompressed."""
    with zipfile.ZipFile(epub_path) as zin:
        infos = zin.infolist()
        data = {info.filename: zin.read(info.filename) for info in infos}
    opf_info = next(i for i in infos if i.filename.endswith(".opf"))
    opf_text = data[opf_info.filename].decode("utf-8")
    m = re.search(r'<item\s+id="([^"]+)"[^>]*href="text/cover\.xhtml"', opf_text)
    if not m:
        raise ValueError(f"couldn't find the cover.xhtml manifest item in {opf_info.filename}")
    fixed_text, n = re.subn(
        rf'(<itemref\s+idref="{re.escape(m.group(1))}")\s*/>', r'\1 linear="no" />', opf_text)
    if n != 1:
        raise ValueError(f"expected one cover <itemref> in {opf_info.filename}, found {n}")
    data[opf_info.filename] = fixed_text.encode("utf-8")
    with zipfile.ZipFile(epub_path, "w") as zout:
        for info in infos:
            zout.writestr(info, data[info.filename])


def render_epub(md_path, out_dir):
    """Render the EPUB from assemble()'s EPUB source (real Part headings,
    everything inside a Part one level deeper, --split-level=2 so each
    chapter starts a new file). Returns True on success."""
    epub_path_abs = os.path.abspath(os.path.join(out_dir, f"{OUTPUT_STEM}.epub"))
    cmd = [
        "pandoc",
        EPUB_SOURCE_NAME,
        "-o", epub_path_abs,
        "--split-level=2",
        "--toc",
        "--toc-depth=2",  # Parts and chapters only
        "-M", f"title={TITLE}",
        "-M", f"subtitle={SUBTITLE}",
        "-M", f"author={AUTHOR}",
    ]
    if os.path.isfile(TITLE_PAGE_IMAGE):
        cmd += ["--epub-cover-image", os.path.relpath(TITLE_PAGE_IMAGE, out_dir)]
    try:
        default_css = subprocess.run(
            ["pandoc", "--print-default-data-file", "epub.css"],
            check=True, capture_output=True, text=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        default_css = None
    if default_css is not None:
        css_path = os.path.join(out_dir, "_epub-style.css")
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(default_css + _EPUB_BOX_CSS)
        cmd += ["--css", os.path.basename(css_path)]
    try:
        subprocess.run(cmd, check=True, cwd=os.path.abspath(out_dir))
    except FileNotFoundError:
        print("pandoc not found on PATH -- skipping EPUB output. "
              f"The assembled Markdown is still at {md_path}.", file=sys.stderr)
        return False
    except subprocess.CalledProcessError:
        print(f"pandoc exited with an error (see above) -- EPUB not written. "
              f"The assembled Markdown is still at {md_path}.", file=sys.stderr)
        return False
    if os.path.isfile(TITLE_PAGE_IMAGE):
        _mark_epub_cover_nonlinear(epub_path_abs)
    print(f"Wrote {epub_path_abs}")
    return True


def check_epub_parts(epub_path):
    """Confirm every Part and the Appendices divider reached the EPUB's
    nav.xhtml, its toc.ncx, and the text as a part-page heading -- the
    second volume's EPUB once lost its Parts unnoticed."""
    expected = [f"Part {_ROMAN_NUMERALS[i]} — {title}"
                for i, title in enumerate(PART_OPENERS.values())] + ["Appendices"]
    with zipfile.ZipFile(epub_path) as z:
        names = z.namelist()

        def read(suffix):
            found = [n for n in names if n.endswith(suffix)]
            return html.unescape(z.read(found[0]).decode("utf-8")) if found else ""
        nav = read("nav.xhtml")
        ncx = read("toc.ncx")
        body = "\n".join(html.unescape(z.read(n).decode("utf-8"))
                         for n in names if n.endswith(".xhtml") and not n.endswith("nav.xhtml"))
    norm = lambda t: t.replace("\u2019", "'")
    nav, ncx, body = norm(nav), norm(ncx), norm(body)
    headings = [norm(re.sub(r"<[^>]+>", "", h)).strip()
                for h in re.findall(r'<h1[^>]*class="[^"]*part-page[^"]*"[^>]*>(.*?)</h1>', body, re.S)]
    problems = []
    for title in expected:
        if title not in nav:
            problems.append(f"missing from nav.xhtml: {title}")
        if title not in ncx:
            problems.append(f"missing from toc.ncx: {title}")
        if title not in headings:
            problems.append(f"no part-page heading in the text: {title}")
    if problems:
        print("EPUB Part check FAILED:")
        for p in problems:
            print("  " + p)
        return False
    print(f"EPUB Part check passed: {len(expected)} dividers in nav.xhtml, toc.ncx, and the text.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Assemble the book into one Markdown file, then PDF/EPUB via pandoc.")
    parser.add_argument("--out", type=str, default="dist", help="Directory to write output into.")
    parser.add_argument("--skip-pdf", action="store_true", help="Don't invoke pandoc for the PDF.")
    parser.add_argument("--skip-epub", action="store_true", help="Don't invoke pandoc for the EPUB.")
    parser.add_argument("--pdf-engine", type=str, default="xelatex", help="pandoc --pdf-engine to use.")
    parser.add_argument("--check-only", action="store_true",
                        help="Verify image tags, figure and chapter references; write nothing.")
    args = parser.parse_args()

    if args.check_only:
        sys.exit(0 if check_only() else 1)
    if not check_only():
        print("Fix the problems above before building.", file=sys.stderr)
        sys.exit(1)

    out_dir = args.out if os.path.isabs(args.out) else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), args.out
    )
    md_path = assemble(out_dir)
    print(f"Wrote {md_path} ({len(_ordered_source_files())} source files)")
    if not args.skip_pdf:
        render_pdf(md_path, out_dir, args.pdf_engine)
    if not args.skip_epub:
        if render_epub(md_path, out_dir):
            if not check_epub_parts(os.path.join(out_dir, f"{OUTPUT_STEM}.epub")):
                sys.exit(1)


if __name__ == "__main__":
    main()
