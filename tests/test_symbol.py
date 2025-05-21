import pytest
from scyseq import Symbol

def test_symbol_badinit():
    with pytest.raises(ValueError) as exc_info:
        Symbol([1,2,3])
    assert "integer" in str(exc_info.value)

@pytest.fixture
def init_str():
    return Symbol("one")

@pytest.fixture
def init_int():
    return Symbol(1)

def test_symbol_initstr(init_str):
# also test properties' getter
    assert init_str.ival is None
    assert init_str.sval == "one"

def test_symbol_initint(init_int):
# also test properties' getter
    assert init_int.ival is None
    assert init_int.sval == "1"

def test_symbol_ival_setter(init_str):
    with pytest.raises(AttributeError) as exc_info:
        init_str.ival = 0
    assert "no setter" in str(exc_info.value)

def test_symbol_ival_deleter(init_str):
    with pytest.raises(AttributeError) as exc_info:
        del init_str.ival
    assert "no deleter" in str(exc_info.value)

def test_symbol_sval_setter(init_str):
    init_str.sval = "zero"
    assert init_str.sval == "zero"
    assert init_str.ival is None

def test_symbol_sval_deleter(init_str):
    with pytest.raises(AttributeError) as exc_info:
        del init_str.sval
    assert "no deleter" in str(exc_info.value)

def test_symbol_equal(init_str):
    assert init_str == Symbol('one')
    assert init_str != Symbol('two')
    assert init_str != Symbol(2)

def test_symbol_equal(init_int):
    assert init_int == Symbol(1)
    assert init_int != Symbol("two")
    assert init_int != Symbol(2)
