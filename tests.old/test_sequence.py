"""
Test the generator module from stimlib
"""
from scikits.symbolic import sequence as S
from scikits.symbolic import exceptions as E
import numpy as np
import numpy.testing as nptest
import unittest

class TestSequenceCreation(unittest.TestCase):
    """
    Testing sequence utilities
    """
    def test_init(self):
        """
        Check initialization
        """
        symseq = [1, 0, 2]
        alen = 3
        alpha = ('a', 'b', 'c')

        seq = S.Sequence(symseq, alen)
        nptest.assert_array_equal(seq.ivals, np.array(symseq).astype(int))
        self.assertEqual(seq.alen, alen)
        self.assertEqual(seq.alphabet, alen) # no alphabet so fallback to alen
        
        seq = S.Sequence(symseq, alpha)
        nptest.assert_array_equal(seq.ivals, np.array(symseq).astype(int))
        self.assertEqual(seq.alen, alen)
        self.assertTupleEqual(seq.alphabet, alpha)
        
        # Exceptions cases
        self.assertRaises(TypeError, S.Sequence, symseq, alen, np.uint64)
        self.assertRaises(ValueError, S.Sequence, symseq) 
        self.assertRaises(E.AlphabetError, S.Sequence, symseq, 2.3) 
        self.assertRaises(E.AlphabetError, S.Sequence, symseq, [2, 3]) 
        symseq = [1, 0, -2]
        self.assertRaises(E.SymbolError, S.Sequence, symseq, alen)
        symseq = [1, 0, 2]
        self.assertRaises(E.AlphabetError, S.Sequence, symseq, alen - 1)
        ddict = ('a', 'b')
        self.assertRaises(E.AlphabetError, S.Sequence, symseq, ddict)

        # Sequence of a sequence
        seq = S.Sequence(symseq, alen)
        seqbis = S.Sequence(seq)
        nptest.assert_array_equal(seqbis.ivals, seq.ivals)
        self.assertEqual(seqbis.alen, seq.alen)
        self.assertEqual(seqbis.alphabet, seq.alphabet)

    # test repr and str

    def test_properties(self):
        """
        Check alphabet properties
        """
        symseq = [1, 0, 2]
        alen = 3
        alpha = ('a', 'b', 'c')
        # with alphabet
        seq1 = S.Sequence(symseq, alpha)
        self.assertTupleEqual(seq1.alphabet, alpha)
        self.assertEqual(seq1.alen, len(alpha))
        # change alphabet
        seq1.alphabet = None
        self.assertIsNone(seq1._alphabet)
        self.assertEqual(seq1.alen, len(alpha))
        self.assertEqual(seq1.alphabet, len(alpha))

        # with alphabet length
        seq2 = S.Sequence(symseq, alen)
        self.assertEqual(seq2.alphabet, alen)
        self.assertEqual(seq2.alen, alen)
        with self.assertRaises(TypeError):
            seq2.alphabet = 3
        with self.assertRaises(E.AlphabetError):
            seq2.alphabet = ['a', 'b']
        seq2.alphabet = ['a', 'b', 'c']
        self.assertEqual(seq2.alen, len(alpha))
        self.assertTupleEqual(seq2.alphabet, ('a', 'b', 'c'))
            

    def test_slicing_methods(self):
        """
        Check slicing methods
        """
        symseq = [1, 0, 2, 2, 1, 0, 2, 0, 0, 0, 1]
        alen = 3
        seq = S.Sequence(symseq, alen)
        self.assertEqual(len(seq), len(symseq))
        self.assertEqual(seq[4], symseq[4])
        nptest.assert_array_equal(seq[2:6].ivals, symseq[2:6])
        nptest.assert_array_equal(seq[-3:].ivals, symseq[-3:])
        with self.assertRaises(ValueError):
            seq[0] = -2
            seq[0] = 3
        seq[0] = 0
        self.assertEqual(seq[0], 0)

        del seq[0:2]
        del symseq[0:2]
        nptest.assert_array_equal(seq.ivals, symseq)

    def test_iterators(self):
        """
        Check iterators
        """
        symseq = [1, 0, 2, 2, 1, 0, 2, 0, 0, 0, 1]
        alen = 3
        seq = S.Sequence(symseq, alen)
        self.assertListEqual(list(iter(seq)), symseq)
        symseq.reverse()
        seq.reverse()
        self.assertListEqual(list(seq.ivals), symseq)

    def test_numerical_methods(self):
        """
        Check numerical methods
        """
        ss1 = [2, 1, 0, 0, 0, 1]
        ss2 = [0, 2, 0, 0, 0, 1]
        alen = 3
        seq1 = S.Sequence(ss1, alen)
        seq2 = S.Sequence(ss2, alen)
        seq = seq1 + seq2
        nptest.assert_array_equal(seq.ivals, ss1 + ss2)
        self.assertEqual(seq.alphabet, seq1.alphabet)
        self.assertEqual(seq.alphabet, seq2.alphabet)

        ss3 = [0, 2, 3, 0, 3, 1]
        alen = 4
        seq3 = S.Sequence(ss3, alen)
        with self.assertRaises(ValueError):
            seq1 + seq3

    def test_logical_methods(self):
        """
        Check logical methods
        """
        ss1 = [1, 1, 0, 0, 0, 1]
        ss2 = [0, 1, 0, 0, 0, 1]
        alen = 2
        bdict = (False, True)
        seq1 = S.Sequence(ss1, alen)
        seq2 = S.Sequence(ss2, alen)
        seq_and = seq1 & seq2
        seq_or = seq1 | seq2
        seq_xor = seq1 ^ seq2
        nptest.assert_array_equal(seq_and.ivals, np.logical_and(ss1, ss2))
        nptest.assert_array_equal(seq_or.ivals, np.logical_or(ss1, ss2))
        nptest.assert_array_equal(seq_xor.ivals, np.logical_xor(ss1, ss2))
        self.assertTupleEqual(seq_and.alphabet, bdict)
        self.assertTupleEqual(seq_or.alphabet, bdict)
        self.assertTupleEqual(seq_xor.alphabet, bdict)

        ss3 = [0, 2, 0, 0, 0, 1]
        alen = 3
        seq3 = S.Sequence(ss3, alen)
        # logical defined only for binary sequences
        with self.assertRaises(NotImplementedError):
            seq1 & seq3
            seq1 | seq3
            seq1 ^ seq3

# FIXME:
#        self.assertTrue(seq1 == seq1)
#        self.assertFalse(seq1 == seq2)
#        self.assertFalse(seq1 == seq1 + seq2)
#        self.assertFalse(seq1 == seq3)
#        self.assertFalse(seq1 != seq1)
#        self.assertTrue(seq1 != seq2)
#        self.assertTrue(seq1 != seq1 + seq2)
#        self.assertTrue(seq1 != seq3)

    def test_roll(self):
        """
        Check roll method
        """
        ss3 = [0, 2, 0, 0, 0, 1]
        alen = 3
        seq = S.Sequence(ss3, alen)
        seq.roll(3)
        nptest.assert_array_equal(seq.ivals, np.roll(ss3, 3))
        seq = S.Sequence(ss3, alen)
        seq.roll(-3)
        nptest.assert_array_equal(seq.ivals, np.roll(ss3, -3))

    def test_reverse(self):
        """
        Check reverse
        """
        symseq = [1, 0, 2, 2, 1, 0, 2, 0, 0, 0, 1]
        alen = 3
        seq = S.Sequence(symseq, alen)
        symseq.reverse()
        seq.reverse()
        self.assertListEqual(list(seq.ivals), symseq)

    def test_shuffle(self):
        """
        Check shuffle in place
        """
        symseq = [1, 0, 2, 2, 1, 0, 2, 0, 0, 0, 1]
        alen = 3
        seq = S.Sequence(symseq, alen)
        np.random.seed(2012)
        np.random.shuffle(symseq)
        np.random.seed(2012)
        seq.shuffle()
        nptest.assert_array_equal(seq.ivals, symseq)


    def test_reduce(self):
        """
        Check reduce method in place
        """
        ss3 = [0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1, 0, 1, 2, 0, 0]
        target = [0, 2, 0, 1, 0, 1, 2, 0]
        alen = 3
        seq = S.Sequence(ss3, alen)
        seq.reduce()
        nptest.assert_array_equal(seq.ivals, np.array(target))

    def test_count(self):
        """
        Check count method
        """
        ss3 = [0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1, 0, 1, 2, 0, 0]
        target = np.array([8, 4, 4]) 
        alen = 3
        seq = S.Sequence(ss3, alen)
        counting = seq.count()
        nptest.assert_array_equal(counting, target)
        ss3 = [2, 2, 2, 1, 1, 1, 1, 2]
        target = np.array([0, 4, 4]) 
        alen = 3
        seq = S.Sequence(ss3, alen)
        counting = seq.count()
        nptest.assert_array_equal(counting, target)

    def test_frequency(self):
        """
        Check frequency method
        """
        ss3 = [0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1, 0, 1, 2, 0, 0]
        target = np.array([8, 4, 4]) / float(len(ss3)) 
        alen = 3
        seq = S.Sequence(ss3, alen)
        prob = seq.frequency()
        nptest.assert_array_equal(prob, target)
        ss3 = [2, 2, 2, 1, 1, 1, 1, 2]
        target = np.array([0, 4, 4]) / float(len(ss3))
        alen = 3
        seq = S.Sequence(ss3, alen)
        prob = seq.frequency()
        nptest.assert_array_equal(prob, target)

    # def test_visit(self):

class TestSequenceFunction(unittest.TestCase):
    """
    Testing sequence utilities
    """
    def test_transform(self):
        """
        Check transform function
        """
        ss3 = [0, 2, 0, 2, 0, 1, 2, 1, 1]
        ssc = [1, 0, 1, 0, 1, 0, 0, 0, 0]
        alen = 3
        # No new alphabet
        seq = S.Sequence(ss3, alen)
        newseq = S.transform(seq, [1, 0, 0])
        nptest.assert_array_equal(newseq.ivals, np.array(ssc))
        self.assertEqual(newseq.alen, 2)
        self.assertEqual(newseq.alphabet, 2)
        # with new alphabet
        newseq = S.transform(seq, [0, 1, 1], ('a', 'b'))
        ssc = [0, 1, 0, 1, 0, 1, 1, 1, 1]
        nptest.assert_array_equal(newseq.ivals, np.array(ssc))
        self.assertEqual(newseq.alen, 2)
        self.assertTupleEqual(newseq.alphabet, ('a', 'b'))
        # Exceptions
        self.assertRaises(ValueError, S.transform, seq, [0, 1])
        self.assertRaises(ValueError, S.transform, seq, [0, 1, 1, 0])
        self.assertRaises(ValueError, S.transform, seq, [2, 1, 6, 0])
        self.assertRaises(ValueError, S.transform, seq, [0, 1, 1], \
                          ('a','b','c'))

    def test_recode(self):
        """
        Check recode function
        """
        ssc = [0, 0, 1, 1]
        ssd = [0, 1, 0, 1]
        alen = 2
        seq1 = S.Sequence(ssc, alen)
        seq2 = S.Sequence(ssd, alen)
        seqr = S.recode([seq1, seq2])
        nptest.assert_array_equal(seqr.ivals, np.array([0, 1, 2, 3]))
        self.assertEqual(seqr.alen, 4)
        self.assertEqual(seqr.alphabet, 4)
        seq1 = S.Sequence(ssc, ('a', 'b'))
        seq2 = S.Sequence(ssd, ('c', 'd'))
        seqr = S.recode([seq1, seq2], new_dict=True)
        nptest.assert_array_equal(seqr.ivals, np.array([0, 1, 2, 3]))
        self.assertEqual(seqr.alen, 4)
        self.assertTupleEqual(seqr.alphabet, (('a', 'c'), ('a', 'd'), \
                                              ('b', 'c'), ('b', 'd')))
        ssc = [0, 0, 0, 1, 1, 1]
        ssd = [0, 1, 2, 0, 1, 2]
        ssr = [0, 1, 2, 3, 4, 5]
        lenc = 2
        lend = 3
        seq1 = S.Sequence(ssc, lenc)
        seq2 = S.Sequence(ssd, lend)
        seqr = S.recode([seq1, seq2])
        nptest.assert_array_equal(seqr.ivals, np.array(ssr))
        self.assertEqual(seqr.alen, 6)
        self.assertEqual(seqr.alphabet, 6)
        seq1 = S.Sequence(ssc, ('a', 'b'))
        seq2 = S.Sequence(ssd, ('c', 'd', 'e'))
        seqr = S.recode([seq1, seq2], new_dict=True)
        nptest.assert_array_equal(seqr.ivals, np.array(ssr))
        self.assertEqual(seqr.alen, 6)
        self.assertTupleEqual(seqr.alphabet, (('a', 'c'), ('a', 'd'), \
                                              ('a', 'e'), ('b', 'c'), \
                                              ('b', 'd'), ('b', 'e')))

        sa = [0] * 18 + [1] * 18
        sb = ([0] * 6 + [1] * 6 + [2] * 6) * 2
        sc = [0, 1, 2, 3, 4, 5] * 6
        a = S.Sequence(sa, ('a', 'b'))
        b = S.Sequence(sb, ('c', 'd', 'e'))
        calpha = (('a', 'c'), ('a', 'd'), ('a', 'e'), \
                  ('b', 'c'), ('b', 'd'), ('b', 'e'))
        c = S.Sequence(sc, calpha)
        d = S.recode([a, b, c], new_dict=True)
        nptest.assert_array_equal(d.ivals, np.array(range(36)))
        dalpha = (('a', 'c', ('a', 'c')), ('a', 'c', ('a', 'd')), \
                  ('a', 'c', ('a', 'e')), ('a', 'c', ('b', 'c')), \
                  ('a', 'c', ('b', 'd')), ('a', 'c', ('b', 'e')), \
                  ('a', 'd', ('a', 'c')), ('a', 'd', ('a', 'd')), \
                  ('a', 'd', ('a', 'e')), ('a', 'd', ('b', 'c')), \
                  ('a', 'd', ('b', 'd')), ('a', 'd', ('b', 'e')), \
                  ('a', 'e', ('a', 'c')), ('a', 'e', ('a', 'd')), \
                  ('a', 'e', ('a', 'e')), ('a', 'e', ('b', 'c')), \
                  ('a', 'e', ('b', 'd')), ('a', 'e', ('b', 'e')), \
                  ('b', 'c', ('a', 'c')), ('b', 'c', ('a', 'd')), \
                  ('b', 'c', ('a', 'e')), ('b', 'c', ('b', 'c')), \
                  ('b', 'c', ('b', 'd')), ('b', 'c', ('b', 'e')), \
                  ('b', 'd', ('a', 'c')), ('b', 'd', ('a', 'd')), \
                  ('b', 'd', ('a', 'e')), ('b', 'd', ('b', 'c')), \
                  ('b', 'd', ('b', 'd')), ('b', 'd', ('b', 'e')), \
                  ('b', 'e', ('a', 'c')), ('b', 'e', ('a', 'd')), \
                  ('b', 'e', ('a', 'e')), ('b', 'e', ('b', 'c')), \
                  ('b', 'e', ('b', 'd')), ('b', 'e', ('b', 'e')))
        self.assertTupleEqual(d.alphabet, dalpha)
        self.assertEqual(d.alen, 36)

        # exception sequence length differ
        self.assertRaises(E.LengthError, S.recode, [a, seq1])

    def test_words(self):
        """
        Check words function (derives from recode)
        """
        ssc = [0, 0, 1, 1, 0]
        alen = 2
        seq = S.Sequence(ssc, alen)
        word1 = S.words(seq, 2)
        nptest.assert_array_equal(word1.ivals, np.array([0, 1, 3, 2]))
        self.assertRaises(AssertionError, S.words, seq, -2)

    def test_visited_states(self):
        """
        Check visited_states function
        """
        ssc = [0, 0, 1, 1, 0]
        alen = 2
        seq = S.Sequence(ssc, alen)
        visit = S.visited_states(seq)
        self.assertListEqual(visit, [(0, 0.6, None), (1, 0.4, None)]) 
        
        ssc = [0, 0, 1, 1, 0]
        alpha = ('a', 'b')
        seq = S.Sequence(ssc, alpha)
        visit = S.visited_states(seq)
        self.assertListEqual(visit, [(0, 0.6, 'a'), (1, 0.4, 'b')]) 
        
        ssc = [0, 0, 1, 1, 1, 2, 2, 2, 2, 2]
        alpha = ('a', 'b', 'c')
        seq = S.Sequence(ssc, alpha)
        visit = S.visited_states(seq)
        self.assertListEqual(visit, \
                             [(2, 0.5, 'c'), (1, 0.3, 'b'), (0, 0.2, 'a')]) 

if __name__ == "__main__":
    unittest.main()

