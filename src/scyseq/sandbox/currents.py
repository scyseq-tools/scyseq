import numpy as np

def probability_current(M, prob, retval="sum"):
    """
    Returns the current of probability either the matrix or the sum

    :param M: a transition matrix
    :param prob: a frequency vector
    :param retval: a string in `["sum", "matrix", "all"]` to decide whether
                   the sum, the matrix or both are computed.
    
    :returns: the matrix of probability currents or the sum or both in a
              tuple

    .. todo::
       Check the implementation see transition_matrix...

    .. todo::
       estimate the transition matrix for order > 1?
    """

    # prob = seq.frequency()
    preJ = np.multiply(M.T, prob).T
    J = preJ - preJ.T
    
    if retval == "matrix": return J
    elif retval == "sum": return np.sum(abs(J[np.isfinite(J)])) / 2.0
    elif retval == "all": return (J, np.sum(abs(J[np.isfinite(J)])) / 2.0)
    # entropy production see Jiang et al. 2004
    elif retval == "ep":
        # idx = np.logical_and(J>0., np.logical_not(np.isnan(J)))
        inter = np.multiply(J, np.log(preJ / (preJ.T)))
        return np.sum(inter[np.isfinite(inter)])/2
