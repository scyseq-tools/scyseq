"""
This module contains the functions for symbolic recurrence plots quantification.

Some references are:

Faure and Lesne (2010) Recurrence plots for symbolic sequence. International
Journal of Bifurcation and Chaos

Zou et al. (2015) Identifying coupling directions by recurrences. In Recurrence
Quantification Analysis.
"""

import numpy as np

# import scipy.spatial.distance as spdist
import warnings
import copy


# def mwords_recurrence(seq_tuple):
#    """
#    Compute recurrence plot for m-words
#
#    See:
#
#    Faure Ph. and Lesne A. (2009) Recurrence plot for symbolic sequence.
#
#    .. todo::
#
#        Make the doc for recurrence plots
#    """
#    if len(seq_tuple) == 1:
#        seq1 = seq2 = seq_tuple[0]
#        N = len(seq1)
#
#    elif len(seq_tuple) == 2:
#        seq1, seq2 = seq_tuple
#        if len(seq1) != len(seq2):
#            raise ValueError("Sequences should have the same length")
#        else:
#            N = len(seq1)
#
#    else:
#        raise ValueError("Cannot make recurrence plot of more than 2 sequences")
#    # x = np.vstack((seq1.svalues,seq2.svalues))
#    x = np.vstack((seq1.ivals,seq2.ivals))
#    # print(x.shape)
#    dist = spdist.squareform(spdist.pdist(x.T))
#    return np.array(dist==0).astype(int)


def recurrence(seq):
    """
    Compute a recurrence plot for the given sequence.

    Parameters
    ----------
    seq : Sequence
        The input symbolic sequence to calculate recurrence for.

    Returns
    -------
    numpy.ndarray
        A 2D array representing the recurrence plot.
    """
    return np.equal.outer(seq.ivals, seq.ivals).astype(int)


#    # x = np.vstack((seq.svalues,seq.svalues))
#    x = np.vstack((seq.ivals, seq.ivals))
#    # print x.shape
#    # FIXME: test if other distance are quicker?
#    dist = spdist.squareform(spdist.pdist(x.T))
#    return np.array(dist==0).astype(int)


def joint_recurrence(x, y):
    assert len(x) == len(y)
    rpx = recurrence(x)
    rpy = recurrence(y)
    return rpx * rpy


def mean_conditional_recurrence(x, y):
    assert len(x) == len(y)
    N = len(x)
    rpx = recurrence(x)
    rpy = recurrence(y)
    rpxy = rpx * rpy
    N = len(x)
    sxy = np.sum(rpxy, axis=0)
    sy = np.sum(rpy, axis=0)

    return np.sum(sxy.astype(float) / sy.astype(float)) / float(N)


mcr = mean_conditional_recurrence


def diagonal_distribution(rp):

    n0, n1 = np.shape(rp)
    assert n0 == n1
    N = n0
    # mrp = 1 - rp
    HD = []
    ct = 0

    for i in range(N):
        for l in range(N - i):
            if rp[i + l, l] == 0:
                HD.append(ct)
                ct = 0
            else:
                ct += 1
                # rp[i+l, l] = 3
            # print(i+l, l, rp[i+l,l], HD)
    HD.append(ct)

    return np.array([HD.count(i) for i in range(1, N)])  # last elt = 1


def recurrence_rate(rp):
    n0, n1 = np.shape(rp)
    assert n0 == n1
    N = n0
    crp = copy.deepcopy(rp)
    np.fill_diagonal(crp, 0)

    return np.sum(crp) / (N**2 - N)


def synchronization_likelihood(x, y):
    # equivalent to recurrence rate of joint recurrence plot
    cr = joint_recurrence(x, y)
    return recurrence_rate(cr)


def determinism(rp, dmin=2):
    dd = diagonal_distribution(rp)[dmin - 1 :]
    lvec = np.arange(dmin, len(dd) + dmin)

    return np.sum(lvec * dd) / np.sum(rp)


def max_line_length(rep):
    dd = diagonal_distribution(rp)
    lvec = np.arange(1, len(dd) + 1)
    idx = np.which(dd != 0)

    return lvec[idx]


def diagonal_entropy(rp, dmin=2):
    dd = diagonal_distribution(rp)[dmin - 1 :]
    prob = dd / np.sum(dd)

    return -np.sum(prob[prob > 0] * np.log(prob[prob > 0]))
