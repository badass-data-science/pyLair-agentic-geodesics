import json
import subprocess
import sys
from pathlib import Path

PYDOME = Path(__file__).resolve().parent.parent / "pyDome.py"


def run_cli(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(PYDOME), *args],
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
    assert "for help use --help" in result.stdout


def test_missing_output_path_reports_error():
    result = run_cli(["-f", "1"])
    assert result.returncode != 0
    assert "output path" in result.stdout.lower()


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
