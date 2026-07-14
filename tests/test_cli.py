import json
import subprocess
import sys
from pathlib import Path

import pytest


def run_cli(args, cwd=None):
    return subprocess.run(
        [sys.executable, "-m", "pydome", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def test_help_flag_short_and_long_print_usage():
    for flag in ["-h", "--help"]:
        result = run_cli([flag])
        assert result.returncode == 0
        assert "Required Command-Line Input" in result.stdout


def test_no_arguments_prints_help_and_exits_nonzero():
    result = run_cli([])
    assert result.returncode != 0
    assert "Required Command-Line Input" in result.stdout


def test_unrecognized_flag_reports_error_and_exits_nonzero():
    result = run_cli(["-Z"])
    assert result.returncode != 0
    assert "not recognized" in result.stdout
    assert "for help use --help" in result.stdout


def test_missing_output_path_reports_error():
    result = run_cli(["-f", "1"])
    assert result.returncode != 0
    assert "output path" in result.stdout.lower()


def test_nonpositive_frequency_reports_clear_error(tmp_path):
    out = tmp_path / "dome"
    for freq in ["0", "-1"]:
        result = run_cli(["-o", str(out), "-f", freq])
        assert result.returncode != 0
        assert "positive integer" in result.stdout.lower()
        assert "Traceback" not in result.stderr


def test_nonpositive_radius_reports_clear_error(tmp_path):
    out = tmp_path / "dome"
    for radius in ["0", "-2.0"]:
        result = run_cli(["-o", str(out), "-r", radius])
        assert result.returncode != 0
        assert "greater than zero" in result.stdout.lower()
        assert "Traceback" not in result.stderr


def test_face_based_output_and_truncation_are_mutually_exclusive(tmp_path):
    out = tmp_path / "dome"
    for flag in ["-F", "-s", "-O"]:
        result = run_cli(["-o", str(out), flag, "-t", "0.5"])
        assert result.returncode != 0
        assert "cannot be used with truncation" in result.stdout.lower() or "does not work" in result.stdout.lower()


def test_default_run_generates_dxf_and_wrl_with_valid_bom_report(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "1"])

    assert result.returncode == 0
    assert (out.with_suffix(".dxf")).exists()
    assert (out.with_suffix(".wrl")).exists()

    report = json.loads(result.stdout)
    assert "pyDome report" in report


def test_face_output_generates_only_wrl(tmp_path):
    out = tmp_path / "dome_face"
    result = run_cli(["-o", str(out), "-f", "1", "-F"])

    assert result.returncode == 0
    assert out.with_suffix(".wrl").exists()
    assert not out.with_suffix(".dxf").exists()


def test_preview_flag_writes_a_png_alongside_the_usual_output(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "1", "-P"])

    assert result.returncode == 0
    assert out.with_suffix(".dxf").exists()
    assert out.with_suffix(".wrl").exists()

    preview_file = out.with_suffix(".png")
    assert preview_file.exists()
    assert preview_file.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_no_preview_flag_means_no_preview_file(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "1"])

    assert result.returncode == 0
    assert not out.with_suffix(".png").exists()


def test_stl_flag_writes_a_valid_stl_alongside_the_usual_output(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "1", "-s"])

    assert result.returncode == 0
    assert out.with_suffix(".dxf").exists()
    assert out.with_suffix(".wrl").exists()

    stl_file = out.with_suffix(".stl")
    assert stl_file.exists()
    content = stl_file.read_text()
    assert content.startswith("solid pydome\n")
    assert content.rstrip().endswith("endsolid pydome")


def test_obj_flag_writes_a_valid_obj_alongside_the_usual_output(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "1", "-O"])

    assert result.returncode == 0
    assert out.with_suffix(".dxf").exists()
    assert out.with_suffix(".wrl").exists()

    obj_file = out.with_suffix(".obj")
    assert obj_file.exists()
    content = obj_file.read_text()
    assert any(line.startswith("v ") for line in content.splitlines())
    assert any(line.startswith("f ") for line in content.splitlines())


def test_no_stl_or_obj_flag_means_no_mesh_files(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "1"])

    assert result.returncode == 0
    assert not out.with_suffix(".stl").exists()
    assert not out.with_suffix(".obj").exists()


def test_class_two_requires_even_frequency(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "3", "-c", "2"])

    assert result.returncode != 0
    assert "even" in result.stdout.lower()
    assert "Traceback" not in result.stderr


def test_class_two_generates_a_valid_dome(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "4", "-c", "2"])

    assert result.returncode == 0
    assert out.with_suffix(".dxf").exists()
    assert out.with_suffix(".wrl").exists()

    report = json.loads(result.stdout)
    assert "pyDome report" in report


def test_invalid_class_reports_clear_error(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-c", "4"])

    assert result.returncode != 0
    assert "1, 2, or 3" in result.stdout
    assert "Traceback" not in result.stderr


def test_class_three_requires_n_frequency(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "3", "-c", "3"])

    assert result.returncode != 0
    assert "n-frequency" in result.stdout.lower()
    assert "Traceback" not in result.stderr


def test_class_three_rejects_equal_frequencies(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "3", "-n", "3", "-c", "3"])

    assert result.returncode != 0
    assert "differ" in result.stdout.lower()
    assert "Traceback" not in result.stderr


def test_class_three_generates_a_valid_dome(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "3", "-n", "2", "-c", "3"])

    assert result.returncode == 0
    assert out.with_suffix(".dxf").exists()
    assert out.with_suffix(".wrl").exists()

    report = json.loads(result.stdout)
    assert "pyDome report" in report


def test_default_run_reports_total_strut_length_without_cost(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "1"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    assert "Total strut length" in report["Total material"]
    assert "Total estimated material cost" not in report["Total material"]


def test_material_cost_flag_adds_estimated_cost(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "1", "-m", "2.5"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    total_material = report["Total material"]

    assert total_material["Total estimated material cost"] == pytest.approx(
        total_material["Total strut length"] * 2.5, abs=0.01
    )


def test_nonpositive_material_cost_reports_clear_error(tmp_path):
    out = tmp_path / "dome"
    for cost in ["0", "-5"]:
        result = run_cli(["-o", str(out), "-f", "1", "-m", cost])
        assert result.returncode != 0
        assert "greater than zero" in result.stdout.lower()
        assert "Traceback" not in result.stderr


def test_hub_templates_flag_writes_dxf_files_and_report_section(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "4", "-H"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    assert "Hub Connector Templates" in report

    rows = report["Hub Connector Templates"]
    assert len(rows) > 0
    for row in rows:
        template_file = Path(row["template_file"])
        assert template_file.exists()
        assert template_file.name.startswith("dome_hubtype")


def test_no_hub_templates_flag_means_no_template_files_or_section(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "4"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    assert "Hub Connector Templates" not in report
    assert list(tmp_path.glob("dome_hubtype*.dxf")) == []


def test_default_elongation_produces_identical_output_to_explicit_one(tmp_path):
    out1 = tmp_path / "default"
    out2 = tmp_path / "explicit"

    result1 = run_cli(["-o", str(out1), "-f", "4"])
    result2 = run_cli(["-o", str(out2), "-f", "4", "-e", "1.0,1.0,1.0"])

    assert result1.returncode == 0
    assert result2.returncode == 0
    assert result1.stdout == result2.stdout
    assert out1.with_suffix(".dxf").read_text() == out2.with_suffix(".dxf").read_text()


def test_elongation_flag_produces_a_taller_dome(tmp_path):
    out_normal = tmp_path / "normal"
    out_tall = tmp_path / "tall"

    run_cli(["-o", str(out_normal), "-f", "4", "-P"])
    run_cli(["-o", str(out_tall), "-f", "4", "-e", "1.0,1.0,1.8", "-P"])

    normal_png = out_normal.with_suffix(".png").read_bytes()
    tall_png = out_tall.with_suffix(".png").read_bytes()
    # not a rigorous geometric check (that's covered elsewhere), just
    # confirms elongation actually changed the rendered output
    assert normal_png != tall_png


def test_elongated_and_truncated_dome_generates_valid_hub_templates(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "4", "-e", "1.0,1.0,1.8", "-t", "0.499999", "-H"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    rows = report["Hub Connector Templates"]
    assert len(rows) > 0
    for row in rows:
        assert Path(row["template_file"]).exists()


def test_elongation_flag_stretches_x_and_y_independently(tmp_path):
    out_normal = tmp_path / "normal"
    out_wide = tmp_path / "wide"

    result_normal = run_cli(["-o", str(out_normal), "-f", "4"])
    result_wide = run_cli(["-o", str(out_wide), "-f", "4", "-e", "2.0,0.5,1.0"])

    assert result_normal.returncode == 0
    assert result_wide.returncode == 0
    # bevel/hub angle math should still succeed (doesn't crash) for a
    # non-Z elongation, which is the case the ellipsoid-normal formula
    # generalization needs to handle correctly
    assert "Bill of materials" in json.loads(result_wide.stdout)["pyDome report"]


def test_truncation_x_and_y_flags_enable_truncation(tmp_path):
    out_x = tmp_path / "trunc_x"
    out_y = tmp_path / "trunc_y"

    result_x = run_cli(["-o", str(out_x), "-f", "4", "-x", "0.499999"])
    result_y = run_cli(["-o", str(out_y), "-f", "4", "-y", "0.499999"])

    assert result_x.returncode == 0
    assert result_y.returncode == 0
    # truncation clears face data, so face-based output (-T etc.) would
    # now be rejected exactly like -t already is
    result_rejected = run_cli(["-o", str(out_x), "-f", "4", "-x", "0.499999", "-T"])
    assert result_rejected.returncode != 0
    assert "does not work" in result_rejected.stdout.lower()


def test_combined_x_y_z_truncation_produces_a_valid_smaller_dome(tmp_path):
    out_full = tmp_path / "full"
    out_clipped = tmp_path / "clipped"

    result_full = run_cli(["-o", str(out_full), "-f", "4"])
    result_clipped = run_cli([
        "-o", str(out_clipped), "-f", "4",
        "-x", "0.5", "-y", "0.5", "-t", "0.499999",
    ])

    assert result_full.returncode == 0
    assert result_clipped.returncode == 0

    full_dxf = out_full.with_suffix(".dxf").read_text()
    clipped_dxf = out_clipped.with_suffix(".dxf").read_text()
    assert full_dxf != clipped_dxf
    assert (out_clipped.with_suffix(".dxf")).exists()


def test_nonpositive_elongation_reports_clear_error(tmp_path):
    out = tmp_path / "dome"
    for factors in ["0,1.0,1.0", "1.0,-2,1.0", "1.0,1.0,0"]:
        result = run_cli(["-o", str(out), "-f", "1", "-e", factors])
        assert result.returncode != 0
        assert "greater than zero" in result.stdout.lower()
        assert "Traceback" not in result.stderr


def test_elongation_with_wrong_number_of_values_reports_clear_error(tmp_path):
    out = tmp_path / "dome"
    for factors in ["1.8", "1.0,1.0", "1.0,1.0,1.0,1.0"]:
        result = run_cli(["-o", str(out), "-f", "1", "-e", factors])
        assert result.returncode != 0
        assert "fx,fy,fz" in result.stdout
        assert "Traceback" not in result.stderr


def test_default_run_reports_panel_sections_without_cost_or_weight(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "3"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    assert "Panel shapes and counts" in report
    assert "Total panel area" in report["Total panel material"]
    assert "Total estimated panel material cost" not in report["Total panel material"]
    assert "Total estimated panel weight" not in report["Total panel material"]
    assert "Bevel angles at panel edges" in report


def test_area_cost_flag_adds_estimated_panel_cost(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "3", "-a", "2.5"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    total_panel_material = report["Total panel material"]

    assert total_panel_material["Total estimated panel material cost"] == pytest.approx(
        total_panel_material["Total panel area"] * 2.5, abs=0.01
    )


def test_panel_density_flag_adds_estimated_panel_weight(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "3", "-w", "0.5"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    total_panel_material = report["Total panel material"]

    assert total_panel_material["Total estimated panel weight"] == pytest.approx(
        total_panel_material["Total panel area"] * 0.5, abs=0.01
    )


def test_nonpositive_area_cost_and_panel_density_report_clear_errors(tmp_path):
    out = tmp_path / "dome"
    for flag in ["-a", "-w"]:
        for value in ["0", "-1"]:
            result = run_cli(["-o", str(out), "-f", "1", flag, value])
            assert result.returncode != 0
            assert "greater than zero" in result.stdout.lower()
            assert "Traceback" not in result.stderr


def test_face_templates_flag_writes_dxf_files_and_report_section(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "4", "-T"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    assert "Panel Cutting Templates" in report

    rows = report["Panel Cutting Templates"]
    assert len(rows) > 0
    for row in rows:
        template_file = Path(row["template_file"])
        assert template_file.exists()
        assert template_file.name.startswith("dome_facetype")


def test_no_face_templates_flag_means_no_template_files_or_section(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "4"])

    assert result.returncode == 0
    report = json.loads(result.stdout)["pyDome report"]
    assert "Panel Cutting Templates" not in report
    assert list(tmp_path.glob("dome_facetype*.dxf")) == []


def test_face_templates_and_truncation_are_mutually_exclusive(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-T", "-t", "0.5"])
    assert result.returncode != 0
    assert "does not work" in result.stdout.lower()


def test_area_cost_and_truncation_are_mutually_exclusive(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-a", "2.0", "-t", "0.5"])
    assert result.returncode != 0
    assert "does not work" in result.stdout.lower()
