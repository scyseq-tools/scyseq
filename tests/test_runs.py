# -*- encoding:utf8
"""
Test the algorithmic module from scikits.symbolic
"""
from scikits.symbolic import sequence as S
from scikits.symbolic.sandbox import runs as R
import numpy as np
import unittest

class TestRuns(unittest.TestCase):
    """
    Testing runs
    """
    def test_simple(self):
        """
        """
        seq = S.Sequence([0,1,1,1,0,0], 2)
        self.assertTrue(R.runs(seq, retlist=True) == [[1,2], [3]])
        seq = S.Sequence([0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,1], 2)
        self.assertTrue(R.runs(seq, retlist=True) == [[1,3,2,1], [3,4,1,1]])
        
        seq = S.Sequence([0,1,1,1,0,0], 2)
        self.assertTrue(R.runs(seq, counts=True) == [[0,1,1], [0,0,0,1]])
        seq = S.Sequence([0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,1], 2)
        self.assertTrue(R.runs(seq, counts=True) == [[0,2,1,1], [0,2,0,1,1]])
        
        seq = S.Sequence([0,1,1,1,0,0], 2)
        print R.runs(seq)
        self.assertListEqual(R.runs(seq), [np.array([0.,1./2.,1./2.]), 
                                        np.array([0.,0.,0.,1./1.])])
        seq = S.Sequence([0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,1], 2)
        self.assertListEqual(R.runs(seq), [np.array([0,2./4.,1./4.,1./4.]), 
                                        np.array([0,2./4.,0,1./4.,1./4.])])

if __name__ == "__main__":
    unittest.main()

