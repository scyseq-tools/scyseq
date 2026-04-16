import numpy as np
import pytest

import scyseq.sequence as S
from scyseq.exceptions import LengthError


def test_sequence_module_exposes_recode_and_words():
    assert callable(S.recode)
    assert callable(S.words)


def test_sequence_module_recode_matches_historical_binary_example():
    seq1 = S.Sequence([0, 0, 1, 1], 2)
    seq2 = S.Sequence([0, 1, 0, 1], 2)

    seqr = S.recode([seq1, seq2])

    np.testing.assert_array_equal(seqr.ivals, np.array([0, 1, 2, 3]))
    assert seqr.k == 4


def test_sequence_module_words_matches_historical_example():
    seq = S.Sequence([0, 0, 1, 1, 0], 2)

    word_seq = S.words(seq, 2)

    np.testing.assert_array_equal(word_seq.ivals, np.array([0, 1, 3, 2]))
    assert word_seq.k == 4


def test_sequence_module_recode_raises_length_error_on_mismatch():
    seq1 = S.Sequence([0, 0, 1, 1], 2)
    seq2 = S.Sequence([0, 1, 0], 2)

    with pytest.raises(LengthError, match="same length"):
        S.recode([seq1, seq2])
