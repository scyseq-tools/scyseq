import numpy as np

def _analyze_subdata(data):

    U, _s, V = np.linalg.svd(data)
    subdata = np.dot(data,V)[:,0]
    med = np.median(subdata)
    seqint = (subdata > med).astype(int)

    return seqint

def clustervar(data, itmax): # FIXME: find a good name
    """
    This program compute a clustering of the data, the method is inspired by
    the method of the singular values decomposition, show Carsten Allefeld and
    al. “Mental as macrostates emerging from brain dynamics”.

    :param it: number of iteration, number of cluster = 2^(number of
        iterations)

    :return: a list of length n=2^it, each items i of the outputlist
        contains every point who belongs at the cluster i 

    """
    data = np.array(data)
    data = data/float(np.linalg.norm(data))
    nbpts = np.shape(data)[0]
    seqint = np.zeros(nbpts).astype(int)

    for no_iter in range(itmax):
        for no_cluster in range(2**no_iter):
            subdata = data[seqint == no_cluster,:]
            seqint[seqint==no_cluster] += _analyze_subdata(subdata) * 2**no_iter

    return seqint

