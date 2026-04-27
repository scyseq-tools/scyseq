import pytest

from scyseq import Alphabet


def test_alphabet_badinit():
    with pytest.raises(ValueError) as exc_info:
        Alphabet([1, 2, 3])
    assert "Symbols or strings" in str(exc_info.value)
