import nose.tools as nt
import numpy as np
import numpy.testing as np_test
import scikits.symbolic.sequence as S

class creation_Test:

    def create_test(self):
        seq = S.Sequence([0,1,0,1], 2)
        np_test.assert_array_equal(seq.s, np.array([0,1,0,1]))
        nt.assert_equal(seq.k, 2)
        nt.assert_equal(seq.d, {0:'0', 1:'1'})

    def copy_test(self):
        seq1 = S.Sequence([1,1,0,0], 2)
        seq2 = S.Sequence(seq1)
        nt.assert_equal(seq1, seq2)


