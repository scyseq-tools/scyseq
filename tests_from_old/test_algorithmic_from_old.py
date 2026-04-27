import pytest

from scyseq import algorithmic as A


def test_contains_sublist_legacy_cases():
    values = [1, 2, 3, 4, 5]

    assert A.contains_sublist(values, [2, 3]) is True
    assert A.contains_sublist(values, [2, 4]) is False


def test_lz_parsers_on_binary_legacy_sequence():
    values = [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0]

    assert A.lz77(values, summary=True) == (
        8,
        [[0], [1], [1, 1], [0, 1], [0, 1, 0], [0, 0], [1, 1, 1], [0]],
    )
    assert A.lz76(values, summary=True) == (
        6,
        [[0], [1], [1, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1, 1, 0]],
    )


def test_lz_parsers_on_general_legacy_alphabet_values():
    values = [0, 10, 11, 1, 10, 11, 0, 1, 10, 0, 0, 11, 1, 11, 10]

    assert A.lz77(values, summary=True) == (
        10,
        [[0], [10], [11], [1], [10, 11], [0, 1], [10, 0], [0, 11], [1, 11], [10]],
    )
    assert A.lz76(values, summary=True) == (
        9,
        [[0], [10], [11], [1], [10, 11, 0], [1, 10, 0], [0, 11], [1, 11], [10]],
    )


def test_lempel_ziv_placeholder_from_legacy_file_is_now_covered_elsewhere():
    pytest.importorskip("scyseq.algorithmic")
