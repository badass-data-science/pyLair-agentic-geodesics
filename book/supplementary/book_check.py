"""Shared helper for the supplementary scripts: print each result beside
the value the book prints, and say whether they agree."""

import sys

_failures = []


def _plain(x):
    """numpy scalars (and containers of them) as plain Python values, so
    results print the way the book prints them."""
    if hasattr(x, "item") and not isinstance(x, (list, tuple, dict)):
        return x.item()
    if isinstance(x, (list, tuple)):
        return type(x)(_plain(v) for v in x)
    if isinstance(x, dict):
        return {k: _plain(v) for k, v in x.items()}
    return x


def check(label, got, book, tol=0.0):
    """Report `got` against the book's `book`. Numbers agree within `tol`
    (absolute); anything else must be equal."""
    got = _plain(got)
    if isinstance(book, (int, float)) and not isinstance(book, bool):
        ok = abs(got - book) <= tol
    else:
        ok = got == book
    mark = "ok  " if ok else "DIFF"
    print(f"  [{mark}] {label}: {got!r}  (book: {book!r})")
    if not ok:
        _failures.append(label)
    return ok


def note(label, value):
    """Report a value the book describes but doesn't pin to a fixed number
    (a timing, say)."""
    print(f"  [info] {label}: {value}")


def done():
    """Exit non-zero if anything disagreed with the book."""
    if _failures:
        print(f"\n{len(_failures)} result(s) differ from the book: {', '.join(_failures)}")
        sys.exit(1)
    print("\nAll results match the book.")
