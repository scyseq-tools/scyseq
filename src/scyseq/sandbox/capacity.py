#-*- encoding:utf8 -*-
import numpy as np

def blahut_arimoto(x, y, kx, ky, eps=0.0001, itermax=1000):
    """
    Blahut-Arimoto algorithm based on Dauwels (2005)

    J. Dauwels, Numerical computation of the capacity of continuous memoryless
    channels, Proceedings of the 26th Symposium on Information Theory in the
    BENELUX, Brussels, Belgium, May 19 -20, 2005, pp. 221-228.
    """
    # x: input / stimulus
    # y: output / response

    # px = x.Pr() # Px(0)
    # py = y.Pr() # experimental or Py(0) = sum(Px(0) Py|x)  (0) 

    # Px(1) 
    # px_inter = Px(0) * exp( KL(Py|x \\ Py(0)))
    # Px(1) = px_inter / sum(px_inter)  # ie Px(1) = px_inter / Z(1)

    # KL (z \\ w) = sum( Pz * log (Pz / Pw)) 

    # Py|x = P(Y=y and X=x) / P(X=x)

    # 1. Try brute force implementation...

    crit = 1. # Initial convergence criterium
    critlist = [] # storing computed criterium values
    I = [] # storing mutual information
    Plist = [] # storing P(input)
    itercur = 0

    lx = len(x)
    ly = len(y)
    assert(lx==ly) # this is mandatory...
    cl = float(lx) # needed for further divisions
    symbx = list(range(kx)) # all input even with P(x) = 0
    symby = list(range(ky)) # idem
    symbx.sort()
    symby.sort()

    Px = np.array([np.sum(x==sx) / cl for sx in symbx])
    Py = np.array([np.sum(y==sy) / cl for sy in symby])

    # normalize so sum = 1
    # FIXME: Is this useful?
    # Px = Px /np.sum(Px)
    # Py = Py /np.sum(Py)

    Plist.append(Px)

    # print Px
    # print Py
# for checking
    ptot = []

    Pyx = [] # Py|x = P(y,x) / Px
    for ny, sy in enumerate(symby):
        Pinter = []
        for nx, sx in enumerate(symbx):
            if Px[nx] != 0.:
                prob_conj = np.sum(np.logical_and(x==sx, y==sy)) / cl
                Pinter.append(prob_conj / Px[nx])
            else:
                print('Borel-Kolmogorov')
                # FIXME: what is Py|x when Px=0? ie Borel-Kolmogorov Paradox
                # see: http://www.statlect.com/cnddst1.htm 
                #      http://en.wikipedia.org/wiki/Borel%E2%80%93Kolmogorov_paradox
                # 
                # Solution chosen here is uniform Py|x = 1/ny so sum_y Py|x = 1
                # does not seem to change results (ie capacity=I) but criterium
                # crit < eps is not obtained so maxiter is used in this case.
                Pinter.append(1./len(symby))
# for checking
        ptot.append(np.sum(np.array(Pinter) * Px))

        Pyx.append(Pinter)
    Pyx = np.array(Pyx)
    
    # print Pyx
    print('NEXT SHOULD BE 1 everywhere')
    print(np.sum(Pyx, axis=0)) # should sum to 1
    # Total probability: sum(Py|x * Px) = Py
    print('NEXT SHOULD BE 0 everywhere')
    print(np.array(ptot) - Py) # should be zero

    # Compute initial I(0)
    # FIXME: write a generic kullbach_liebler(Px, Py) function
    #        here we assume that P(y) > 0; what to do with P(y) = 0...
    DKL = []
    for ind in range(len(symbx)):
        # Py always != 0
        # need to deal with Pyx == 0 and 0 log 0 = 0
        notnull = np.where(Pyx[:, ind] != 0.)[0]
        DKL.append(np.sum(Pyx[notnull, ind] * np.log(Pyx[notnull, ind] / Py[notnull])))
    DKL = np.array(DKL)

    # print DKL
        
    I.append(np.sum(Px * DKL))

    while (crit > eps) and (itercur < itermax):   #iterations nbre

        # KL distance of DKL(Pyx||Py) is a function of x
        DKL = []
        for ind in range(len(symbx)):
            # Py always != 0
            # need to deal with Pyx == 0 and 0 log 0 = 0
            notnull = np.where(Pyx[:, ind] != 0.)[0]
            DKL.append(np.sum(Pyx[notnull, ind] * np.log(Pyx[notnull, ind] / Py[notnull])))
        DKL = np.array(DKL)

        P = Px * np.exp(DKL)
        P = P / np.sum(P)
        Px = P
        Plist.append(Px)

        # Update Py
        Py = []
        for ind in range(len(symby)):
            Py.append(np.sum(Px * Pyx[ind, :])) 
        Py = np.array(Py)
        
        DKLn = []
        for ind in range(len(symbx)):
            # Py always != 0
            # need to deal with Pyx == 0 and 0 log 0 = 0
            notnull = np.where(Pyx[:, ind] != 0.)[0]
            DKLn.append(np.sum(Pyx[notnull, ind] * np.log(Pyx[notnull, ind] / Py[notnull])))
        DKLn = np.array(DKLn)

        In = np.sum(Px * DKLn)
        crit = max(DKLn) - In

        critlist.append(crit)
        I.append(In)
        itercur += 1

#    print 'I: ', I
#    print 'Converge: ', critlist

    return Plist, I, critlist
