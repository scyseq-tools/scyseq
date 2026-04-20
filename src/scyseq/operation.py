"""
Definitons of operations some of which are just wrappers to sequences' methods.
"""

import itertools

import numpy as np

from . import exceptions as E
from .sequence import Alphabet, Sequence

def roll(seq, step):
    """
    Roll the sequence

    >>> seq = Sequence([0, 1, 2, 0, 1], 3)
    >>> roll(seq, 2).ivals.tolist()
    [0, 1, 0, 1, 2]
    """
    return seq.roll(step)

def reverse(seq):
    """
    Reverse the sequence

    >>> seq = Sequence([0, 1, 2, 0, 1], 3)
    >>> reverse(seq).ivals.tolist()
    [1, 0, 2, 1, 0]
    """
    return seq.reverse()

def shuffle(seq):
    """
    Shuffle the sequence

    >>> seq = Sequence([0, 1, 2, 0, 1], 3)
    >>> shuffled = shuffle(seq)
    >>> sorted(shuffled.ivals.tolist())
    [0, 0, 1, 1, 2]
    >>> seq.ivals.tolist()
    [0, 1, 2, 0, 1]
    """
    shuffled = np.array(seq.ivals, copy=True)
    np.random.shuffle(shuffled)

    return Sequence(shuffled, seq.alphabet, check=False)

def reduce(seq):
    """
    Returns a reduced sequence (ie only keep the transitions)

    >>> seq = Sequence([0, 0, 2, 2, 2, 0, 1, 1], 3)
    >>> reduce(seq).ivals.tolist()
    [0, 2, 0, 1]
    """
    return seq.reduce()

#def issequence(obj):
#    """
#    Returns True if x is a symbolic sequence
#    """
#    return isinstance(obj, Sequence) 

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
    if not all(isinstance(c, (int, np.integer)) for c in correspondance):
       # raise ValueError('Correspondences are strings, ints or Symbols.')
       raise ValueError('Correspondences are given as integers.')

    correspondance = [int(c) for c in correspondance]
    nb_symbols = len(set(correspondance))

    # make sure that corresp is [0, k-1]
   
    if min(correspondance) != 0 or max(correspondance) != nb_symbols - 1:
         raise ValueError('Correspondence should be [0, k-1]')

    if new_alphabet is None:
        alphabet = Alphabet(nb_symbols)
    else:
        if type(new_alphabet) is not Alphabet:
           raise E.AlphabetError('New alphabet should be an Alphabet object')
        elif len(set(correspondance)) != len(new_alphabet):
           raise E.AlphabetError(
               'Length of new alphabet does not fit the correspondance length.'
           )
        else:
            alphabet = new_alphabet

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
        return Sequence(new_s, Alphabet(new_alphabet), check=False)
#
    else:
        # return Sequence(new_s, int(new_alen), check=False)
        return Sequence(new_s, Alphabet(int(new_k)), check=False)

def words(seq, wlen, new_alphabet=False):
    """
    Returns a sequence encoded according to the m-words in seq

    >>> seq = Sequence([0, 0, 1, 1, 0], 2)
    >>> word_seq = words(seq, 2)
    >>> word_seq.ivals.tolist()
    [0, 1, 3, 2]
    >>> word_seq.k
    4

    .. todo::
        Write the doc of "words"
    """
    if not isinstance(wlen, (int, np.integer)):
        raise ValueError("Word length should be a positive integer.")

    if wlen <= 0:
        raise ValueError("Word length should be > 0.")
    if wlen > len(seq):
        raise ValueError("Word length should be <= sequence length.")

    slen = len(seq)
    lseq = [seq[i:slen-wlen+i+1] for i in range(wlen)]

    return recode(lseq, new_alphabet=new_alphabet)

