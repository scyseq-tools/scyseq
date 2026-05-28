# Copyright (c) 2007-2026 The scyseq developers.
# SPDX-License-Identifier: BSD-3-Clause BSD

"""
Utilities for algorithmic complexity on symbolic sequences.

The public helpers in this module compute Lempel-Ziv complexities on
integer-encoded symbolic sequences. ``lz76`` and ``lz77`` accept non-empty
one-dimensional arrays of integers and can optionally return the parsing
history used to count phrases. ``lempel_ziv`` works on
:class:`scyseq.sequence.Sequence` objects and returns either the raw or the
normalized complexity score.
"""

__docformat__ = "reStructuredText"

import numpy as np

from scyseq import sequence as S
from scyseq.generator import uniform_sequence


def contains_sublist(lst, sublst):
    """
    Return whether ``sublst`` appears contiguously inside ``lst``.

    :param lst: Sequence to inspect.
    :param sublst: Candidate contiguous subsequence.
    :returns: ``True`` if ``sublst`` appears in ``lst``, ``False`` otherwise.

    The empty sublist is considered to be contained in every list.

    >>> contains_sublist([1, 2, 3, 4], [2, 3])
    True
    >>> contains_sublist([1, 2, 3], [2, 4])
    False
    >>> contains_sublist([1, 2], [])
    True
    """
    sublist_length = len(sublst)
    return any(
        sublst == lst[index : index + sublist_length]
        for index in range(len(lst) - sublist_length + 1)
    )


def lz76(arr, summary=False):
    """
    Return the Lempel-Ziv complexity obtained with the LZ76 parsing.

    :param arr: Non-empty array-like object of integers.
    :param summary: If ``True``, also return the parsing history.
    :returns: Either an integer or a tuple ``(complexity, history)`` when
              ``summary=True``.
    :raises: :exc:`IndexError` if ``arr`` is empty.

    The returned history is the ordered list of phrases discovered during the
    parsing.

    >>> arr = np.array([0, 0, 1, 0, 1, 1], dtype=np.uint8)
    >>> lz76(arr)
    3
    >>> lz76(arr, summary=True)
    (3, [[0], [0, 1], [0, 1, 1]])
    """
    dot, ind = 1, 0
    history = [[int(arr[0])]]
    previous = [int(arr[0])]
    current = []

    while ind < len(arr) - 1:
        current.append(int(arr[ind + 1]))

        if not contains_sublist(previous, current):
            dot += 1
            history.append(current)
            previous.extend(current)
            current = []

        ind += 1

    if current:
        dot += 1
        history.append(current)

    if summary:
        return dot, history

    return dot


def lz77(arr, summary=False):
    """
    Return the Lempel-Ziv complexity obtained with the LZ77 parsing.

    :param arr: Non-empty array-like object of integers.
    :param summary: If ``True``, also return the parsing history.
    :returns: Either an integer or a tuple ``(complexity, history)`` when
              ``summary=True``.
    :raises: :exc:`IndexError` if ``arr`` is empty.

    The returned history is the ordered list of phrases discovered during the
    parsing.

    >>> arr = np.array([0, 0, 1, 0, 1, 1], dtype=np.uint8)
    >>> lz77(arr)
    3
    >>> lz77(arr, summary=True)
    (3, [[0], [0, 1], [0, 1, 1]])
    """
    dot, ind = 1, 0
    history = [[int(arr[0])]]
    current = []

    while ind < len(arr) - 1:
        current.append(int(arr[ind + 1]))

        if current not in history:
            dot += 1
            history.append(current)
            current = []

        ind += 1

    if current:
        dot += 1
        history.append(current)

    if summary:
        return dot, history

    return dot


def _get_parser(parsing):
    parsers = {
        "lz76": lz76,
        "lz77": lz77,
    }

    try:
        return parsers[parsing]
    except KeyError as exc:
        msg = f"The parsing {parsing} is not implemented"
        raise NotImplementedError(
            msg
        ) from exc


def _complexity_from_phrases(dotcount, alphabet_length, sequence_length):
    """
    Return the normalized Lempel-Ziv score for a phrase count.
    """
    return float(
        dotcount * (np.log(dotcount) / np.log(alphabet_length) + 1.0) / sequence_length
    )


def lempel_ziv(seq, parsing="lz76", norm=False, nbsur=None):
    """
    Return the Lempel-Ziv complexity of a symbolic sequence.

    :param seq: A symbolic :class:`scyseq.sequence.Sequence`.
    :param parsing: Parsing name in ``["lz76", "lz77"]``.
    :param norm: If ``True``, normalize the raw score with surrogate sequences.
    :param nbsur: Number of surrogate sequences used for normalization.
    :returns: A float complexity score.

    :raises:
       :exc:`NotImplementedError` if ``parsing`` is not implemented.
       :exc:`ValueError` if ``norm`` is ``True`` and ``nbsur`` is not provided.

    >>> seq = S.Sequence(np.array([0, 0, 1, 0, 1, 1], dtype=np.uint8), 2)
    >>> lempel_ziv(seq)
    1.292481250360578
    >>> np.random.seed(123)
    >>> lempel_ziv(seq, norm=True, nbsur=5)
    0.0
    """
    algorithm = _get_parser(parsing)
    seqlen = len(seq)
    dotcount = algorithm(seq.ivals)
    lz_raw = _complexity_from_phrases(dotcount, seq.k, seqlen)

    if not norm:
        return lz_raw

    if nbsur is None:
        msg = "You should give the number of surrogate data"
        raise ValueError(msg)

    zero_ivals = np.zeros(seqlen, dtype=seq.ivals.dtype)
    c_min = algorithm(S.Sequence(zero_ivals, seq.k).ivals)
    c_max = max(
        algorithm(uniform_sequence(seqlen, alen=seq.k).ivals) for _ in range(nbsur)
    )
    lz_min = _complexity_from_phrases(c_min, seq.k, seqlen)
    lz_max = _complexity_from_phrases(c_max, seq.k, seqlen)

    return float((lz_raw - lz_min) / (lz_max - lz_min))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
