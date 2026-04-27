import numpy as np
import pytest

from scyseq.algorithmic import contains_sublist, lempel_ziv, lz76, lz77
from scyseq.sequence import Sequence


def test_contains_sublist_cases():
    assert contains_sublist([1, 2, 3, 4], [2, 3]) is True
    assert contains_sublist([1, 2, 3], [2, 4]) is False
    assert contains_sublist([1, 2], []) is True
    assert contains_sublist([], [1]) is False


def test_contains_sublist_legacy_cases():
    values = [1, 2, 3, 4, 5]

    assert contains_sublist(values, [2, 3]) is True
    assert contains_sublist(values, [2, 4]) is False


def test_lz76_and_lz77_share_reference_history():
    arr = np.array([0, 0, 1, 0, 1, 1], dtype=np.uint8)
    expected = (3, [[0], [0, 1], [0, 1, 1]])

    assert lz76(arr) == 3
    assert lz77(arr) == 3
    assert lz76(arr, summary=True) == expected
    assert lz77(arr, summary=True) == expected


def test_lz76_and_lz77_differ_on_alternating_sequence():
    arr = np.array([0, 1, 0, 1, 0, 1], dtype=np.uint8)

    assert lz76(arr, summary=True) == (4, [[0], [1], [0, 1, 0], [1]])
    assert lz77(arr, summary=True) == (4, [[0], [1], [0, 1], [0, 1]])


def test_lz_parsers_on_binary_legacy_sequence():
    values = [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0]

    assert lz77(values, summary=True) == (
        8,
        [[0], [1], [1, 1], [0, 1], [0, 1, 0], [0, 0], [1, 1, 1], [0]],
    )
    assert lz76(values, summary=True) == (
        6,
        [[0], [1], [1, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1, 1, 0]],
    )


def test_lz_parsers_on_general_legacy_alphabet_values():
    values = [0, 10, 11, 1, 10, 11, 0, 1, 10, 0, 0, 11, 1, 11, 10]

    assert lz77(values, summary=True) == (
        10,
        [[0], [10], [11], [1], [10, 11], [0, 1], [10, 0], [0, 11], [1, 11], [10]],
    )
    assert lz76(values, summary=True) == (
        9,
        [[0], [10], [11], [1], [10, 11, 0], [1, 10, 0], [0, 11], [1, 11], [10]],
    )


@pytest.mark.parametrize("parsing", ["lz76", "lz77"])
def test_lempel_ziv_raw_reference_value(parsing):
    seq = Sequence(np.array([0, 0, 1, 0, 1, 1], dtype=np.uint8), 2)

    assert lempel_ziv(seq, parsing=parsing) == pytest.approx(1.292481250360578)


def test_lempel_ziv_rejects_unknown_parser():
    seq = Sequence(np.array([0, 0, 1, 0, 1, 1], dtype=np.uint8), 2)

    with pytest.raises(NotImplementedError, match="The parsing nope is not implemented"):
        lempel_ziv(seq, parsing="nope")


def test_lempel_ziv_requires_nbsur_for_normalization():
    seq = Sequence(np.array([0, 0, 1, 0, 1, 1], dtype=np.uint8), 2)

    with pytest.raises(ValueError, match="You should give the number of surrogate data"):
        lempel_ziv(seq, norm=True)


@pytest.mark.parametrize("parsing", ["lz76", "lz77"])
@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([0, 0, 1, 0, 1, 1], 0.0),
        ([0, 1, 0, 1, 0, 1], 1.0),
    ],
)
def test_lempel_ziv_normalization_reference_values(parsing, values, expected):
    seq = Sequence(np.array(values, dtype=np.uint8), 2)

    np.random.seed(123)
    assert lempel_ziv(seq, parsing=parsing, norm=True, nbsur=5) == expected
