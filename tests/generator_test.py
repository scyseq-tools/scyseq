import numpy as np
import pytest

from scyseq.generator import (
    binary_logistic_sequence,
    binary_map1d_sequence,
    generate,
    markov_sequence,
    uniform_sequence,
)
from scyseq.sequence import boolean_alphabet


def test_uniform_sequence_respects_length_and_alphabet_size():
    np.random.seed(123)

    seq = uniform_sequence(8, 3)

    np.testing.assert_array_equal(seq.ivals, np.array([2, 1, 2, 2, 0, 2, 2, 1]))
    assert len(seq) == 8
    assert seq.k == 3


def test_generate_dispatches_uniform_sequence():
    np.random.seed(123)

    seq = generate("uniform", 8, 3)

    np.testing.assert_array_equal(seq.ivals, np.array([2, 1, 2, 2, 0, 2, 2, 1]))
    assert seq.k == 3


def test_binary_map1d_sequence_thresholds_generated_values():
    seq = binary_map1d_sequence(4, lambda x: x + 0.2, xinit=0.0, threshold=0.5, skip=0)

    np.testing.assert_array_equal(seq.ivals, np.array([0, 0, 0, 1]))
    assert seq.alphabet == boolean_alphabet


def test_binary_logistic_sequence_returns_boolean_alphabet_sequence():
    seq = binary_logistic_sequence(4, param=4.0, xinit=0.2, threshold=0.5, skip=0)

    np.testing.assert_array_equal(seq.ivals, np.array([0, 1, 1, 0]))
    assert seq.alphabet == boolean_alphabet


def test_generate_dispatches_binary_logistic_sequence():
    seq = generate("binary_logistic", 4, 2, 4.0, 0.2)

    np.testing.assert_array_equal(seq.ivals, np.array([1, 0, 1, 0]))
    assert seq.alphabet == boolean_alphabet


def test_markov_sequence_uses_transition_matrix_shape_and_probabilities():
    matrix = np.array([[1.0, 0.0], [0.0, 1.0]])

    np.random.seed(5)
    seq = markov_sequence(6, 2, matrix, order=1)

    np.testing.assert_array_equal(seq.ivals, np.array([1, 1, 1, 1, 1, 1]))
    assert seq.k == 2


def test_generate_dispatches_markov_sequence():
    matrix = np.array([[1.0, 0.0], [0.0, 1.0]])

    np.random.seed(5)
    seq = generate("markov", 6, 2, matrix, 1)

    np.testing.assert_array_equal(seq.ivals, np.array([1, 1, 1, 1, 1, 1]))


def test_markov_sequence_rejects_bad_transition_matrix_shape():
    with pytest.raises(AssertionError, match="shape"):
        markov_sequence(4, 2, np.ones((2, 2)), order=2)


def test_generate_rejects_unknown_method():
    with pytest.raises(NotImplementedError, match="not implemented"):
        generate("unknown", 4, 2)
