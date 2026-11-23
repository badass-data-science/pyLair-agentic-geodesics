"""Chapter 21: pyFit's progress notifications, timestamped as they arrive.

Starts the real `pyfit-mcp` server as a subprocess, the way an agent's MCP
client does, calls design_nest on Chapter 21's 40-panel job (the Lair's
first eight panel templates, five of each, on 0.6 x 0.5 sheets), and
timestamps every progress notification as it arrives.

The book's run: 214 notifications over 23.03 s, the first at 0.008 s
("placed 0/40 parts (checking sheet 1)"), the last at 23.026 s ("placed
39/40 parts (checking sheet 10)"). The count and the times depend on the
machine; what this checks is the shape: notifications start almost at
once and keep arriving until the end, rather than bunching up at the end,
which is what a blocked event loop would produce.
"""
import asyncio
import json
import os
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "jobs"))
import make_jobs
from book_check import check, done, note
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = shutil.which("pyfit-mcp") or os.path.join(os.path.dirname(sys.executable), "pyfit-mcp")


async def main(job_dir):
    spec = json.load(open(os.path.join(job_dir, "ch21_eight_shapes.json")))
    arrivals = []
    params = StdioServerParameters(command=SERVER, args=[], cwd=job_dir)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            start = time.perf_counter()

            async def on_progress(progress, total, message):
                arrivals.append((time.perf_counter() - start, message))

            result = await session.call_tool(
                "design_nest",
                {"sheet_width": spec["sheet"]["width"], "sheet_height": spec["sheet"]["height"],
                 "parts": spec["parts"]},
                progress_callback=on_progress)
            elapsed = time.perf_counter() - start
    return elapsed, arrivals, json.loads(result.content[0].text)


job_dir = tempfile.mkdtemp(prefix="book-jobs-")
make_jobs.main(job_dir)
elapsed, arrivals, result = asyncio.run(main(job_dir))

print("\nChapter 21: progress notifications from a 40-panel design_nest call")
note("elapsed", f"{elapsed:.2f} s, {len(arrivals)} progress notifications (book: 23.03 s, 214)")
note("first", f"t={arrivals[0][0]:.3f}s ({arrivals[0][1]})")
note("last", f"t={arrivals[-1][0]:.3f}s ({arrivals[-1][1]})")
check("result", result["sheets_used"], 10)
check("first notification's message", arrivals[0][1], "placed 0/40 parts (checking sheet 1)")
check("last notification's message", arrivals[-1][1], "placed 39/40 parts (checking sheet 10)")
check("first notification within the first second", arrivals[0][0] < 1.0, True)
halves = sum(1 for t, _ in arrivals if t < elapsed / 2), sum(1 for t, _ in arrivals if t >= elapsed / 2)
check("notifications in both halves of the call, not bunched at the end", all(halves), True)
done()
