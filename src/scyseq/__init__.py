"""
scyseq is a Python package for defining, manipulating, analysing and
representing symbolic sequences
"""

# should be replaced by hatch at building with hatch build

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

from scyseq.exceptions import *
from scyseq.io import read_codix, write_codix
from scyseq.operations import count, frequency, recode, reduce, rename, reverse, roll, shuffle, transform, words
from scyseq.sequence import Alphabet, Sequence, Symbol, binary_alphabet, boolean_alphabet
