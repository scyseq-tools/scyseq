"""
Module for information theory related functions.
"""

import numpy as np

from .operation import recode

from . import sequence as S
from . import algorithmic as A
from .stochastic import conditional_matrix


def metric_entropy(seq):
    """
    Returns # Shannon's (metric) entropy of sequence

    :param seq: a symbolic Sequence object

    :returns: a float

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])  
    >>> A = S.Alphabet(['a','b'])
    >>> seq = S.Sequence(a,A)
    >>> metric_entropy(seq)
    0.6003511877776578

    """
    prob = seq.frequency()
    return - np.sum(prob[prob > 0] * np.log(prob[prob > 0]))

# shortcuts for Shannon (metric) entropy
H = metric_entropy
shannon_entropy = metric_entropy

def topological_entropy(seq):
    """
    Returns the topological entropy

    :param seq: a symbolic Sequence object

    :returns: a float

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq = S.Sequence(a,A)
    >>> topological_entropy(seq)
    0.6931471805599453

    """
    nb_visit = np.sum(seq.count() > 0)
    return np.log(float(nb_visit))

# shortcut for topological entropy
T = topological_entropy

def renyi_entropy(seq, coef):
    """
    Returns the Rényi entropy

    ..todo:: 

         Make the doc of renyi_entropy!

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq = S.Sequence(a,A)
    >>> renyi_entropy(seq, 0.9)
    0.6088567303148161

    """
    prob = seq.frequency()
    return (np.log(np.sum(prob[prob > 0]**coef))) / (1 - coef)

# shortcut for Renyi entropy
R = renyi_entropy

# def block_entropy(seq, n, method="metric", *args):
def block_entropy(seq, wlen): #, method="metric", *args):
    """
    Returns the block entropy

    :param seq: a symbolic Sequence object
    :param n: the block length
    :param method: a string in `[ "metric", "shannon", "topological", "renyi",  "all"]`

    :raises:
       :exc:`ValueError` if :math:`n< 0`

       :exc:`NotImplementedError` if the method is not in the list above.

    :returns: either the value of the demanded entropy or all their value
              in a tuple `Tn, Hn, hav`

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq = S.Sequence(a,A)
    >>> block_entropy(seq, 6)
    3.577559335188841

    """
#    if (n < 0): 
#        raise ValueError("Block size cannot be <0")
    nwords = S.words(seq, wlen)
    return H(nwords)

# shortcut for n-block entropy
# HN = block_entropy

##    N = len(seq)
##    seq_list = [seq[i:N-n+i+1] for i in range(n)]
###     for se in seq_list: print len(se)
##    new_seq = recode(seq_list, new_dict=False)
#
#    if method.lower() in ["metric", "shannon"]: 
#        return new_seq.H()
#    
#    elif method.lower() == "topological": 
#        return new_seq.T() / n
#
#    elif method.lower() == "renyi":
#        b = args[0]
#        return renyi_entropy(new_seq, b)
#    
##    elif method.lower() == "average": 
##        return new_seq.H() / n
#    
#    elif method.lower() == "all":
#        Tn = new_seq.T() / n
#        Hn = new_seq.H()
#        return Tn, Hn #, Hn / n
#
#    else: raise NotImplementedError("The %s entropy is not implemented" % method)

# def entropy_rate(seq, method, **kwargs):
def entropy_rate(seq, wlen, method='average'):
    """
    Returns the entropy rate

    :param seq: a symbolic Sequence object
    :param method: a string in ['lempel_ziv', 'average']
    :param kwargs: parameter to pass to the method

    :returns: the entropy rate computed using the method

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq = S.Sequence(a,A)
    >>> entropy_rate(seq, 6)
    0.5962598891981402

    """
#    if method.lower() == "lempel_ziv":
#        #FIXME: how to handle kwargs and default values in lempel_ziv
#        return A.lempel_ziv(seq) * np.log(seq.alen)
    
    # elif method.lower() == "average":
    if method.lower() == "average":
        # wlen = kwargs['n']
        return block_entropy(seq, wlen) / wlen

    elif method.lower() == "difference":
        # wlen = kwargs['n']
        return block_entropy(seq, wlen+1) - block_entropy(seq, wlen)
    
    else:
        raise NotImplementedError(\
                "The %s entropy rate is not implemented" % method)

def effective_complexity(seq, n_max):
    """
    Computes the effective complexity defined by Grassberger

    ..todo::

        Make the doc of effective complexity
    """
    # EC =  \sum_n n.(h_{n-1}-h_n) where h_n = H_{n+1} - H_n
    # FIXME: this is only valid for n \geq 2
    # FIXME: check this against real results!
   
    blocks = [block_entropy(seq, wlen) for wlen in range(1, n_max + 1)]
    rates = np.diff(blocks) # from 0  to n
    drate = np.diff(np.flipud(rates)) # from n to 0 then last flipud below
    return np.sum(np.arange(2, len(drate)+2) * np.flipud(drate))

#def block_entropies(seq, n):
#    """
#    .. warning::
#       Do not use this function: it will be deprecated
#
#    It is equivalent to::
#
#       block_entropy(seq, n, method="all")
#    """
#    warnings.warn("Use block_entropy and entropy_rate instead", DeprecationWarning)
#    return block_entropy(seq, n, method="all"), entropy_rate(seq, method="metric", n=n)

def mutual_information(seq1, seq2):
    """
    Computes the mutual information for symbolic sequences

    :param x, y: two symbolic Sequences

    :returns: the mutual information (float)

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> np.random.seed(6)
    >>> b = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq1 = S.Sequence(a,A)
    >>> seq2 = S.Sequence(b,A)
    >>> mutual_information(seq1, seq2)
    0.0002988020334349084
    """
    seq12 = recode([seq1, seq2])
    return H(seq1) + H(seq2) - H(seq12)

def multi_information(seq1, seq2, seq3):
    """
    Computes the multi information for 3 symbolic sequences, 
    
    A kind of 3 variables mutual information (See Blanc J.L. & Coq J.O.,
    J.Physiol. 2007)
    
    :param x, y, z: three symbolic Sequences

    :returns: the three variable mutual information

    Example :

    >>> np.random.seed(9)
    >>> a = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> np.random.seed(6)
    >>> b = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> np.random.seed(3)
    >>> c = np.random.choice([0,1],1000,replace=True, p=[0.7,0.3])
    >>> A = S.Alphabet(['a','b'])
    >>> seq1 = S.Sequence(a,A)
    >>> seq2 = S.Sequence(b,A)
    >>> seq3 = S.Sequence(c,A)
    >>> multi_information(seq1, seq2, seq3)
    -4.8757282800737656e-05

    """
    seq12 = S.recode([seq1, seq2])
    seq13 = S.recode([seq1, seq3])
    seq23 = S.recode([seq2, seq3])    
    seq123 = S.recode([seq1, seq2, seq3])

    # return x.H() + y.H() + z.H() + xyz.H() - xy.H() - xz.H() - yz.H()
    return H(seq1) + H(seq2) + H(seq3) + H(seq123) - \
           H(seq12) - H(seq13) - H(seq23)

def transfer_entropy(seq1, seq1p, seq2):
    """
    Computes the symbolic transfer entropy T y->x

    we can use: P(x|y) = P(x,y) / P(y) in the formula:
    P(x+, x, y) log (P(x+|x,y) / P(x+|x))

    but (see Kugiumtzis, 2011)
    
    -H(x+, x, y) + H(x, y) + H(x+, x) - H(x) 
    
    gives a better implementation

    see:

    Schreiber (2000)
    Staniek and Lehnertz (2008) Symbolic transfer entropy PRE
    Kugiumtzis (2011) Journal of Nonlinear Systems and Applications vol. 2 n°3
    http://arxiv.org/abs/1007.0357
    """
    seq1p21 = S.recode([seq1p, seq2, seq1])
    seq21 = S.recode([seq2, seq1])
    seq1p1 = S.recode([seq1p, seq1])

    return - H(seq1p21) + H(seq21) + H(seq1p1) - H(seq1)

#    return - recode([xp, y, x], new_dict=False).H() \
#           + recode([y, x], new_dict=False).H() \
#           + recode([xp, x], new_dict=False).H() \
#           - x.H()
