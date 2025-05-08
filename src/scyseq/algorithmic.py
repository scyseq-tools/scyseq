"""
Algorithms and procedures related to algorithmic approach of complexity
"""
__docformat__ = 'reStructuredText'

import numpy as np
import sequence as S
from generator import uniform_sequence

def contains_sublist(lst, sublst):
    """
    Check wether a sublist appears in a list
    
    found at: http://stackoverflow.com/questions/3313590/...
    ... check-for-presence-of-a-sublist-in-python
   """
    sll = len(sublst) # sublist length
    return any((sublst == lst[i:i+sll]) for i in range(len(lst)-sll+1))

def lz76(arr, summary=False):
    """
    Returns Lempel-Ziv complexity according to LZ76 parsing.

    :param arr: an array of integers
    :param summary: A boolean (should the dictionary be returned)

    :returns: either an integer (`summary=False`) or a tuple
              (`summary=True`) with an integer and a list of strings.
    
    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> lz76(a)
    92
    """
    dot, ind = 1, 0
    history = [[int(arr[0])]]
    previous = [int(arr[0])]
    current = []

    while ind < len(arr)-1:

        current.append(int(arr[ind+1]))
        
        if not contains_sublist(previous, current):
            dot += 1
            history.append(current)
            previous.extend(current)
            current = []
        ind += 1

    if len(current) != 0:
        dot += 1
        history.append(current)

    if summary:
        return dot, history
    else:
        return dot

def lz77(arr, summary=False):
    """
    Returns Lempel-Ziv complexity according to LZ77 parsing.

    :param arr: an array of integers
    :param summary: A boolean (should the dictionary be returned)

    :returns: either an integer (`summary=False`) or a tuple
              (`summary=True`) with an integer and a list of strings.
    
    Example : 

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> lz77(a)
    158
    """
    dot, ind = 1, 0
    # need to convert into integers since if I keep np.int16 the test
    # Q in history does not work
    history = [[int(arr[0])]]
    current = []

    while ind < len(arr)-1:

        current.append(int(arr[ind+1]))
        
        if not current in history: 
            dot += 1
            history.append(current)
            current = []
        ind += 1 

    if len(current) != 0:
        dot += 1
        history.append(current)

    if summary:
        return dot, history
    else:
        return dot

def lempel_ziv(seq, parsing='lz76', norm=False, nbsur=None):
    """
    Returns the Lempel-Ziv normalized complexity using either lz76 or lz77
    parsing.

    :param seq: a Sequence object
    :param parsing: a string in `["lz76", "lz77"]`
    :param norm: a bolean (should the complexity be normalized?)
    :param ns: the number of surrogate data used in the normalization.

    :raise:
       :exc:`NotImplementedError` if `parsing` is not in the list above.

    :returns: a float (the Lempel-Ziv complexity)

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq = S.Sequence(a,A)
    >>> lempel_ziv(seq)
    0.6
    """
    try:
        algorithm = eval(parsing)
    except NameError:
        raise NotImplementedError("The parsing %s is not implemented" % parsing)

    seqlen = len(seq)
    dotcount = algorithm(seq.ivals)
    # (log(c)/log(k)) + 1  since we want log_k(c)
    lz_raw  = dotcount * (np.log(dotcount) / np.log(seq.k) + 1.) / seqlen

    if norm:
        if nbsur is None:
            raise ValueError('You should give the number of surrogate data')
        c_min  = algorithm(S.Sequence(np.zeros(seqlen), seq.k).ivals)
        c_max  = max([algorithm(uniform_sequence(seqlen, \
                                alen=seq.k).ivals) for i in range(nbsur)])
        lz_min = c_min * (np.log(c_min) / np.log(seq.k) + 1) / seqlen
        lz_max = c_max * (np.log(c_max) / np.log(seq.k) + 1) / seqlen
        return (lz_raw - lz_min) / (lz_max - lz_min)
    else:
        return lz_raw

if __name__ == "__main__":
    import doctest
    doctest.testmod()