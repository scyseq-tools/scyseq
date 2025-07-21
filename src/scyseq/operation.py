"""
Definitions of operations some of which are just wrappers to sequences' methods.
"""

import copy
import numpy as np
from .sequence import Sequence, Alphabet, Symbol

def roll(seq, step):
    """
    Roll the sequence
    """
#    newseq = copy.deepcopy(seq)
#    newseq.roll(step)
    return seq.roll(step)

def reverse(seq):
    """
    Reverse the sequence
    """
#    newseq = copy.deepcopy(seq)
#    newseq.reverse()
    return seq.reverse()

def shuffle(seq):
    """
    Shuffle the sequence
    """
#    newseq = copy.deepcopy(seq)
#    newseq.shuffle()
    return seq.shuffle()

def reduce(seq):
    """
    Returns a reduced sequence (ie only keep the transitions)
    """
#    newseq = copy.deepcopy(seq)
#    newseq.reduce()
    return seq.reduce()

#def issequence(obj):
#    """
#    Returns True if x is a symbolic sequence
#    """
#    return isinstance(obj, Sequence) 

def transform(seq, correspondance, new_alphabet=None):
    """
    Transforms the initial sequence according to the correspondence iterable
    """
    if len(correspondance) != len(seq.alphabet):
        raise ValueError('Correspondence does not match sequence alphabet')

    # if (not all([type(c) is str for c in correspondance])) and \
       #(not all([type(c) is Symbol for c in correspondance])) and \
    if (not all([type(c) is int for c in correspondance])):
       # raise ValueError('Correspondences are strings, ints or Symbols.')
       raise ValueError('Correspondences are given as integers.')

    if new_alphabet is None:
        alphabet = Alphabet(list(set(correspondance)))
    else:
        if type(new_alphabet) is not Alphabet:
           raise E.AlphabetError('New alphabet should be an Alphabet object')
        elif len(set(correspondance)) != len(new_alphabet):
           raise 
           E.AlphabetError('Length of new alphabet does not fit the correspondance length.')
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

    .. todo::
        Write the doc of "words"
    """
    assert wlen > 0, 'Word length should be > 0.'
    slen = len(seq)
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

