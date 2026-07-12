import asyncio
import json
from pathlib import Path

import pytest

pytest.importorskip("mcp")

from mcp.shared.memory import create_connected_server_and_client_session

from pydome.mcp_server import mcp, design_dome, preview_dome, get_bill_of_materials, export_dome


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


def test_design_dome_truncated_has_no_face_count():
    result = design_dome(frequency=4, truncation_amount=0.499999)

    assert result["truncated"] is True
    assert result["face_count"] is None


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
    assert "Bill of materials" in report["pyDome report"]


def test_export_dome_writes_dxf_and_wrl(tmp_path):
    out = str(tmp_path / "dome")
    result = export_dome(out, frequency=1)

    assert set(result["files_written"]) == {out + ".dxf", out + ".wrl"}
    for f in result["files_written"]:
        assert Path(f).exists()
    assert "Bill of materials" in result["bill_of_materials"]["pyDome report"]


def test_export_dome_face_output_incompatible_with_truncation(tmp_path):
    out = str(tmp_path / "dome")
    with pytest.raises(ValueError, match="does not work"):
        export_dome(out, frequency=4, face_output=True, truncation_amount=0.5)


def test_export_dome_with_preview_and_hub_templates(tmp_path):
    out = str(tmp_path / "dome")
    result = export_dome(out, frequency=4, preview=True, hub_templates=True)

    files = result["files_written"]
    assert out + ".png" in files
    assert any(f.endswith(".dxf") and "_hubtype" in f for f in files)
    for f in files:
        assert Path(f).exists()


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
            assert names == {"design_dome", "preview_dome", "get_bill_of_materials", "export_dome"}

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
