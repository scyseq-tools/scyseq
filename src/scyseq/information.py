# Copyright (c) 2007-2026 The scyseq developers.
# SPDX-License-Identifier: BSD-3-Clause BSD

"""
Information-theoretic measures for symbolic sequences.

This module gathers entropy, mutual-information, and transfer-entropy helpers
for :class:`scyseq.sequence.Sequence` objects. All logarithms are natural
logarithms, so the returned values are expressed in nats.
"""

import numpy as np

import scyseq as sq


def metric_entropy(seq):
    """
    Return Shannon's metric entropy of a symbolic sequence.

    :param seq: A symbolic :class:`scyseq.sequence.Sequence`.
    :returns: A float entropy value in nats.

    >>> np.random.seed(9)
    >>> a = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> alpha = sq.Alphabet(["a", "b"])
    >>> seq = sq.Sequence(a, alpha)
    >>> metric_entropy(seq)
    0.6003511877776578
    """
    prob = seq.frequency()
    entropy = -np.sum(prob[prob > 0] * np.log(prob[prob > 0]))
    return float(entropy)


# shortcuts for Shannon (metric) entropy
H = metric_entropy
shannon_entropy = metric_entropy


def topological_entropy(seq):
    """
    Return the topological entropy of a symbolic sequence.

    :param seq: A symbolic :class:`scyseq.sequence.Sequence`.
    :returns: A float entropy value in nats.

    >>> np.random.seed(9)
    >>> a = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> alpha = sq.Alphabet(["a", "b"])
    >>> seq = sq.Sequence(a, alpha)
    >>> topological_entropy(seq)
    0.6931471805599453
    """
    nb_visit = np.sum(seq.count() > 0)
    return float(np.log(float(nb_visit)))


# shortcut for topological entropy
T = topological_entropy


def renyi_entropy(seq, coef):
    """
    Return the Renyi entropy of order ``coef``.

    :param seq: A symbolic :class:`scyseq.sequence.Sequence`.
    :param coef: Renyi order. The formula used here assumes ``coef != 1``.
    :returns: A float entropy value in nats.

    >>> np.random.seed(9)
    >>> a = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> alpha = sq.Alphabet(["a", "b"])
    >>> seq = sq.Sequence(a, alpha)
    >>> renyi_entropy(seq, 0.9)
    0.6088567303148161
    """
    prob = seq.frequency()
    return float(np.log(np.sum(prob[prob > 0] ** coef)) / (1 - coef))


# shortcut for Renyi entropy
R = renyi_entropy


def block_entropy(seq, wlen):
    """
    Return the entropy of the overlapping words of length ``wlen``.

    :param seq: A symbolic :class:`scyseq.sequence.Sequence`.
    :param wlen: Positive word length not exceeding ``len(seq)``.
    :returns: A float entropy value in nats.
    :raises: :exc:`ValueError` if ``wlen`` is invalid.

    >>> np.random.seed(9)
    >>> a = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> alpha = sq.Alphabet(["a", "b"])
    >>> seq = sq.Sequence(a, alpha)
    >>> block_entropy(seq, 6)
    3.577559335188841
    """
    nwords = sq.words(seq, wlen)
    return H(nwords)


def entropy_rate(seq, wlen, method="average"):
    """
    Return an entropy-rate estimate based on block entropies.

    :param seq: A symbolic :class:`scyseq.sequence.Sequence`.
    :param wlen: Positive word length not exceeding ``len(seq)``.
    :param method: One of ``["average", "difference"]``.
    :returns: The entropy-rate estimate as a float.
    :raises:
       :exc:`ValueError` if ``wlen`` is invalid.
       :exc:`NotImplementedError` if ``method`` is unsupported.

    >>> np.random.seed(9)
    >>> a = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> alpha = sq.Alphabet(["a", "b"])
    >>> seq = sq.Sequence(a, alpha)
    >>> entropy_rate(seq, 6)
    0.5962598891981402
    >>> entropy_rate(seq, 6, method="difference")
    0.5689107029836205
    """
    if method.lower() == "average":
        return block_entropy(seq, wlen) / wlen

    if method.lower() == "difference":
        return block_entropy(seq, wlen + 1) - block_entropy(seq, wlen)

    msg = f"The {method} entropy rate is not implemented"
    raise NotImplementedError(msg)


def effective_complexity(seq, n_max):
    """
    Return Grassberger's effective complexity estimate.

    :param seq: A symbolic :class:`scyseq.sequence.Sequence`.
    :param n_max: Maximum block length used in the estimate.
    :returns: A float effective-complexity value.

    >>> np.random.seed(9)
    >>> a = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> alpha = sq.Alphabet(["a", "b"])
    >>> seq = sq.Sequence(a, alpha)
    >>> effective_complexity(seq, 6)
    0.05784767682768299
    """
    blocks = [block_entropy(seq, wlen) for wlen in range(1, n_max + 1)]
    rates = np.diff(blocks)
    drate = np.diff(np.flipud(rates))
    return float(np.sum(np.arange(2, len(drate) + 2) * np.flipud(drate)))


def mutual_information(seq1, seq2):
    """
    Return the mutual information between two symbolic sequences.

    :param seq1: First symbolic :class:`scyseq.sequence.Sequence`.
    :param seq2: Second symbolic :class:`scyseq.sequence.Sequence`.
    :returns: The mutual information as a float.
    :raises: :exc:`LengthError` if the sequences do not have the same length.

    >>> np.random.seed(9)
    >>> a = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> np.random.seed(6)
    >>> b = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> alpha = sq.Alphabet(["a", "b"])
    >>> seq1 = sq.Sequence(a, alpha)
    >>> seq2 = sq.Sequence(b, alpha)
    >>> mutual_information(seq1, seq2)
    0.0002988020334349084
    """
    seq12 = sq.recode([seq1, seq2])
    return float(H(seq1) + H(seq2) - H(seq12))


def multi_information(seq1, seq2, seq3):
    """
    Return the three-variable mutual information for symbolic sequences.

    :param seq1: First symbolic :class:`scyseq.sequence.Sequence`.
    :param seq2: Second symbolic :class:`scyseq.sequence.Sequence`.
    :param seq3: Third symbolic :class:`scyseq.sequence.Sequence`.
    :returns: The three-variable mutual information as a float.
    :raises: :exc:`LengthError` if the sequences do not have the same length.

    >>> np.random.seed(9)
    >>> a = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> np.random.seed(6)
    >>> b = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> np.random.seed(3)
    >>> c = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> alpha = sq.Alphabet(["a", "b"])
    >>> seq1 = sq.Sequence(a, alpha)
    >>> seq2 = sq.Sequence(b, alpha)
    >>> seq3 = sq.Sequence(c, alpha)
    >>> multi_information(seq1, seq2, seq3)
    -4.8757282800737656e-05
    """
    seq12 = sq.recode([seq1, seq2])
    seq13 = sq.recode([seq1, seq3])
    seq23 = sq.recode([seq2, seq3])
    seq123 = sq.recode([seq1, seq2, seq3])

    return float(
        H(seq1) + H(seq2) + H(seq3) + H(seq123) - H(seq12) - H(seq13) - H(seq23)
    )


def transfer_entropy(seq1, seq1p, seq2):
    """
    Return the symbolic transfer entropy from ``seq2`` to ``seq1``.

    ``seq1`` corresponds to :math:`x_t`, ``seq1p`` to :math:`x_{t+1}`, and
    ``seq2`` to :math:`y_t`.

    :param seq1: Target sequence at time :math:`t`.
    :param seq1p: Shifted version of the target sequence at time :math:`t+1`.
    :param seq2: Driving sequence at time :math:`t`.
    :returns: The transfer entropy as a float.
    :raises: :exc:`LengthError` if the sequences do not have the same length.

    >>> np.random.seed(9)
    >>> a = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> np.random.seed(6)
    >>> b = np.random.choice([0, 1], 1000, replace=True, p=[0.7, 0.3])
    >>> alpha = sq.Alphabet(["a", "b"])
    >>> seq1 = sq.Sequence(a, alpha)
    >>> seq2 = sq.Sequence(b, alpha)
    >>> transfer_entropy(seq1[:-1], seq1[1:], seq2[:-1])
    0.00019242807727182232
    """
    seq1p21 = sq.recode([seq1p, seq2, seq1])
    seq21 = sq.recode([seq2, seq1])
    seq1p1 = sq.recode([seq1p, seq1])

    return float(-H(seq1p21) + H(seq21) + H(seq1p1) - H(seq1))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
