"""
Definitions of operations on objects Sequence and Alphabet.

The object's methods are wrappers to these operations
"""

import copy
import itertools
import numpy as np

from .sequence import Sequence, Alphabet, Symbol
from . import exceptions as E

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
            raise TypeError ('The input must be a dictionary')

        if not all(isinstance(k, int) and isinstance(v, str)
                    for k, v in replacement.items()):
            raise E.AlphabetAccessError("Replacements should be {integer : string, ...}")

        if not len(set(replacement.values())) == len(replacement):
            raise E.AlphabetAccessError("Replacement values should all be different.")

        for k, v in replacement.items():
            # symbol.sval setter takes care of the unicity of the symbol in
            # the alphabet.
            obj[k].sval = v
#        return obj

    else:
        raise ValueError(f"Cannot rename an object of type {type(obj)}.")


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
        raise ValueError(f"Cannot roll from object of type {type(obj)}.")

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
        raise ValueError(f"Cannot roll from object of type {type(obj)}.")

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
        raise ValueError(f"Cannot roll from object of type {type(obj)}.")

def reduce(obj):
    """
    Returns a reduced sequence (ie Delete the repetitions of symbols in a sequence)

    >>> seq = Sequence([0, 0, 2, 2, 2, 0, 1, 1], 3)
    >>> reduce(seq).ivals.tolist()
    [0, 2, 0, 1]
    """
    if isinstance(obj, Sequence):
        diff = np.ediff1d(obj.ivals)
        bool_idx = list(diff!=0)
        bool_idx.append(True)
        reduced = obj.ivals[bool_idx]
        return Sequence(reduced, obj.alphabet)

    else:
        raise ValueError(f"Cannot reduce from object of type {type(obj)}.")


# Methods that compute characteristics of the sequence

def count(obj, value=None):
    """
    Counts the number of each symbol in :math:`{0, k-1}` if code is None
    or the number of the code symbol

    :returns: a numpy.ndarray of integers
    """
    if isinstance(obj, Sequence):
        if value is None:
            return np.array([np.sum(obj.ivals == i) for i in range(obj.k)])

        if isinstance(value, int):
            return np.sum(obj.ivals == value)

        if isinstance(value, str):
            return np.sum(obj.svals == value)

        raise ValueError("Value should be an integer or a string")
    else:
        raise ValueError(f"Cannot count from object of type {type(obj)}.")

def frequency(obj, value=None):
    """
    Returns the probability of each symbol in :math:`{0, k-1}`

    :returns: a numpy.ndarray of floats
    """
    if isinstance(obj, Sequence):
        return obj.count(value) / float(len(obj))
    else:
        raise ValueError(f"Cannot compute frequency from object of type {type(obj)}.")

def transform(seq, correspondance, new_alphabet=None):
    """
    Transforms the initial sequence according to the correspondence iterable

    >>> seq = Sequence([0, 2, 0, 1], 3)
    >>> transform(seq, [1, 0, 0]).ivals.tolist()
    [1, 0, 1, 0]
    >>> alphabet = Alphabet(['low', 'high'])
    >>> transformed = transform(seq, [1, 0, 0], alphabet)
    >>> transformed.alphabet.svals
    ('low', 'high')
    """
    if len(correspondance) != len(seq.alphabet):
        raise ValueError('Correspondence does not match sequence alphabet')

    # if (not all([type(c) is str for c in correspondance])) and \
       #(not all([type(c) is Symbol for c in correspondance])) and \

    if (not all([type(c) is int for c in correspondance])):
       # raise ValueError('Correspondences are strings, ints or Symbols.')
       raise ValueError('Correspondences are given as integers.')

    if new_alphabet is None:
        alphabet = Alphabet([str(i) for i in list(set(correspondance))])
    else:
        if type(new_alphabet) is not Alphabet:
           raise E.AlphabetError('New alphabet should be an Alphabet object')
        elif len(set(correspondance)) != len(new_alphabet):
           raise E.AlphabetError(
               'Length of new alphabet does not fit the correspondence length.'
           )
        else:
            alphabet = new_alphabet
    nb_symbols = len(alphabet)

    if all([type(c) is int for c in correspondance]):     
        # make sure that corresp is [0, k-1]
        # FIXME: make a better test... 
        if min(correspondance) != 0 or max(correspondance) != nb_symbols - 1:
             raise ValueError('Correspondence should be [0, k-1]') 

#    if new_alphabet is not None and len(set(correspondance)) != len(new_alphabet): 
# #        alphabet = Alphabet(new_alphabet) 
# #    if new_alphabet is not None and len(set(correspondance)) != len(new_alphabet): 
#        raise ValueError(\ 
#            'New alphabet and correspondence table do not match')     
# ivals = np.array([alphabet[idx]._ival for idx in seq.ivals]).astype(seq.ivals.dtype)

    ivals = [alphabet[correspondance[idx]].ival for idx in seq.ivals]

    return Sequence(np.array(ivals).astype(seq.ivals.dtype), alphabet) 

def recode(lseq, new_alphabet=False, sep='+', names=None):
    """
    Recodes a list of sequences with (possibly) different alphabets but
    with the same length (This is an error to pass Sequences with different
    length.) A new dictionnary is built for the new sequence.

    :param lseq: a list of Sequences

    :raises:
       :exc:`LengthError`: when the length of the Sequences are different.

    :returns: a Sequence

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
    if not all([len(seq) == len(lseq[0]) for seq in lseq]):
        raise E.LengthError("Sequence should have the same length") 

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
    if new_alphabet: # and all([type(alpha) is not int for alpha in alld]):

        if names is None:
            raise ValueError('Names should be the same length as lseq')
        else:
            alld = []
            for seq, name in zip(lseq, names):
                alld.append(['_'.join((name, anitem.sval)) for anitem in seq.alphabet])
#
        new_alphabet = []
        for pp in itertools.product(*alld):
            strlist = [jj for jj in pp]
            new_alphabet.append(sep.join(strlist))
#
        # return Sequence(new_s, new_alphabet, check=False)
        return Sequence(new_s, Alphabet(new_alphabet))#, check=False)
#
    else:
        # return Sequence(new_s, int(new_alen), check=False)
        return Sequence(new_s, Alphabet(int(new_k))) #, check=False)

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
        raise ValueError("Word length should be a positive integer.")
    if wlen <= 0:
        raise ValueError("Word length should be > 0.")

    slen = len(seq)
    if wlen > slen:
        raise ValueError("Word length should be <= sequence length.")

    lseq = [seq[i:slen-wlen+i+1] for i in range(wlen)]

    return recode(lseq, new_alphabet=new_alphabet)

#def from_iterable(val, valrange):
#    """
#    Map a set of values to symbolic coding (i.e. integers between 0 and k-1)
#    """
#    lrange = list(valrange)
#    symb = [lrange.index(tmp) for tmp in val]
#    return Sequence(symb, len(lrange))

#def visited_states(seq, sort=True):  #, meaning=True, complete=False, ordering=True):
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

