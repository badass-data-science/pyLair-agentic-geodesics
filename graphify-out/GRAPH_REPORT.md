# Graph Report - .  (2026-07-29)

## Corpus Check
- 3 files · ~60,066 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 470 nodes · 1010 edges · 47 communities (16 shown, 31 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Class III Subdivision Tests
- MCP Tool Tests
- Class II Subdivision Tests
- Dome Build API Tests
- Bill of Materials Tests
- CLI Integration Tests
- Elongation Tests
- Output Format Exporter Tests
- Truncation Geometry Tests
- Dome Wireframe Renders
- Spoke Angle STDOUT
- Hub Tangent Angle STDOUT
- Projected Sphere Render
- Unprojected Panel Render
- Truncated Wireframe Render
- Ellipsoid Dome Views
- Spoke Angle Diagram
- QCAD Truncated Render
- Sample Wireframe Image
- BOM/Truncation CLI Flags and Rationale
- Docs-Sync and Project Concepts
- pylair Package Root
- CI Pipeline
- Companion Book Series
- Geodesic Method Summary
- Hub Tangent Angle Concept
- The Proof-of-Concept Yurt
- The Actual Secret Lair
- The Under-the-Ocean Prototype
- The Orbital Panopticon
- The Magma Redoubt
- The Permafrost Cache
- The Ostentatious Mesa Spire
- Diagonal-Seam Doc-Drift Case Study
- Trusting the Agent Checklist
- Golden-Value Count Formulas
- Further Reading Appendix
- Book Outline Practicum Chapter
- Package Init (pylair)
- Output Flag
- Frequency/Radius Validation
- Polyhedron Flag
- Vertex Threshold Flag
- Help Flag
- CI Pipeline Detail
- README Badges

## God Nodes (most connected - your core abstractions)
1. `run_cli()` - 46 edges
2. `build_dome()` - 35 edges
3. `Icosahedron` - 32 edges
4. `get_bill_of_materials()` - 30 edges
5. `GeodesicSphere` - 25 edges
6. `ClassOneMethodOneSymmetryTriangle` - 22 edges
7. `truncate()` - 22 edges
8. `export_dome()` - 20 edges
9. `Vertex` - 20 edges
10. `build_sphere()` - 19 edges

## Surprising Connections (you probably didn't know these)
- ``pylair` CLI console command` --references--> `validate_geometry_params()`  [EXTRACTED]
  AGENTS.md → pylair/api.py
- `MCP interface (README section)` --references--> `validate_geometry_params()`  [EXTRACTED]
  README.md → pylair/api.py
- ``pylair` CLI console command` --references--> `build_dome()`  [EXTRACTED]
  AGENTS.md → pylair/api.py
- `pylair/__main__.py` --references--> `main()`  [EXTRACTED]
  README.md → pylair/cli.py
- `SKILL.md (OpenClaw skill definition)` --references--> `main()`  [EXTRACTED]
  README.md → pylair/cli.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **CLI, MCP server, and OpenClaw skill all share one geometry engine** — pylair_cli, pylair_mcp_server, skill, pylair_api [EXTRACTED 1.00]
- **Class I/II/III subdivisions as special cases of the (m,n) Goldberg-Coxeter / Caspar-Klug construction** — readme_class_i, readme_class_ii, readme_class_iii, siber_2007 [EXTRACTED 1.00]
- **CLI flags that require face data (truncation-aware)** — readme_flag_face, readme_flag_stl, readme_flag_obj, readme_flag_face_templates, readme_flag_area_cost, readme_flag_panel_density [EXTRACTED 1.00]
- **Documentation kept in sync across README/METHOD/SKILL/CHANGELOG/blog post** — agents, blog_posts_method, skill, blog_posts_introducing_pylair [EXTRACTED 1.00]

## Communities (47 total, 31 thin omitted)

### Community 5 - "Class III Subdivision Tests"
Cohesion: 0.11
Nodes (27): object, build_class_three_sphere(), parametrize, test_class_three_sphere_counts_match_verified_formulas(), test_class_three_sphere_satisfies_euler_formula(), test_class_three_no_two_final_vertices_occupy_the_same_location(), test_class_three_cross_face_matches_are_necessary_not_just_helpful(), test_class_three_has_no_anomalously_long_chords() (+19 more)

### Community 8 - "MCP Tool Tests"
Cohesion: 0.11
Nodes (29): tool, DomeClass, test_design_dome_returns_summary_stats(), parametrize, test_design_dome_truncated_on_any_axis_still_has_a_face_count(), test_design_dome_elongation_x_y_z_are_independent(), test_design_dome_rejects_bad_class_frequency_combo(), test_preview_dome_returns_summary_and_inline_image() (+21 more)

### Community 0 - "Class II Subdivision Tests"
Cohesion: 0.08
Nodes (44): object, object, build_class_two_sphere(), parametrize, test_class_two_sphere_counts_match_verified_formulas(), test_class_two_sphere_satisfies_euler_formula(), test_class_two_sphere_vertices_lie_at_the_given_radius(), test_class_two_no_two_final_vertices_occupy_the_same_location() (+36 more)

### Community 7 - "Dome Build API Tests"
Cohesion: 0.12
Nodes (31): test_class_one_golden_counts(), test_class_two_golden_counts(), test_class_three_golden_counts(), test_polyhedron_accepts_octahedron_name(), test_elongation_changes_z_extent_only(), test_elongation_scales_x_and_y_independently(), parametrize, test_truncation_on_any_axis_or_combination_preserves_clipped_face_data() (+23 more)

### Community 4 - "Bill of Materials Tests"
Cohesion: 0.13
Nodes (39): build_sphere(), build_sphere_with_faces(), test_bill_of_materials_reports_expected_sections(), test_bill_of_materials_chord_length_counts_sum_correctly(), test_bill_of_materials_does_not_merge_distinct_strut_lengths_at_fine_precision(), test_bill_of_materials_coarse_precision_merges_near_identical_lengths(), test_bill_of_materials_reports_total_strut_length_by_default(), test_bill_of_materials_reports_cost_when_given_a_unit_price() (+31 more)

### Community 2 - "CLI Integration Tests"
Cohesion: 0.08
Nodes (46): run_cli(), test_help_flag_short_and_long_print_usage(), test_no_arguments_prints_help_and_exits_nonzero(), test_unrecognized_flag_reports_error_and_exits_nonzero(), test_missing_output_path_reports_error(), test_nonpositive_frequency_reports_clear_error(), test_nonpositive_radius_reports_clear_error(), test_face_based_output_now_works_with_x_or_y_truncation() (+38 more)

### Community 10 - "Elongation Tests"
Cohesion: 0.39
Nodes (8): test_elongate_scales_only_the_z_axis(), test_elongate_factors_of_one_are_a_no_op(), test_elongate_does_not_mutate_the_input_list(), parametrize, test_elongate_preserves_x_and_y(), test_elongate_scales_x_and_y_independently_of_z(), test_elongate_scales_all_three_axes_independently(), elongate()

### Community 3 - "Output Format Exporter Tests"
Cohesion: 0.10
Nodes (36): test_face_template_dxf_geometry_matches_ezdxf_parse(), make_triangle(), test_output_dxf_writes_one_line_entity_per_chord(), test_output_wireframe_vrml_contains_all_points_and_indices(), test_output_face_vrml_contains_face_indices(), test_output_stl_writes_one_facet_per_face_with_correct_normal(), test_output_obj_writes_1_indexed_face_references(), test_output_hub_connector_template_dxf_writes_one_line_and_label_per_spoke() (+28 more)

### Community 6 - "Truncation Geometry Tests"
Cohesion: 0.12
Nodes (29): build_sphere(), test_truncate_removes_vertices_below_cutoff(), test_truncate_chords_reference_valid_vertex_indices(), parametrize, test_truncate_never_adds_chords(), test_truncate_raises_clearly_on_horizontal_chord_at_cutoff(), test_truncate_removes_vertices_below_cutoff_on_any_axis(), test_truncate_on_x_leaves_full_z_range_untouched_elsewhere() (+21 more)

### Community 13 - "Dome Wireframe Renders"
Cohesion: 0.67
Nodes (3): CAD Wireframe Rendering of Geodesic Dome, Geodesic Dome Structure, Triangulated Panel Grid

### Community 9 - "BOM/Truncation CLI Flags and Rationale"
Cohesion: 0.10
Nodes (26): -b/--bom-rounding, -m/--material-cost, -F/--face, -s/--stl, -O/--obj, -H/--hub-templates, -T/--face-templates, -a/--area-cost (+18 more)

### Community 1 - "Docs-Sync and Project Concepts"
Cohesion: 0.05
Nodes (51): _lattice_to_xy(), _roll3(), compute_face_adjacency(), pyLair, AGENTS.md (agent-facing guide), Introducing pyLair (blog post), OpenClaw, mcp<2.0 version pin rationale (+43 more)

### Community 11 - "CI Pipeline"
Cohesion: 0.29
Nodes (8): CI Pipeline (ci.yml), Python 3.9-3.13 test matrix, cli-smoke job (full-format dome export), test extra, mcp extra, verify extra, mcp extra unsupported on Python 3.9, Ch.21: agent-authored CI catching real bugs

### Community 14 - "Diagonal-Seam Doc-Drift Case Study"
Cohesion: 0.67
Nodes (3): Ch.20: catching doc drift with graphify, commit 26de45e (strut the diagonal seam), /graphify knowledge-graph tool

### Community 12 - "Frequency/Radius Validation"
Cohesion: 0.50
Nodes (4): -r/--radius, -f/--frequency, -f must be a positive integer and -r must be > 0, validated with clear errors, Validate frequency/radius CLI arguments and narrow bare except clauses

## Knowledge Gaps
- **63 isolated node(s):** `Geodesic Dome Structure`, `Triangulated Panel Grid`, `STDOUT: Spoke Angles Terminal Output`, `STDOUT: Angles at Hub Between Outbound Cords and Tangential Plane`, `Geodesic Sphere Projection Render (edited_4_projected1)` (+58 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_dome()` connect `Dome Build API Tests` to `Class II Subdivision Tests`, `Output Format Exporter Tests`, `Bill of Materials Tests`, `Class III Subdivision Tests`, `Truncation Geometry Tests`, `Elongation Tests`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `Icosahedron` connect `Class II Subdivision Tests` to `Output Format Exporter Tests`, `Bill of Materials Tests`, `Class III Subdivision Tests`, `Truncation Geometry Tests`, `Dome Build API Tests`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **What connects `Geodesic Dome Structure`, `Triangulated Panel Grid`, `STDOUT: Spoke Angles Terminal Output` to the rest of the system?**
  _63 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Class III Subdivision Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.10510510510510511 - nodes in this community are weakly interconnected._
- **Should `MCP Tool Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.10887096774193548 - nodes in this community are weakly interconnected._
- **Should `Class II Subdivision Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.08469945355191257 - nodes in this community are weakly interconnected._
- **Should `Dome Build API Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.11931818181818182 - nodes in this community are weakly interconnected._