def stationary_bootstrap(seq, p):
    """
    Returns a sequence using the stationary bootstrap method.

    :param seq: A Sequence
    :param p: probability

    :raises:
       :exc:`ValueError`: if p is not in :math:`[0.,1.]`.

    :returns: A Sequence

    .. todo::
       Explain the exact meaning of p 

    See Politis D.N. and Romano J.P. (1994) "The stationary bootstrap"
    *Journal of the American Statistical Association* **89** (428):1303-1313.
    """
    if (p>1.) or (p<0): 
        raise ValueError("A probability (p) needs to be between 0. and 1." )

    N = len(seq)
    new_seq = list(seq.s)
    Xstar = []

    while len(Xstar) < N:
        I = np.random.randint(0, N) 
        L = np.random.geometric(p) 
        Xstar += new_seq[I:min(N, I+L)]

    return Sequence(Xstar[0:N], either(seq.k, seq.d), check=False)

def shuffle_surrogates(seq):
    """
    Shuffle
    """
    surrogate = copy.deepcopy(seq)
    return surrogate

def surrogate_set(seq, method, ns, *args):
    """
    Returns a list of `ns` surrogate sequences using `method`

    :param seq: a Sequence object
    :param method: a string in `["shuffle", "stationary_bs"]`
    :param ns: the number of surrogate
    :type ns: int
    :param args: more parameters for the functions that are called

    :raises:
       :exc:`NotImplementedError`: if method is not in the list above.

    :returns: a list of sequences

    .. todo::
       Deal with the extra parameters in a more elegant/standard way.
    """
    if method == 'shuffle':
        return [shuffle(seq) for i in xrange(ns)]

    elif method == 'stationary_bs':
        try:
            p = args[0]
        except:
            raise ValueError("method stationary_bs needs a probability parameter.")
        return [stationary_bs(seq, p) for i in xrange(ns)]

    else:
        raise NotImplementedError("The surrogate method is unavailable")

#def stationary_surrogate_set(seq, p, ns=100):
#    """
#    .. warning::
#       Do not use this function it will be deprecated.
#
#    It is equivalent to::
#       
#       surrogate_set(seq, method='stationary_bs', ns=ns, args=(p,))
#    """
#    warnings.warn("Use surrogate_set(method='stationary_bs'...)", DeprecationWarning)
#    return surrogate_set(seq, method='stationary_bs', ns=ns, args=(p,))
#
