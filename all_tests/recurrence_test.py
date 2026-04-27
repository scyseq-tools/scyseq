import numpy as np

from scyseq.generator import uniform_sequence
from scyseq.recurrence import recurrence, recurrence_rate
from scyseq.sequence import Sequence


def test_recurrence_plot_matches_equal_outer_product():
    seq = Sequence([0, 1, 0, 2], 3)

    expected = np.array(
        [
            [1, 0, 1, 0],
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    np.testing.assert_array_equal(recurrence(seq), expected)


def test_recurrence_rate_ignores_main_diagonal():
    rp = np.array(
        [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
    )

    assert recurrence_rate(rp) == 2 / 6


def test_uniform_generated_sequence_can_be_used_for_recurrence_plot():
    np.random.seed(123)
    seq = uniform_sequence(10, 4)

    rp = recurrence(seq)

    assert rp.shape == (10, 10)
    np.testing.assert_array_equal(np.diag(rp), np.ones(10, dtype=int))
