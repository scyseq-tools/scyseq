def coarse_grained_information(x, y, tau):
    """
    Computes the symmetric coarse grained information rate for 2 symbolic
    sequences 
    
    i(X,Y), according to tau (close to correlation time).  See
    Palus M., Phys. Rev. E, 2001.

    .. todo::

       check this function `coarse_grained_information`
    """ 
    N = len(x.s) 
    I =[]

    for i in range(1,tau+1):
        Xplus = Sequence(x.s[0:N-i], x.k)
        Yplus = Sequence(y.s[i:N],y.k)
        Xminus = Sequence(x.s[i:N],x.k) 
        Yminus = Sequence(y.s[0:N-i],y.k) 
        I.append(mutual_information(Xplus,Yplus))
        I.append(mutual_information(Xminus,Yminus))
    
    return  np.sum(I) / (2 * tau)


def coarse_grained_transinformation(x, y, tau):
    """
    Computes the asymmetric coarse grained transinformation rate for 2
    symbolic sequences.
    
    i(X|Y), according to tau (close to correlation
    time).  See Palus M., Phys. Rev. E, 2001.

    .. todo::
       check this function `coarse_grained_transinformation`
    """
    N = len(x.s)
    I =[]
    
    for i in range(1,tau+1):
        X = Sequence(x.s[0:N-i],x.k)
        X_tau = Sequence(x.s[i:N],x.k)
        Y = Sequence(y.s[0:N-i],y.k)
        I.append(multi_information(X,X_tau,Y)) # because i(X|Y) = i0(X|Y)-i(X) = sum[I(x;x_tau|y) - I(x;x_tau)]/tau = -sum[I(x;x_tau;y)]/tau

    return np.sum(I) / -tau

def block_mutual_information(x, y, n):
    """
    Computes the mutual information rate for symbolic sequences using the
    block entropie estimator         
    
    .. todo::
       check this function `block_mutual_information`
    """
    # FIXME: Explain this constants!!!!
    Hn1max = 6.9275 # computed on a N=10^5 random sequence Hn1XYmax = 1.145
    Hnmax = 6.236 
    HnXYmax = 11.27

    # Recode sequences x and y
    xy = recode([x,y], new_dict=False)
    
    #Block entropy
    Hnx = block_entropies(x, n)
    Hny = block_entropies(y, n)
    Hnxy = block_entropies(xy, n)
    # Block entropy order n+1
    Hn1x   = block_entropies(x, n+1)
    Hn1y   = block_entropies(y, n+1)
    #Hxn1yn = block_JointEntropy(x,y,n)
    #Hyn1xn = block_JointEntropy(y,x,n)
    Hn1xy = block_entropies(xy, n+1)
    
    #Normalization 
    Hnx = Hnx/Hnmax
    Hny = Hny/Hnmax
    Hnxy = Hnxy/HnXYmax
    Hn1x = Hn1x/Hn1max
    Hn1y = Hn1y/Hn1max
    Hn1xy = Hn1xy/Hn1XYmax
        #entropy rate
    hnx   = Hn1x  - Hnx
    hny   = Hn1y  - Hny 
    hnxy  = Hn1xy - Hnxy    
#block mutual information of order n
    In   = Hnx  + Hny  - Hnxy
    In1  = Hn1x + Hn1y - Hn1xy

    return In/n,In1-In,2*In/(Hnx + Hny),(In1-In)/(hnx+hny)

#def Block_MutualInformation(x, y, n):
#    """
#    .. warning::
#       Do not use this function: it will be deprecated
#
#    It is equivalent to::
#
#       block_mutual_information(x, y, n)
#    """
#    warnings.warn("Use block_mutual_information() instead", DeprecationWarning)
#    return block_mutual_information(x, y, n)

