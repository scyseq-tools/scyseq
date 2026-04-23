import pytest
import copy

import numpy as np
import scyseq as sq


@pytest.fixture
def init_sequence():
    return sq.Sequence([1,0,0,0,1], 2)

def test_rename(init_sequence):
    sq.rename(init_sequence, {0: "a", 1: "b"})
    assert init_sequence.svals == ('b', 'a', 'a', 'a', 'b')

def test_roll(init_sequence, nroll=2):
    rseq = sq.roll(init_sequence, nroll)
    assert all(rseq.ivals == np.roll(init_sequence.ivals, nroll))

def test_reverse(init_sequence):
    rseq = sq.reverse(init_sequence)
    assert all(rseq.ivals == np.flipud(init_sequence.ivals))

def test_shuffle(init_sequence):
    np.random.seed(1234)
    sseq = sq.shuffle(init_sequence)
    np.random.seed(1234)
    tmp = copy.copy(init_sequence.ivals)
    np.random.shuffle(tmp)
    assert all(sseq.ivals == tmp)

def test_reduce(init_sequence):
    rseq = sq.reduce(init_sequence)
    assert all(rseq.ivals == np.array([1,0,1]))

def test_count(init_sequence):
    assert all(sq.count(init_sequence) == np.array([3,2]))
    assert sq.count(init_sequence, 0) == 3
    assert sq.count(init_sequence, 1) == 2

def test_frequency(init_sequence):
    assert all(sq.frequency(init_sequence) == (np.array([3,2]) / 5))
    assert sq.frequency(init_sequence, 0) == 3/5
    assert sq.frequency(init_sequence, 1) == 2/5

@pytest.fixture
def test_sequence():
    return sq.Sequence([1, 0, 3, 2, 3, 3, 2, 0, 2, 1, 0, 1], 4)

def test_transform(test_sequence, corr = [0,0,1,1]):
    tseq = sq.transform(test_sequence, corr)
    assert all(tseq.ivals == np.array([0,0,1,1,1,1,1,0,1,0,0,0]))

def test_recode(init_sequence):
    lseq = [init_sequence, init_sequence]
    nseq = sq.recode(lseq)
    assert all(nseq.ivals == np.array([3,0,0,0,3]))

def test_words(init_sequence, lw=2):
    wseq = sq.words(init_sequence, 2)
    assert all(wseq.ivals == np.array([2,0,0,1]))
    assert wseq.alphabet == sq.Alphabet(4)
