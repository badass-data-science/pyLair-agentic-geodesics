"""Re-lay out the book's ```json blocks to fit a narrow (Kindle) width.

Like Python's pprint, but for JSON: a list or object that fits on one line
stays on one line; one that doesn't is broken open, one level at a time,
until every line fits within WIDTH characters (where possible: a single
key or string longer than WIDTH can't be broken). Lists of plain numbers or
strings are filled several to a line instead of one per line.

The book's JSON blocks are often *snapshots* (see Chapter 2): a bare `...`
stands for omitted list entries or object fields, and a block may hold
several JSON values, one after another. Both are understood here. Every
number and string is kept exactly as written (its original text, never
re-rounded), and each reformatted block is parsed again and checked to
hold exactly the same values as before.

Usage:
    python3 tools/json_pretty.py FILE.md [...]           # rewrite in place
    python3 tools/json_pretty.py --check FILE.md [...]   # report, change nothing
"""

import re
import sys

WIDTH = 52
INDENT = 2


class Ellipsis_:
    def __eq__(self, other):
        return isinstance(other, Ellipsis_)

    def __repr__(self):
        return "..."


ELL = Ellipsis_()


class Atom:
    """A number, string, true/false/null, kept as its exact source text."""

    def __init__(self, text):
        self.text = text

    def __eq__(self, other):
        return isinstance(other, Atom) and other.text == self.text

    def __repr__(self):
        return self.text


TOKEN = re.compile(r'''\s*(?:(?P<str>"(?:[^"\\]|\\.)*")|(?P<ell>\.\.\.)|(?P<num>-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)|(?P<word>true|false|null)|(?P<p>[{}\[\]:,]))''')


def tokenize(text):
    pos, out = 0, []
    text = text.rstrip()
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m or m.end() == pos:
            raise ValueError(f"can't parse near: {text[pos:pos + 40]!r}")
        pos = m.end()
        kind = m.lastgroup
        out.append((kind, m.group(kind)))
    return out


class Parser:
    def __init__(self, tokens):
        self.t, self.i = tokens, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self, value=None):
        kind, v = self.peek()
        if value is not None and v != value:
            raise ValueError(f"expected {value!r}, got {v!r}")
        self.i += 1
        return kind, v

    def value(self):
        kind, v = self.peek()
        if v == "{":
            return self.obj()
        if v == "[":
            return self.arr()
        if kind == "ell":
            self.take()
            return ELL
        if kind in ("str", "num", "word"):
            self.take()
            return Atom(v)
        raise ValueError(f"unexpected token {v!r}")

    def obj(self):
        self.take("{")
        items = []
        while self.peek()[1] != "}":
            if self.peek()[0] == "ell":
                self.take()
                items.append(ELL)
            else:
                _, k = self.take()
                self.take(":")
                items.append((k, self.value()))
            if self.peek()[1] == ",":
                self.take()
        self.take("}")
        return ("obj", items)

    def arr(self):
        self.take("[")
        items = []
        while self.peek()[1] != "]":
            items.append(self.value())
            if self.peek()[1] == ",":
                self.take()
        self.take("]")
        return ("arr", items)

    def values(self):
        out = []
        while self.i < len(self.t):
            out.append(self.value())
            if self.peek()[1] == ",":   # a stray separator between values
                self.take()
        return out


def parse_block(text):
    return Parser(tokenize(text)).values()


def flat(node):
    if node is ELL or isinstance(node, Ellipsis_):
        return "..."
    if isinstance(node, Atom):
        return node.text
    kind, items = node
    if kind == "arr":
        return "[" + ", ".join(flat(x) for x in items) + "]"
    return "{" + ", ".join("..." if x is ELL else f"{x[0]}: {flat(x[1])}" for x in items) + "}"


def is_scalar(x):
    return isinstance(x, (Atom, Ellipsis_))


PACK_MAX = 34      # a container this short (flattened) can share a line
HANG_MAX = 24      # deepest column a pprint-style hanging indent may start at


def pieces(node):
    """The items of a container as one-line strings, or None if any item
    is too big to share a line with its neighbours."""
    kind, items = node
    out = []
    for x in items:
        if x is ELL:
            out.append("...")
            continue
        p = flat(x) if kind == "arr" else f"{x[0]}: {flat(x[1])}"
        v = x if kind == "arr" else x[1]
        if not is_scalar(v) and len(flat(v)) > PACK_MAX:
            return None
        out.append(p)
    return out


def packed(start, cont_col, ps, close, suffix):
    """Fill pieces onto lines, pprint style: the first line begins with
    `start`, later lines are indented to `cont_col`."""
    lines, cur = [], start
    for n, p in enumerate(ps):
        tail = close + suffix if n == len(ps) - 1 else ","
        sep = "" if cur.endswith(("[", "{")) or cur.strip() == "" else " "
        trial = cur + sep + p + tail
        if len(trial) > WIDTH and cur.strip() not in ("", "[", "{") and not cur.endswith(("[", "{")):
            lines.append(cur.rstrip())
            cur = " " * cont_col + p + tail
        else:
            cur = trial
    lines.append(cur)
    return lines


def fmt(node, indent, prefix="", suffix=""):
    """Lines for `prefix + node + suffix` at `indent` columns."""
    pad = " " * indent
    one = pad + prefix + flat(node) + suffix
    if len(one) <= WIDTH or is_scalar(node):
        return [one]
    kind, items = node
    open_, close = ("[", "]") if kind == "arr" else ("{", "}")
    ps = pieces(node)
    if ps:
        head = pad + prefix + open_
        fits = lambda ls: max(len(l) for l in ls) <= WIDTH
        if len(head) <= HANG_MAX:
            # {"a": 1, "b": 2,
            #  "c": 3}
            hanging = packed(head, len(head), ps, close, suffix)
            if fits(hanging):
                return hanging
        # open here, pack the items on indented lines below
        body = [head] + packed(" " * (indent + INDENT), indent + INDENT, ps, "", "") + [pad + close + suffix]
        if fits(body):
            return body
        # still too wide: fall through to one item per line
    lines = [pad + prefix + open_]
    inner = indent + INDENT
    ipad = " " * inner
    if kind == "arr" and items and all(is_scalar(x) for x in items):
        # fill: several scalars per line
        cur = ""
        for n, x in enumerate(items):
            piece = flat(x) + ("," if n < len(items) - 1 else "")
            if cur and len(ipad + cur + " " + piece) > WIDTH:
                lines.append(ipad + cur)
                cur = piece
            else:
                cur = (cur + " " + piece) if cur else piece
        lines.append(ipad + cur)
    else:
        for n, x in enumerate(items):
            comma = "," if n < len(items) - 1 else ""
            if x is ELL:
                lines.append(ipad + "..." + comma)
            elif kind == "arr":
                lines += fmt(x, inner, "", comma)
            else:
                lines += fmt(x[1], inner, x[0] + ": ", comma)
    lines.append(pad + close + suffix)
    return lines


def same(a, b):
    if isinstance(a, (Atom, Ellipsis_)) or isinstance(b, (Atom, Ellipsis_)):
        return a == b
    return a[0] == b[0] and len(a[1]) == len(b[1]) and all(
        (x is ELL and y is ELL) or (not (x is ELL or y is ELL) and (
            same(x, y) if a[0] == "arr" else (x[0] == y[0] and same(x[1], y[1]))))
        for x, y in zip(a[1], b[1]))


def reformat(text):
    values = parse_block(text)
    out = []
    for v in values:
        out += fmt(v, 0)
    new = "\n".join(out)
    again = parse_block(new)
    assert len(again) == len(values) and all(same(x, y) for x, y in zip(values, again)), "content changed"
    return new


BLOCK = re.compile(r"(^```json\n)(.*?)(^```$)", re.M | re.S)


def process(path, check=False):
    text = open(path, encoding="utf-8").read()
    problems, changed = [], 0

    def sub(m):
        nonlocal changed
        body = m.group(2).rstrip("\n")
        try:
            new = reformat(body)
        except Exception as e:  # leave the block as it is, and say so
            line = text[:m.start()].count("\n") + 1
            problems.append(f"{path}:{line}: {e}")
            return m.group(0)
        if new != body:
            changed += 1
        return m.group(1) + new + "\n" + m.group(3)

    new_text = BLOCK.sub(sub, text)
    if not check and new_text != text:
        open(path, "w", encoding="utf-8").write(new_text)
    long_lines = [(n, l) for n, l in enumerate(new_text.split("\n"), 1) if len(l) > WIDTH and _in_json(new_text, n)]
    return changed, problems, long_lines


def _in_json(text, lineno):
    inside = False
    for n, l in enumerate(text.split("\n"), 1):
        if l.startswith("```json"):
            inside = True
            continue
        if l.startswith("```"):
            inside = False
            continue
        if n == lineno:
            return inside
    return False


if __name__ == "__main__":
    args = sys.argv[1:]
    check = "--check" in args
    files = [a for a in args if a != "--check"]
    for f in files:
        changed, problems, long_lines = process(f, check)
        print(f"{f}: {changed} block(s) {'would change' if check else 'reformatted'}")
        for p in problems:
            print("  UNPARSED", p)
        for n, l in long_lines:
            print(f"  still {len(l)} chars at line {n}: {l.strip()[:60]}")
