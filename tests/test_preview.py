import numpy as np
import pytest

from pylair.preview import (
    equal_axis_limits,
    render_preview_png_bytes,
    save_preview,
    render_assembly_schematic_png_bytes,
    save_assembly_schematic,
)
from pylair.assembly import build_assembly_manifest


def test_equal_axis_limits_gives_every_axis_the_same_span():
    # a badly asymmetric point cloud: X spans 4, Y spans 2, Z spans 1.
    # equal_axis_limits must widen Y and Z out to X's span rather than
    # leaving them at their own tighter data range, otherwise a plot
    # built from these limits would stretch/squash axes relative to each
    # other -- exactly the distortion that would make a spherical dome
    # look elliptical.
    vertices = [
        np.array([-2., -1., -0.5]),
        np.array([2., 1., 0.5]),
    ]
    xlim, ylim, zlim = equal_axis_limits(vertices)

    x_span = xlim[1] - xlim[0]
    y_span = ylim[1] - ylim[0]
    z_span = zlim[1] - zlim[0]

    assert x_span == pytest.approx(y_span)
    assert y_span == pytest.approx(z_span)
    assert x_span == pytest.approx(4.0)


def test_equal_axis_limits_centered_on_each_axis_own_midpoint():
    vertices = [
        np.array([0., 10., -5.]),
        np.array([2., 12., -3.]),
    ]
    xlim, ylim, zlim = equal_axis_limits(vertices)

    assert (xlim[0] + xlim[1]) / 2 == pytest.approx(1.0)
    assert (ylim[0] + ylim[1]) / 2 == pytest.approx(11.0)
    assert (zlim[0] + zlim[1]) / 2 == pytest.approx(-4.0)


def test_equal_axis_limits_handles_a_single_point_without_a_zero_span():
    vertices = [np.array([1., 1., 1.])]
    xlim, ylim, zlim = equal_axis_limits(vertices)

    for lo, hi in (xlim, ylim, zlim):
        assert hi > lo


def test_save_preview_writes_a_png_file(tmp_path):
    V = [
        np.array([0., 0., 0.]),
        np.array([1., 0., 0.]),
        np.array([0., 1., 0.]),
    ]
    C = [[0, 1], [1, 2], [2, 0]]

    out_file = tmp_path / "preview.png"
    save_preview(V, C, str(out_file))

    assert out_file.exists()
    assert out_file.stat().st_size > 0
    # PNG magic bytes
    assert out_file.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_preview_png_bytes_returns_valid_png_bytes():
    V = [
        np.array([0., 0., 0.]),
        np.array([1., 0., 0.]),
        np.array([0., 1., 0.]),
    ]
    C = [[0, 1], [1, 2], [2, 0]]

    png_bytes = render_preview_png_bytes(V, C)

    assert isinstance(png_bytes, bytes)
    assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"


def test_save_preview_writes_the_same_bytes_render_preview_png_bytes_returns(tmp_path):
    V = [
        np.array([0., 0., 0.]),
        np.array([1., 0., 0.]),
        np.array([0., 1., 0.]),
    ]
    C = [[0, 1], [1, 2], [2, 0]]

    out_file = tmp_path / "preview.png"
    save_preview(V, C, str(out_file))

    assert out_file.read_bytes() == render_preview_png_bytes(V, C)


def test_render_assembly_schematic_defaults_to_no_labels_and_returns_valid_png():
    V = [
        np.array([1.0, 0.1, 0.05]),
        np.array([0.1, 1.0, 0.2]),
        np.array([0.05, 0.2, 1.0]),
    ]
    C = [[0, 1], [1, 2], [2, 0]]
    manifest = build_assembly_manifest(V, C)

    png_bytes = render_assembly_schematic_png_bytes(V, C, manifest)

    assert isinstance(png_bytes, bytes)
    assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_assembly_schematic_with_labels_differs_from_without():
    # turning a label kind on must actually change the rendered image --
    # otherwise the opt-in flag would be silently doing nothing
    V = [
        np.array([1.0, 0.1, 0.05]),
        np.array([0.1, 1.0, 0.2]),
        np.array([0.05, 0.2, 1.0]),
    ]
    C = [[0, 1], [1, 2], [2, 0]]
    manifest = build_assembly_manifest(V, C)

    unlabeled = render_assembly_schematic_png_bytes(V, C, manifest)
    with_hub_labels = render_assembly_schematic_png_bytes(V, C, manifest, show_hub_labels=True)
    with_strut_labels = render_assembly_schematic_png_bytes(V, C, manifest, show_strut_labels=True)

    assert unlabeled != with_hub_labels
    assert unlabeled != with_strut_labels


def test_save_assembly_schematic_writes_the_same_bytes_the_renderer_returns(tmp_path):
    V = [
        np.array([1.0, 0.1, 0.05]),
        np.array([0.1, 1.0, 0.2]),
        np.array([0.05, 0.2, 1.0]),
    ]
    C = [[0, 1], [1, 2], [2, 0]]
    manifest = build_assembly_manifest(V, C)

    out_file = tmp_path / "schematic.png"
    save_assembly_schematic(V, C, manifest, str(out_file), show_hub_labels=True)

    assert out_file.read_bytes() == render_assembly_schematic_png_bytes(V, C, manifest, show_hub_labels=True)
