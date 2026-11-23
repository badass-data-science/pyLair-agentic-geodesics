"""Run every measurement script and report which reproduce the book.

Usage:
    python3 run_all.py           # everything quick (a few minutes)
    python3 run_all.py --long    # also Chapter 20's big nesting jobs (+45 min)
"""
import glob
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
scripts = sorted(glob.glob(os.path.join(HERE, "measurements", "*.py")))
results = []
for script in scripts:
    args = [sys.executable, script] + (["--long"] if "--long" in sys.argv and "nesting_jobs" in script else [])
    name = os.path.basename(script)
    print(f"\n=== {name}")
    t0 = time.perf_counter()
    ok = subprocess.run(args).returncode == 0
    results.append((name, ok, time.perf_counter() - t0))

print("\n=== Summary")
for name, ok, secs in results:
    print(f"  {'matches the book' if ok else 'DIFFERS          '}  {name}  ({secs:.0f} s)")
sys.exit(0 if all(ok for _, ok, _ in results) else 1)
