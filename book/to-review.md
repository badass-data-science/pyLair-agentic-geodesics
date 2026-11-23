# To review: book revision (PR #29)

Items the unattended book revision (PR #29, branch `book-revision-2026-11`, merged 2026-11-23) flagged for the author.

## Front matter (your own prose)

The revision changed only what the later volumes had already established. Please check:

- [ ] Title page now carries the *Lady Napalm* byline and a copyright line (© 2026 Emily Marie Williams).
- [ ] About the Author page now uses your Lady Napalm text from the other volumes.
- [ ] Blog link is now an absolute URL.
- [ ] "heroine" capitalized to "our Heroine."

## Citation

- [ ] **Coxeter (1971)** in Appendix C: secondary sources give Oxford University Press as the publisher, and some give Auckland University Press. The page range 98–107 is confirmed only via secondary sources.

## Code/doc discrepancies (found, not changed)

- [ ] `pylair/mcp_server.py` `export_dome` docstring says `face_output=True` is required for STL/OBJ/templates/area cost. The code doesn't require it (`face_output` only swaps the VRML and drops the DXF). Chapter 17 was corrected to match the code.
- [ ] `tests/test_class_three.py` comment calls Class II's golden values "T=3m²". With pyLair's m=f/2, Class II's 120m² faces correspond to T=6m². (pyLair's Class II is the LCD construction, not the Goldberg–Coxeter (k,k) case.)
- [ ] `truncate()` initializes `min_vy=1., max_vy=-1.` rather than ±inf. Harmless for origin-centered spheres, but would misbehave if every coordinate on an axis exceeded ±1 after an earlier cut.

## Chapter 20

- [ ] The `GEOSException ... side location conflict` crash recorded in the first draft did not happen in any run during the revision. The chapter now says so instead of presenting it as current.
- [ ] The old mirroring experiment couldn't be reproduced (its sheet size wasn't recorded), so it was re-run on new terms and its two figures regenerated. Worth a read to confirm the new framing works.

## Leaked private notes (urgent)

- [ ] The unattended run committed `EMILYS-NOTES-do-not-commit.docx` and `.mcp.json` in commit `7ef3a56`, and they reached public `main` through the merge of PR #29. `main` has since been rewritten without them (force-pushed 2026-11-23; commits before `180ed2c` are unchanged), and both files are now in `.gitignore`. **GitHub still serves the old commits through PR #29's refs.** For example, `https://github.com/badass-data-science/pyLair-agentic-geodesics/commit/7ef3a56369472b5d9c04d2d5b6dcccda935d12df` is still reachable. To remove them completely, ask GitHub Support to purge cached views and dereferenced commits: https://support.github.com/contact (pick "Removing sensitive data"). Give them the repo, PR #29 and commit `7ef3a56` (plus the old merge `ff4181f`).
- [ ] Backups of both files and the old `main` SHA: `/home/emily/claude-scheduled/leak-backup/`.

## CI

- [ ] The `test (3.9, test,verify)` job fails at setup: `The version '3.9' with architecture 'x64' was not found for Ubuntu 26.04.` GitHub's current runner image has no Python 3.9. This is unrelated to the book and will hit every PR and push to main. Options: drop 3.9 from the CI matrix (and maybe `requires-python`), or pin that job to an older `runs-on` image.
