# Graph Report - .  (2026-07-26)

## Corpus Check
- 55 files · ~58,905 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 384 nodes · 906 edges · 35 communities (13 shown, 22 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.72)
- Token cost: 568,026 input · 0 output

## Community Hubs (Navigation)
- Polyhedral Base Geometry
- CLI Integration Tests
- API & MCP Interface
- Bill of Materials Engine
- Truncation & Elongation Design
- CLI & File Output
- Geodesic Sphere Projection
- Subdivision Method Documentation
- Class III Symmetry Triangle
- Preview Rendering
- Ellipsoid Elongation
- CAD Dome Renderings
- Geodesic Sphere Projection Render
- Unprojected Panel Diagram
- Icosahedron Render
- Truncated Dome Wireframe
- Ellipsoid Dome Views
- Spoke Angle Diagram
- Spoke Angles Terminal Output
- Tangent Angles Terminal Output
- Tangent Angle Diagram
- Truncated Dome QCAD Render
- CAD Dome Wireframe
- Projected Sphere Render
- Unprojected Panel Layout
- Icosahedron Render (Images Dir)
- Truncated Dome Render
- Spoke Angle Diagram (Images Dir)
- Spoke Angles Table
- Tangent Angles at Hub
- Tangent Angle Diagram (Images Dir)
- Truncated Dome QCAD (Focused)
- pylair Package Root
- Sample Dome Image

## God Nodes (most connected - your core abstractions)
1. `run_cli()` - 46 edges
2. `build_dome()` - 38 edges
3. `Icosahedron` - 34 edges
4. `GeodesicSphere` - 33 edges
5. `get_bill_of_materials()` - 30 edges
6. `truncate()` - 27 edges
7. `export_dome()` - 22 edges
8. `ClassOneMethodOneSymmetryTriangle` - 22 edges
9. `Vertex` - 21 edges
10. `build_sphere()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Projection onto Unit Sphere` --semantically_similar_to--> `GeodesicSphere`  [INFERRED] [semantically similar]
  METHOD.md → pylair/geodesic_sphere.py
- `Starting Icosahedron` --semantically_similar_to--> `Icosahedron`  [INFERRED] [semantically similar]
  METHOD.md → pylair/polyhedral.py
- `Truncation at the Equator` --semantically_similar_to--> `truncate()`  [INFERRED] [semantically similar]
  METHOD.md → pylair/truncation.py
- `GeodesicSphere` --shares_data_with--> `pylair/output.py`  [INFERRED]
  pylair/geodesic_sphere.py → README.md
- `Next Step: Optional Boundary Capping` --references--> `truncate()`  [EXTRACTED]
  blog-posts/introducing-pylair.md → pylair/truncation.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **build_dome() Geometry Pipeline** — pylair_api_build_dome, pylair_polyhedral_icosahedron, pylair_symmetry_triangle_module, pylair_geodesic_sphere_geodesicsphere, pylair_elongation_module, pylair_truncation_truncate [EXTRACTED 1.00]
- **Geodesic Method Walkthrough (METHOD.md)** — method_icosahedron_start, method_face_subdivision, method_sphere_projection, method_truncation_equator, method_hub_tangent_angle, method_spoke_angle [EXTRACTED 1.00]
- **pyLair Core Runtime Dependencies** — readme_pylair_project, readme_numpy_dependency, readme_pandas_dependency, readme_scipy_dependency, readme_matplotlib_dependency [EXTRACTED 1.00]

## Communities (35 total, 22 thin omitted)

### Community 0 - "Polyhedral Base Geometry"
Cohesion: 0.10
Nodes (34): Starting Icosahedron, DomeResult, build_lcd_faces(), Chord, Face, Icosahedron, Octahedron, Polyhedron (+26 more)

### Community 1 - "CLI Integration Tests"
Cohesion: 0.08
Nodes (46): run_cli(), test_area_cost_flag_adds_estimated_panel_cost(), test_area_cost_now_works_with_x_or_y_truncation(), test_class_three_generates_a_valid_dome(), test_class_three_rejects_equal_frequencies(), test_class_three_requires_n_frequency(), test_class_two_generates_a_valid_dome(), test_class_two_requires_even_frequency() (+38 more)

### Community 2 - "API & MCP Interface"
Cohesion: 0.09
Nodes (42): DomeClass, build_dome(), validate_geometry_params(), design_dome(), _design_summary(), export_dome(), get_bill_of_materials(), preview_dome() (+34 more)

### Community 3 - "Bill of Materials Engine"
Cohesion: 0.13
Nodes (42): compute_dihedral_angles(), compute_face_data(), compute_hub_data(), compute_spoke_angles(), _ellipsoid_normal(), _face_chirality_key(), _face_type_signature(), get_bill_of_materials() (+34 more)

### Community 4 - "Truncation & Elongation Design"
Cohesion: 0.09
Nodes (35): Bill of Materials (narrative description), Hub and Panel Cutting Templates, Elliptical Stretching / Ellipsoid Elongation, Next Step: Proactive Truncation-Risk Warning, Next Step: Unstrutted Diagonal / Quad Panel Handling, Hub-to-Tangent-Plane Deflection Angle, Hub Spoke Angle, Truncation at the Equator (+27 more)

### Community 5 - "CLI & File Output"
Cohesion: 0.15
Nodes (27): display_help(), main(), OutputDXF(), OutputFaceTemplateDXF(), OutputFaceVRML(), OutputHubConnectorTemplateDXF(), OutputOBJ(), OutputSTL() (+19 more)

### Community 6 - "Geodesic Sphere Projection"
Cohesion: 0.12
Nodes (21): Projection onto Unit Sphere, cross_face_matches, local_priority, GeodesicSphere, build_class_two_sphere(), parametrize, test_class_two_chords_and_faces_reference_valid_vertex_indices(), test_class_two_no_duplicate_chords() (+13 more)

### Community 7 - "Subdivision Method Documentation"
Cohesion: 0.09
Nodes (26): AI-Assisted Development of pyLair (Claude Code collaboration), Introducing pyLair (blog post), Kenner, H. (1976). Geodesic math and how to use it., Next Step: Optional Boundary Capping, Next Step: AI-Assisted Door-Frame DXF Design, Face Subdivision into Triangular Grid, METHOD.md (Geometric Method Walkthrough), pylair/class_three.py (+18 more)

### Community 8 - "Class III Symmetry Triangle"
Cohesion: 0.18
Nodes (17): ClassThreeSymmetryTriangle, _lattice_to_xy(), object, _roll3(), compute_face_adjacency(), build_class_three_sphere(), parametrize, test_class_three_chords_and_faces_reference_valid_vertex_indices() (+9 more)

### Community 9 - "Preview Rendering"
Cohesion: 0.40
Nodes (9): equal_axis_limits(), render_preview_png_bytes(), save_preview(), test_equal_axis_limits_centered_on_each_axis_own_midpoint(), test_equal_axis_limits_gives_every_axis_the_same_span(), test_equal_axis_limits_handles_a_single_point_without_a_zero_span(), test_render_preview_png_bytes_returns_valid_png_bytes(), test_save_preview_writes_a_png_file() (+1 more)

### Community 10 - "Ellipsoid Elongation"
Cohesion: 0.36
Nodes (8): elongate(), parametrize, test_elongate_does_not_mutate_the_input_list(), test_elongate_factors_of_one_are_a_no_op(), test_elongate_preserves_x_and_y(), test_elongate_scales_all_three_axes_independently(), test_elongate_scales_only_the_z_axis(), test_elongate_scales_x_and_y_independently_of_z()

### Community 11 - "CAD Dome Renderings"
Cohesion: 0.67
Nodes (3): CAD Wireframe Rendering of Geodesic Dome, Geodesic Dome Structure, Triangulated Panel Grid

## Ambiguous Edges - Review These
- `Strutted Diagonal Seam on Quad Boundary Panels` → `Next Step: Unstrutted Diagonal / Quad Panel Handling`  [AMBIGUOUS]
  blog-posts/introducing-pylair.md · relation: references

## Knowledge Gaps
- **44 isolated node(s):** `pylair`, `DXF Output`, `VRML Output`, `NumPy`, `pandas` (+39 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Strutted Diagonal Seam on Quad Boundary Panels` and `Next Step: Unstrutted Diagonal / Quad Panel Handling`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `build_dome()` connect `API & MCP Interface` to `Polyhedral Base Geometry`, `Bill of Materials Engine`, `Truncation & Elongation Design`, `CLI & File Output`, `Geodesic Sphere Projection`, `Class III Symmetry Triangle`, `Ellipsoid Elongation`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `GeodesicSphere` connect `Geodesic Sphere Projection` to `Polyhedral Base Geometry`, `API & MCP Interface`, `Bill of Materials Engine`, `Truncation & Elongation Design`, `CLI & File Output`, `Subdivision Method Documentation`, `Class III Symmetry Triangle`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `truncate()` connect `Truncation & Elongation Design` to `Polyhedral Base Geometry`, `API & MCP Interface`, `Geodesic Sphere Projection`, `Subdivision Method Documentation`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Icosahedron` (e.g. with `Starting Icosahedron` and `DomeResult`) actually correct?**
  _`Icosahedron` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `GeodesicSphere` (e.g. with `Projection onto Unit Sphere` and `DomeResult`) actually correct?**
  _`GeodesicSphere` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `pylair`, `DXF Output`, `VRML Output` to the rest of the system?**
  _44 weakly-connected nodes found - possible documentation gaps or missing edges._