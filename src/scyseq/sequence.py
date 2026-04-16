"""
This module defines the base classes: Symbol, Alphabet and Sequence, their
attributes and methods.

A symbolic sequence is a list of symbols taken from a finite alphabet of length
:math:`k`

Internally they are encoded according to integers from :math:`0` to :math:`k-1`
called `ivals` and all the computations use this representation. For human
readability, there is also a string value (`svals`) which is associated with the
integer representation when needed.

Alphabet behaves like bidirectional dictionaries with restrictions to avoid
problems.
"""

import copy
import itertools
import operator

import numpy as np

from . import exceptions as E
from . import utils as U

# DTYPES = [np.uint8, np.uint16]
# DEFAULT_DTYPE = np.uint16

class Symbol:
    """
    A symbol (or state) is used to define the state of the system at time
    :math:`t`.
    """

    def __init__(self, value):
        """
        Initialize an instance of Symbol.

        :param value: Value associated with the sval property. Must be an
               integer or a string.  It is automatically converted to a string.

        :type value: int or str

        *Examples:*

        >>> Symbol(1) # 1 is converted to a string
        Symbol(- | 1)
        >>> Symbol('One')
        Symbol(- | One)

        The integer value (ival) of a symbol is only attributed once the symbol is
        inserted in an alphabet.

        It has two properties: ival and sval
        """
        if not isinstance(value, (str, int)):
            raise E.SymbolDefinitionError(value, "Value must be an integer or a string")
        self._sval = str(value)
        self._ival = None
        self._alphabet = None

    @property
    def sval(self):
        """
        The "string value" of the Symbol (i.e. its "name") which can be accessed or
        changed (set) but not deleted (deleter raises exception for explicit
        behavior).

        If the symbol is inserted in an alphabet, the sval should not already
        exist in the alphabet.
        """
        return self._sval

    @sval.setter
    def sval(self, value):
        if not isinstance(value, str):
            raise E.SymbolDefinitionError(value, "Value must be a string")

        if self._alphabet is not None:
            if value in self._alphabet.svals:
                raise E.AlphabetAccessError("Symbol sval already exists in alphabet")

        self._sval = value

    @sval.deleter
    def sval(self):
        raise E.SymbolAccessError("sval cannot be deleted")

    @property
    def ival(self):
        """
        The "integer value" of the Symbol associated integer value which can be
        accessed but neither changed nor deleted

        setter and deleter raise exception for explicit behavior.
        """
        return self._ival

    @ival.setter
    def ival(self, value):
        raise E.SymbolAccessError("ival is read-only")

    @ival.deleter
    def ival(self):
        raise E.SymbolAccessError("ival cannot be deleted")


    def _attach(self, alphabet, value):
        """
        Explicit change of _ival for access from the Alphabet class in
        Alphabet.__init__
        """
        if isinstance(value, int) and isinstance(alphabet, Alphabet):
            self._ival = value
            self._alphabet = alphabet
        else:
            # This is the sign of a bug...
            raise E.SymbolAccessError("Attachment of symbol failed.")

    def __eq__(self, other):
        """
        Returns True if self.ival == other.ival and self.sval == other.sval
        """
        return (self._sval == other._sval) & (self._ival == other._ival)

    def __str__(self):
        if self._ival is not None:
            return f"({self._ival} | {self._sval})"

        return f"(- | {self._sval})"

    def __repr__(self):
        if self._ival is not None:
            return f"Symbol({self._ival} | {self._sval})"

        return f"Symbol(- | {self._sval})"

    def __deepcopy__(self, memo):
        # Create a new instance without calling __init__
        copied = self.__class__.__new__(self.__class__)

        # Insert the original in the memo to take care of the cycles
        memo[id(self)] = copied

        copied._ival = copy.deepcopy(self._ival, memo)
        copied._sval = copy.deepcopy(self._sval, memo)
        copied._alphabet = copy.deepcopy(self._alphabet, memo)

        return copied

class Alphabet(tuple):
    """
    The set of symbols that can be visited in a Sequence.
    """
    def __new__(cls, symbols):
        """
        Create an instance of the Alphabet class
        """
        if isinstance(symbols, cls):
            return copy.deepcopy(symbols)

        if isinstance(symbols, int):
            elements = [Symbol(str(ii)) for ii in range(symbols)]

        elif isinstance(symbols, (list, tuple)):
             # Check that all the elements of symbols are different"
            if all([sa != sb for sa, sb in itertools.combinations(symbols, 2)]):

                if all([isinstance(symb, Symbol) for symb in symbols]):
                    elements = symbols

                elif all([isinstance(symb, str) for symb in symbols]):
                    elements = [Symbol(symb) for symb in symbols]
                else:
                    raise ValueError("Values must all be Symbols or strings")
            else:
                raise E.AlphabetError("The values must all be different.")
        else:
            raise E.AlphabetError("The values must be an integer, a list or a tuple.")

        return super().__new__(cls, [copy.deepcopy(e) for e in elements])

    def __init__(self, symbols):
        """
        Initialize an instance of the Alphabet class

        :param symbols: The objects used to build the alphabet
        :type symbols: int or list or tuple

        Alphabets can be created using:

        1. the length (an integer):

        >>> Alphabet(3)
        Alphabet(Symbol(0 | 0), Symbol(1 | 1), Symbol(2 | 2))

        2. a list or tuple of strings:

        >>> Alphabet(['a', 'b', 'c'])
        Alphabet(Symbol(0 | a), Symbol(1 | b), Symbol(2 | c))

        3. a list or tuple of symbols:

        >>> Alphabet([Symbol('s0'), Symbol('s1'), Symbol('s2')])
        Alphabet(Symbol(0 | s0), Symbol(1 | s1), Symbol(2 | s2))
        """
        for n, symb in enumerate(self):
            symb._attach(self, n)

        self._ivals = tuple(s.ival for s in self)
        self._svals = tuple(s.sval for s in self)
        self._symbols = tuple(s for s in self)
        # FIXME: Not sure this is useful
        # When an alphabet is associated to a sequence it cannot be modified.
        # self._islinked = False

    def __str__(self):
        return '('+', '.join([s.__str__() for s in self])+')'

    def __repr__(self):
        return 'Alphabet('+', '.join([s.__repr__() for s in self])+')'

    def __eq__(self, other):
        """
        Two alphabets are equal if they have the same length and if their
        ivals and svals coincide.

        >>> alpha_a = Alphabet(['a','b','c'])
        >>> alpha_b = Alphabet(['a','b','c'])
        >>> alpha_c = Alphabet(3)
        >>> alpha_a == alpha_b
        True
        >>> alpha_a == alpha_c
        False
        """
        if not isinstance(other, Alphabet):
            raise E.AlphabetAccessError("Can only compare alphabets with alphabets")
        if len(self) != len(other):
            return False

        return all([ssymbol == osymbol for ssymbol, osymbol in zip(self, other)])

    def __getitem__(self, key):
        try:
            if isinstance(key, int):
                return self._symbols[key]
            if isinstance(key, str):
                idx = self.svals.index(key)
                return self._symbols[idx]
        except:
            raise E.AlphabetAccessError('Key not in alphabet')

    def __setitem__(self, key, value):
        raise E.AlphabetAccessError("'Alphabet' object does not support item assignment")

    def __deepcopy__(self, memo):
        # Deepcopy of the content of the tuple
        deepcopied = copy.deepcopy(tuple(self), memo)
        # Create a new instance without calling __init__
        copied = tuple.__new__(self.__class__, deepcopied)

        # Insert the original in the memo to take care of the cycles
        memo[id(self)] = copied

        copied._ivals = copy.deepcopy(self._ivals, memo)
        copied._svals = copy.deepcopy(self._svals, memo)
        copied._symbols = copy.deepcopy(self._symbols, memo)

        return copied

    @property
    def svals(self):
        """
        The tuple of string values in the alphabet

        >>> alpha_a = Alphabet(['a','b','c'])
        >>> alpha_a.svals
        ('a', 'b', 'c')
        """
        return self._svals

#    @svals.setter
#    def svals(self, value):
#        self._sval = str(value)

#    @svals.deleter
#    def svals(self):
#        raise KeyError("Cannot delete the name of a symbol")

    @property
    def ivals(self):
        """
        The tuple of integer values in the alphabet

        >>> alpha_a = Alphabet(['a','b','c'])
        >>> alpha_a.ivals
        (0, 1, 2)
        """
        return self._ivals

#    @ivals.setter
#    def ivals(self, value):
#        raise TypeError("Cannot change the ival of a symbol")
#
#    @ivals.deleter
#    def ivalself):
#        raise TypeError("Cannot delete the ival of a symbol")

    def items(self):
        """
        Returns the pair ival : sval for each symbol.

        >>> alpha_a = Alphabet(['a','b','c'])
        >>> list(alpha_a.items())
        [(0, 'a'), (1, 'b'), (2, 'c')]
        >>> dict(alpha_a.items())
        {0: 'a', 1: 'b', 2: 'c'}
        """
        return zip(self.ivals, self.svals)

    def rename(self, replacement):
        """
        To rename symbols in an alphabet, pass a dictionary with integers as
        keys and strings as values so that the replacement of ivals and svals
        are explicit.

        :param replacement: The dictionary which describes the replacement. 
        :type  replacement: dict

        >>> alpha_d = Alphabet(['a','b','c', 'd'])
        >>> alpha_d
        Alphabet(Symbol(0 | a), Symbol(1 | b), Symbol(2 | c), Symbol(3 | d))
        >>> alpha_d.rename({1: 'One', 3: 'Three'})
        >>> alpha_d
        Alphabet(Symbol(0 | a), Symbol(1 | One), Symbol(2 | c), Symbol(3 | Three))
        """
        if not isinstance(replacement, dict):
            raise TypeError ('The input must be a dictionnary')
        if not all(isinstance(k, int) and isinstance(v, str)
                    for k, v in replacement.items()):
            raise E.AlphabetAccessError("Replacements should be int : str")

        for k, v in replacement.items():
            # symbol.sval setter takes care of the unicity of the symbol in
            # the alphabet.
            self[k].sval = v

class Sequence:
    """
    Defines a symbolic sequence coded using integers in :math:`{0,
    k-1}` and their methods.
    """
    def __new__(cls, symbols, alphabet, check=True):
        """
        Creates a Sequence object.
        """
        if isinstance(symbols, cls):
            return copy.deepcopy(symbols)

        array = np.asarray(symbols)

        if array.ndim != 1:
            raise ValueError("The symbols argument should be unidimensional (1D).")

        # Try to cast to unsigned integer
        if not np.issubdtype(array.dtype, np.unsignedinteger):
            if np.issubdtype(array.dtype, np.integer):
                if np.any(array < 0):
                    raise ValueError("All values should be >=0")
                dtype = U.choose_uint_dtype(array)
                array = array.astype(dtype)
                array.flags.writeable = False
            else:
                raise TypeError("Symbols should be convertible into unsigned integers")

        alpha = Alphabet(alphabet)

        # Check correspondence between symbols and alphabet
        if check:
            if max(array) >= len(alpha):
                raise E.AlphabetError("Invalid alphabet length")

        instance = super().__new__(cls)
        instance._validivals = array
        instance._validalphabet = alpha

        return instance

#        # 4. Création de l'objet
#        instance = super().__new__(cls)
#        instance._array = array
#        return instance
#
##        if dtype not in DTYPES:
##            raise TypeError(\
##                    'Wrong dtype. Maybe you entered both alphabet and its length.')
##        # symbols = np.array(symbols)
##        # Check if data can be represented in the dtype
##        if np.any(symbols < np.iinfo(dtype).min) or \
##           np.any(symbols > np.iinfo(dtype).max):
##            raise E.SymbolError(\
##                  'Data can not be represented in %s' % str(dtype))
##        # Check the dimension of the data
##        if len(symbols.shape) != 1: # 1D sequences for now
##            raise E.ShapeError(\
##                  'Data shape is not one-dimensional')
#        # self._ivals = np.asarray(symbols).astype(dtype)
#        # Parse the alphabet
#
#        if isinstance(alphabet, Alphabet):
#            self._alphabet = copy.deepcopy(alphabet)
#
## FIXME: is the islinked is useful?
##                self._alphabet._islinked = True
#
#        elif type(alphabet) == int :
#            # self._alphabet = Alphabet(alphabet)
#            self._alphabet = Alphabet(alphabet)
#        else:
#            raise 
# TypeError('The parameter alphabet must be an integer or a sequence.Alphabet object')

    def __init__(self, symbols, alphabet, check=True):
        """
        Initializes a Sequence object.

        :param symbols: the sequence of symbols.
        :type symbols: an object that can be coerced into an np.array of
                  integers.

        :param alphabet: the alphabet which is either a alphabet or the alphabet
                  length

        :param check: should the validity of the construction be checked
        :type check: boolean

        or

        :param s: a sequence object
        :exc: `TypeError`: when parameter `a` is not given and `s` is not a
               sequence 

        :raises:
            :exc:`ValueError`: when `a` is neither a `dict` nor an `int`
            :exc:`ValueError`: when `s` contains negative values

            :exc:`AlphabetError`: when `s` contains values greater or equal to `k`

            :exc:`DictionaryError`: if keys of `d` are not in :math:`{0, k-1}`

        :returns: a Sequence object with attribute `s`, `k` and `d`

        >>> seqA = Sequence([1, 0, 0, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 1], 3)
        >>> seqA
        Sequence: [1 0 0 2 0 0 0 2 2 0 2 2 0 0 1]
        Alphabet(Symbol(0 | 0), Symbol(1 | 1), Symbol(2 | 2))
        N = 15 ; k = 3
        """
        if isinstance(symbols, Sequence):
            pass

        else:
            self._alphabet = self._validalphabet
            self._ivals = self._validivals

            del self._validalphabet, self._validivals

#            if dtype not in DTYPES:
#                raise TypeError(\
#                        'Wrong dtype. Maybe you entered both alphabet and its length.')
#            symbols = np.array(symbols)
#            # Check if data can be represented in the dtype
#            if np.any(symbols < np.iinfo(dtype).min) or \
#               np.any(symbols > np.iinfo(dtype).max):
#                raise E.SymbolError(\
#                      'Data can not be represented in %s' % str(dtype))
#            # Check the dimension of the data
#            if len(symbols.shape) != 1: # 1D sequences for now
#                raise E.ShapeError(\
#                      'Data shape is not one-dimensional')
#            self._ivals = np.asarray(symbols).astype(dtype)
#            # Parse the alphabet
#            if isinstance(alphabet, Alphabet):
#                self._alphabet = copy.deepcopy(alphabet)
#
## FIXME: is the islinked is useful?
##                self._alphabet._islinked = True
#
#            elif type(alphabet) == int :
#                # self._alphabet = Alphabet(alphabet)
#                self._alphabet = Alphabet(alphabet)
#            else:
#                raise
# TypeError('The parameter alphabet must be an integer or a sequence.Alphabet object')
#            # Check correspondence between symbols and alphabet
#            if check:
#                if (max(self._ivals) >= len(self._alphabet)):
#                    raise E.AlphabetError("Invalid alphabet length")

## Alphabet property

    @property
    def alphabet(self):
        """
        The alphabet property
        """
        return self._alphabet

    @property
    def k(self):
        """
        The length of the alphabet
        """
        return len(self.alphabet)

    @property
    def ivals(self):
        """
        The tuple of integer values
        """
        return self._ivals

    @property
    def svals(self):
        """
        The tuple of string values
        """
        tmp = np.array([self.alphabet[i]._sval for i in self._ivals])
        tmp.flags.writeable = False
        return tmp

# Copy method
    def __deepcopy__(self, memo):
        """
        Returns a copy of the Sequence object
        """
        return Sequence(np.copy(self._ivals), \
                        copy.deepcopy(self.alphabet))

# Sequences representation
# FIXME: change the repr and str (print -> str)
    def __str__(self):
        """
        Defines the string representation of a Sequence.

        .. todo::
           Do we need more information when we want to print a Sequence
        """
        return self.ivals.__str__() # FIXME: need more info ??

    def __repr__(self):
        """
        Defines the representation of a Sequence.
        """
        return "Sequence: %s\n%s\nN = %d ; k = %d" % (self.ivals.__str__(),
                self.alphabet.__repr__(), len(self), self.k)

    def __len__(self):
        """
        Returns the length of a Sequence (:func:`len`).
        """
        return len(self._ivals)

    def __getitem__(self, key):
        """
        Allows to slice a sequence. Can be sliced with an int, a slice or an
        ndarray 
        """
        if isinstance(key, int):
            tmpval = [self._ivals[key]]
        elif isinstance(key, slice):
            tmpval = self._ivals[key]
        elif isinstance(key, np.ndarray):
            # print(key, type(key))
            tmpval = self._ivals[np.where(key)[0]]
#        elif type(key) is Sequence:
#            tmpval = self._ivals[np.where(key._ivals)[0]]
        else:
            print(key, type(key))
            raise ValueError(f"Cannot slice with {str(type(key))}")

        return Sequence(tmpval, self.alphabet, check=False)

# FIXME: is it useful?
#    def __setitem__(self, key, value):
#        """
#        Allows to change the value of an element of a Sequence.
#
#        :raises:
#           :exc:`ValueError`: if `value` is not in :math:`{0, k-1}`
#        """
#        if (value<0) or (value>=self._alen) or type(value) is not int:
#            raise ValueError("%d is not allowed for alphabet length=%d" % \
#                            (value, self._alen))
#        self.ivals.__setitem__(key, int(value))
#
#    def __delitem__(self, key):
#        """
#        Allows to delete elements of a Sequence.
#
#        .. todo::
#           Give an example of the deletion of elements of a sequence
#        """
#        lseq = list(self.ivals)
#        del lseq[key]
#        self.ivals = np.array(lseq)

# Iterators

    def __iter__(self): # returns an iterator
        """
        Returns an iterator on the Sequence. Should return an itertor over the
        ivals otherwise the all(seq != seq) returns True...
        """
        return self._ivals.__iter__()

    def iteritems(self):
        """
        Returns the pairs ival : sval
        """
        return zip(self._ivals, self.svals)

    def iterivals(self):
        """
        Returns the iterator over the integer values
        """
        return self._ivals.__iter__()

    def itersvals(self):
        """
        Returns the iterator over the string values
        """
        return self.svals.__iter__()

## FIXME:
## I do not know when this is really used... for checking reversibility etc.
#    def __reversed__(self): # returns an iterator
#        """
#        Returns an iterator on the Sequence in the reverse order
#        """
#        # return np.flipud(self.ivals).__iter__()
#
#        # return zip(np.flipud(self.ivals), np.flipud(self.svals))
##        raises:
##        AttributeError: property 'ivals' of 'Sequence' object has no setter


# "numeric" operations

#    def __add__(self, other):
#        """
#        Allows to add two sequences: they are concatenated
#
#        :raises:
#           :exc:`ValueError`: when the alphabets are different
#        """
#        if (self.alphabet != other.alphabet):
#            raise ValueError('Alphabets are different')
#        else:
#            return Sequence(np.concatenate((self._ivals, other._ivals)), \
#                            self.alphabet, check=False)

# Logical operations
# FIXME:
# np.logical_? are defined for any array. Why do we check binary?
# This is strange to change logical_? to operators, no?

#    def __and__(self, other):
#        """
#        Returns a binary sequence which is the result of comparison with `&`
#
#        .. seealso::
#           numpy.logical_and
#
#        .. caution::
#           This corresponds to the `&` operator and not the `and` keyword.
#        """
#        # if self._alen != 2 or other._alen != 2:
#        if self.k != 2 or other.k != 2:
#            raise NotImplementedError('& is defined for binary sequences only')
#        else:
#            seq = np.logical_and(self._ivals, other._ivals)
#            return Sequence(seq.astype(self._ivals.dtype), Alphabet(('False', 'True')), \
#                            check=False)
#
#    def __or__(self, other):
#        """
#        Returns a binary sequence which is the result of comparison with `|`
#
#        .. seealso::
#           numpy.logical_or
#
#        .. caution::
#           This corresponds to the `|` operator and not the `or` keyword.
#        """
#        # if self._alen != 2 or other._alen != 2:
#        if self.k != 2 or other.k != 2:
#            raise NotImplementedError('| is defined for binary sequences only')
#        else:
#            arr = np.logical_or(self._ivals, other._ivals)
#            return Sequence(arr.astype(self._ivals.dtype), Alphabet(('False', 'True')), \
#                            check=False)
#
#    def _xor_(self, other):
#        """
#        Returns a binary sequence which is the result of comparison with `^`
#
#        .. seealso::
#           numpy.logical_xor
#
#        .. caution::
#           This corresponds to the `^` operator.
#        """
#        # if self._alen != 2 or other._alen != 2:
#        if self.k != 2 or other.k != 2:
#            raise NotImplementedError('| is defined for binary sequences only')
#        else:
#            arr = np.logical_xor(self._ivals, other._ivals)
#            return Sequence(arr.astype(self._ivals.dtype), Alphabet(('False', 'True')), \
#                            check=False)

# Rich comparison methods"

    def __mkcomp__(self, other, op): 

        if isinstance(other, Sequence):
            if self.alphabet == other.alphabet:
                if len(other) == len(self):
                    arr = op(self._ivals, other._ivals)
                else:
                    raise \
                    ValueError('Cannot compare Sequences with different lengths')
            else:
                raise \
                ValueError('Cannot compare Sequences with different alphabets')

        elif isinstance(other, int) and other >= 0:
            arr = op(self._ivals, other)
        else:
            raise \
            ValueError("Sequence can be compared with a Sequence or a positive integer only")

        return Sequence(arr.astype(self._ivals.dtype), Alphabet(('False', 'True')), check=False)

    def __lt__(self, other):
        return self.__mkcomp__(other, operator.__lt__)

    def __le__(self, other):
        return self.__mkcomp__(other, operator.__le__)

    def __eq__(self, other):
        return self.__mkcomp__(other, operator.__eq__)

    def __ne__(self, other):
        return self.__mkcomp__(other, operator.__ne__)

    def __gt__(self, other):
        return self.__mkcomp__(other, operator.__gt__)

    def __ge__(self, other):
        return self.__mkcomp__(other, operator.__ge__)

# Methods that transform the sequence
    def roll(self, step):
        """
        Return a "rolled" sequence
        """
#        self._ivals = np.roll(self._ivals, step)

        return Sequence(np.roll(self._ivals, step), self._alphabet)

    def reverse(self):
        """
        Return a "reversed" the sequence
        """
        # self._ivals = np.flipud(self._ivals)
        return Sequence(np.flipud(self._ivals), self._alphabet)

    def shuffle(self):
        """
        Return a "shuffled" sequence
        """
        shuffled = np.random.shuffle(copy.copy(self._ivals))

        return Sequence(shuffled, self._alphabet)

    def reduce(self):
        """
        Delete the repetitions of symbols in a sequence
        """
        diff = np.ediff1d(self._ivals)
        bool_idx = list(diff!=0)
        bool_idx.append(True)
        reduced = self._ivals[bool_idx]

        return Sequence(reduced, self._alphabet)

# Methods that compute characteristics of the sequence

    def count(self, value=None):
        """
        Counts the number of each symbol in :math:`{0, k-1}` if code is None
        or the number of the code symbol

        :returns: a numpy.ndarray of integers
        """
        if value is None:
            return np.array([np.sum(self._ivals == i) for i in range(self.k)])

        if isinstance(value, int):
            return np.sum(self._ivals == value)

        if isinstance(value, str):
            return np.sum(self.svals == value)

        raise ValueError("Value should be an integer or a string")


    def frequency(self):
        """
        Returns the probability of each symbol in :math:`{0, k-1}`

        :returns: a numpy.ndarray of floats
        """
        return self.count() / float(len(self))


# Compatibility re-exports for the historical ``sequence`` module API.
from .operation import recode, words
