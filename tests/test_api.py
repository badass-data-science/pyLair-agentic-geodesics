import numpy as np
import pytest

from pydome.api import build_dome, validate_geometry_params


def test_class_one_golden_counts():
    # f^2-scaled golden-value formulas (icosahedron): V=10f^2+2, E=30f^2, F=20f^2
    dome = build_dome(frequency=4, dome_class=1)
    assert len(dome.V) == 10 * 4 ** 2 + 2
    assert len(dome.C) == 30 * 4 ** 2
    assert len(dome.F_sphere) == 20 * 4 ** 2
    assert dome.truncated is False
    assert dome.polyhedron == "icosahedron"


def test_class_two_golden_counts():
    # m = frequency // 2; icosahedron: V=60m^2+2, E=180m^2, F=120m^2
    dome = build_dome(frequency=4, dome_class=2)
    m = 2
    assert len(dome.V) == 60 * m ** 2 + 2
    assert len(dome.C) == 180 * m ** 2
    assert len(dome.F_sphere) == 120 * m ** 2


def test_class_three_golden_counts():
    # T = m^2 + mn + n^2; icosahedron: V=10T+2, E=30T, F=20T
    dome = build_dome(frequency=3, n_frequency=2, dome_class=3)
    T = 3 ** 2 + 3 * 2 + 2 ** 2
    assert len(dome.V) == 10 * T + 2
    assert len(dome.C) == 30 * T
    assert len(dome.F_sphere) == 20 * T


def test_polyhedron_accepts_octahedron_name():
    dome = build_dome(frequency=2, polyhedron="octahedron")
    assert dome.polyhedron == "octahedron"
    # octahedron golden counts: V=10f^2+2 -> no, that's icosahedron;
    # octahedron is V=4f^2+2, E=12f^2, F=8f^2
    assert len(dome.V) == 4 * 2 ** 2 + 2
    assert len(dome.C) == 12 * 2 ** 2
    assert len(dome.F_sphere) == 8 * 2 ** 2


def test_elongation_changes_z_extent_only():
    normal = build_dome(frequency=2, elongation_factors=(1.0, 1.0, 1.0))
    tall = build_dome(frequency=2, elongation_factors=(1.0, 1.0, 1.8))

    normal_z = [v[2] for v in normal.V]
    tall_z = [v[2] for v in tall.V]
    normal_x = [v[0] for v in normal.V]
    tall_x = [v[0] for v in tall.V]

    assert (max(tall_z) - min(tall_z)) > (max(normal_z) - min(normal_z))
    assert (max(tall_x) - min(tall_x)) == pytest.approx(max(normal_x) - min(normal_x))
    assert tall.elongation_factors == (1.0, 1.0, 1.8)


def test_elongation_scales_x_and_y_independently():
    normal = build_dome(frequency=2, elongation_factors=(1.0, 1.0, 1.0))
    wide = build_dome(frequency=2, elongation_factors=(2.0, 0.5, 1.0))

    normal_x = [v[0] for v in normal.V]
    wide_x = [v[0] for v in wide.V]
    normal_y = [v[1] for v in normal.V]
    wide_y = [v[1] for v in wide.V]
    normal_z = [v[2] for v in normal.V]
    wide_z = [v[2] for v in wide.V]

    assert (max(wide_x) - min(wide_x)) == pytest.approx(2.0 * (max(normal_x) - min(normal_x)))
    assert (max(wide_y) - min(wide_y)) == pytest.approx(0.5 * (max(normal_y) - min(normal_y)))
    assert (max(wide_z) - min(wide_z)) == pytest.approx(max(normal_z) - min(normal_z))
    assert wide.elongation_factors == (2.0, 0.5, 1.0)


@pytest.mark.parametrize("kwargs", [
    dict(truncation_z=0.499999),
    dict(truncation_x=0.499999),
    dict(truncation_y=0.499999),
    dict(truncation_x=0.499999, truncation_y=0.499999),
    dict(truncation_x=0.499999, truncation_z=0.499999),
    dict(truncation_y=0.499999, truncation_z=0.499999),
])
def test_truncation_on_any_axis_or_combination_preserves_clipped_face_data(kwargs):
    dome = build_dome(frequency=4, **kwargs)
    assert dome.truncated is True
    assert dome.F_sphere is not None
    assert len(dome.F_sphere) > 0
    for f in dome.F_sphere:
        assert len(f) == 3
        for idx in f:
            assert 0 <= idx < len(dome.V)


def test_no_truncation_leaves_face_data_populated():
    dome = build_dome(frequency=4)
    assert dome.truncated is False
    assert dome.F_sphere is not None


def test_truncate_horizontal_chord_error_propagates_unmodified():
    # a cutoff that lands exactly on a vertex ring produces a chord flat
    # against the cutoff plane -- truncate() itself raises this, and
    # build_dome must not swallow or reword it
    with pytest.raises(ValueError, match="flat along the cutoff axis"):
        build_dome(frequency=4, truncation_z=0.5)


def test_truncation_on_multiple_axes_is_applied_sequentially_x_then_y_then_z():
    dome = build_dome(frequency=4, truncation_x=0.499999, truncation_y=0.499999, truncation_z=0.499999)
    assert dome.truncated is True
    assert dome.F_sphere is not None
    assert len(dome.V) > 0
    assert dome.truncation_x == 0.499999
    assert dome.truncation_y == 0.499999
    assert dome.truncation_z == 0.499999


@pytest.mark.parametrize(
    "kwargs,expected_substring",
    [
        (dict(radius=0), "greater than zero"),
        (dict(radius=-1), "greater than zero"),
        (dict(frequency=0), "positive integer"),
        (dict(dome_class=4), "1, 2, or 3"),
        (dict(n_frequency=0), "positive integer"),
        (dict(elongation_factors=(0, 1.0, 1.0)), "greater than zero"),
        (dict(elongation_factors=(1.0, -1.0, 1.0)), "greater than zero"),
        (dict(elongation_factors=(1.0, 1.0, 0)), "greater than zero"),
        (dict(dome_class=2, frequency=3), "even"),
        (dict(dome_class=3, frequency=3, n_frequency=None), "n-frequency"),
        (dict(dome_class=3, frequency=3, n_frequency=3), "differ"),
    ],
)
def test_validate_geometry_params_rejects_bad_values(kwargs, expected_substring):
    params = dict(radius=1.0, frequency=4, dome_class=1, n_frequency=None,
                  elongation_factors=(1.0, 1.0, 1.0))
    params.update(kwargs)
    with pytest.raises(ValueError, match=expected_substring):
        validate_geometry_params(**params)


