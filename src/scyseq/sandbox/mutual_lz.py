"""
.. todo::

    Code conditinal parsing see Ziv and Merhav IEEE Trans. Inf. Theory vol
    39 1993
"""
def mutual_lempel_ziv(x, y, parsing="lz76", norm=False, ns=None):
    """
    Computes the mutual information rate for symbolic sequences using LZ
    complexity estimator

    .. todo::
       Check this function (mutual_lempal_ziv)
    """
    xy = recode([x,y], new_dict=False)
    # FIXME: choose the normalization here also
    lz_x   =  lempel_ziv(x, parsing=parsing)
    lz_y   =  lempel_ziv(y, parsing=parsing)
    lz_xy  =  lempel_ziv(xy, parsing=parsing)

    #Normalization
# FIXME: the normalization can be done outside this function
    if norm:
        lxmax = max([lempel_ziv(uniform_sequence(x.n, x.alen), parsing=parsing) for i in ns])
        lz_x = lz_x / lxmax
        lxmax = max([lempel_ziv(uniform_sequence(y.n, y.alen), parsing=parsing) for i in ns])
        lz_y = lz_y / lymax
        lxmax = max([lempel_ziv(uniform_sequence(xy.n, xy.alen), parsing=parsing) for i in ns])
        lz_xy = lz_xy / lxymax

    I_rate   =  np.log(x.alen)*lz_x + np.log(y.alen)*lz_y - np.log(xy.alen)*lz_xy  

    return I_rate 

#def Mutual_LempelZiv(x, y,Lxmax,Lxymax):
#    """
#    .. warning::
#       Do not use this function: it will be deprecated.
#
#    It is equivalent to::
#    
#       mutual_lempel_ziv(x,y, norm=True)
#    """
#    warnings.warn("Use mutual_lempel_ziv instead", DeprecationWarning)
#    return mutual_lempel_ziv(x,y, norm=True)

#(JLB)    #Lxmax = 0.8335 #computed on a random N+10^5 long sequence
#    #Lxymax = 0.9244
#    xy = recode([x,y])
#    #entropy rate
#    lz_x   =  Lempel_Ziv(x,parsing='lz76',norm=False)
#    lz_y   =  Lempel_Ziv(y,parsing='lz76',norm=False)
#    lz_xy  =  Lempel_Ziv(xy,parsing='lz76',norm=False)
#
#   #Nomalisation
#    lz_x = lz_x/Lxmax
#    lz_y = lz_y/Lxmax
#    lz_xy = lz_xy/Lxymax
#
##mutual information rate    
#    I_rate   =  np.log(x.k)*lz_x + np.log(y.k)*lz_y - np.log(xy.k)*lz_xy  
#
#    return I_rate #,2*I_rate/(lz_x + lz_y)

#(NS) def mlz(x,y,parsing=lz76):
#    xy=recode([x,y])
#    Lzx=[]
#    Lzx=[]
#    Lzxy=[]
#    Lzx=Lempel_Ziv(x,parsing)
#    Lzy=Lempel_Ziv(y,parsing)
#    Lzxy=Lempel_Ziv(xy,parsing)
#    return [Lzx[0]+Lzy[0]-Lzxy[0],Lzx[0],Lzxy[0],Lzx[1],Lzxy[1],Lzy[1]]

