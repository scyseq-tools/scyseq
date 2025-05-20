import pytest
from scyseq import Symbol

def test_symbol_badinit():
    with pytest.raises(ValueError) as exc_info:
        Symbol([1,2,3])
    assert "integer" in str(exc_info.value)

def test_symbol_initstr():
    onestr = Symbol("one")
    assert onestr.ival is None
    assert onestr.sval == "one"

def test_symbol_initint():
    oneint = Symbol(1)
    assert oneint.ival is None
    print(oneint.sval)
    assert oneint.sval == "1"
