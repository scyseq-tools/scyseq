# -*- encoding:utf-8 -*-
"""
Converts a set of event times (ie such as neo.SpikeTrains) into a binary sequence
"""
import quantities as pq
import numpy as np
from scikits.symbolic import sequence as S

def event2seq(times, t_bin):
    """
    Times is a quantified array
    t_bin is the time period (also in quantities)
    """
    times.units = 's'
    t_bin.units = 's'
    seq_len = times.max() / t_bin
    # print seq_len
    seq = np.zeros(seq_len)
    ind = (times / t_bin).astype(int)
    # print ind
    seq[ind-1] = 1
    return S.Sequence(seq, 2)
    
if __name__ == '__main__':

    times = np.array([0.023, 0.5, 1.0])*pq.s
    t_bin = 1.*pq.ms
    seq = event2seq(times, t_bin)
    print seq

