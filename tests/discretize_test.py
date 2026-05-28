import numpy as np
import pytest

from scyseq.discretize import partition, subdivision, symbolize


def test_symbolize_uses_bins_to_create_sequence():
    seq = symbolize(np.array([0.2, 0.8, 1.2, 1.8]), bins=np.array([0.0, 1.0]))

    np.testing.assert_array_equal(seq.ivals, np.array([0, 0, 1, 1]))
    assert seq.k == 2


def test_symbolize_keeps_underflow_bin_when_values_precede_first_bin():
    seq = symbolize(np.array([-1.0, 0.2, 1.2]), bins=np.array([0.0, 1.0]))

    np.testing.assert_array_equal(seq.ivals, np.array([0, 1, 2]))
    assert seq.k == 3


def test_partition_histogram_matches_documented_example():
    seq = partition(np.linspace(0, 10, 11), method="histogram", nbin=6)

    np.testing.assert_array_equal(
        seq.ivals, np.array([0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5])
    )
    assert seq.k == 6


def test_partition_marginal_equi_quantization_matches_documented_example():
    seq = partition(np.linspace(0, 10, 11), method="marginal_equiquantization", nbin=6)

    np.testing.assert_array_equal(
        seq.ivals, np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5])
    )
    assert seq.k == 6


def test_partition_rejects_unknown_method():
    with pytest.raises(NotImplementedError, match="method"):
        partition(np.arange(5), method="unknown", nbin=3)


def test_subdivision_returns_boxes_and_reference_splits():
    data = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])

    boxes, refs = subdivision(data, iter_max=2)

    np.testing.assert_array_equal(boxes, np.array([0, 1, 2, 3]))
    assert refs == [[0.5], [0.5, 0.5]]
