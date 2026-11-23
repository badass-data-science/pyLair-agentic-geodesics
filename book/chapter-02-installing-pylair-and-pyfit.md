# Chapter 2: Installing pyLair and pyFit (OpenClaw, Claude Code, Hermes, Claude Desktop, and Any MCP Framework)

The Unbending Foreman's first act as head of construction was to refuse to look at any dome. He wanted a shed first: something small enough to check by hand, built on the new equipment, before anyone's lair depended on it. "The Rival's crew trusted the first thing the machine said," he pointed out. "Make the machine say something we can check."

So before Chapter 3 picks a polyhedron, something more tedious happens: the wiring. This chapter has no geometry in it and no nesting either. What it has is a working connection between an AI agent and two small servers that know how to talk to it, plus one installation failure, shown as it happens, because you are going to hit some version of it too, and it is much less alarming once you've seen it coming.

## What You're Installing

Both pyLair and pyFit are ordinary, installable **Python** packages. As of this writing, neither has been published to PyPI, the Python Package Index that `pip install` normally downloads from (pyLair's blog post lists that under "Next Steps," and pyFit's `AGENTS.md` says "publishing is a separate, deliberate step"). So for now both install the same way: clone the repository (pyLair's lives at [github.com/badass-data-science/pyLair-agentic-geodesics](https://github.com/badass-data-science/pyLair-agentic-geodesics), pyFit's at [github.com/badass-data-science/pyFit-agentic-polygon-nesting](https://github.com/badass-data-science/pyFit-agentic-polygon-nesting)), then install it in editable mode with the `mcp` extra:

```bash
git clone \
  https://github.com/badass-data-science/pyLair-agentic-geodesics.git
cd pyLair-agentic-geodesics
pip install -e ".[mcp]"
```

```bash
git clone \
  https://github.com/badass-data-science/pyFit-agentic-polygon-nesting.git
cd pyFit-agentic-polygon-nesting
pip install -e ".[mcp]"
```

Each install gives you two **console scripts**, small executable commands: a plain CLI (`pylair`, `pyfit`) and, with the `mcp` extra, an MCP server (`pylair-mcp`, `pyfit-mcp`), a lightweight process that speaks the Model Context Protocol over standard input and output and, when asked, reports which typed tools it exposes.

One naming detail for when pyFit *is* published: its distribution name is `pyfit-agentic-polygon-nesting` (plain `pyfit` was already taken on PyPI by an unrelated neural-network library), but the importable package, the CLI, and the MCP server stay `pyfit` and `pyfit-mcp`. pyLair has no such split; everything is `pylair`.

Once both are installed, confirm all four console scripts landed on your `PATH`:

```bash
which pylair pylair-mcp pyfit pyfit-mcp
```

Each should resolve to a path inside the virtual environment you installed into. If any comes back empty, the install didn't finish cleanly. Fix that before going further: nearly every installation problem after this point is a variation on "the agent couldn't find the command."

## Understanding the Connection, Not Just Copying It

Every agentic platform that can use pyLair or pyFit does the same three things, however its configuration format phrases them:

1. **Know the command** that starts each server (`pylair-mcp`, `pyfit-mcp`).
2. **Launch it over stdio**: the platform starts the server as a subprocess and talks to it through its standard input and output streams, not over a network port.
3. **Discover its tools** by asking the running server what it exposes, rather than having them hard-coded anywhere.

Once you see that this is *all* that happens underneath any platform's configuration screen, installing pyLair or pyFit stops being platform trivia and becomes "fill in these three things in whatever format this tool wants." The rest of this section walks through a few platforms, and then "whatever you're using instead," because the pattern matters more than any one platform.

### OpenClaw

For [OpenClaw](https://openclaw.ai/), each project ships an **OpenClaw skill** instead of relying on its MCP server: a Markdown playbook that teaches an OpenClaw agent to drive the plain CLI (`pylair`, `pyfit`) directly. (pyLair's repository notes that OpenClaw has no MCP client, which is why its skill wraps the CLI.) This is a separate integration path from the `pylair-mcp` and `pyfit-mcp` servers below, and **the two skills use different directory conventions**, so following pyLair's layout for pyFit will leave pyFit's skill undiscovered.

**pyLair's skill** is a single file at the repository root, `SKILL.md`. To install it:

1. Copy (or symlink) `SKILL.md` into your OpenClaw workspace's skills directory, for example `~/.openclaw/workspace/skills/pylair/SKILL.md`.
2. Merge pyLair's `openclaw.config.snippet.jsonc` into `~/.openclaw/openclaw.json`:

```jsonc
{
  skills: {
    entries: {
      pylair: {
        enabled: true,
      },
    },
  },
}
```

That's the whole configuration: pyLair has no API key or environment variable to set. The skill's frontmatter gates it on the `pylair` binary being on `PATH` (`metadata.openclaw.requires.bins: ["pylair"]`), so the entry only needs to exist and be enabled once the CLI is installed.

**pyFit's skill** lives one level down, at `skills/pyfit/SKILL.md` in its repository. OpenClaw discovers skills by scanning configured roots for `<root>/<skill-name>/SKILL.md`, and pyFit's config snippet uses that by pointing at the repository's `skills/` directory instead of asking you to copy anything into your workspace:

```jsonc
{
  "skills": {
    "load": {
      "extraDirs": [
        "/absolute/path/to/pyFit-agentic-polygon-nesting/skills"
      ]
    },
    "entries": {
      "pyfit": {
        "enabled": true
      }
    }
  }
}
```

Merge that into `~/.openclaw/openclaw.json`, replacing the `extraDirs` path with wherever you cloned the repository, with `pyfit` installed and on `PATH`. Again there's no API key, just the same `requires.bins` gate pyLair's skill uses.

Two skills, two conventions: **copy pyLair's file in; point at pyFit's directory.** Getting this backwards (symlinking pyFit's nested file the way pyLair's flat one works, or pointing `extraDirs` at pyLair's repository root) is an easy mistake. Read each project's own installation section rather than assuming the two mirror each other.

### Claude Code

Claude Code registers MCP servers either in a project-level `.mcp.json` file, using the same `command`/`args` shape shown throughout this chapter, or with `claude mcp add` from the command line. CLI flags are the part of any tool most likely to have changed by the time you read this, so run `claude mcp add --help` for the current syntax. The stable fact is that you give it the same information as everywhere else: a name, a command, and (here, empty) arguments, once per server:

```jsonc
{
  "mcpServers": {
    "pylair": {"command": "pylair-mcp", "args": []},
    "pyfit": {"command": "pyfit-mcp", "args": []}
  }
}
```

Both projects' `SKILL.md` files are written in the format OpenClaw consumes. Claude Code doesn't load them the same way, but they remain useful reference material: point your agent at one when you want it to follow that project's documented CLI workflow.

### Hermes, and Other MCP-Speaking Agent Frameworks

Rather than guess at a configuration format this book can't verify, here is the general rule: **if Hermes, or any other agent framework, can launch a subprocess by command and arguments and speak MCP over stdio, the three steps above apply unchanged.** Register `pylair-mcp` and `pyfit-mcp` the way you would any other server. That platform's documentation says where its configuration file lives and which key holds the server list; the *shape* of what goes in it is what this chapter has already shown.

### Generic MCP Clients (Claude Desktop and Others)

Several general-purpose AI assistants also speak MCP directly. Claude Desktop is a common one, configured through a `claude_desktop_config.json` file (its location varies by operating system) whose `mcpServers` key holds the same `command`/`args` shape once more:

```jsonc
{
  "mcpServers": {
    "pylair": {"command": "pylair-mcp", "args": []},
    "pyfit": {"command": "pyfit-mcp", "args": []}
  }
}
```

If this is starting to feel repetitive, that's the point: MCP is a *standard*, and once you've set pyLair and pyFit up on one client, setting them up on the next is mostly a matter of finding where it keeps its configuration file.

## The Gotcha, Hit on Purpose

The AI Henchman's first words to the new servers were an apology. "The tool `pylair-mcp` does not exist," it reported, with total confidence, thirty seconds after our Heroine had watched `which` find it. Both of them were right, which is what makes this the most common installation problem across both projects, and worth hitting once on purpose.

The setup: a virtual environment, both projects installed into it with `pip install -e ".[mcp]"`, both console scripts confirmed with `which pylair-mcp pyfit-mcp`. Then a client configuration that names a server by its bare command:

```json
{
  "mcpServers": {
    "pylair": {"command": "pylair-mcp", "args": []}
  }
}
```

Connecting can produce something like:

```
RuntimeError: Client failed to connect:
[Errno 2] No such file or directory: 'pylair-mcp'
```

That is confusing the first time, because `pylair-mcp` *does* exist: `which` just said so, in the same terminal.

Here's what's going on. When your agentic platform launches a server, it starts a **new subprocess**, and that subprocess doesn't necessarily inherit the activated virtual environment's `PATH` the way your interactive terminal does. The bare name `pylair-mcp` resolves only if the launching process's `PATH` includes the environment's `bin/` directory, and depending on how the platform spawns subprocesses, it may not. The same happens to `pyfit-mcp` for the same reason. It isn't a pyLair or pyFit bug; it's how subprocess launching works, so fix it for both servers at once rather than being surprised twice.

The fix is one line per server: use the **absolute path** to the installed console script instead of its bare name.

```jsonc
{
  "mcpServers": {
    "pylair": {
      "command": "/path/to/your/venv/bin/pylair-mcp",
      "args": []
    },
    "pyfit": {
      "command": "/path/to/your/venv/bin/pyfit-mcp",
      "args": []
    }
  }
}
```

Find those paths with `which pylair-mcp pyfit-mcp` while your environment is activated, and paste them in verbatim. This one change resolves most "the tool obviously exists but the client can't find it" reports on every platform in this chapter. (The AI Henchman, once its configuration held absolute paths, withdrew its apology.)

A second, smaller gotcha, for anyone reaching for an older interpreter: **the MCP servers don't run on Python 3.9.** Both projects pin `mcp<2.0`, because `mcp` 2.0.0 removed `mcp.server.fastmcp`, which both servers import, and no published release of `mcp` supports Python 3.9. The plain CLIs (`pylair`, `pyfit`) install and run fine on 3.9; only the `mcp` extra needs 3.10 or later.

## Proof of Life

Installation isn't finished until you've watched tool calls succeed: "the install command didn't error" is a different claim from "the connection works." Here is the Unbending Foreman's shed, one for each toolkit, too small to be anyone's lair and unimpressive on purpose, so nothing distracts from watching the wiring work: **the Proof-of-Concept Yurt** for pyLair and **the Proof-of-Concept Nesting Job** for pyFit.

**Prompt:**
> Confirm the pyLair MCP server is running and list every tool it exposes. Then run `design_dome` on the smallest, cheapest configuration you can, just to prove the connection works end to end.

**What Comes Back** (from a running server: a Class I icosahedral sphere at frequency 2 and radius 1.0, the Proof-of-Concept Yurt):

```
Tools exposed: design_dome, preview_dome,
  get_bill_of_materials, export_dome,
  get_assembly_manifest,
  export_assembly_job_spec,
  render_assembly_schematic
```

The `design_dome` result:

```json
{
  "vertex_count": 42,
  "edge_count": 120,
  "face_count": 80,
  "truncated": false,
  "bounding_box": {
    "x": [-0.9510565162951536, 0.9510565162951536],
    "y": [-1.0, 1.0],
    "z": [-1.0, 1.0]
  },
  "height": 2.0,
  "footprint_diameter": 2.0,
  "total_strut_length": 69.87402279451425,
  "resolved_parameters": {
    "radius": 1.0,
    "frequency": 2,
    "polyhedron": "icosahedron",
    "dome_class": 1,
    "n_frequency": null,
    "elongation_factors": {
      "x": 1.0, "y": 1.0, "z": 1.0
    },
    "truncation": {"x": null, "y": null, "z": null}
  }
}
```

**What It Means:** Seven tools came back from a running subprocess. The first four (design, preview, bill of materials, export) are the core loop Chapter 18 teaches; the last three handle per-piece assembly and arrive in Chapter 22. The counts, 42 vertices, 120 edges, and 80 faces, match Chapter 3's golden-value formulas for a Class I icosahedral sphere at `f=2`: `10f²+2 = 42`, `30f² = 120`, `20f² = 80`. A frequency-2 sphere is about as coarse as this construction gets, closer to a yurt than a fortress, which is how it got its name. It proves the wiring works, not that the design is good.

Look at the shape, too, rather than only trusting the summary:

**[IMAGE: examples/images/poc-yurt.png | A depth-cued wireframe of a coarse geodesic sphere made of 80 large triangles.]**
**[CAPTION: The Proof-of-Concept Yurt, rendered by `preview_dome`: a frequency-2 Class I icosahedral sphere, unremarkable on purpose.]**

**Prompt:**
> Now confirm the pyFit MCP server is running and list every tool it exposes. Run `design_nest` on six unit squares and a 3×2 sheet, a case small enough to check by hand, just to prove that connection works too.

**What Comes Back:**

```
Tools exposed: design_nest, preview_nest,
  get_nest_report, export_nest
```

The `design_nest` result:

```json
{"sheets_used": 1, "utilization_by_sheet": [1.0]}
```

**What It Means:** Four more tools, from a second subprocess, and a result you can check by hand: six unit squares have a combined area of 6, a 3×2 sheet has an area of 6, and pyFit's README says this case tiles perfectly. `utilization_by_sheet: [1.0]`, or 100%, confirms it did, on one sheet. It's a boring, hand-checkable result, chosen because there's nowhere for a packing mistake to hide in it. The Unbending Foreman checked it with a pencil anyway, and nodded.

**[IMAGE: examples/images/poc-nest_sheet1.png | Six unit squares filling a 3-by-2 rectangular sheet in two rows of three, with no gaps.]**
**[CAPTION: The Proof-of-Concept Nesting Job, rendered by `preview_nest`: six unit squares tiling a 3×2 sheet at 100% utilization.]**

One more thing to confirm while you're here, since Chapter 1 made a point of it: calling `design_dome` instead of the command line doesn't let an invalid configuration slip through.

**Prompt:**
> Ask `design_dome` for a Class II (Triacon) dome at frequency 3, which is deliberately invalid, since Class II needs an even frequency. What comes back?

**What Comes Back** (a tool error, not a crash):

```
Error executing tool design_dome: -c 2
(Class II / Triacon) requires an even
--frequency. Exiting.
```

**What It Means:** After the MCP framework's "Error executing tool" prefix, that's the same message the `pylair` CLI gives for `-c 2 -f 3`, flag names and all. It isn't a coincidence: one shared engine (`pylair/api.py`, and `pyfit/api.py` on the nesting side) validates every request, whichever interface it arrived through. That is why this book trusts an agent's tool calls as much as a terminal's. Chapter 5 explains why Class II needs an even frequency.

## Reading, and Keeping, What Comes Back

Most of the tools answer with JSON (JavaScript Object Notation), a plain-text format of named fields, lists in square brackets, and nested groups in braces, that any program can read back. The exceptions are the three that draw pictures: pyLair's `preview_dome` and `render_assembly_schematic` and pyFit's `preview_nest` send an image with a one-line caption ("42 vertices, 120 struts"), not JSON. A picture is for your eyes and the JSON is for the record, so wherever this book asks for a picture, its prompt also asks for the matching JSON: `design_dome`'s summary beside a preview, `get_assembly_manifest` beside a schematic, `get_nest_report` beside a sheet layout.

The two results above are shown whole. Most results are far longer: a bill of materials lists an angle for every strut end at every hub, nearly a thousand entries on a modest dome. So from here on, each **What Comes Back** shows a **snapshot**: every top-level field appears, each list shows its first entry or two, nested groups show their first few fields, and a bare `...` marks what was left out. Numbers are rounded to four decimal places. A snapshot isn't valid JSON as printed, because of the `...` marks; the real output is, in full and at full precision.

That real output is worth keeping, and it's easy to keep. There are two ways:

- **Ask the agent.** "Save that result, exactly as the tool returned it, to `yurt.json`." An agent that can write files, as Claude Code can, writes the JSON as it came back. Ask for the tool's own output rather than a summary; this book keeps asking for raw results for a reason. This is also how to keep the JSON from the export tools: `export_dome`, `export_assembly_job_spec`, and `export_nest` write their drawings and models to disk, but their reports (a bill of materials, a job spec, a placement report) come back to the agent as JSON, like every other tool's.
- **Use the command line.** `pylair` prints its bill of materials as JSON, so `pylair -f 2 -o yurt > yurt-bom.json` saves it (the DXF and VRML files land beside it). Adding `--assembly-manifest` also writes `yurt_manifest.json`, and `--pyfit-job-spec=panels` writes `yurt_jobspec.json`. `pyfit -j job.json -o squares` writes its placement report to `squares_report.json` on its own.

A saved result is a record: it can be compared with tomorrow's run, attached to a work order, or read back by the next tool in the chain, the way Chapter 20 feeds a bill of materials into pyFit.

## What's Next

The plumbing works on both toolkits, and Part I closes with it. That evening a third envelope from the HOA appeared under the apartment door. It turned out to be about the recycling bins. Our Heroine took it as a warning anyway.

Part II starts the design: a base polyhedron, a subdivision, and the first geometric question, not "does the connection work," but "which shape should this start from, and why."
