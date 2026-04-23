# FIXME: I do not understand how to manage version

# from version import __version__

__authors__ = ["Laurent Pezard", 
               "Jean-Luc Blanc", 
               "Noelia Montejo-Cervera", 
               "XX Schmidt", 
               "Yann Manhoun", 
               "Florent Boyer-Aymé"]

from .sequence import Symbol, Alphabet, boolean_alphabet, binary_alphabet, Sequence
from .exceptions import *
from .operations import recode, words, rename, roll, reverse, shuffle, reduce, count, frequency, transform
