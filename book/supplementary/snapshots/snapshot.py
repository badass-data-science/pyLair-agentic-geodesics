"""Book-style JSON snapshots of real pyLair and pyFit tool output.

This is the generator behind the book's What Comes Back snapshots (the
convention Chapter 2 explains): every top-level field appears; lists show
their first entry or two, then a bare ...; nested objects show their first
few fields, then ...; numbers are rounded to four places, except the
resolved parameters, which are never rounded (0.499999 rounded to 0.5
would be the one cutoff that fails). Floating-point noise below 1e-12
prints as 0.0. The output is then laid out to the book's 52-character
width with ../../tools/json_pretty.py.

Command line: name a tool and its arguments, get its snapshot.

    python3 snapshot.py design_dome frequency=4
    python3 snapshot.py get_bill_of_materials frequency=6 truncation_z=0.499999
    python3 snapshot.py get_assembly_manifest frequency=4 n_frequency=1 dome_class=3 \
        elongation_z=1.8 truncation_z=0.499999

The book's own snapshots sometimes show more entries of the list a chapter
discusses (hub 1's angles, say); the functions below take options for that
(`show`, `pick`), and each chapter's What Comes Back label says what it
shows.
"""
import json
import math

ROUND = 4


def num(x):
    if isinstance(x, bool) or x is None:
        return json.dumps(x)
    if isinstance(x, int):
        return str(x)
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return json.dumps(x)
    if math.isfinite(xf) and xf == int(xf) and abs(xf) < 1e12:
        return f"{xf:.1f}"
    if abs(xf) < 1e-12:
        return "0.0"   # floating-point noise, not a measurement
    r = round(xf, ROUND)
    if r == 0 and xf != 0:
        return f"{xf:.2e}"
    return repr(r)


def scalar(x, maxstr=60):
    if isinstance(x, str):
        s = x if len(x) <= maxstr else x[:maxstr].rstrip() + "..."
        return json.dumps(s)
    return num(x)


def inline(o, items=2, keys=4, maxstr=50):
    """One-line rendering with truncation."""
    if isinstance(o, dict):
        ks = list(o.items())
        parts = [f"{json.dumps(k)}: {inline(v, items, keys, maxstr)}" for k, v in ks[:keys]]
        if len(ks) > keys:
            parts.append("...")
        return "{" + ", ".join(parts) + "}"
    if isinstance(o, (list, tuple)):
        if all(not isinstance(v, (dict, list, tuple)) for v in o) and len(o) <= max(items, 4):
            return "[" + ", ".join(scalar(v, maxstr) for v in o) + "]"
        parts = [inline(v, items, keys, maxstr) for v in o[:items]]
        if len(o) > items:
            parts.append("...")
        return "[" + ", ".join(parts) + "]"
    return scalar(o, maxstr)


def snap(o, items=1, keys=4, expand=(), indent=2, maxstr=50, list_items=None, pick=None):
    """Pretty snapshot: each key of the top-level dict on its own line;
    keys named in `expand` are themselves shown one key/item per line."""
    pad = " " * indent
    if not isinstance(o, dict):
        return inline(o, items, keys, maxstr)
    lines = ["{"]
    for n, (k, v) in enumerate(o.items()):
        comma = "," if n < len(o) - 1 else ""
        if k in expand and isinstance(v, dict):
            sub = snap(v, items, keys, expand, indent, maxstr, list_items, pick).split("\n")
            lines.append(f"{pad}{json.dumps(k)}: " + sub[0])
            lines += [pad + s for s in sub[1:-1]]
            lines.append(pad + sub[-1] + comma)
        elif isinstance(v, list) and k in (pick or {}):
            # chosen entries (by index), with ... wherever entries are skipped
            idx = sorted(pick[k])
            lines.append(f"{pad}{json.dumps(k)}: [")
            prev = -1
            for i in idx:
                if i != prev + 1:
                    lines.append(f"{pad}{pad}...")
                lines.append(f"{pad}{pad}{inline(v[i], items, 10, maxstr)},")
                prev = i
            if prev < len(v) - 1:
                lines.append(f"{pad}{pad}...")
            else:
                lines[-1] = lines[-1].rstrip(",")
            lines.append(f"{pad}]{comma}")
        elif isinstance(v, list) and (k in expand or (list_items or {}).get(k, 1) > 1):
            li = (list_items or {}).get(k, items)
            lines.append(f"{pad}{json.dumps(k)}: [")
            for it in v[:li]:
                lines.append(f"{pad}{pad}{inline(it, items, keys, maxstr)},")
            if len(v) > li:
                lines.append(f"{pad}{pad}...")
            else:
                lines[-1] = lines[-1].rstrip(",")
            lines.append(f"{pad}]{comma}")
        else:
            li = (list_items or {}).get(k, items)
            lines.append(f"{pad}{json.dumps(k)}: {inline(v, li, keys, maxstr)}{comma}")
    lines.append("}")
    return "\n".join(lines)


def bom_snap(b, show=None, keys=3, items=1, pick=None):
    """Snapshot of a get_bill_of_materials report: every section, with the
    section(s) in `show` given more entries ({section name: n})."""
    return snap(b, items=items, keys=keys,
                expand=("pyLair report", "Bill of materials", "Panel shapes and counts"),
                list_items=show or {}, pick=pick)


DEFAULT_RP = {"n_frequency": None,
              "elongation_factors": {"x": 1.0, "y": 1.0, "z": 1.0},
              "truncation": {"x": None, "y": None, "z": None}}


def rp_inline(rp):
    """resolved_parameters: radius, frequency, polyhedron, dome_class, plus
    every setting that differs from its default; ... if anything is left out."""
    shown = []
    for k, v in rp.items():
        if k in DEFAULT_RP and v == DEFAULT_RP[k]:
            continue
        # Parameters are shown exactly as resolved, never rounded: 0.499999
        # rounded to 0.5 would be the one cutoff that fails (Chapter 9).
        shown.append(f"{json.dumps(k)}: {json.dumps(v)}")
    more = len(shown) < len(rp)
    return "{" + ", ".join(shown + (["..."] if more else [])) + "}"


def design_snap(d, rp_keys=None):
    lines = ["{"]
    items = list(d.items())
    for n, (k, v) in enumerate(items):
        comma = "," if n < len(items) - 1 else ""
        val = rp_inline(v) if k == "resolved_parameters" else inline(v, 3, 3)
        lines.append(f'  "{k}": {val}{comma}')
    lines.append("}")
    return "\n".join(lines)


def manifest_snap(man, hub="H0", conns=3, strut="S0", panel="P0", show_struts=None):
    """Snapshot of get_assembly_manifest: every section, one entry each
    (the named hub with `conns` of its connections), groups one entry each."""
    def entry(d, key, inner=None, n=1):
        e = dict(d[key])
        lines = [f'    "{key}": {{']
        items = list(e.items())
        for i, (k, v) in enumerate(items):
            comma = "," if i < len(items) - 1 else ""
            if k == inner and isinstance(v, list):
                lines.append(f'      "{k}": [')
                for it in v[:n]:
                    lines.append(f"        {inline(it, 2, 8)},")
                lines.append("        ..." if len(v) > n else lines.pop().rstrip(","))
                lines.append(f"      ]{comma}")
            else:
                lines.append(f'      "{k}": {inline(v, 3, 6)}{comma}')
        lines.append("    },")
        return lines
    out = ["{", '  "hubs": {']
    out += entry(man["hubs"], hub, "connections", conns)
    out += ["    ...", "  },", '  "struts": {']
    for sk in (show_struts or [strut]):
        out += entry(man["struts"], sk)
    out += ["    ...", "  },", '  "panels": {']
    out += entry(man["panels"], panel, "edges", 1)
    out += ["    ...", "  },"]
    for g in ("hub_groups", "strut_groups", "panel_groups"):
        comma = "," if g != "panel_groups" else ""
        out.append(f'  "{g}": [{inline(man[g][0], 2, 6)}, ...]{comma}')
    out.append("}")
    return "\n".join(out)


def snapshot_of(tool, result):
    """The default snapshot for a tool's result."""
    if tool in ("design_dome",):
        return design_snap(result)
    if tool == "get_bill_of_materials":
        return bom_snap(result)
    if tool == "get_assembly_manifest":
        return manifest_snap(result)
    if tool == "export_dome":
        return snap(result, items=1, keys=3, list_items={"files_written": 4},
                    expand=("bill_of_materials", "pyLair report", "Bill of materials", "Panel shapes and counts"))
    return snap(result, items=2, keys=6, list_items={"placements": 2, "files_written": 4})


def _value(text):
    try:
        return json.loads(text)
    except ValueError:
        return text


def main(argv):
    import asyncio
    import inspect
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
    import json_pretty
    from pylair import mcp_server as pylair
    from pyfit import mcp_server as pyfit
    tool, kwargs = argv[0], dict(a.split("=", 1) for a in argv[1:])
    kwargs = {k: _value(v) for k, v in kwargs.items()}
    fn = getattr(pylair, tool, None) or getattr(pyfit, tool)
    result = fn(**kwargs)
    if inspect.isawaitable(result):
        result = asyncio.run(result)
    print(json_pretty.reformat(snapshot_of(tool, result)))


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1:])
