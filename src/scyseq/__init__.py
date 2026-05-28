"""
scyseq is a Python package for defining, manipulating, analysing and
representing symbolic sequences
"""

__version__ = "0.1.0"

__authors__ = [
    "Laurent Pezard",
    "Jean-Luc Blanc",
    "Noelia Montejo-Cervera",
    "Nicolas Schmidt",
    "Yann Manhoun",
    "Florent Boyer-Aymé",
    "Dewmith Weerasena",
]

# from scyseq.exceptions import *
from .io import read_codix  #, write_codix
from .operations import count, frequency, recode, reduce, rename, reverse, roll, shuffle, transform, words
from .sequence import Alphabet, Sequence, Symbol, binary_alphabet, boolean_alphabet

__all__ = ["Symbol", "Alphabet", "Sequence", 
           "binary_alphabet", "boolean_alphabet",
           "count", "frequency", "recode", "reduce", "rename", "reverse",
           "roll", "shuffle", "transform", "words", "read_codix"]

def __dir__():
    return __all__
