# FIXME: I do not understand how to manage version

# from version import __version__

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
