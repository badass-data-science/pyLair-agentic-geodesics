import json
import subprocess
import sys


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


def test_face_and_truncation_are_mutually_exclusive(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-F", "-t", "0.5"])
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

    preview_file = tmp_path / "dome_preview.png"
    assert preview_file.exists()
    assert preview_file.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_no_preview_flag_means_no_preview_file(tmp_path):
    out = tmp_path / "dome"
    result = run_cli(["-o", str(out), "-f", "1"])

    assert result.returncode == 0
    assert not (tmp_path / "dome_preview.png").exists()
