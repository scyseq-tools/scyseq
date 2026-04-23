# -*- encoding:utf8
"""
Test the stochastic module from scikits.symbolic
"""
from scikits.symbolic import sequence as S
from scikits.symbolic import stochastic as St
import numpy as np
import numpy.testing as nptest
import unittest

class TestConditionalMatrix(unittest.TestCase):
    """
    Testing conditional matrix
    """
    def test_simple(self):
        """
        Check conditional matrix with same binary alphabet
        """
        seq = S.Sequence([1, 0, 1, 0, 1, 0], 2)
        m = St.conditional_matrix(seq, seq)
        nptest.assert_array_equal(m, np.matrix([[1, 0], \
                                                [0, 1]]))

        seq1 = S.Sequence([1, 1, 0, 0], 2)
        seq2 = S.Sequence([1, 0, 0, 1], 2)
        m = St.conditional_matrix(seq1, seq2)
        nptest.assert_array_equal(m, np.matrix([[0.5, 0.5], \
                                                [0.5, 0.5]]))

    def test_different(self):
        """
        Check conditional matrix with different alphabet
        """
        seq1 = S.Sequence([1, 1, 1, 0, 0, 0], 2)
        seq2 = S.Sequence([0, 1, 2, 0, 1, 2], 3)
        m = St.conditional_matrix(seq1, seq2)
        nptest.assert_array_equal(m, np.matrix([[0.5, 0.5], \
                                                [0.5, 0.5], \
                                                [0.5, 0.5]]))
        m = St.conditional_matrix(seq2, seq1)
        nptest.assert_array_equal(m, np.matrix([[1./3., 1./3., 1./3.], \
                                                [1./3., 1./3., 1./3.]]))

        seq1 = S.Sequence([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], 2)
        seq2 = S.Sequence([0, 0, 1, 2, 2, 0, 1, 1, 1, 2, 2, 2, 2], 3)
        m = St.conditional_matrix(seq1, seq2)
        nptest.assert_array_equal(m, np.matrix([[1./3., 2./3.], \
                                                [3./4., 1./4.], \
                                                [2./3., 1./3.]]))
        m = St.conditional_matrix(seq2, seq1)
        nptest.assert_array_equal(m, np.matrix([[1./8., 3./8., 1./2.], \
                                                [2./5., 1./5., 2./5.]]))

