import numpy as np
import pytest

from pylair.elongation import elongate


def test_elongate_scales_only_the_z_axis():
    V = [np.array([1., 2., 3.]), np.array([-1., 0.5, -2.])]
    result = elongate(V, (1.0, 1.0, 2.0))

    assert result[0] == pytest.approx(np.array([1., 2., 6.]))
    assert result[1] == pytest.approx(np.array([-1., 0.5, -4.]))


def test_elongate_factors_of_one_are_a_no_op():
    V = [np.array([1., 2., 3.]), np.array([-1., 0.5, -2.])]
    result = elongate(V, (1.0, 1.0, 1.0))

    for original, scaled in zip(V, result):
        assert scaled == pytest.approx(original)


def test_elongate_does_not_mutate_the_input_list():
    V = [np.array([1., 2., 3.])]
    original = V[0].copy()
    elongate(V, (5.0, 5.0, 5.0))

    assert V[0] == pytest.approx(original)


@pytest.mark.parametrize("factor", [0.5, 2.0, 3.7])
def test_elongate_preserves_x_and_y(factor):
    V = [np.array([1., 2., 3.]), np.array([-4., 5., -6.])]
    result = elongate(V, (1.0, 1.0, factor))

    for original, scaled in zip(V, result):
        assert scaled[0] == pytest.approx(original[0])
        assert scaled[1] == pytest.approx(original[1])
        assert scaled[2] == pytest.approx(original[2] * factor)


def test_elongate_scales_x_and_y_independently_of_z():
    V = [np.array([1., 2., 3.]), np.array([-4., 5., -6.])]
    result = elongate(V, (2.0, 0.5, 1.0))

    for original, scaled in zip(V, result):
        assert scaled[0] == pytest.approx(original[0] * 2.0)
        assert scaled[1] == pytest.approx(original[1] * 0.5)
        assert scaled[2] == pytest.approx(original[2])


def test_elongate_scales_all_three_axes_independently():
    V = [np.array([1., 2., 3.])]
    result = elongate(V, (2.0, 3.0, 4.0))

    assert result[0] == pytest.approx(np.array([2., 6., 12.]))
