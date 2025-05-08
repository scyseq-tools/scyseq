import numpy as np
from . import nessgraph as G

class Markov:
    """
    Define a Markov process, with pi the matrix representing the 
    state probability and wij the matrix representing the state transition rate
    """
    def __init__(self, states, pi, wij):
        
        self.pi = pi
        self.wij = wij
        self.states = states # a set of states ie an Alphabet defined in sequence
        for s, p in zip(states, pi):
            s.pi = p

    def currents(self):
        """
        Returns the matrix of probability currents.

        .. todo::
           Check the implementation see transition_matrix...
        """
        M = self.wij
        prob = self.pi
        preJ = np.multiply(M.T, prob).T
        J = preJ - preJ.T
        return J
        
    def currents_sum(self):
        J = self.currents()
        return np.sum(abs(J[np.isfinite(J)])) / 2.0
        
    def entropy_production(self):
    # entropy production see Jiang et al. 2004
        J = self.currents()
        M = self.wij
        prob = self.pi
        preJ = np.multiply(M.T, prob).T
        # FIXME; deal with divide by 0
        inter = np.multiply(J, np.log(preJ / (preJ.T)))
        return np.sum(inter[np.isfinite(inter)])/2

    def entropy_rate(self):
        # See Cover and Thomas
        # FIXME: implement!
        raise NotImplementedError

    def to_graph(self):
        """
        Create a Graph from the transition matrix of the markov process
        and assign it to a Mesograph. For each node, assign the value 
        corresponding to the state probability of the markov process.
        For each edge in the newly created graph, calculate the probability 
        flux according to the well known formula:
        
            probability_flux[i,j] = state_probability * transition_rate[i,j]
        
        which determines the probability flowing from state i to the state j
        in a markov process
        """
        tmp = G.NESSGraph()
        tmp.add_nodes_from(self.states.strvals)
        
        for nb1, s1 in enumerate(self.states):
            ns1 = s1.strval
            for nb2, s2 in enumerate(self.states):
                ns2 = s2.strval
                w = self.wij[nb1, nb2]
                if w > 0:
                    tmp.add_edge(ns1, ns2, transition=w, flux=s2.pi*w)
            
        return tmp
