#-*- coding:Utf-8 -*-
"""
Defines stochastic matrices
"""
__docformat__ = 'reStructuredText'

import numpy as np
import numpy.testing as testing
# import warnings
import sequence as S

# warnings.simplefilter('always', RuntimeWarning)

def conditional_matrix(seq1, seq2):
    """
    Returns the conditional matrix ie P(s1=j | x2=i).

    This is estimated using the maximum likelihood estimator.

    :param seq1: a symbolic Sequence object
    :param seq2: a symbolic Sequence object

    :returns: A numpy.matrix of floats

    ..todo::

        check the doc and implementation of conditional_matrix

    NB: lines should sum to one (one should go somewhere) see
    markov_sequence in generate.py
    ie np.sum(matrix, axis=1) == [[1]...[1]]

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> np.random.seed(6)
    >>> b = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq1 = S.Sequence(a,A)
    >>> seq2 = S.Sequence(b,A)
    >>> conditional_matrix(seq1, seq2)
    [[0.71947674 0.28052326]
     [0.69551282 0.30448718]] [688 312]
    (array([], dtype=int64),)
    matrix([[0.71947674, 0.28052326],
            [0.69551282, 0.30448718]])
    """
    assert len(seq1) == len(seq2), 'Sequence should have the same length.'

    alen1 = seq1.k
    alen2 = seq2.k
    # slen = len(seq1)

    # Joint probabilities
    # x = seq1; y = seq2 and P(x|y) ie transition from y -> x (seq2 -> seq1)
    join_seq = S.recode([seq2, seq1])
    # Freq: (y0, x0) (y0, x1) ... (y0, xn) (y1, x0) ...
    # reshape: k2 rows and ordered by rows:
    # [(y0, x0) (y0, x1) ... (y0, xn) 
    #  (y1, x0) ...]
    p_join = np.reshape(join_seq.count(), (alen2, -1))

    # Marginal probabilities
    fq_marg = seq2.count()
    # freq: y0, y1, ... yn, y0, y1, ...  k1 times
    # reshape with k1 rows and ordered by rows:
    # [y0, y1, ... yn
    #  y0, y1, ... yn
    #  ...] so we need to transpose
    p_marg =  np.reshape(np.tile(fq_marg, alen1), (alen1, -1)).T
    # Borel-Kolmogorov paradox
    ind0 = np.where(p_marg == 0.)
    p_marg[ind0] = 1 # avoid divide by zero
    p_cond = p_join / p_marg
    print(p_cond, fq_marg)
    # set nulls -> nulls transitions / conditions = 1
    nulls = np.where(fq_marg==0.)
    # p_cond[nulls[0], nulls[0]] = 1
    print(nulls)
    p_cond[nulls] = 1
    testing.assert_allclose(np.sum(p_cond, 1), 1)

    # FIXME: add a warning for Borel-Kolmogorov paradox
    
    return np.matrix(p_cond)

def transition_matrix(seq, time=1):
    """
    Returns the transition matrix.

    This is estimated using the maximum likelihood estimator.

    :param seq: a symbolic Sequence object

    :returns: A numpy.matrix of floats

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq = S.Sequence(a,A)
    >>> transition_matrix(seq)
    [[0.70224719 0.29775281]
     [0.73519164 0.26480836]] [712 287]
    (array([], dtype=int64),)
    matrix([[0.70224719, 0.29775281],
            [0.73519164, 0.26480836]])
    """
    # Do not change: not tested (or write test...)
    return conditional_matrix(seq[time:], seq[:-time])

def influence_matrix(seq1, seq2, time=1):
    """
    Returns the influence matrix ie P(x1(T+t)=j | x2(T)=i).

    This is estimated using the maximum likelihood estimator.

    :param seq1: a symbolic Sequence object
    :param seq2: a symbolic Sequence object

    :returns: A numpy.matrix of floats

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> np.random.seed(6)
    >>> b = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq1 = S.Sequence(a,A)
    >>> seq2 = S.Sequence(b,A)
    >>> influence_matrix(seq1, seq2)
    [[0.70887918 0.29112082]
     [0.71794872 0.28205128]] [687 312]
    (array([], dtype=int64),)
    matrix([[0.70887918, 0.29112082],
            [0.71794872, 0.28205128]])
    """
    # Do not change: not tested (or write test...)
    return conditional_matrix(seq1[time:], seq2[:-time])

if __name__ == "__main__":
    import doctest
    doctest.testmod()