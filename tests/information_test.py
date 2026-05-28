import numpy as np
import pytest

import scyseq.information as I
from scyseq.exceptions import LengthError
from scyseq.sequence import Alphabet, Sequence


def make_reference_sequence():
    np.random.seed(9)
    values = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    return Sequence(values, Alphabet(["a", "b"]))


def make_reference_triplet():
    alpha = Alphabet(["a", "b"])

    np.random.seed(9)
    seq1 = Sequence(np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3]), alpha)
    np.random.seed(6)
    seq2 = Sequence(np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3]), alpha)
    np.random.seed(3)
    seq3 = Sequence(np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3]), alpha)

    return seq1, seq2, seq3


def test_information_aliases():
    assert I.H is I.metric_entropy
    assert I.shannon_entropy is I.metric_entropy
    assert I.T is I.topological_entropy
    assert I.R is I.renyi_entropy


def test_scalar_entropy_reference_values():
    seq = make_reference_sequence()

    assert I.metric_entropy(seq) == pytest.approx(0.6003511877776578)
    assert isinstance(I.metric_entropy(seq), float)
    assert I.topological_entropy(seq) == pytest.approx(0.6931471805599453)
    assert I.renyi_entropy(seq, 0.9) == pytest.approx(0.6088567303148161)


def test_word_based_entropy_reference_values():
    seq = make_reference_sequence()

    assert I.block_entropy(seq, 6) == pytest.approx(3.577559335188841)
    assert I.entropy_rate(seq, 6) == pytest.approx(0.5962598891981402)
    assert I.entropy_rate(seq, 6, method="difference") == pytest.approx(
        0.5689107029836205
    )
    assert I.effective_complexity(seq, 6) == pytest.approx(0.05784767682768299)


def test_joint_information_reference_values():
    seq1, seq2, seq3 = make_reference_triplet()

    assert I.mutual_information(seq1, seq2) == pytest.approx(0.0002988020334349084)
    assert I.multi_information(seq1, seq2, seq3) == pytest.approx(
        -4.8757282800737656e-05
    )
    assert I.transfer_entropy(seq1[:-1], seq1[1:], seq2[:-1]) == pytest.approx(
        0.00019242807727182232
    )


@pytest.mark.parametrize("wlen", [0, 1001])
def test_block_entropy_rejects_invalid_word_lengths(wlen):
    seq = make_reference_sequence()

    with pytest.raises(ValueError, match="Word length"):
        I.block_entropy(seq, wlen)


def test_entropy_rate_rejects_unsupported_method():
    seq = make_reference_sequence()

    with pytest.raises(NotImplementedError, match="entropy rate"):
        I.entropy_rate(seq, 6, method="unsupported")


def test_mutual_information_rejects_unequal_lengths():
    seq1, seq2, _ = make_reference_triplet()

    with pytest.raises(LengthError, match="same length"):
        I.mutual_information(seq1, seq2[:-1])


def test_multi_information_rejects_unequal_lengths():
    seq1, seq2, seq3 = make_reference_triplet()

    with pytest.raises(LengthError, match="same length"):
        I.multi_information(seq1, seq2, seq3[:-1])


def test_transfer_entropy_rejects_unequal_lengths():
    seq1, seq2, _ = make_reference_triplet()

    with pytest.raises(LengthError, match="same length"):
        I.transfer_entropy(seq1[:-1], seq1[1:], seq2)


def test_information_routes_through_sequence_module_helpers(monkeypatch):
    seq = make_reference_sequence()
    seq1, seq2, _ = make_reference_triplet()
    calls = {"words": 0, "recode": 0}

    original_words = I.sq.words
    original_recode = I.sq.recode

    def tracked_words(*args, **kwargs):
        calls["words"] += 1
        return original_words(*args, **kwargs)

    def tracked_recode(*args, **kwargs):
        calls["recode"] += 1
        return original_recode(*args, **kwargs)

    monkeypatch.setattr(I.sq, "words", tracked_words)
    monkeypatch.setattr(I.sq, "recode", tracked_recode)

    I.block_entropy(seq, 6)
    I.mutual_information(seq1, seq2)

    assert calls["words"] == 1
    assert calls["recode"] == 1
