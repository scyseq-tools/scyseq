#!/usr/bin/env python
#-*- coding:Utf-8 -*-
"""
Some tools to deal with (chaotic) maps. Only some one-dimensional maps are
currently implemented.

This is composed of 

1. Functions

    a. Utils
    b. 1D maps functions
    c. 2D maps (to be implemented)

2. Maps objects

    a. One dimensional maps
    b. Two dimensional maps (to be implemented)

3. Analytic functions

    a. Lyapunov exponents
    b. Miscellaneous (to be implemented)
"""

__docformat__ = 'ReStructuredText'

import numpy as np
from math import floor

# 1. Functions
# ============

#   a. utils
#   ~~~~~~~~

def indsup(x,p):
    """
    Indicatrice function (for x>p)
    """
    if x>p: return 1.
    else: return 0.

def indinf(x,p):
    """
    Indicatrice function for (x<=p)
    """
    if x<=p: return 1.
    else: return 0.

def differentiate(f, eps=1e-10):
    """
    Numerical differentiation of the function f.
    """
    return lambda x: (f(x+eps)-f(x))/eps


#   b. Maps functions
#   ~~~~~~~~~~~~~~~~~

def tent(p):
    #FIXME
    """
    Tent map [CHECK ME]:
    if x<=p: tent(x)=x/p
    if x>p: tent(x)=(1-x)/(1-p)
    """
    return lambda x: indinf(x,p)*(x/p) + indsup(x,p)*((1-x)/(1-p))

# mu_c = 3.5699456
def logistic(mu):
    """
    The logistic map. x(t+1) = mu . x(t) . (1-x(t))
    """
    return lambda x: mu * x * (1-x)

def bernouilli(p=2.0):
    #FIXME
    """
    The Bernouilli shift [CHECK ME]:
    """
    return lambda x: p * x - floor(p * x)

#Ikeda, Henon

# 2. Maps objects
# ===============

#   a. One dimensional maps
#   ~~~~~~~~~~~~~~~~~~~~~~~

class Map1D:
# gérer:
# 1/ l'absence de paramètres
# 2/ les maps 2D

    def __init__(self, func, param):
        self.f = func(param)
        self.p = param

    def iterate(self, x0, T):
    
        X = [x0]
        t = 1
        while t<T:
            X.append(self.f(X[t-1]))
            t += 1

        return np.array(X)

    def lyapunov(self, x0, T, Tskip):
        """
        Approximate Lyapunov exponent lyaplog(mu, x0,based on numerical differenciation
        Do not use for precise results: prefer analytic functions if they exists
        (or code them...)
        """
        x = self.iterate(x0=x0, T=T)[Tskip:]
        fp = np.vectorize(differentiate(self.f))

        lyap = np.mean(np.log(np.abs(fp(x))))

        return lyap

# 3. Analytic functions
# =====================

#   a. Lyapunov exponents
#   ~~~~~~~~~~~~~~~~~~~~~

def lyaplog(mu, x0, T=1e6+1e3, Tskip=1e3):
    """
    Analytic Lyapunov exponent of the logisitic map.
    """
    def logisticPrime(mu):
        return lambda x: mu * (1 - 2.0 * x)

    def vlP(x,p):
        return np.vectorize(logisticPrime(p))(x)
# On devrait faire beaucoup mieux...
    if Tskip < T:
        logis = Map1D(func=logistic, param=mu).iterate(x0, T)[Tskip:]
        lyap = np.mean(np.log(np.abs(vlP(logis,mu))))
        return lyap
    else:
        raise 
