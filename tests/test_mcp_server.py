import asyncio
import json
from pathlib import Path

import pytest

pytest.importorskip("mcp")

from mcp.shared.memory import create_connected_server_and_client_session

from pylair.mcp_server import (
    mcp,
    design_dome,
    preview_dome,
    get_bill_of_materials,
    export_dome,
    get_assembly_manifest,
    export_assembly_job_spec,
    render_assembly_schematic,
)


#
# direct calls: @mcp.tool() leaves the decorated function callable as a
# plain Python function, so these exercise the tool bodies without
# spinning up a protocol session
#

def test_design_dome_returns_summary_stats():
    result = design_dome(frequency=4)

    assert result["vertex_count"] == 10 * 4 ** 2 + 2
    assert result["edge_count"] == 30 * 4 ** 2
    assert result["face_count"] == 20 * 4 ** 2
    assert result["truncated"] is False
    assert result["resolved_parameters"]["frequency"] == 4


@pytest.mark.parametrize("kwargs", [
    dict(truncation_z=0.499999),
    dict(truncation_x=0.499999),
    dict(truncation_y=0.499999),
    dict(truncation_x=0.499999, truncation_y=0.499999, truncation_z=0.499999),
])
def test_design_dome_truncated_on_any_axis_still_has_a_face_count(kwargs):
    result = design_dome(frequency=4, **kwargs)

    assert result["truncated"] is True
    assert result["face_count"] is not None
    assert result["face_count"] > 0


def test_design_dome_elongation_x_y_z_are_independent():
    result = design_dome(frequency=2, elongation_x=2.0, elongation_y=0.5, elongation_z=1.0)

    resolved = result["resolved_parameters"]["elongation_factors"]
    assert resolved == {"x": 2.0, "y": 0.5, "z": 1.0}

    bbox = result["bounding_box"]
    normal = design_dome(frequency=2)
    normal_bbox = normal["bounding_box"]
    assert (bbox["x"][1] - bbox["x"][0]) == pytest.approx(
        2.0 * (normal_bbox["x"][1] - normal_bbox["x"][0]))
    assert (bbox["y"][1] - bbox["y"][0]) == pytest.approx(
        0.5 * (normal_bbox["y"][1] - normal_bbox["y"][0]))


def test_design_dome_rejects_bad_class_frequency_combo():
    with pytest.raises(ValueError, match="even"):
        design_dome(dome_class=2, frequency=3)


def test_preview_dome_returns_summary_and_inline_image():
    result = preview_dome(frequency=1)

    assert isinstance(result[0], str)
    assert "vertices" in result[0]
    image = result[1]
    assert image.data[:8] == b"\x89PNG\r\n\x1a\n"


def test_get_bill_of_materials_tool_returns_dict_without_printing(capsys):
    report = get_bill_of_materials(frequency=1)

    captured = capsys.readouterr()
    assert captured.out == ""  # must not corrupt the stdio JSON-RPC stream
    assert "Bill of materials" in report["pyLair report"]


def test_export_dome_writes_dxf_and_wrl(tmp_path):
    out = str(tmp_path / "dome")
    result = export_dome(out, frequency=1)

    assert set(result["files_written"]) == {out + ".dxf", out + ".wrl"}
    for f in result["files_written"]:
        assert Path(f).exists()
    assert "Bill of materials" in result["bill_of_materials"]["pyLair report"]


def test_get_bill_of_materials_tool_reports_panel_sections_when_untruncated():
    report = get_bill_of_materials(frequency=3, cost_per_unit_area=2.0)

    sections = report["pyLair report"]
    assert "Panel shapes and counts" in sections
    assert "Total panel material" in sections
    assert "Total estimated panel material cost" in sections["Total panel material"]
    assert "Bevel angles at panel edges" in sections


def test_export_dome_with_face_templates_writes_facetype_files(tmp_path):
    out = str(tmp_path / "dome")
    result = export_dome(out, frequency=4, face_templates=True)

    files = result["files_written"]
    assert any(f.endswith(".dxf") and "_facetype" in f for f in files)
    for f in files:
        assert Path(f).exists()
    assert "Panel Cutting Templates" in result["bill_of_materials"]["pyLair report"]


def test_export_dome_face_templates_work_with_x_or_y_truncation(tmp_path):
    out = str(tmp_path / "dome")
    result = export_dome(out, frequency=4, face_templates=True, truncation_x=0.499999)

    assert any(f.endswith(".dxf") and "_facetype" in f for f in result["files_written"])
    assert "Panel Cutting Templates" in result["bill_of_materials"]["pyLair report"]


def test_export_dome_face_output_works_with_x_or_y_truncation(tmp_path):
    out = str(tmp_path / "dome")
    result = export_dome(out, frequency=4, face_output=True, truncation_y=0.499999)

    assert (out + ".wrl") in result["files_written"]


def test_export_dome_face_templates_work_with_z_only_truncation(tmp_path):
    out = str(tmp_path / "dome")
    result = export_dome(out, frequency=4, face_templates=True, truncation_z=0.499999)

    assert any(f.endswith(".dxf") and "_facetype" in f for f in result["files_written"])
    assert "Panel Cutting Templates" in result["bill_of_materials"]["pyLair report"]


def test_export_dome_face_templates_work_with_combined_x_y_z_truncation(tmp_path):
    out = str(tmp_path / "dome")
    result = export_dome(out, frequency=4, face_templates=True,
                          truncation_x=0.499999, truncation_y=0.499999, truncation_z=0.499999)

    assert any(f.endswith(".dxf") and "_facetype" in f for f in result["files_written"])
    assert "Panel Cutting Templates" in result["bill_of_materials"]["pyLair report"]


def test_export_dome_with_preview_and_hub_templates(tmp_path):
    out = str(tmp_path / "dome")
    result = export_dome(out, frequency=4, preview=True, hub_templates=True)

    files = result["files_written"]
    assert out + ".png" in files
    assert any(f.endswith(".dxf") and "_hubtype" in f for f in files)
    for f in files:
        assert Path(f).exists()


def test_get_assembly_manifest_returns_a_json_safe_dict():
    manifest = get_assembly_manifest(frequency=3)

    assert set(manifest.keys()) == {
        "hubs", "struts", "panels", "hub_groups", "strut_groups", "panel_groups",
    }
    assert len(manifest["hubs"]) == 10 * 3 ** 2 + 2
    assert len(manifest["struts"]) == 30 * 3 ** 2
    # round-trips through real JSON with no numpy/tuple leakage (see
    # pylair/assembly.py's own _to_float normalization)
    assert json.loads(json.dumps(manifest)).keys() == manifest.keys()


def test_get_assembly_manifest_reports_bordering_panels_on_a_truncated_dome():
    manifest = get_assembly_manifest(frequency=6, truncation_z=0.4)

    counts = {len(s["bordering_panels"]) for s in manifest["struts"].values()}
    assert counts == {1, 2}  # base-ring struts border 1 panel, interior struts border 2


def test_export_assembly_job_spec_panels_writes_templates_and_one_part_per_instance(tmp_path):
    out = str(tmp_path / "dome")
    result = export_assembly_job_spec(out, kind="panels", frequency=3)

    assert any(f.endswith(".dxf") and "_facetype" in f for f in result["files_written"])
    for f in result["files_written"]:
        assert Path(f).exists()

    parts = result["job_spec"]["parts"]
    assert len(parts) == 20 * 3 ** 2  # one entry per panel instance, not per shape
    assert all(p["quantity"] == 1 for p in parts)
    names = [p["name"] for p in parts]
    assert len(names) == len(set(names))  # every instance is its own part entry


def test_export_assembly_job_spec_hubs_writes_templates_and_one_part_per_instance(tmp_path):
    out = str(tmp_path / "dome")
    result = export_assembly_job_spec(out, kind="hubs", frequency=3, sheet_width=24, sheet_height=24)

    assert any(f.endswith(".dxf") and "_hubtype" in f for f in result["files_written"])
    assert result["job_spec"]["sheet"] == {"width": 24, "height": 24}
    parts = result["job_spec"]["parts"]
    assert len(parts) == 10 * 3 ** 2 + 2  # one entry per hub instance
    assert all(p["quantity"] == 1 for p in parts)


def test_render_assembly_schematic_returns_summary_and_inline_image():
    result = render_assembly_schematic(frequency=2)

    assert "hubs" in result[0] and "struts" in result[0] and "panels" in result[0]
    assert result[1].data[:8] == b"\x89PNG\r\n\x1a\n"


#
# protocol-level: a real MCP client/server session over an in-memory
# transport (no subprocess), proving the tools are actually reachable as
# MCP tool calls, not just as plain functions
#

def test_tools_are_reachable_over_a_real_mcp_session():
    async def run():
        async with create_connected_server_and_client_session(mcp) as client:
            tools = await client.list_tools()
            names = {t.name for t in tools.tools}
            assert names == {
                "design_dome", "preview_dome", "get_bill_of_materials", "export_dome",
                "get_assembly_manifest", "export_assembly_job_spec", "render_assembly_schematic",
            }

            result = await client.call_tool("design_dome", {"frequency": 2})
            assert result.isError is False
            payload = json.loads(result.content[0].text)
            assert payload["vertex_count"] == 10 * 2 ** 2 + 2

    asyncio.run(run())


def test_invalid_params_become_an_mcp_error_result():
    async def run():
        async with create_connected_server_and_client_session(mcp) as client:
            result = await client.call_tool("design_dome", {"dome_class": 2, "frequency": 3})
            assert result.isError is True
            assert "even" in result.content[0].text

    asyncio.run(run())
