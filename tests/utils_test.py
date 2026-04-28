import numpy as np

import scyseq as sq
from scyseq.utils import choose_uint_dtype, delegate_to


def test_choose_uint_dtype_uses_smallest_unsigned_dtype():
    assert choose_uint_dtype(np.array([0, 255])) is np.uint8
    assert choose_uint_dtype(np.array([0, 256])) is np.uint16
    assert choose_uint_dtype(np.array([0, 65536])) is np.uint32
    assert choose_uint_dtype(np.array([0, 2**32])) is np.uint64


def test_delegate_to_builds_method_that_calls_target_function():
    delegated_count = delegate_to(".operations", "count")
    seq = sq.Sequence([0, 1, 1, 0, 1], 2)

    np.testing.assert_array_equal(delegated_count(seq), np.array([2, 3]))
