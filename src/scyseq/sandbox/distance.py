# -*- encoding:utf8 -*-
"""
Implements distances between sequences
"""
import numpy as np

def kullbach_liebler(seq1, seq2):
    """
    Computes Kullbach-Liebler divergence between seq1 and seq2
    """
    if seq1.alen != seq2.alen:
        raise ValueError('Sequences should have the same alphabet')
    pseq1 = seq1.frequency()
    pseq2 = seq2.frequency()
    if np.any(pseq2 == 0):
        return np.Inf
    else:
        return np.sum(pseq1[pseq1>0] * np.log(pseq1[pseq1>0] / pseq2[pseq1>0]))
# Kullbach-Liebler divergence shortcut 
KL = kullbach_liebler
