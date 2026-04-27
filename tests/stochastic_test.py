import numpy as np

from scyseq import stochastic as St
from scyseq.sequence import Sequence


def test_conditional_matrix_with_same_binary_alphabet_legacy_cases():
    seq = Sequence([1, 0, 1, 0, 1, 0], 2)

    np.testing.assert_array_equal(
        St.conditional_matrix(seq, seq),
        np.array([[1, 0], [0, 1]]),
    )

    seq1 = Sequence([1, 1, 0, 0], 2)
    seq2 = Sequence([1, 0, 0, 1], 2)

    np.testing.assert_array_equal(
        St.conditional_matrix(seq1, seq2),
        np.array([[0.5, 0.5], [0.5, 0.5]]),
    )


def test_conditional_matrix_with_different_alphabets_legacy_cases():
    seq1 = Sequence([1, 1, 1, 0, 0, 0], 2)
    seq2 = Sequence([0, 1, 2, 0, 1, 2], 3)

    np.testing.assert_array_equal(
        St.conditional_matrix(seq1, seq2),
        np.array([[0.5, 0.5], [0.5, 0.5], [0.5, 0.5]]),
    )
    np.testing.assert_array_equal(
        St.conditional_matrix(seq2, seq1),
        np.array([[1 / 3, 1 / 3, 1 / 3], [1 / 3, 1 / 3, 1 / 3]]),
    )


def test_conditional_matrix_with_different_alphabets_weighted_legacy_cases():
    seq1 = Sequence([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], 2)
    seq2 = Sequence([0, 0, 1, 2, 2, 0, 1, 1, 1, 2, 2, 2, 2], 3)

    np.testing.assert_array_equal(
        St.conditional_matrix(seq1, seq2),
        np.array([[1 / 3, 2 / 3], [3 / 4, 1 / 4], [2 / 3, 1 / 3]]),
    )
    np.testing.assert_array_equal(
        St.conditional_matrix(seq2, seq1),
        np.array([[1 / 8, 3 / 8, 1 / 2], [2 / 5, 1 / 5, 2 / 5]]),
    )
