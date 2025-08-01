import pytest
import scyseq as sq
from scyseq import Symbol, Alphabet

def test_symbol_badinit():
    with pytest.raises(sq.SymbolDefinitionError) as exc_info:
        Symbol([1,2,3])
    assert "integer" in str(exc_info.value)

@pytest.fixture
def init_str():
    return Symbol("one")

@pytest.fixture
def init_int():
    return Symbol(1)

def test_symbol_initstr(init_str):
# also test ival and sval getters
    assert init_str.ival is None
    assert init_str.sval == "one"

def test_symbol_initint(init_int):
# also test ival and sval getters
    assert init_int.ival is None
    assert init_int.sval == "1"

# test sval property (setter and deleter; getter tested above)

def test_symbol_sval_setter(init_str):
    init_str.sval = "zero"
    assert init_str.sval == "zero"
    assert init_str.ival is None
# test error outside a dictionary
    with pytest.raises(sq.SymbolDefinitionError) as exc_info:
        init_str.sval = 99
    assert "must be a string" in str(exc_info.value)
# test error inside a dictionary
    a = Alphabet(3)
    assert a[0].sval == "0"
    a[0].sval = "zero"
    assert a[0].sval == "zero"
    with pytest.raises(sq.AlphabetAccessError) as exc_info:
        a[1].sval = "zero"
    assert "already exists" in str(exc_info.value)

def test_symbol_sval_deleter(init_str):
    with pytest.raises(sq.SymbolAccessError) as exc_info:
        del init_str.sval
    assert "cannot be deleted" in str(exc_info.value)

# test ival property (setter and deleter; getter tested above)

def test_symbol_ival_setter(init_str):
    with pytest.raises(sq.SymbolAccessError) as exc_info:
        init_str.ival = 0
    assert "read-only" in str(exc_info.value)

def test_symbol_ival_deleter(init_str):
    with pytest.raises(sq.SymbolAccessError) as exc_info:
        del init_str.ival
    assert "cannot be deleted" in str(exc_info.value)

def test_symbol_equal(init_str):
    assert init_str == Symbol('one')
    assert init_str != Symbol('two')
    assert init_str != Symbol(2)

def test_symbol_equal(init_int):
    assert init_int == Symbol(1)
    assert init_int != Symbol("two")
    assert init_int != Symbol(2)
