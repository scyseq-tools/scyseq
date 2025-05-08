# -*- encoding:utf8
"""
Test the algorithmic module from scikits.symbolic
"""
from scikits.symbolic import sequence as S
from scikits.symbolic import algorithmic as A
# import numpy as np
# import numpy.testing as nptest
import unittest

class TestContainsSublist(unittest.TestCase):
    """
    Testing contains sublist
    """
    def test_simple(self):
        """
        Check contains sublist
        """
        lst = [1, 2, 3, 4, 5]
        self.assertTrue(A.contains_sublist(lst, [2, 3]))
        self.assertFalse(A.contains_sublist(lst, [2, 4]))

class TestLZ(unittest.TestCase):
    """
    Testing Lempel-Ziv 1976 and 1977 algorithm
    """
    def test_simple_alphabet(self):
        """
        Check alphabet with one digit
        """
        arr = [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0]
        dot, hist = A.lz77(arr, summary=True)
        self.assertEqual(dot, 8)
        self.assertListEqual(hist, [[0], [1], [1, 1], [0, 1], [0, 1, 0], \
                                    [0, 0], [1, 1, 1], [0]])
        dot, hist = A.lz76(arr, summary=True)
        self.assertEqual(dot, 6)
        self.assertListEqual(hist, [[0], [1], [1, 1], [0, 1, 0], [1, 0, 0], \
                                    [0, 1, 1, 1, 0]])
    
    def test_general_alphabet(self):
        """
        Check alphabet with several digits
        """
        arr = [0, 10, 11, 1, 10, 11, 0, 1, 10, 0, 0, 11, 1, 11, 10]
        dot, hist = A.lz77(arr, summary=True)
        self.assertEqual(dot, 10)
        self.assertListEqual(hist, [[0], [10], [11], [1], [10, 11], \
                                    [0, 1], [10, 0], [0, 11], [1, 11], [10]])
        dot, hist = A.lz76(arr, summary=True)
        self.assertEqual(dot, 9)
        self.assertListEqual(hist, [[0], [10], [11], [1], [10, 11, 0], \
                                    [1, 10, 0], [0, 11], [1, 11], [10]])

class TestLempelZiv(unittest.TestCase):
    """
    Testing the Lempel-Ziv procedure
    """
    raise NotImplementedError('Implement me...')
