import numpy as np
from scikits.symbolic.stochastic import transition_matrix

def probability_current(seq, M=None, retval="sum"):

    # SEE Also sandbox/currents.py

    """
    Returns the current of probability either the matrix or the sum

    :param seq: a symbolic Sequence object
    :param M: a transition matrix
    :param retval: a string in `["sum", "matrix", "all"]` to decide whether
                   the sum, the matrix or both are computed.
    
    :returns: the matrix of probability currents or the sum or both in a
              tuple

    .. todo::
       Check the implementation see transition_matrix...

    .. todo::
       estimate the transition matrix for order > 1?
    """
    if M == None:
        M = transition_matrix(seq)

#    print M
#    raw_input()
    # FIXME:
    # M[np.isnan(M)] = 0.

    p = seq.frequency()
    preJ = np.multiply(M.T, p).T
    J = preJ - preJ.T
    
    if retval == "matrix": return J
    elif retval == "sum": return np.sum(abs(J[np.isfinite(J)])) / 2.0
    elif retval == "all": return (J, np.sum(abs(J[np.isfinite(J)])) / 2.0)
    # entropy production see Jiang et al. 2004
    elif retval == "ep":
        # idx = np.logical_and(J>0., np.logical_not(np.isnan(J)))
        inter = np.multiply(J, np.log(preJ / (preJ.T)))
#        print J
#        print np.log(preJ / preJ.T)
#        print inter
#        raw_input()
#        print preJ / (preJ.T)
#        print inter
#        raw_input()
        return np.sum(inter[np.isfinite(inter)])/2


#(NS) def courant_proba(seq): 
#    if seq.M=="none":
#	seq.M=seq.transitions()
#    if seq.P=="none":
#	seq.P=seq.Pr()
#    v=range(len(seq.P))
#    a=0
#    for i in v:
#	for j in v:
#       	    a=a+abs(seq.P[i]*seq.M[i][j]-seq.P[j]*seq.M[j][i])
#    return a/2.0

#def transitions(seq):
#    """
#    .. warning::
#       Do not use this function it will be deprecated
#
#    It is equivalent to::
#
#      return transition_matrix(seq), probability_current(seq, retval="sum")
#    """
#    warnings.warn("Use transition_matrix and probability_current instead", DeprecationWarning)
#
#    M = transition_matrix(seq)
#    J = probability_current(seq, retval="sum")
#    return M, J

def correl(x, s):
    """
    Computes the correlation function for a sequence.
    Note that it deals with symbols so that correlation for words should first
    recode the sequence according to words.

    .. todo::
       Check this function with  `Autocorr`
    """
    k = x.k
    N = len(x)
    Tmax = N/2
    fTmax = float(Tmax)
    C = []
    
    for t in range(Tmax):

        dsx = (x.s[0:Tmax] == s)
        dsxt = (x.s[t:t+Tmax] == s)
        dd = dsx * dsxt
	mdsx = np.sum(dsx)/fTmax
	mdsxt = np.sum(dsxt)/fTmax
	mdd = np.sum(dd)/fTmax
	#Cov = mdd - mdsx * mdsxt
	Cov = mdd - mdsx**2
	C.append(Cov)
 
    return np.array(C)

def Autocorr(x, s):
    """
    Computes the Autocorrelation function for a sequence.
    Note that it deals with symbols so that correlation for words should first
    recode the sequence according to words.
    
    .. todo::
       Check this function with  `correl`
    """
    k = x.k
    N = len(x)
    Tmax = N/2
    fTmax = float(Tmax)
    C = []
    
    for t in range(Tmax):

        dsx = x.s[t]
        dsxt = x.s[t:t+Tmax]
        dd = dsx * dsxt
	mdsx = np.sum(dsx)/fTmax
	mdsxt = np.sum(dsxt)/fTmax
	mdd = np.sum(dd)/fTmax
	#Cov = mdd - mdsx * mdsxt
	Cov = mdd - mdsx**2
	C.append(Cov)
	
    return np.array(C)

#(NS) def markov_autocorrelation(tau,a,b):
#	"""a=nprand.random()
#	b=nprand.random()
#	print a,b"""
#	L=np.exp(-1.0/tau)
#	return np.array([[(a+L*b)/(a+b),1-(a+L*b)/(a+b)],[a*(1-L)/(a+b),1-a*(1-L)/(a+b)]])
#	#return np.array([[a+L*b,b*(1.0-L)/(a+b)],[a*(1-L)/(a+b),(a*L+b)/(a+b)]])

