# Copyright (c) 2007-2026 The scyseq developers.
# SPDX-License-Identifier: BSD-3-Clause BSD

"""
Definitions of operations on objects Sequence and Alphabet.

The object's methods are wrappers to these operations
"""

import copy
import itertools

import numpy as np

from scyseq import exceptions as E
from scyseq.sequence import Alphabet, Sequence


def rename(obj, replacement):
    """
    To rename **in place** symbols in an alphabet or a sequence, pass a
    dictionary with integers as keys and strings as values so that the
    replacement of ivals and svals are explicit.

    :param replacement: The dictionary which describes the replacement.
    :type  replacement: dict

    >>> alpha_d = Alphabet(['a','b','c', 'd'])
    >>> alpha_d
    Alphabet(Symbol(0 | a), Symbol(1 | b), Symbol(2 | c), Symbol(3 | d))
    >>> alpha_d.rename({1: 'One', 3: 'Three'})
    >>> alpha_d
    Alphabet(Symbol(0 | a), Symbol(1 | One), Symbol(2 | c), Symbol(3 | Three))

    The replacement variable should be a valid replacement candidate. So exceptions
    are raised if:

    >>> alpha_d.rename(['bad1', 'bad2', 'bad3']) # not a dictionary
    Traceback (most recent call last):
    ...
    TypeError: The input must be a dictionary

    >>> alpha_d.rename({'bad1': 'bad2', 'bad3': 'bad4'}) # not {int : str}
    Traceback (most recent call last):
    ...
    scyseq.exceptions.AlphabetAccessError: Replacements should be {integer : string, ...}

    >>> alpha_d.rename({0: 'bad0', 1: 'bad0'}) # values are not different
    Traceback (most recent call last):
    ...
    scyseq.exceptions.AlphabetAccessError: Replacement values should all be different.

    >>> alpha_d.rename({0: 'Three'}) # values already exists
    Traceback (most recent call last):
    ...
    scyseq.exceptions.AlphabetAccessError: Symbol 'Three' already exists in alphabet

    """
    if isinstance(obj, Sequence):
        rename(obj.alphabet, replacement)

    #       return Sequence(obj.ivals, rename(obj.alphabet, replacement))

    elif isinstance(obj, Alphabet):
        if not isinstance(replacement, dict):
            msg = "The input must be a dictionary"
            raise TypeError(msg)

        if not all(
            isinstance(k, int) and isinstance(v, str) for k, v in replacement.items()
        ):
            msg = "Replacements should be {integer : string, ...}"
            raise E.AlphabetAccessError(
                msg
            )

        if len(set(replacement.values())) != len(replacement):
            msg = "Replacement values should all be different."
            raise E.AlphabetAccessError(msg)

        for k, v in replacement.items():
            # symbol.sval setter takes care of the unicity of the symbol in
            # the alphabet.
            obj[k].sval = v
    #        return obj

    else:
        msg = f"Cannot rename an object of type {type(obj)}."
        raise ValueError(msg)


def roll(obj, step):
    """
    Roll the sequence

    >>> seq = Sequence([0, 1, 2, 0, 1], 3)
    >>> roll(seq, 2).ivals.tolist()
    [0, 1, 0, 1, 2]
    """

    if isinstance(obj, Sequence):
        return Sequence(np.roll(obj.ivals, step), obj.alphabet)
    else:
        msg = f"Cannot roll from object of type {type(obj)}."
        raise ValueError(msg)


def reverse(obj):
    """
    Reverse the sequence

    >>> seq = Sequence([0, 1, 2, 0, 1], 3)
    >>> reverse(seq).ivals.tolist()
    [1, 0, 2, 1, 0]
    """
    if isinstance(obj, Sequence):
        return Sequence(np.flipud(obj.ivals), obj.alphabet)
    else:
        msg = f"Cannot roll from object of type {type(obj)}."
        raise ValueError(msg)


def shuffle(obj):
    """
    Shuffle the sequence

    >>> seq = Sequence([0, 1, 2, 0, 1], 3)
    >>> shuffled = shuffle(seq)
    >>> sorted(shuffled.ivals.tolist())
    [0, 0, 1, 1, 2]
    >>> seq.ivals.tolist()
    [0, 1, 2, 0, 1]
    """
    if isinstance(obj, Sequence):
        tmp = copy.copy(obj.ivals)
        np.random.shuffle(tmp)
        return Sequence(tmp, obj.alphabet)
    else:
        msg = f"Cannot roll from object of type {type(obj)}."
        raise ValueError(msg)


def reduce(obj):
    """
    Returns a reduced sequence (ie Delete the repetitions of symbols in a sequence)

    >>> seq = Sequence([0, 0, 2, 2, 2, 0, 1, 1], 3)
    >>> reduce(seq).ivals.tolist()
    [0, 2, 0, 1]
    """
    if isinstance(obj, Sequence):
        diff = np.ediff1d(obj.ivals)
        bool_idx = list(diff != 0)
        bool_idx.append(True)
        reduced = obj.ivals[bool_idx]
        return Sequence(reduced, obj.alphabet)

    else:
        msg = f"Cannot reduce from object of type {type(obj)}."
        raise ValueError(msg)


# Methods that compute characteristics of the sequence


def count(obj, value=None):
    """
    Counts the number of each symbol in :math:`{0, k-1}` if code is None
    or the number of the code symbol.

    Parameters
    ----------
    obj : Sequence
        The sequence object to count symbols in.
    value : int or str, optional
        The specific symbol value to count. If None, counts all symbols.

    Returns
    -------
    numpy.ndarray or int
        An array of counts for each symbol, or a single integer count if value is provided.
    """
    if isinstance(obj, Sequence):
        if value is None:
            return np.array([np.sum(obj.ivals == i) for i in range(obj.k)])

        if isinstance(value, int):
            return np.sum(obj.ivals == value)

        if isinstance(value, str):
            return np.sum(obj.svals == value)

        msg = "Value should be an integer or a string"
        raise ValueError(msg)
    else:
        msg = f"Cannot count from object of type {type(obj)}."
        raise ValueError(msg)


def frequency(obj, value=None):
    """
    Returns the probability of each symbol in :math:`{0, k-1}`.

    Parameters
    ----------
    obj : Sequence
        The sequence object.
    value : int or str, optional
        The specific symbol value to find the probability of. If None, computes probabilities for all symbols.

    Returns
    -------
    numpy.ndarray or float
        An array of floats representing probabilities, or a single float if value is provided.
    """
    if isinstance(obj, Sequence):
        return obj.count(value) / float(len(obj))
    else:
        msg = f"Cannot compute frequency from object of type {type(obj)}."
        raise ValueError(msg)


def transform(seq, correspondance, new_alphabet=None):
    """
    Transforms the initial sequence according to the correspondence iterable.

    Parameters
    ----------
    seq : Sequence
        The sequence to transform.
    correspondance : iterable
        A list or array representing correspondence to transfer current symbols.
    new_alphabet : Alphabet, optional
        A new alphabet obj to use for the transformed sequence.

    Returns
    -------
    Sequence
        The new mathematically transformed Sequence.

    Example
    -------

    >>> seq = Sequence([0, 2, 0, 1], 3)
    >>> transform(seq, [1, 0, 0]).ivals.tolist()
    [1, 0, 1, 0]
    >>> alphabet = Alphabet(['low', 'high'])
    >>> transformed = transform(seq, [1, 0, 0], alphabet)
    >>> transformed.alphabet.svals
    ('low', 'high')
    """
    if len(correspondance) != len(seq.alphabet):
        msg = "Correspondence does not match sequence alphabet"
        raise ValueError(msg)

    # if (not all([type(c) is str for c in correspondance])) and \
    # (not all([type(c) is Symbol for c in correspondance])) and \

    if not all(type(c) is int for c in correspondance):
        # raise ValueError('Correspondences are strings, ints or Symbols.')
        msg = "Correspondences are given as integers."
        raise ValueError(msg)

    if new_alphabet is None:
        alphabet = Alphabet([str(i) for i in list(set(correspondance))])
    elif type(new_alphabet) is not Alphabet:
        msg = "New alphabet should be an Alphabet object"
        raise E.AlphabetError(msg)
    elif len(set(correspondance)) != len(new_alphabet):
        msg = "Length of new alphabet does not fit the correspondence length."
        raise E.AlphabetError(
            msg
        )
    else:
        alphabet = new_alphabet
    nb_symbols = len(alphabet)

    if all(type(c) is int for c in correspondance):
        # make sure that corresp is [0, k-1]
        # FIXME: make a better test...
        if min(correspondance) != 0 or max(correspondance) != nb_symbols - 1:
            msg = "Correspondence should be [0, k-1]"
            raise ValueError(msg)

    #    if new_alphabet is not None and len(set(correspondance)) != len(new_alphabet):
    # #        alphabet = Alphabet(new_alphabet)
    # #    if new_alphabet is not None and len(set(correspondance)) != len(new_alphabet):
    #        raise ValueError(\
    #            'New alphabet and correspondence table do not match')
    # ivals = np.array([alphabet[idx]._ival for idx in seq.ivals]).astype(seq.ivals.dtype)

    ivals = [alphabet[correspondance[idx]].ival for idx in seq.ivals]

    return Sequence(np.array(ivals).astype(seq.ivals.dtype), alphabet)


def recode(lseq, new_alphabet=False, sep="+", names=None):
    """
    Recodes a list of sequences with (possibly) different alphabets but
    with the same length (This is an error to pass Sequences with different
    length.) A new dictionnary is built for the new sequence.

    Parameters
    ----------
    lseq : list
        A list of Sequence objects.
    new_alphabet : bool, optional
        Whether to generate a new alphabet instead of integers, defaults to False.
    sep : str, optional
        Separator to use if new_alphabet is True, defaults to '+'.
    names : list, optional
        Optional names for the new alphabets.

    Raises
    ------
    LengthError
        When the length of the Sequences are different.

    Returns
    -------
    Sequence
        A newly recoded Sequence object.

    Example
    -------

    >>> seq_a = Sequence([0, 0, 1, 1], 2)
    >>> seq_b = Sequence([0, 1, 0, 1], 2)
    >>> recoded = recode([seq_a, seq_b])
    >>> recoded.ivals.tolist()
    [0, 1, 2, 3]
    >>> recoded.k
    4
    >>> named = recode([seq_a, seq_b], new_alphabet=True, names=['x', 'y'])
    >>> named.alphabet.svals
    ('x_0+y_0', 'x_0+y_1', 'x_1+y_0', 'x_1+y_1')
    """
    if not all(len(seq) == len(lseq[0]) for seq in lseq):
        msg = "Sequence should have the same length"
        raise E.LengthError(msg)

    # The alphabet size of the recoded sequence is an extension of the alphabet
    # within the original sequences list. This is equivalent to numbering
    # items in n-dimensional (n=nbseq) tables each dimension has k cases.
    # The convention: we use the lexicographic order from left to right; the
    #    # highest weight is on the left (ie index 0) the lower on the right (ie
    #    # index -1)
    #
    #    allk = [seq._alen for seq in lseq]
    allk = [seq.k for seq in lseq]
    #    new_alen = np.prod(allk)
    new_k = np.prod(allk)
    #
    #    # recode each word as an integer as a matrix product of the matrix of
    #    # the sequences and a kernel
    symbolic_matrix = np.vstack([seq.ivals for seq in lseq]).T
    allk.reverse()
    kernel = np.cumprod(allk)
    kernel = np.flipud(np.insert(kernel[:-1], 0, 1))
    new_s = np.dot(symbolic_matrix, kernel).astype(int)
    #
    #    # construction of the new alphabet
    if new_alphabet:  # and all([type(alpha) is not int for alpha in alld]):
        if names is None:
            msg = "Names should be the same length as lseq"
            raise ValueError(msg)
        else:
            alld = []
            for seq, name in zip(lseq, names):
                alld.append([f"{name}_{anitem.sval}" for anitem in seq.alphabet])
        #
        new_alphabet = []
        for pp in itertools.product(*alld):
            strlist = list(pp)
            new_alphabet.append(sep.join(strlist))
        #
        # return Sequence(new_s, new_alphabet, check=False)
        return Sequence(new_s, Alphabet(new_alphabet))  # , check=False)
    #
    else:
        # return Sequence(new_s, int(new_alen), check=False)
        return Sequence(new_s, Alphabet(int(new_k)))  # , check=False)


def words(seq, wlen, new_alphabet=False):
    """
    Returns a sequence encoded according to the m-words in seq

    >>> seq = Sequence([0, 0, 1, 1, 0], 2)
    >>> word_seq = words(seq, 2)
    >>> word_seq.ivals.tolist()
    [0, 1, 3, 2]
    >>> word_seq.k
    4
    """
    if not isinstance(wlen, (int, np.integer)):
        msg = "Word length should be a positive integer."
        raise ValueError(msg)
    if wlen <= 0:
        msg = "Word length should be > 0."
        raise ValueError(msg)

    slen = len(seq)
    if wlen > slen:
        msg = "Word length should be <= sequence length."
        raise ValueError(msg)

    lseq = [seq[i : slen - wlen + i + 1] for i in range(wlen)]

    return recode(lseq, new_alphabet=new_alphabet)


# def from_iterable(val, valrange):
#    """
#    Map a set of values to symbolic coding (i.e. integers between 0 and k-1)
#    """
#    lrange = list(valrange)
#    symb = [lrange.index(tmp) for tmp in val]
#    return Sequence(symb, len(lrange))

# def visited_states(seq, sort=True):  #, meaning=True, complete=False, ordering=True):
#    """
#    Returns the set of visited symbols ie those that really appear in
#    the sequence.
#
#    :returns: a numpy.ndarray of integers
#
#    .. todo::
#       should we had frequencies, etc?
#
#    .. todo::
#       should we return a sequence, with alphabet?
#    """
#    freq = S.frequency()
#    # alph_ivals = seq.alphabet.ivals
#    # alph_svals = seq.alphabet.svals
#    alphabet = seq.alphabet
#    if sort:
#        lsort = list(np.argsort(freq))
#        lsort.reverse() # decreasing order *in place*!!!!
#        # FIXME: lsort elements have type numpy.int64 which is not directly usable for
#        # indexing Alphabet. See the __index__ method for that.
#        # so here is a local hack which might be generalized if needed...
#        # return [(alph_ivals[idx], freq[idx], alph_svals[idx]) for idx in lsort]
#        indices = [int(i) for i in lsort]
#        return [(alphabet[idx], freq[idx]) for idx in indices]
#    else:
#        return list(zip(alphabet, freq))
#
#    # alpha = list(range(seq.alen))
##    if seq.alphabet is None:
##        return [(alpha[index], frequencies[index], None) for index in lsort]
##    else:
##        return [(alpha[index], frequencies[index], seq.alphabet[index]) \
##                for index in lsort]
