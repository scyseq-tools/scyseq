import numpy as np
from scipy.stats import scoreatpercentile

import math
import itertools

from scyseq import sequence as S
from scyseq import algorithmic as A

def symbolize(arr, bins, d=None):
    """
    .. todo:: 
       is this funtion `symbolize` useful? (duplicate numpy.digitize?)
       Qu'est-ce que nbin ? Peut-être d ?

    """
    if np.any(arr < bins[0]):
        seq = np.digitize(arr, bins)
    else:
        seq = np.digitize(arr, bins) - 1

    alen = len(np.unique(seq))
    return S.Sequence(seq, alen)

def partition(arr, method='histogram', nbin=10, d=None):
    """
    Discretize a continuous series according to method.
    
    Methods are described in Hlavackova-Schindler et al. Physics Reports
    441 (2007) 1--46 pages 14--19

    method = 'histogram' 
       simple histogram method with equidistant binning

    method = 'marginal_equiquantization' 
       marginal equiquantization ie does its best to let equal number of
       observation in each bin. 

    :param x: a continuous series
    :param method: a string in `["histogram", "marginal_equiquantization"]`
    :param nbin: the number of bins ie the length of the alphabet
    :param d: a dictionary

    :raises:
       :exc:`NotImplementedError`  if method is not in the list above.

    :returns: A symbolic Sequence


    .. todo:: 
       To be completed with the other methods described in
       Hlavackova-Schindler (2007)

       Hint: look at R implementation of histogram function.

    Tests and examples of the functionnement of the module

    >>> x = np.linspace(0,10,11)
    >>> x 
    array([ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10.])
    >>> seq = partition(x, method='histogram', nbin=6)
    >>> seq
    Sequence: [0 0 1 1 2 3 3 4 4 5 5]
    Alphabet(Symbol(0 | 0), Symbol(1 | 1), Symbol(2 | 2), Symbol(3 | 3), Symbol(4 | 4), Symbol(5 | 5))
    N = 11 ; k = 6
    >>> seq = partition(x, method='marginal_equiquantization',nbin=6)
    >>> seq
    Sequence: [0 0 1 1 2 2 3 3 4 4 5]
    Alphabet(Symbol(0 | 0), Symbol(1 | 1), Symbol(2 | 2), Symbol(3 | 3), Symbol(4 | 4), Symbol(5 | 5))
    N = 11 ; k = 6

    """

    if (method == 'histogram'):
        lag = np.ptp(np.array(arr)) / float(nbin) # ptp: peak-to-peak=max-min
        bins = np.min(arr) + np.arange(nbin) * lag
        seq = np.digitize(arr, bins) - 1 # symbols between 0 and k-1

    elif (method == 'marginal_equiquantization'):
        bins = []
        lag = 100.0 / float(nbin-1)
        for pc in range(nbin):
            bins.append(scoreatpercentile(arr, per=pc*lag))
        seq = np.digitize(arr, np.array(bins)) -1

    else:
        raise NotImplementedError("The method is not impleneted")

    # return Sequence(s=S, k=nbin, d=d)
    return S.Sequence(seq, nbin)

def subdivision(data, iter_max):
    """
    Ulam method
    Adaptive subdivision technique based on:

    Set oriented numerical methods for dynamical systems
    Dellnitz M. and Junge O.  Handbook of dynamical systems vol. 2 p. 221-264
    Elsevier 2002.

    and 

    Numerical approximation of random attractors
    Keller H. and Ochs G. in "Stochastic dynamics" Crauel H. and Gundlach M. Eds
    Springer 1999. p. 93-115

    :input:

    ``x``: numpy array
    ``kmax``: integer, maximum number of boxes
    """
    # we consider that lines=time columns=dims ie. [line, col]
    nb_time, nb_dim = data.shape
    boxes = np.zeros(nb_time).astype(int)
    no_iter = 0
    refs = []
    mins = []
    maxs = []

    while no_iter < iter_max:
        box_indice = np.unique(boxes)
        nb_box = len(box_indice)
        # Step 0ne: split the boxes
        no_dim = no_iter % nb_dim
        lref = []
#       lmin = []
#       lmax = []

        for no_box in box_indice:

            databox = data[boxes==no_box, :]
            min_value = np.min(databox, axis=0)
            max_value = np.min(databox, axis=0)
            diameter = np.max(databox, axis=0) - min_value
            ref_value = min_value + diameter / 2.
            lref.append(ref_value[no_dim])

#           lmin.append(min_value[no_dim])
#           lmax.append(max_value[no_dim])

            bool_box = (databox > ref_value)[:, no_dim]
            boxes[boxes==no_box] += bool_box.astype(int) * 2**no_iter

        refs.append(lref)
#        mins.append(lmin)
#        maxs.append(lmax)
        no_iter += 1
    
#   return boxes, refs, mins, maxs
    return boxes, refs

def phase_cluster(data, nb_symb, target_dim=2):
    """
    This function provides the symbolic dynamic of a multivariate data It is
    based on the clusterisation of the "phase space" of the channels of MEG
    temporal signal 


    :param data: The input matrix, the lines are the channels and the columns
           are the time, must be an array

    :param nb_symb: The number of bins used for the clusterisation i.e. the
           number of symbols of the symbolic sequences that will be created

    :param nb_vp : The number of eigen vectors that we want to conserve to
           project our data on it

    """
    # SVD
    data = data.T
    U, Valeurs_propres, Vt = np.linalg.svd(data, full_matrices=False)
    reduced_data = np.dot(data, Vt[:target_dim, :].T)
    reduced_data = reduced_data.T

    # Partitionnage
    edges = np.histogramdd(reduced_data.T, bins= nb_symb)[1]

    #FIXME: this is not the place to compute entropy!!!
    
    # entropy_list = []

#    for i in range(len(reduced_data)):
#        edges[i][-1] = edges[i][-1] + 1
#        seq = np.digitize(reduced_data[i], edges[i]) - 1 # symbols between 0 and k-1
#        entropy_rate = A.lempel_ziv(S.Sequence(seq, nb_symb))
#        entropy_list.append(entropy_rate)

    # return np.array(entropy_list)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
