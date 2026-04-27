import copy

import numpy as np
import pytest

import scyseq as sq
from scyseq import exceptions as E


def test_sequence_initialization_with_length_and_named_alphabet():
    symbols = [1, 0, 2]

    seq = sq.Sequence(symbols, 3)
    np.testing.assert_array_equal(seq.ivals, np.array(symbols))
    assert seq.k == 3
    assert seq.alphabet == sq.Alphabet(3)

    named = sq.Sequence(symbols, ("a", "b", "c"))
    np.testing.assert_array_equal(named.ivals, np.array(symbols))
    assert named.k == 3
    assert named.alphabet.svals == ("a", "b", "c")


def test_sequence_initialization_errors_from_legacy_cases():
    symbols = [1, 0, 2]

    with pytest.raises(TypeError):
        sq.Sequence(symbols)
    with pytest.raises(E.AlphabetError):
        sq.Sequence(symbols, 2.3)
    with pytest.raises(ValueError, match="Symbols or strings"):
        sq.Sequence(symbols, [2, 3])
    with pytest.raises(ValueError, match=">=0"):
        sq.Sequence([1, 0, -2], 3)
    with pytest.raises(E.AlphabetError, match="Invalid alphabet length"):
        sq.Sequence(symbols, 2)
    with pytest.raises(E.AlphabetError, match="Invalid alphabet length"):
        sq.Sequence(symbols, ("a", "b"))


def test_sequence_copy_from_existing_sequence():
    seq = sq.Sequence([1, 0, 2], 3)

    copied = sq.Sequence(seq, seq.alphabet)

    np.testing.assert_array_equal(copied.ivals, seq.ivals)
    assert copied.k == seq.k
    assert copied.alphabet == seq.alphabet
    assert copied is not seq


def test_sequence_slicing_returns_sequences_with_same_alphabet():
    values = [1, 0, 2, 2, 1, 0, 2, 0, 0, 0, 1]
    seq = sq.Sequence(values, 3)

    assert len(seq) == len(values)
    np.testing.assert_array_equal(seq[4].ivals, np.array([values[4]]))
    np.testing.assert_array_equal(seq[2:6].ivals, np.array(values[2:6]))
    np.testing.assert_array_equal(seq[-3:].ivals, np.array(values[-3:]))
    assert seq[2:6].alphabet == seq.alphabet


def test_sequence_iterators_expose_symbols_integer_values_and_labels():
    seq = sq.Sequence([1, 0, 2], ("a", "b", "c"))

    assert [symbol.sval for symbol in seq] == ["b", "a", "c"]
    assert list(seq.iterivals()) == [1, 0, 2]
    assert list(seq.itersvals()) == ["b", "a", "c"]
    assert list(seq.iteritems()) == [(1, "b"), (0, "a"), (2, "c")]


def test_sequence_transform_methods_return_new_sequences():
    values = [0, 2, 0, 0, 0, 1]
    seq = sq.Sequence(values, 3)

    np.testing.assert_array_equal(seq.roll(3).ivals, np.roll(values, 3))
    np.testing.assert_array_equal(seq.roll(-3).ivals, np.roll(values, -3))
    np.testing.assert_array_equal(seq.reverse().ivals, np.flipud(values))

    np.random.seed(2012)
    shuffled_values = copy.copy(seq.ivals)
    np.random.shuffle(shuffled_values)
    np.random.seed(2012)
    np.testing.assert_array_equal(seq.shuffle().ivals, shuffled_values)

    np.testing.assert_array_equal(seq.ivals, np.array(values))


def test_sequence_reduce_count_and_frequency_legacy_cases():
    values = [0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1, 0, 1, 2, 0, 0]
    seq = sq.Sequence(values, 3)

    np.testing.assert_array_equal(seq.reduce().ivals, np.array([0, 2, 0, 1, 0, 1, 2, 0]))
    np.testing.assert_array_equal(seq.count(), np.array([8, 4, 4]))
    np.testing.assert_array_equal(seq.frequency(), np.array([8, 4, 4]) / len(values))

    sparse = sq.Sequence([2, 2, 2, 1, 1, 1, 1, 2], 3)
    np.testing.assert_array_equal(sparse.count(), np.array([0, 4, 4]))
    np.testing.assert_array_equal(sparse.frequency(), np.array([0, 4, 4]) / 8)


def test_transform_function_legacy_cases_with_current_alphabet_api():
    seq = sq.Sequence([0, 2, 0, 2, 0, 1, 2, 1, 1], 3)

    transformed = sq.transform(seq, [1, 0, 0])
    np.testing.assert_array_equal(transformed.ivals, np.array([1, 0, 1, 0, 1, 0, 0, 0, 0]))
    assert transformed.k == 2
    assert transformed.alphabet == sq.Alphabet(2)

    named = sq.transform(seq, [0, 1, 1], sq.Alphabet(("a", "b")))
    np.testing.assert_array_equal(named.ivals, np.array([0, 1, 0, 1, 0, 1, 1, 1, 1]))
    assert named.k == 2
    assert named.alphabet.svals == ("a", "b")


@pytest.mark.parametrize(
    "correspondence,new_alphabet,error",
    [
        ([0, 1], None, ValueError),
        ([0, 1, 1, 0], None, ValueError),
        ([2, 1, 6], None, ValueError),
        ([0, 1, 1], sq.Alphabet(("a", "b", "c")), E.AlphabetError),
    ],
)
def test_transform_rejects_invalid_legacy_cases(correspondence, new_alphabet, error):
    seq = sq.Sequence([0, 2, 0, 2, 0, 1, 2, 1, 1], 3)

    with pytest.raises(error):
        sq.transform(seq, correspondence, new_alphabet)


def test_recode_legacy_binary_and_mixed_alphabet_cases():
    seq1 = sq.Sequence([0, 0, 1, 1], 2)
    seq2 = sq.Sequence([0, 1, 0, 1], 2)

    recoded = sq.recode([seq1, seq2])

    np.testing.assert_array_equal(recoded.ivals, np.array([0, 1, 2, 3]))
    assert recoded.k == 4
    assert recoded.alphabet == sq.Alphabet(4)

    named1 = sq.Sequence([0, 0, 1, 1], ("a", "b"))
    named2 = sq.Sequence([0, 1, 0, 1], ("c", "d"))
    named_recoded = sq.recode([named1, named2], new_alphabet=True, names=["x", "y"])

    np.testing.assert_array_equal(named_recoded.ivals, np.array([0, 1, 2, 3]))
    assert named_recoded.k == 4
    assert named_recoded.alphabet.svals == (
        "x_a+y_c",
        "x_a+y_d",
        "x_b+y_c",
        "x_b+y_d",
    )


def test_recode_legacy_two_by_three_case_and_length_error():
    seq1 = sq.Sequence([0, 0, 0, 1, 1, 1], 2)
    seq2 = sq.Sequence([0, 1, 2, 0, 1, 2], 3)

    recoded = sq.recode([seq1, seq2])
    np.testing.assert_array_equal(recoded.ivals, np.array([0, 1, 2, 3, 4, 5]))
    assert recoded.k == 6

    with pytest.raises(E.LengthError, match="same length"):
        sq.recode([seq1, sq.Sequence([0, 1], 2)])


def test_recode_three_sequence_legacy_cardinality_case():
    seq_a = sq.Sequence([0] * 18 + [1] * 18, ("a", "b"))
    seq_b = sq.Sequence(([0] * 6 + [1] * 6 + [2] * 6) * 2, ("c", "d", "e"))
    seq_c = sq.Sequence([0, 1, 2, 3, 4, 5] * 6, 6)

    recoded = sq.recode([seq_a, seq_b, seq_c])

    np.testing.assert_array_equal(recoded.ivals, np.arange(36))
    assert recoded.k == 36


def test_words_legacy_case_and_invalid_word_length():
    seq = sq.Sequence([0, 0, 1, 1, 0], 2)

    words = sq.words(seq, 2)

    np.testing.assert_array_equal(words.ivals, np.array([0, 1, 3, 2]))
    with pytest.raises(ValueError, match="Word length"):
        sq.words(seq, -2)
