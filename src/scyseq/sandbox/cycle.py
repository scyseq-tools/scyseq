# = encoding:utf8 =

import scikits.symbolic.sequence as S
from scipy.stats import scoreatpercentile

#def _get_cycle(slist, symb):
#    idx = slist.index(symb)
#    return slist[idx:], slist[:idx]

def cyclic_permutation(vals):
    ll = len(vals)
    perms = []
    for idx in range(ll):
        start = list(vals[idx:ll])
        start.extend(vals[0:idx])
        perms.append(tuple(start))
    perms.sort()
    return tuple(perms)

class Cycle(object):

    def __init__(self, vals, check=True):
        vals = tuple(vals)
        if check:
            valset = set(vals)
            assert all([vals.count(x) == 1 for x in valset]), \
                   "Cycle cannot have duplicate states"
        # We compute all the cyclic permutations here so it is done only once
        # But is this a good choice?
        self.permutations = cyclic_permutation(vals)
        # We normalize the states so that we get the lower symbol first
        self.states = self.permutations[0]
    
    def __len__(self):
        """
        Returns the length of a Cycle (:func:`len`).
        """
        return len(self.states)

    def __eq__(self, other):
        if type(other) is not Cycle:
            return False
        if len(self) != len(other):
            return False
        else:
            if self.states in other.permutations:
                return True
            else:
                return False

    # Needed to be able to use Cycles as keys in dicts (with the __eq__ method)
    def __hash__(self):
        return hash(self.permutations)

#    # Not sure this is useful...
#    def itercyclic(self):
#        vals = self.states
#        ll = len(self)
#        for idx in range(ll):
#            start = list(vals[idx:ll])
#            start.extend(vals[0:idx])
#            yield tuple(start)

def cyclic_decomposition(seq):
    arr = seq.ivals
    seqlen = len(seq)
    cur = []
    cycles = {}

    for symb in arr:
        # print symb, cur
        if symb in cur:
            # cycle, remain = _get_cycle(cur, symb)
            idx = cur.index(symb)
            cycle, remain = cur[idx:], cur[:idx]
            if Cycle(cycle) not in cycles.keys():
                cycles[Cycle(cycle)] = 1.
            else:
                cycles[Cycle(cycle)] += 1.
            remain.append(symb)
            cur = remain
        else:
            cur.append(symb)

    # FIXME:
    # What to do with the remaining current states (remaining of the sequence) ?
    # 1. right now we add one if the key exists (suppose that the cycle will loop
    #    in the next symbol --- which is not available in the current sequence)
    #    and make a new cycle with the remaining with the same supposition.
    # 2. Just do not take care of it (and possibly return it as an option?
    if Cycle(cur) not in cycles.keys():
        cycles[Cycle(cur)] = 1.
    else:
        cycles[Cycle(cur)] += 1.

#    set_cycles = list(set(cycles))
#    nb_cycles = [cycles.count(cycle) for cycle in set_cycles]
#    w_cycles = [float(nb) / float(seqlen) for nb in nb_cycles] 
#    retcycles = dict([(cycle, float(cycles.count(cycle))) for cycle in set_cycles])
#    return set_cycles, nb_cycles, w_cycles

    return cycles

def surrogate_cycles(seq, nbsur=500):

    retval = {}

    for nosur in range(nbsur):
        scycles = cyclic_decomposition(S.shuffle(seq))

        for cycle in scycles.keys():
            if retval.has_key(cycle):
                retval[cycle].append(scycles[cycle])
            else:
                retval[cycle] = [scycles[cycle]]

    for cycle in retval.keys():
        retval[cycle].extend([0]*(nbsur-len(retval[cycle])))

    return retval

def get_non_random_cycles(seq, nbsur=500, threshold=0.05):

    # test that nbsur and threshold corresponds
    if (1./float(nbsur)) > threshold:
        threshold = 1. / float(nbsur)
        print "Warning threshold changed to %4.2f" % threshold
    # FIXME: make a warning 

    retcycles = []
    raw_cycles = cyclic_decomposition(seq)
    sur_cycles = surrogate_cycles(seq, nbsur=nbsur)

    for cycle in raw_cycles.keys():
        if not sur_cycles.has_key(cycle):
            retcycles.append(cycle)
            # FIXME
            # raise ValueError('Surrogate cycles do not depict raw cycle...')
        else:
            nb_raw = raw_cycles[cycle]
            dist = sur_cycles[cycle]
            n_max = scoreatpercentile(dist, 100. - (threshold * 100.))
            if nb_raw > n_max:
                retcycles.append(cycle)

    return dict((k, raw_cycles[k]) for k in retcycles)

#    if return_raw:
#        return retcycles, raw_cycles
#    else:
#        return retcycles

if __name__ == "__main__":


    a = S.Sequence([1,2,0,3,2,1,2,0,3,2,1,2,1,2,1,2,1,2], 4)
    decomp = cyclic_decomposition(a)
    for k, v in decomp.iteritems():
        print k.states, v

    surrog = surrogate_cycles(a, 10)
    for k, v in surrog.iteritems():
        print k.states, v

    nrcycles = get_non_random_cycles(a)
    for k, v in nrcycles.iteritems():
        print k.states, v

 
#    print get_cycles(a)
#    print surrogate_cycles(a, 10)
#    print get_non_random_cycles(a)
#    for i in range(10):
#        print extractor.extract(S.shuffle(a))

