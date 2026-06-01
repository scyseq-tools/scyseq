# Copyright (c) 2007-2026 The scyseq developers.
# SPDX-License-Identifier: BSD-3-Clause BSD

"""
Generation of specified symbolic sequences
"""

import numpy as np

from scyseq.sequence import Sequence, boolean_alphabet

# Sequences generators
# =====================


def generate(method, N, k, *args):
    """
    Generates a Sequence according to a `method`


    :param method: a string in `["uniform", "markov", "binary_logistic"]`
    :type method: str

    :param N: the length of the sequence
    :type N: int

    :param k: the length of the alphabet
    :type k: int

    :param args: supplementary parameters (transition matrix and order for
           `"markov"` and parameter for `"binary_logisitic"`)

    :raises:
       :exc:`NotImplementedError` if `method` is not in the list above.

    :returns: A Sequence object.

    .. todo::
       Should we check the type of `N` and `k`

    .. todo::
       Deal with args more clearly (make a dict)?

    .. todo::
       should (N,k,d) be replaced by a dictionary dict(N=..., k=...,d=...)

    .. todo::
       Check NS code for cantor and cantor_id sequence

    .. todo::
       implement binary_tent, Gaussian, Poissonian, etc.??
    """
    if method.lower() == "uniform":
        return uniform_sequence(int(N), int(k))
    #    elif method.lower() == "cantor":
    #    elif method.lower() == "cantor_it"

    elif method.lower() == "markov":
        M = args[0]
        o = args[1]
        return markov_sequence(int(N), int(k), M, o)

    elif method.lower() == "binary_logistic":
        mu = args[0]
        xinit = args[1]
        return binary_logistic_sequence(int(N), mu, xinit)

    else:
        msg = f"The method {method} is not implemented."
        raise NotImplementedError(msg)


def uniform_sequence(length, alen):
    """
    Returns an uniform random sequence.

    :param N: the length of the sequence
    :param k: the length of the alphabet

    :returns: a Sequence object
    """
    return Sequence(
        np.random.randint(low=0, high=alen, size=length),
        alen,
        check=False,
    )


def binary_map1d_sequence(length, map1d, xinit, threshold=0.5, skip=100):
    """
    Returns a binary sequence with a specified one-dimensional map dynamics

    map1d can be specified such as: map1d = lambda x: 3.4 * x * (1 - x) or any
    function the defines x(t+1) as a function of x(t)

    :param N: the length of the sequence
    :param thresh: the threshold value to make a binary sequence

    :returns: A binary Sequence
    """
    seq = [xinit]
    for step in range(1, length + skip):
        seq.append(map1d(seq[step - 1]))
    bseq = np.array(seq[skip:]) > threshold

    return Sequence(bseq.astype(np.bool_), boolean_alphabet, check=False)


def binary_logistic_sequence(length, param, xinit, threshold=0.5, skip=100):
    """
    Returns a binary sequence with logistic dynamics according to the
    parameter :math:`\\mu`.

    The equation used here is: :math:`x(t+1) = \\mu x (1-x)`

    :param N: the length of the sequence
    :param mu: the paramter for the logistic equation
    :param thresh: the threshold value to make a binary sequence

    :returns: A binary Sequence
    """
    def logistic(x):
        return param * x * (1.0 - x)

    return binary_map1d_sequence(length, logistic, xinit, threshold, skip)


def markov_sequence(length, alen, markov_matrix, order):
    """
    Returns as sequence of a Markov process of order o with transition
    matrix M.

    :param N: the length of the sequence
    :param k: the length of the alphabet
    :param M: the transition matrix
    :param order: the order of the Markov process

    :raises:
       :exc:`ValueError`: if the shape of M does not correspond to the
       order of the process ie :math:`k^o \times k`

    :returns: A sequence object

    NB:

    - lines of Markov matrix give the probability to transition to one of the k
      symbols of the alphabet (so sum(markov_matrix[line] == 1)
      (ie np.sum(matrix, axis=1) == [[1]...[1]]
    """
    assert np.shape(markov_matrix) == (alen**order, alen), (
        "The shape of M does not match Markov process definition."
    )

    seq = list(np.random.randint(low=0, high=alen, size=order))

    for step in range(order, length):
        testval = np.random.uniform(0, 1)
        # encode previous Markov states (ie order previous symbols)
        prev_state = sum(seq[step - order : step] * alen ** np.arange(order))
        # cumulative probability
        cumprob = np.cumsum(markov_matrix[prev_state])
        # choose first symbol where cumprob > testval
        seq.append(np.where(cumprob > testval)[0][0])

    return Sequence(seq, alen, check=False)
