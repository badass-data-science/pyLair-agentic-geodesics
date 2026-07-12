import numpy as np
import pytest

from pydome.api import build_dome, validate_geometry_params, validate_output_combo


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
    normal = build_dome(frequency=2, elongation_factor=1.0)
    tall = build_dome(frequency=2, elongation_factor=1.8)

    normal_z = [v[2] for v in normal.V]
    tall_z = [v[2] for v in tall.V]
    normal_x = [v[0] for v in normal.V]
    tall_x = [v[0] for v in tall.V]

    assert (max(tall_z) - min(tall_z)) > (max(normal_z) - min(normal_z))
    assert (max(tall_x) - min(tall_x)) == pytest.approx(max(normal_x) - min(normal_x))
    assert tall.elongation_factor == 1.8


def test_truncation_leaves_face_data_none_and_sets_truncated_flag():
    dome = build_dome(frequency=4, truncation_amount=0.499999)
    assert dome.truncated is True
    assert dome.F_sphere is None


def test_no_truncation_leaves_face_data_populated():
    dome = build_dome(frequency=4)
    assert dome.truncated is False
    assert dome.F_sphere is not None


def test_truncate_horizontal_chord_error_propagates_unmodified():
    # a cutoff that lands exactly on a vertex ring produces a horizontal
    # chord at the cutoff plane -- truncate() itself raises this, and
    # build_dome must not swallow or reword it
    with pytest.raises(ValueError, match="horizontal chord"):
        build_dome(frequency=4, truncation_amount=0.5)


@pytest.mark.parametrize(
    "kwargs,expected_substring",
    [
        (dict(radius=0), "greater than zero"),
        (dict(radius=-1), "greater than zero"),
        (dict(frequency=0), "positive integer"),
        (dict(dome_class=4), "1, 2, or 3"),
        (dict(n_frequency=0), "positive integer"),
        (dict(elongation_factor=0), "greater than zero"),
        (dict(dome_class=2, frequency=3), "even"),
        (dict(dome_class=3, frequency=3, n_frequency=None), "n-frequency"),
        (dict(dome_class=3, frequency=3, n_frequency=3), "differ"),
    ],
)
def test_validate_geometry_params_rejects_bad_values(kwargs, expected_substring):
    params = dict(radius=1.0, frequency=4, dome_class=1, n_frequency=None, elongation_factor=1.0)
    params.update(kwargs)
    with pytest.raises(ValueError, match=expected_substring):
        validate_geometry_params(**params)


def test_validate_output_combo_rejects_face_formats_with_truncation():
    for kwargs in (dict(face_output=True), dict(stl_output=True), dict(obj_output=True)):
        with pytest.raises(ValueError, match="does not work"):
            validate_output_combo(True, **kwargs)


def test_validate_output_combo_allows_face_formats_without_truncation():
    validate_output_combo(False, face_output=True, stl_output=True, obj_output=True)


def test_validate_output_combo_allows_truncation_without_face_formats():
    validate_output_combo(True)


def test_validate_output_combo_rejects_face_templates_with_truncation():
    with pytest.raises(ValueError, match="does not work"):
        validate_output_combo(True, face_template_output=True)


def test_validate_output_combo_rejects_area_cost_or_panel_density_with_truncation():
    for kwargs in (dict(cost_per_unit_area=2.0), dict(panel_areal_density=0.5)):
        with pytest.raises(ValueError, match="does not work"):
            validate_output_combo(True, **kwargs)


def test_validate_output_combo_allows_panel_options_without_truncation():
    validate_output_combo(False, face_template_output=True, cost_per_unit_area=2.0,
                           panel_areal_density=0.5)
