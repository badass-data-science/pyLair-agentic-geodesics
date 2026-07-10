import json
import subprocess
import sys

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
    result = run_cli(["-o", str(out), "-c", "3"])

    assert result.returncode != 0
    assert "1 or 2" in result.stdout
    assert "Traceback" not in result.stderr


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
