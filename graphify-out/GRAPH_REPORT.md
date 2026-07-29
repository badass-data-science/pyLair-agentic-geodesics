# Graph Report - .  (2026-07-29)

## Corpus Check
- 4 files · ~72,323 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 405 nodes · 946 edges · 50 communities (16 shown, 34 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 22 edges (avg confidence: 0.66)
- Token cost: 0 input · 115,548 output

## Community Hubs (Navigation)
- Polyhedral Face Geometry
- Bill of Materials Computation
- CLI Test Suite
- Output Format Exporters
- Dome Build API
- Class III + Sphere Assembly
- MCP Tool Interface
- Docs-Sync and Project Concepts
- Truncation Geometry
- Elongation and Historical Bug Fixes
- Geodesic Sphere Tests
- CI Pipeline
- Dome Wireframe Renders
- Diagonal-Seam Doc-Drift Case Study
- Book Outline Series
- Projected Sphere Render
- Unprojected Panel Render
- Truncated Wireframe Render
- Ellipsoid Dome Views
- Geodesic Method Summary
- Hub Tangent Angle Concept
- Spoke Angle Diagram
- Spoke Angle STDOUT
- Hub Tangent Angle STDOUT
- QCAD Truncated Render
- The Actual Secret Lair
- Further Reading Appendix
- Trusting the Agent Checklist
- Golden-Value Count Formulas
- The Magma Redoubt
- The Ostentatious Mesa Spire
- The Orbital Panopticon
- The Permafrost Cache
- The Proof-of-Concept Yurt
- The Under-the-Ocean Prototype
- CAD Dome Render
- Projected Sphere Render (Dup)
- Panel Layout Diagram
- Icosahedron Render
- Truncated Dome Render
- Spoke Angle Diagram (Alt)
- Spoke Angle Table
- Tangent Angle STDOUT
- Tangent Angle Diagram
- Focused QCAD Wireframe
- pylair Package Root
- Sample Wireframe Image
- SKILL.md

## God Nodes (most connected - your core abstractions)
1. `run_cli()` - 46 edges
2. `build_dome()` - 36 edges
3. `Icosahedron` - 32 edges
4. `get_bill_of_materials()` - 30 edges
5. `GeodesicSphere` - 25 edges
6. `ClassOneMethodOneSymmetryTriangle` - 22 edges
7. `export_dome()` - 20 edges
8. `Vertex` - 20 edges
9. `truncate()` - 20 edges
10. `build_sphere()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `pylair OpenClaw skill definition` --references--> `main()`  [EXTRACTED]
  SKILL.md → pylair/cli.py
- `build_lcd_faces()` --references--> `Class II (Triacon) subdivision`  [EXTRACTED]
  pylair/polyhedral.py → README.md
- ``pylair` CLI console command` --references--> `validate_geometry_params()`  [EXTRACTED]
  AGENTS.md → pylair/api.py
- ``pylair-mcp` MCP server command` --references--> `validate_geometry_params()`  [EXTRACTED]
  AGENTS.md → pylair/api.py
- ``pylair` CLI console command` --references--> `build_dome()`  [EXTRACTED]
  AGENTS.md → pylair/api.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Documentation kept in sync across README/METHOD/SKILL/CHANGELOG/blog post** — agents, readme, blog_posts_method, skill, changelog, blog_posts_introducing_pylair [EXTRACTED 1.00]
- **CLI, MCP server, and OpenClaw skill all built on one geometry engine (pylair/api.py)** — pylair_cli_console, pylair_mcp_console, skill, pylair_api [EXTRACTED 1.00]
- **Class I, II, and III as special cases of the Goldberg-Coxeter (m,n) construction** — class_i_alternate, class_ii_triacon, class_iii_skew, goldberg_coxeter_construction [EXTRACTED 1.00]

## Communities (50 total, 34 thin omitted)

### Community 0 - "Polyhedral Face Geometry"
Cohesion: 0.10
Nodes (38): Class II orthogonal coordinate-basis bug (historical), build_lcd_faces(), Chord, Face, Icosahedron, Vertex, ClassOneMethodOneSymmetryTriangle, ClassTwoMethodOneSymmetryTriangle (+30 more)

### Community 1 - "Bill of Materials Computation"
Cohesion: 0.11
Nodes (46): Per-strut panel bevel angle, Bill of Materials (BOM) report, -b/--bom-rounding dual-purpose display+merge tolerance, Hub-template rotation-invariant clustering tolerance, compute_face_data(), compute_hub_data(), compute_spoke_angles(), _ellipsoid_normal() (+38 more)

### Community 2 - "CLI Test Suite"
Cohesion: 0.08
Nodes (46): run_cli(), test_area_cost_flag_adds_estimated_panel_cost(), test_area_cost_now_works_with_x_or_y_truncation(), test_class_three_generates_a_valid_dome(), test_class_three_rejects_equal_frequencies(), test_class_three_requires_n_frequency(), test_class_two_generates_a_valid_dome(), test_class_two_requires_even_frequency() (+38 more)

### Community 3 - "Output Format Exporters"
Cohesion: 0.13
Nodes (30): display_help(), main(), OutputDXF(), OutputFaceTemplateDXF(), OutputFaceVRML(), OutputHubConnectorTemplateDXF(), OutputOBJ(), OutputSTL() (+22 more)

### Community 4 - "Dome Build API"
Cohesion: 0.12
Nodes (30): pyLair's Agentic AI Interface (MCP + OpenClaw), build_dome(), DomeResult, validate_geometry_params(), compute_dihedral_angles(), `pylair` CLI console command, `pylair-mcp` MCP server command, Octahedron (+22 more)

### Community 5 - "Class III + Sphere Assembly"
Cohesion: 0.12
Nodes (20): KD-tree vertex deduplication (replaced O(n^2) scan), ClassThreeSymmetryTriangle, cross_face_matches, _lattice_to_xy(), object, _roll3(), GeodesicSphere, compute_face_adjacency() (+12 more)

### Community 6 - "MCP Tool Interface"
Cohesion: 0.12
Nodes (26): DomeClass, design_dome(), _design_summary(), export_dome(), get_bill_of_materials(), preview_dome(), Compute the dome and return its Bill of Materials (strut lengths and   counts, h, Compute the dome and write output files to disk (mirrors the `pylair`   CLI): DX (+18 more)

### Community 7 - "Docs-Sync and Project Concepts"
Cohesion: 0.14
Nodes (25): AGENTS.md (agent-facing guide), antitile (brsr) library, Introducing pyLair (blog post), METHOD.md, Agentic Geodesic Lair Design for Supervillains (book outline), Panel mirror-image (chirality) flag, GitHub Actions CI pipeline, Class I (Alternate) subdivision (+17 more)

### Community 8 - "Truncation Geometry"
Cohesion: 0.18
Nodes (20): Diagonal-seam strut handling for clipped quad panels, _clip_face(), truncate(), build_sphere(), parametrize, test_clip_face_fully_above_cutoff_is_kept_unchanged(), test_clip_face_fully_below_cutoff_is_dropped(), test_clip_face_one_vertex_above_cutoff_produces_a_smaller_triangle() (+12 more)

### Community 9 - "Elongation and Historical Bug Fixes"
Cohesion: 0.24
Nodes (11): Class III cross-face combinatorial stitching fix, Ellipsoid true surface-normal formula for elongated angles, Goldberg-Coxeter / Caspar-Klug (m,n) construction, elongate(), parametrize, test_elongate_does_not_mutate_the_input_list(), test_elongate_factors_of_one_are_a_no_op(), test_elongate_preserves_x_and_y() (+3 more)

### Community 10 - "Geodesic Sphere Tests"
Cohesion: 0.40
Nodes (9): build_sphere(), parametrize, test_all_sphere_vertices_lie_at_the_given_radius(), test_chords_reference_valid_vertex_indices(), test_faces_reference_valid_vertex_indices(), test_icosahedron_frequency_one_matches_original_icosahedron_edge_length(), test_no_duplicate_chords(), test_no_two_final_vertices_occupy_the_same_location() (+1 more)

### Community 11 - "CI Pipeline"
Cohesion: 0.29
Nodes (8): Ch.21: agent-authored CI catching real bugs, cli-smoke job (full-format dome export), mcp extra, mcp extra unsupported on Python 3.9, CI Pipeline (ci.yml), test extra, Python 3.9-3.13 test matrix, verify extra

### Community 12 - "Dome Wireframe Renders"
Cohesion: 0.67
Nodes (3): CAD Wireframe Rendering of Geodesic Dome, Geodesic Dome Structure, Triangulated Panel Grid

### Community 13 - "Diagonal-Seam Doc-Drift Case Study"
Cohesion: 0.67
Nodes (3): Ch.20: catching doc drift with graphify, commit 26de45e (strut the diagonal seam), /graphify knowledge-graph tool

## Knowledge Gaps
- **45 isolated node(s):** `Geodesic Dome Structure`, `Triangulated Panel Grid`, `STDOUT: Spoke Angles Terminal Output`, `STDOUT: Angles at Hub Between Outbound Cords and Tangential Plane`, `Geodesic Sphere Projection Render (edited_4_projected1)` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_dome()` connect `Dome Build API` to `Polyhedral Face Geometry`, `Bill of Materials Computation`, `Output Format Exporters`, `Class III + Sphere Assembly`, `Truncation Geometry`, `Elongation and Historical Bug Fixes`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `Icosahedron` connect `Polyhedral Face Geometry` to `Bill of Materials Computation`, `Output Format Exporters`, `Dome Build API`, `Class III + Sphere Assembly`, `Truncation Geometry`, `Geodesic Sphere Tests`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `GeodesicSphere` connect `Class III + Sphere Assembly` to `Polyhedral Face Geometry`, `Bill of Materials Computation`, `Dome Build API`, `Truncation Geometry`, `Geodesic Sphere Tests`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **What connects `Geodesic Dome Structure`, `Triangulated Panel Grid`, `STDOUT: Spoke Angles Terminal Output` to the rest of the system?**
  _45 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Polyhedral Face Geometry` be split into smaller, more focused modules?**
  _Cohesion score 0.09577677224736049 - nodes in this community are weakly interconnected._
- **Should `Bill of Materials Computation` be split into smaller, more focused modules?**
  _Cohesion score 0.11436170212765957 - nodes in this community are weakly interconnected._
- **Should `CLI Test Suite` be split into smaller, more focused modules?**
  _Cohesion score 0.0841813135985199 - nodes in this community are weakly interconnected._