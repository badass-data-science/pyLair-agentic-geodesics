# book-assembly

Concatenates the book's front matter, all chapters, and appendices into one Markdown file, then renders it to PDF and EPUB via `assemble_book.py`. Adapted from the later "for Supervillains" volumes' script; it replaces the older `examples/assemble_book.py`.

## Usage

Run from this directory:

```bash
python3 assemble_book.py
```

That writes `dist/geodesic-lair-book.{md,pdf,epub}`. Useful variants:

```bash
python3 assemble_book.py --out DIR            # write elsewhere
python3 assemble_book.py --skip-pdf           # markdown + EPUB only
python3 assemble_book.py --skip-epub          # markdown + PDF only
python3 assemble_book.py --check-only         # verify images and references, writes nothing
python3 assemble_book.py --pdf-engine ENGINE  # default is xelatex
```

Every build runs the `--check-only` checks first and stops if any fails:

- every figure is written as `**[IMAGE: path | alt-text description]**` followed by `**[CAPTION: caption]**`, and its file exists (paths are relative to `book/`);
- every "Figure N.M" in the prose names a real figure (figures are numbered per chapter, in order of appearance), and no old-style "Figure N-M" is left;
- every "Chapter N" reference is in range;
- no chapter embeds a raw `![...](...)` image that would bypass numbering.

After writing the EPUB, the script checks that all seven Parts and the Appendices divider appear in its `nav.xhtml`, its `toc.ncx`, and the text.

Only the files the script names are read: `README.md`, `outline.md`, `AGENTS.md`, and `examples/` are never included.

## Requirements

- The Markdown output needs nothing extra.
- The PDF step needs `pandoc` and a LaTeX engine (`xelatex` by default), plus the DejaVu fonts.
- The EPUB step needs only `pandoc`.

`dist/` is gitignored; its contents are rebuildable.
