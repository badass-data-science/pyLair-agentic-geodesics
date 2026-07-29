# Graph Report - .  (2026-07-29)

## Corpus Check
- 24 files · ~72,217 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 414 nodes · 954 edges · 38 communities (14 shown, 24 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.71)
- Token cost: 0 input · 153,544 output

## Community Hubs (Navigation)
- Polyhedral Face Geometry
- CLI Test Suite
- Bill of Materials Computation
- Output Format Exporters
- Docs-Sync and Narrative Voice
- Method Rationale and Risk Notes
- MCP Tool Interface
- Dome Build API Tests
- Truncation Geometry
- Class III Symmetry Triangle
- Geodesic Sphere Assembly
- Axis Elongation
- Dome Wireframe Renders
- Projected Sphere Render
- Unprojected Panel Render
- Truncated Wireframe Render
- Ellipsoid Dome Views
- Boundary Cap Idea
- AI Doorframe Design Idea
- Spoke Angle Diagram
- Spoke Angle STDOUT
- Hub Tangent Angle STDOUT
- QCAD Truncated Render
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
- Preview Rendering
- Octahedron Base Polyhedron
- Sample Wireframe Image

## God Nodes (most connected - your core abstractions)
1. `run_cli()` - 46 edges
2. `build_dome()` - 38 edges
3. `Icosahedron` - 32 edges
4. `get_bill_of_materials()` - 30 edges
5. `GeodesicSphere` - 25 edges
6. `export_dome()` - 22 edges
7. `ClassOneMethodOneSymmetryTriangle` - 22 edges
8. `Vertex` - 20 edges
9. `build_sphere()` - 19 edges
10. `truncate()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `pylair OpenClaw skill definition` --references--> `main()`  [EXTRACTED]
  SKILL.md → pylair/cli.py
- `[Unreleased] section` --references--> `design_dome()`  [EXTRACTED]
  CHANGELOG.md → pylair/mcp_server.py
- `Ch.20: catching doc drift with graphify` --semantically_similar_to--> `Docs-stay-in-sync rule`  [INFERRED] [semantically similar]
  book/outline.md → AGENTS.md
- `Next Steps: proactive truncation-risk warning` --semantically_similar_to--> `Truncation-artifact sliver flagging`  [INFERRED] [semantically similar]
  blog-posts/introducing-pylair.md → README.md
- `Four MCP tools narrative` --references--> `design_dome()`  [EXTRACTED]
  blog-posts/introducing-pylair.md → pylair/mcp_server.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Geodesic geometry pipeline stages (polyhedron to dome)** — pylair_polyhedral_module, pylair_symmetry_triangle_module, pylair_class_three_module, pylair_geodesic_sphere_module, pylair_truncation_module, pylair_elongation_module [EXTRACTED 1.00]
- **pyLair MCP tool set (design/preview/BOM/export)** — pylair_mcp_server_design_dome, pylair_mcp_server_preview_dome, pylair_mcp_server_get_bill_of_materials, pylair_mcp_server_export_dome [EXTRACTED 1.00]
- **Docs that must stay in sync (README/METHOD/SKILL/blog)** — readme_readme_md, blog_posts_method_md, skill_skill_md, blog_posts_introducing_pylair_md [EXTRACTED 1.00]

## Communities (38 total, 24 thin omitted)

### Community 0 - "Polyhedral Face Geometry"
Cohesion: 0.09
Nodes (42): DomeResult, build_lcd_faces(), Chord, Face, Icosahedron, Octahedron, Polyhedron, object (+34 more)

### Community 1 - "CLI Test Suite"
Cohesion: 0.08
Nodes (46): run_cli(), test_area_cost_flag_adds_estimated_panel_cost(), test_area_cost_now_works_with_x_or_y_truncation(), test_class_three_generates_a_valid_dome(), test_class_three_rejects_equal_frequencies(), test_class_three_requires_n_frequency(), test_class_two_generates_a_valid_dome(), test_class_two_requires_even_frequency() (+38 more)

### Community 2 - "Bill of Materials Computation"
Cohesion: 0.13
Nodes (42): compute_dihedral_angles(), compute_face_data(), compute_hub_data(), compute_spoke_angles(), _ellipsoid_normal(), _face_chirality_key(), _face_type_signature(), get_bill_of_materials() (+34 more)

### Community 3 - "Output Format Exporters"
Cohesion: 0.12
Nodes (30): display_help(), main(), OutputDXF(), OutputFaceTemplateDXF(), OutputFaceVRML(), OutputHubConnectorTemplateDXF(), OutputSTL(), OutputWireframeVRML() (+22 more)

### Community 4 - "Docs-Sync and Narrative Voice"
Cohesion: 0.09
Nodes (33): Docs-stay-in-sync rule, graphify-out/ generated knowledge-graph artifacts, introducing-pylair.md (blog post), AI Use Statement, Next Steps: diagonal seam strutting (marked Done), Our heroine (narrative persona), Kenner (1976), Geodesic math and how to use it, Works Consulted section (+25 more)

### Community 5 - "Method Rationale and Risk Notes"
Cohesion: 0.08
Nodes (35): Geometry pipeline: plausible-but-wrong risk, Bill of materials (narrative description), Next Steps: proactive truncation-risk warning, Geodesic method: subdivide/project/truncate, Hub tangent-plane deflection angle, The Actual Secret Lair, Ch.22: when to trust the agent checklist, Golden-value vertex/edge/face count formulas (+27 more)

### Community 6 - "MCP Tool Interface"
Cohesion: 0.12
Nodes (28): Four MCP tools narrative, DomeClass, design_dome(), _design_summary(), export_dome(), get_bill_of_materials(), preview_dome(), Compute the dome and return its Bill of Materials (strut lengths and   counts, h (+20 more)

### Community 7 - "Dome Build API Tests"
Cohesion: 0.17
Nodes (22): build_dome(), validate_geometry_params(), OutputOBJ(), parametrize, test_class_one_golden_counts(), test_class_three_golden_counts(), test_class_two_golden_counts(), test_elongation_changes_z_extent_only() (+14 more)

### Community 8 - "Truncation Geometry"
Cohesion: 0.19
Nodes (19): _clip_face(), truncate(), build_sphere(), parametrize, test_clip_face_fully_above_cutoff_is_kept_unchanged(), test_clip_face_fully_below_cutoff_is_dropped(), test_clip_face_one_vertex_above_cutoff_produces_a_smaller_triangle(), test_clip_face_one_vertex_above_cutoff_works_on_any_axis() (+11 more)

### Community 9 - "Class III Symmetry Triangle"
Cohesion: 0.18
Nodes (17): ClassThreeSymmetryTriangle, _lattice_to_xy(), object, _roll3(), compute_face_adjacency(), build_class_three_sphere(), parametrize, test_class_three_chords_and_faces_reference_valid_vertex_indices() (+9 more)

### Community 10 - "Geodesic Sphere Assembly"
Cohesion: 0.22
Nodes (9): GeodesicSphere, build_class_two_sphere(), parametrize, test_class_two_chords_and_faces_reference_valid_vertex_indices(), test_class_two_no_duplicate_chords(), test_class_two_no_two_final_vertices_occupy_the_same_location(), test_class_two_sphere_counts_match_verified_formulas(), test_class_two_sphere_satisfies_euler_formula() (+1 more)

### Community 11 - "Axis Elongation"
Cohesion: 0.36
Nodes (8): elongate(), parametrize, test_elongate_does_not_mutate_the_input_list(), test_elongate_factors_of_one_are_a_no_op(), test_elongate_preserves_x_and_y(), test_elongate_scales_all_three_axes_independently(), test_elongate_scales_only_the_z_axis(), test_elongate_scales_x_and_y_independently_of_z()

### Community 12 - "Dome Wireframe Renders"
Cohesion: 0.67
Nodes (3): CAD Wireframe Rendering of Geodesic Dome, Geodesic Dome Structure, Triangulated Panel Grid

## Ambiguous Edges - Review These
- `Diagonal-seam strutting for quad boundary panels` → `Next Steps: diagonal seam strutting (marked Done)`  [AMBIGUOUS]
  blog-posts/introducing-pylair.md · relation: references

## Knowledge Gaps
- **41 isolated node(s):** `Geodesic Dome Structure`, `Triangulated Panel Grid`, `STDOUT: Spoke Angles Terminal Output`, `STDOUT: Angles at Hub Between Outbound Cords and Tangential Plane`, `Geodesic Sphere Projection Render (edited_4_projected1)` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Diagonal-seam strutting for quad boundary panels` and `Next Steps: diagonal seam strutting (marked Done)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `design_dome()` connect `MCP Tool Interface` to `Polyhedral Face Geometry`, `Output Format Exporters`, `Docs-Sync and Narrative Voice`, `Dome Build API Tests`?**
  _High betweenness centrality (0.245) - this node is a cross-community bridge._
- **Why does `build_dome()` connect `Dome Build API Tests` to `Polyhedral Face Geometry`, `Bill of Materials Computation`, `Output Format Exporters`, `MCP Tool Interface`, `Truncation Geometry`, `Class III Symmetry Triangle`, `Geodesic Sphere Assembly`, `Axis Elongation`?**
  _High betweenness centrality (0.234) - this node is a cross-community bridge._
- **Why does `[Unreleased] section` connect `Docs-Sync and Narrative Voice` to `MCP Tool Interface`?**
  _High betweenness centrality (0.230) - this node is a cross-community bridge._
- **What connects `Geodesic Dome Structure`, `Triangulated Panel Grid`, `STDOUT: Spoke Angles Terminal Output` to the rest of the system?**
  _41 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Polyhedral Face Geometry` be split into smaller, more focused modules?**
  _Cohesion score 0.08766803039158387 - nodes in this community are weakly interconnected._
- **Should `CLI Test Suite` be split into smaller, more focused modules?**
  _Cohesion score 0.0841813135985199 - nodes in this community are weakly interconnected._