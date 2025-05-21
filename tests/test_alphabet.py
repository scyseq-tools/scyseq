import pytest
from scyseq import Symbol, Alphabet

def test_alphabet_badinit():
    with pytest.raises(ValueError) as exc_info:
        Alphabet([1,2,3])
    assert "integer" in str(exc_info.value)

@pytest.fixture
def init_int():
    alph_int = Alphabet(3)
    assert 

@pytest.fixture
def init_int():
    return Alphabet(1)

def test_alphabet_initstr(init_str):
# also test properties' getter
    assert init_str.ival is None
    assert init_str.sval == "one"

def test_alphabet_initint(init_int):
# also test properties' getter
    assert init_int.ival is None
    assert init_int.sval == "1"

def test_alphabet_ival_setter(init_str):
    with pytest.raises(AttributeError) as exc_info:
        init_str.ival = 0
    assert "no setter" in str(exc_info.value)

def test_alphabet_ival_deleter(init_str):
    with pytest.raises(AttributeError) as exc_info:
        del init_str.ival
    assert "no deleter" in str(exc_info.value)

def test_alphabet_sval_setter(init_str):
    init_str.sval = "zero"
    assert init_str.sval == "zero"
    assert init_str.ival is None

def test_alphabet_sval_deleter(init_str):
    with pytest.raises(AttributeError) as exc_info:
        del init_str.sval
    assert "no deleter" in str(exc_info.value)

def test_alphabet_equal(init_str):
    assert init_str == Alphabet('one')
    assert init_str != Alphabet('two')
    assert init_str != Alphabet(2)

def test_alphabet_equal(init_int):
    assert init_int == Alphabet(1)
    assert init_int != Alphabet("two")
    assert init_int != Alphabet(2)
