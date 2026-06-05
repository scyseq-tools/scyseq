# Copyright (c) 2007-2026 The scyseq developers.
# SPDX-License-Identifier: BSD-3-Clause BSD

"""
scyseq is a Python package for defining, manipulating, analysing and
representing symbolic sequences
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("scyseq")
except PackageNotFoundError:
    __version__ = "unknown"

__authors__ = [
    "Laurent Pezard",
    "Jean-Luc Blanc",
    "Noelia Montejo-Cervera",
    "Nicolas Schmidt",
    "Yann Manhoun",
    "Florent Boyer-Aymé",
    "Dewmith Weerasena",
]

from scyseq.exceptions import (
    AlphabetAccessError,
    AlphabetError,
    EmptyAlphabetError,
    InvalidSymbolError,
    LengthError,
    ScyseqError,
    SequenceError,
    SequenceParseError,
    SymbolAccessError,
    SymbolDefinitionError,
    SymbolError,
    SymbolMismatchError,
)
from scyseq.io import read_codix  #, write_codix
from scyseq.operations import count, frequency, recode, reduce, rename, reverse, roll, shuffle, transform, words
from scyseq.sequence import Alphabet, Sequence, Symbol, binary_alphabet, boolean_alphabet

__all__ = ["Symbol", "Alphabet", "Sequence",
           "binary_alphabet", "boolean_alphabet",
           "count", "frequency", "recode", "reduce", "rename", "reverse",
           "roll", "shuffle", "transform", "words",
           "read_codix",
           "ScyseqError", "SymbolError", "SymbolDefinitionError",
           "SymbolAccessError", "AlphabetError", "AlphabetAccessError",
           "InvalidSymbolError", "EmptyAlphabetError", "SequenceError",
           "SequenceParseError", "LengthError", "SymbolMismatchError", "__version__" ]

def __dir__():
    return __all__
