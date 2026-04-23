"""
Defines stochastic matrices
"""

import numpy as np
import numpy.testing as testing
# import warnings

from . import sequence as S
from . import operations as O

# warnings.simplefilter('always', RuntimeWarning)

def conditional_matrix(dependent, conditioning, smooth=0):
    """
    Returns the conditional matrix ie P(y=j | x=i).

    P(x) = 0 is dealt with add-k smoothing:

    P(y | x) = (P(x,y) + k) / (P(x) + k * |Ay|)

    with |Ay| the alphabet length of the dependent sequence

    This is estimated using the maximum likelihood estimator.

    :param seq1: a symbolic Sequence object
    :param seq2: a symbolic Sequence object

    :returns: A numpy.array of floats

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
    array([[0.71947674, 0.28052326],
           [0.69551282, 0.30448718]])
    """
    dseq, cseq = dependent, conditioning
    assert len(dseq) == len(cseq), 'Sequence should have the same length.'
    if not isinstance(smooth, (int, float, np.integer)):
        raise ValueError(f"Smooth should be float or integer not {type(smooth)}")

# FIXME: Give a better exception
    if any(cseq.count() == 0) and smooth == 0:
        raise ValueError('Cannot compute conditional probabilities with null marginals and no smoothing')

    d_alen = dseq.k
    c_alen = cseq.k

    # Joint probabilities:
    # P(dseq | cseq) ie transition from conditioning -> dependent (cseq -> dseq)
    join_seq = O.recode([cseq, dseq]) #, new_alphabet=True, names=['From_', 'To_'])

#    # Freq: (cond0, dep0) (cond0, dep1) ... (cond0, depn) (cond1, dep0) ...
#    # reshape: c_alen rows and ordered by rows:
#    # [(cond0, dep0) (cond0, dep1) ... (cond0, depn) 
#    #  (cond1, dep0) ...]
    p_join = np.reshape(join_seq.count(), (c_alen, -1))

#    # Marginal probabilities
    fq_marg = cseq.count()
#    # freq: y0, y1, ... yn, y0, y1, ...  k1 times
#    # reshape with k1 rows and ordered by rows:
#    # [y0, y1, ... yn
#    #  y0, y1, ... yn
#    #  ...] so we need to transpose
    p_marg =  np.reshape(np.tile(fq_marg, d_alen), (d_alen, -1)).T

# Add-k smoothing
    p_cond = (p_join + smooth) / (p_marg + smooth * d_alen)
    testing.assert_allclose(np.sum(p_cond, 1), 1)
    return p_cond

#    ind0 = np.where(p_marg == 0.)
#    p_marg[ind0] = 1 # avoid divide by zero
#    p_cond = p_join / p_marg
#    # print(p_cond, fq_marg)
#    # set nulls -> nulls transitions / conditions = 1
#    nulls = np.where(fq_marg==0.)
#    # p_cond[nulls[0], nulls[0]] = 1
#    #print(nulls)
#    p_cond[nulls] = 1
#    print(p_cond)
#    testing.assert_allclose(np.sum(p_cond, 1), 1)
#
#    # FIXME: add a warning for P(x) = 0 and / or P(x,y)=0 P(y)=0
#    
#    return np.array(p_cond)

def transition_matrix(seq, time=1, smooth=0):
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
    array([[0.70224719, 0.29775281],
           [0.73519164, 0.26480836]])
    """
    # Do not change: not tested (or write test...)
    return conditional_matrix(seq[time:], seq[:-time], smooth=smooth)

def influence_matrix(seq1, seq2, time=1, smooth=0):
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
    array([[0.70887918, 0.29112082],
           [0.71794872, 0.28205128]])
    """
    # Do not change: not tested (or write test...)
    return conditional_matrix(seq1[time:], seq2[:-time], smooth=smooth)

