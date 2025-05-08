import copy
import itertools
import operator

import numpy as np

from . import exceptions as E

#from . import stochastic as Sto
#from . import markov as M

__docformat__ = 'reStructuredText'

DTYPES = [np.uint8, np.uint16]
DEFAULT_DTYPE = np.uint8

"""
This module defines Symbols, Alphabets and symbolic Sequences objects, their
related methods and functions.
"""

class Symbol(object):
    """
    A symbol (or state) is used to define the state of the system at time $t$.

    It has two properties:

    - `strval`: its name which can be accessed, changed but not deleted
    
    - `ival`: its associated integer value which can be accessed but neither
      changed nor deleted

    setter and deleter raise exception for explicit behavior.
    """

    def __init__(self, strval):
        self.__strval = str(strval)
        # __ival is set to an integer when state is included in an alphabet
        self.__ival = None

    @property
    def strval(self):
        return self.__strval

    @strval.setter
    def strval(self, value):
        self.__strval = str(value)

    @property
    def ival(self):
        return self.__ival

    def _set__ival(self, value):
        """Explicit change of __ival for access from external classes"""
        if type(value) is int:
            self.__ival = value
        else:
            raise ValueError("Should be interger value")

    def __eq__(self, other):
        return (self.__strval == other.__strval) & (self.__ival == other.__ival)

    def __str__(self):
        if self.__ival is not None:
            return 'Symbol(%d | %s)' % (self.__ival, self.__strval)
        else:
            return 'Symbol(- | %s)' % self.__strval

    def __repr__(self):
        if self.__ival is not None:
            return 'Symbol(%d | %s)' % (self.__ival, self.__strval)
        else:
            return 'Symbol(- | %s)' % self.__strval

class Alphabet(object): 
    """
    The set of states or symbols that can be visited for a sequence or Markov
    process realization.

    Tests on Symbol and Alphabet

    >>> state1 = Symbol('One')
    >>> state1
    Symbol(- | One)

    An integer representation of a state is only attributed once the state is
    inserted in an alphabet.

    >>> state2 = Symbol('Two')
    >>> state3 = Symbol('Three')

    Alphabets can be created with a list of states:

    >>> alpha = Alphabet([state1, state2, state3])
    >>> alpha
    Alphabet[Symbol(0 | One), Symbol(1 | Two), Symbol(2 | Three)]
    >>> print(alpha)
    Alphabet[Symbol(0 | One), Symbol(1 | Two), Symbol(2 | Three)]
    >>> len(alpha)
    3

    Alphabets can also be created using only the length as argument.

    >>> beta = Alphabet(3)
    >>> beta 
    Alphabet[Symbol(0 | 0), Symbol(1 | 1), Symbol(2 | 2)]
    >>> alpha[0]
    Symbol(0 | One)

    Symbols can be changed but the integer value is kept:

    >>> alpha[1] = Symbol('Deux')
    >>> alpha
    Alphabet[Symbol(0 | One), Symbol(1 | Deux), Symbol(2 | Three)]

    Alphabet's states can be changed using a dictionary representation.

    >>> alpha.rename({0 : 'Uno', 2 : 'Tre'})
    >>> alpha
    Alphabet[Symbol(0 | Uno), Symbol(1 | Deux), Symbol(2 | Tre)]
    >>> beta.rename({0 : 'Uno', 1 : 'Deux', 2 : 'Tre'})
    >>> alpha == beta
    True
    """
    def __init__(self, nsymb):
        
        if type(nsymb) is int:
            states = [Symbol(str(ii)) for ii in range(nsymb)]
            for n, s in enumerate(states):
                s._set__ival(n)

        elif (type(nsymb) is list) or (type(nsymb) is tuple):

             # Check that all the elements of nsymb are different" 
             if all([sa != sb for sa, sb in itertools.combinations(nsymb, 2)]):

                if all([type(symb) == Symbol for symb in nsymb]):
                        states = list(nsymb)
                        for n, s in enumerate(states):
                            s._set__ival(n)
            
                elif all([type(symb) == str for symb in nsymb]):
                    states = [Symbol(strval=ii) for ii in nsymb]
                    for n, s in enumerate(states):
                        s._set__ival(n)

                else:
                    raise ValueError("Values must be Symbols or strings")
            
             else:
                raise E.AlphabetError("The values must all be different.")
        else:
            raise E.AlphabetError(\
            "The values must be an integer, a list or a tuple.")

        self.__states = states

# FIXME: Not sure this is useful
        # When an alphabet is associated to a sequence it cannot be modified.
        # self.__islinked = False

## FIXME:
## Just in case...
#        self.__ditos = dict([(s.ival, s.strval) for s in self.__states])
#        self.__dstoi = dict([(s.strval, s.ival) for s in self.__states])

    def __str__(self):
        return 'Alphabet['+', '.join([s.__str__() for s in self.__states])+']'

    def __repr__(self):
        return 'Alphabet['+', '.join([s.__repr__() for s in self.__states])+']'

    def __len__(self):
        return len(self.__states)

    def __eq__(self, other):

        if len(self) != len(other):
            return False
        else:
            return all([sstate == ostate for sstate, ostate in zip(self, other)]) 

    def __getitem__(self, key):
        return self.__states[key]

    def __setitem__(self, key, value):

# FIXME: Not sure this is useful
#        if self.__islinked:
#            raise E.AlphabetError(\
#            'The alphabet is linked to a sequence and cannot be modified')

        if type(value) == Symbol:
            if value.ival is None:
                if all([value.strval != s.strval for s in self.__states]):
                    self.__states[key] = value
                    self.__states[key]._set__ival(key)
                else:
                    raise ValueError('The Symbol already exists')
            else:
                raise ValueError(\
                'The Symbol is already associated to an integer')
        else:
            raise ValueError("Alphabet contains only Symbols") 
    

    @property
    def states(self):
        return tuple(s for s in self.__states)
    
    @property
    def strvals(self):
        return tuple([s.strval for s in self.__states])

#    @strvals.setter
#    def strvals(self, value):
#        self.__strval = str(value)

#    @strvals.deleter
#    def strval(self):
#        raise KeyError("Cannot delete the name of a state")

    @property
    def ivals(self):
        return tuple([s.ival for i in __states])

#    @ivals.setter
#    def ival(self, value):
#        raise TypeError("Cannot change the ival of a state")
#
#    @ivals.deleter
#    def ival(self):
#        raise TypeError("Cannot delete the ival of a state")
#
#    def get_ivals(self):
#        return tuple([s._ival for s in self])
#    ivals = property(fget=get_ivals)
#    
#    def get_strvals(self):
#        return tuple([s.strval for s in self])
#    strvals = property(fget=get_strvals)
#
#    def items(self):
#        return zip(self.ivals, self.strvals)
#        # FIXME: get a dict for each index?
##        for index in range(len(self)):
##            yield self[index]._ival, self[index].strval
#
# Binary_Alphabet = Alphabet(('False', 'True'))

# FIXME: this is not the definitive implementation.
# we have to think about it...
# can we just enumerate a list or tuple?
    def rename(self, replacement):
        # replacement is the dictionnary that contains the symbols that we want to modify
        if type(replacement) != dict :
            raise TypeError ('The input must be a dictionnary')
        else:
            for k, v in replacement.items():
                self[k] = Symbol(v)
            # for el in remplacement :
                #self.__setitem__(el, Symbol(remplacement[el]))

class Sequence(object):
    """
    Defines a symbolic sequence coded using integers in :math:`{0,
    k-1}` and their methods.
    
    Test for the Sequence class and its methods

    >>> a = [1,0,0,0,1,0,1,0,1,1,0,1]
    >>> b = [0,1,0,0,1,1,1,1,0,0,1,0]
    >>> A = Alphabet(['a','b'])
    >>> s1 = Sequence(a,A)
    >>> s2 = Sequence(b,A)
    >>> s1
    Sequence: [1 0 0 0 1 0 1 0 1 1 0 1]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 12 ; k = 2
    >>> print(s1)
    [1 0 0 0 1 0 1 0 1 1 0 1]

    The length of the alphabet is a property named `k` of the sequence.

    >>> s1.k
    2
    >>> s1.alphabet
    Alphabet[Symbol(0 | a), Symbol(1 | b)]

    Slices return Sequence object

    >>> s1[0]
    Sequence: [1]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 1 ; k = 2
    >>> s1[4:8]
    Sequence: [1 0 1 0]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 4 ; k = 2
    >>> s1[s1.ivals < 1]
    Sequence: [0 0 0 0 0 0]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 6 ; k = 2

    We can access to the lenght of a sequence

    >>> len(s1)
    12

    Concatenation of two sequences return Sequence object if the alphabet of the two sequences are the same

    >>> s1 + s2
    Sequence: [1 0 0 0 1 0 1 0 1 1 0 1 0 1 0 0 1 1 1 1 0 0 1 0]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 24 ; k = 2

    Comparison between two sequences with the same length returns a Sequence object with the results of the comparison

    >>> s1 == s2
    Sequence: [0 0 1 1 1 0 1 0 0 0 0 0]
    Alphabet[Symbol(0 | False), Symbol(1 | True)]
    N = 12 ; k = 2
    >>> s1 > s2
    Sequence: [1 0 0 0 0 0 0 0 1 1 0 1]
    Alphabet[Symbol(0 | False), Symbol(1 | True)]
    N = 12 ; k = 2
    >>> s1 >= s2
    Sequence: [1 0 1 1 1 0 1 0 1 1 0 1]
    Alphabet[Symbol(0 | False), Symbol(1 | True)]
    N = 12 ; k = 2
    >>> s1 < s2
    Sequence: [0 1 0 0 0 1 0 1 0 0 1 0]
    Alphabet[Symbol(0 | False), Symbol(1 | True)]
    N = 12 ; k = 2
    >>> s1 <= s2
    Sequence: [0 1 1 1 1 1 1 1 0 0 1 0]
    Alphabet[Symbol(0 | False), Symbol(1 | True)]
    N = 12 ; k = 2
    >>> s1 != s2
    Sequence: [1 1 0 0 0 1 0 1 1 1 1 1]
    Alphabet[Symbol(0 | False), Symbol(1 | True)]
    N = 12 ; k = 2

    With binary sequences, logical operators return e Sequence object with the result

    >>> s1 & s2
    Sequence: [0 0 0 0 1 0 1 0 0 0 0 0]
    Alphabet[Symbol(0 | False), Symbol(1 | True)]
    N = 12 ; k = 2
    >>> s1 ^ s2
    Sequence: [1 1 0 0 0 1 0 1 1 1 1 1]
    Alphabet[Symbol(0 | False), Symbol(1 | True)]
    N = 12 ; k = 2
    >>> s1 | s2
    Sequence: [1 1 0 0 1 1 1 1 1 1 1 1]
    Alphabet[Symbol(0 | False), Symbol(1 | True)]
    N = 12 ; k = 2

    It is possible to transform a sequence in place

    >>> s1.roll(2)
    >>> s1
    Sequence: [0 1 1 0 0 0 1 0 1 0 1 1]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 12 ; k = 2
    >>> s1.reverse()
    >>> s1
    Sequence: [1 1 0 1 0 1 0 0 0 1 1 0]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 12 ; k = 2
    >>> s1.reduce()
    >>> s1
    Sequence: [1 0 1 0 1 0 1 0]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 8 ; k = 2

    And we can do the same creating a new sequence modified from a base sequence

    >>> s3 = roll(s2,12)
    >>> s3
    Sequence: [0 1 0 0 1 1 1 1 0 0 1 0]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 12 ; k = 2
    >>> s3 = reduce(s2)
    >>> s3
    Sequence: [0 1 0 1 0 1 0]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 7 ; k = 2
    >>> s3 = reverse(s2)
    >>> s3
    Sequence: [0 1 0 0 1 1 1 1 0 0 1 0]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 12 ; k = 2

    This functions provide us information about a sequence

    >>> s1.count()
    array([4, 4])
    >>> s1.frequency()
    array([0.5, 0.5])
    >>> issequence(s2)
    True

    From a list of sequences of the same length but that can have different alphabets, we can recode them creating a new sequence with new symbols and a new alphabet

    >>> B = Alphabet(['aa','bb','cc'])
    >>> s4 = Sequence([2,2,1,0,2,0,0,1,2,1,0,0],B)
    >>> s4
    Sequence: [2 2 1 0 2 0 0 1 2 1 0 0]
    Alphabet[Symbol(0 | aa), Symbol(1 | bb), Symbol(2 | cc)]
    N = 12 ; k = 3
    >>> s2
    Sequence: [0 1 0 0 1 1 1 1 0 0 1 0]
    Alphabet[Symbol(0 | a), Symbol(1 | b)]
    N = 12 ; k = 2
    >>> s3 = recode([s2,s4], new_alphabet=True, names=['seq2','seq4'])
    >>> s3
    Sequence: [2 5 1 0 5 3 3 4 2 1 3 0]
    Alphabet[Symbol(0 | seq2_a+seq4_aa), Symbol(1 | seq2_a+seq4_bb), Symbol(2 | seq2_a+seq4_cc), Symbol(3 | seq2_b+seq4_aa), Symbol(4 | seq2_b+seq4_bb), Symbol(5 | seq2_b+seq4_cc)]
    N = 12 ; k = 6

    """
    def __init__(self, symbols, alphabet, dtype=DEFAULT_DTYPE, check=True):
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
        """
        if isinstance(symbols, Sequence):
            self.__init__(np.copy(symbols.__ivals), \
                          copy.deepcopy(symbols.alphabet))
        else:
            if dtype not in DTYPES:
                raise TypeError(\
                        'Wrong dtype. Maybe you entered both alphabet and its length.')
            symbols = np.array(symbols)
            # Check if data can be represented in the dtype
            if np.any(symbols < np.iinfo(dtype).min) or \
               np.any(symbols > np.iinfo(dtype).max):
                raise E.SymbolError(\
                      'Data can not be represented in %s' % str(dtype))
            # Check the dimension of the data
            if len(symbols.shape) != 1: # 1D sequences for now
                raise E.ShapeError(\
                      'Data shape is not one-dimensional')
            self.__ivals = np.asarray(symbols).astype(dtype)
            # Parse the alphabet
            if isinstance(alphabet, Alphabet):
                self.__alphabet = copy.deepcopy(alphabet)

# FIXME: is the islinked is useful?
#                self.__alphabet.__islinked = True

            elif type(alphabet) == int :
                # self._alphabet = Alphabet(alphabet)
                self.__alphabet = Alphabet(alphabet)
            else:
                raise TypeError('The parameter alphabet must be an integer or a sequence.Alphabet object')
            # Check correspondence between symbols and alphabet
            if check:
                if (max(self.__ivals) >= len(self.__alphabet)): 
                    raise E.AlphabetError("Invalid alphabet length")

## Alphabet property

    @property
    def alphabet(self):
        return self.__alphabet

    @property
    def k(self):
        return len(self.alphabet)

    @property
    def ivals(self):
        vals = np.array(self.__ivals)
        vals.flags.writeable = False
        return vals

    @property
    def strvals(self):
        # FIXME: check .flags.writeable = False as for ivals.
        return np.array([self.alphabet[i].strval for i in self.__ivals])

# Copy method
    def __deepcopy__(self, memo):
        """
        Returns a copy of the Sequence object
        """
        return Sequence(np.copy(self.__ivals), \
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
        return len(self.__ivals)

    def __getitem__(self, key):
        """
        Allows to slice a sequence. Can be sliced with an int, a slice or an
        ndarray 
        """
        if type(key) is int:
            tmpval = [self.__ivals[key]]
        elif type(key) is slice:
            tmpval = self.__ivals[key]
        elif type(key) is np.ndarray:
            # print(key, type(key))
            tmpval = self.__ivals[np.where(key)[0]]
        elif type(key) is Sequence:
            tmpval = self.__ivals[np.where(key.__ivals)[0]]
        else:
            print(key, type(key))
            raise ValueError("Cannot slice with %s" % str(type(key)))

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
        return self.__ivals.__iter__()

    def iteritems(self):
        return zip(self.__ivals, self.strvals)

    def iterivals(self):
        return self.__ivals.__iter__()

    def iterstrvals(self):
        return self.strvals.__iter__()

## FIXME:
## I do not know when this is really used... for checking reversibility etc.
#    def __reversed__(self): # returns an iterator
#        """
#        Returns an iterator on the Sequence in the reverse order
#        """
#        # return np.flipud(self.ivals).__iter__()
#
#        # return zip(np.flipud(self.ivals), np.flipud(self.strvals))
##        raises:
##        AttributeError: property 'ivals' of 'Sequence' object has no setter


# "numeric" operations

    def __add__(self, other):
        """
        Allows to add two sequences: they are concatenated

        :raises:
           :exc:`ValueError`: when the alphabets are different
        """
        if (self.alphabet != other.alphabet):
            raise ValueError('Alphabets are different')
        else:
            return Sequence(np.concatenate((self.__ivals, other.__ivals)), \
                            self.alphabet, check=False)

# Logical operations
# FIXME: 
# np.logical_? are defined for any array. Why do we check binary?
# This is strange to change logical_? to operators, no?

    def __and__(self, other):
        """
        Returns a binary sequence which is the result of comparison with `&`

        .. seealso::
           numpy.logical_and

        .. caution::
           This corresponds to the `&` operator and not the `and` keyword.
        """
        # if self._alen != 2 or other._alen != 2:
        if self.k != 2 or other.k != 2:
            raise NotImplementedError('& is defined for binary sequences only')
        else:
            seq = np.logical_and(self.__ivals, other.__ivals)
            return Sequence(seq.astype(self.__ivals.dtype), Alphabet(('False', 'True')), \
                            check=False)

    def __or__(self, other):
        """
        Returns a binary sequence which is the result of comparison with `|`

        .. seealso::
           numpy.logical_or

        .. caution::
           This corresponds to the `|` operator and not the `or` keyword.
        """
        # if self._alen != 2 or other._alen != 2:
        if self.k != 2 or other.k != 2:
            raise NotImplementedError('| is defined for binary sequences only')
        else:
            arr = np.logical_or(self.__ivals, other.__ivals)
            return Sequence(arr.astype(self.__ivals.dtype), Alphabet(('False', 'True')), \
                            check=False)

    def __xor__(self, other):
        """
        Returns a binary sequence which is the result of comparison with `^`

        .. seealso::
           numpy.logical_xor

        .. caution::
           This corresponds to the `^` operator.
        """
        # if self._alen != 2 or other._alen != 2:
        if self.k != 2 or other.k != 2:
            raise NotImplementedError('| is defined for binary sequences only')
        else:
            arr = np.logical_xor(self.__ivals, other.__ivals)
            return Sequence(arr.astype(self.__ivals.dtype), Alphabet(('False', 'True')), \
                            check=False)

# Rich comparison methods"

    def __mkcomp__(self, other, op): 

        if isinstance(other, Sequence):
            if self.alphabet == other.alphabet:
                if len(other) == len(self):
                    arr = op(self.__ivals, other.__ivals)
                else:
                    raise \
                    ValueError('Cannot compare Sequences with different lengths')
            else:
                raise \
                ValueError('Cannot compare Sequences with different alphabets')

        elif isinstance(other, int) and other >= 0:
                arr = op(self.__ivals, other)
        else:
            raise \
            ValueError("Sequence can be compared with a Sequence or a positive integer only")

        return Sequence(arr.astype(self.__ivals.dtype), Alphabet(('False', 'True')), check=False)

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

# Methods that transform the sequence IN PLACE
    def roll(self, step):
        """
        Roll the sequence *in place*

        .. seealso::
           numpy.roll function
        """
        self.__ivals = np.roll(self.__ivals, step)

    def reverse(self):
        """
        Reverse the sequence *in place*

        .. seealso::
           numpy.flipud function
        """
        self.__ivals = np.flipud(self.__ivals)

    def shuffle(self):
        """
        Shuffle the order of the sequence *in place*.
        
        .. seealso:: 
           numpy.random.shuffle function
        """
        np.random.shuffle(self.__ivals)

    def reduce(self):
        """
        Delete the repetitions of symbols in a sequence *in place*
        """
        #diff = np.diff(self.ivals)
        diff = np.ediff1d(self.__ivals)
        bool_idx = list(diff!=0)
        bool_idx.append(True)
        self.__ivals = self.__ivals[bool_idx]
        # self.ivals = np.hstack((self.ivals[diff!=0], self.ivals[-1]))

# Methods that compute characteristics of the sequence

    def count(self, ival=None):
        """
        Counts the number of each symbol in :math:`{0, k-1}` if code is None
        or the number of the code symbol

        :returns: a numpy.ndarray of integers
        """
        if ival is None:
            return np.array([len(np.where(self.__ivals == i)[0]) \
                                   for i in range(self.k)])  
        else:
            assert(type(code) is int)
            return len(np.where(self.__ivals == ival)[0])

    def frequency(self):
        """
        Returns the probability of each symbol in :math:`{0, k-1}`

        :returns: a numpy.ndarray of floats
        """
        return self.count() / float(len(self))

#-----------------------------
# Functions (return sequences)
#-----------------------------

def roll(seq, step):
    """
    Roll the sequence
    """
    newseq = copy.deepcopy(seq)
    newseq.roll(step)
    return newseq

def reverse(seq):
    """
    Reverse the sequence
    """
    newseq = copy.deepcopy(seq)
    newseq.reverse()
    return newseq

def shuffle(seq):
    """
    Shuffle the sequence
    """
    newseq = copy.deepcopy(seq)
    newseq.shuffle()
    return newseq

def reduce(seq):
    """
    Returns a reduced sequence (ie only keep the transitions)
    """
    newseq = copy.deepcopy(seq)
    newseq.reduce()
    return newseq

def issequence(obj):
    """
    Returns True if x is a symbolic sequence
    """
    return isinstance(obj, Sequence) 

def transform(seq, correspondance, new_alphabet=None):
    """
    Transforms the initial sequence according to the correspondence iterable
    """
    if len(correspondance) != len(seq.alphabet):
        raise ValueError('Correspondence does not match sequence alphabet')

    # if (not all([type(c) is str for c in correspondance])) and \
       #(not all([type(c) is Symbol for c in correspondance])) and \
    if (not all([type(c) is int for c in correspondance])):
       # raise ValueError('Correspondences are strings, ints or Symbols.')
       raise ValueError('Correspondences are given as integers.')

    if new_alphabet is None:
        alphabet = Alphabet(list(set(correspondance)))
    else:
        if type(new_alphabet) is not Alphabet:
           raise E.AlphabetError('New alphabet should be an Alphabet object')
        elif len(set(correspondance)) != len(new_alphabet):
           raise 
           E.AlphabetError('Length of new alphabet does not fit the correspondance length.')
        else:
            alphabet = new_alphabet
            nb_symbols = len(alphabet)

    if all([type(c) is int for c in correspondance]):     
        # make sure that corresp is [0, k-1]
        # FIXME: make a better test... 
        if min(correspondance) != 0 or max(correspondance) != nb_symbols - 1:
             raise ValueError('Correspondence should be [0, k-1]') 

#    if new_alphabet is not None and len(set(correspondance)) != len(new_alphabet): 
# #        alphabet = Alphabet(new_alphabet) 
# #    if new_alphabet is not None and len(set(correspondance)) != len(new_alphabet): 
#        raise ValueError(\ 
#            'New alphabet and correspondence table do not match')     
# ivals = np.array([alphabet[idx]._ival for idx in seq.ivals]).astype(seq.ivals.dtype)

    ivals = [alphabet[correspondance[idx]].ival for idx in seq.ivals]

    return Sequence(np.array(ivals).astype(seq.ivals.dtype), alphabet) 

def recode(lseq, new_alphabet=False, sep='+', names=None):
    """
    Recodes a list of sequences with (possibly) different alphabets but
    with the same length (This is an error to pass Sequences with different
    length.) A new dictionnary is built for the new sequence.

    :param lseq: a list of Sequences

    :raises:
       :exc:`LengthError`: when the length of the Sequences are different.

    :returns: a Sequence
    """    
    if not all([len(seq) == len(lseq[0]) for seq in lseq]):
        raise E.LengthError("Sequence should have the same length") 

    # The alphabet size of the recoded sequence is an extension of the alphabet 
    # within the original sequences list. This is equivalent to numbering
    # items in n-dimensional (n=nbseq) tables each dimension has k cases.
    # The convention: we use the lexicographic order from left to right; the
#    # highest weight is on the left (ie index 0) the lower on the right (ie
#    # index -1)
#
#    allk = [seq._alen for seq in lseq]
    allk = [seq.k for seq in lseq]
#    new_alen = np.prod(allk)
    new_k = np.prod(allk)
#
#    # recode each word as an integer as a matrix product of the matrix of
#    # the sequences and a kernel 
    symbolic_matrix = np.vstack([seq.ivals for seq in lseq]).T
    allk.reverse()
    kernel = np.cumprod(allk)
    kernel = np.flipud(np.insert(kernel[:-1], 0, 1))
    new_s = np.dot(symbolic_matrix, kernel).astype(int)
#
#    # construction of the new alphabet
    if new_alphabet: # and all([type(alpha) is not int for alpha in alld]):
#        
        if names is None:
            raise ValueError('Names should be the same length as lseq')
        else:
            alld = []
            for seq, name in zip(lseq, names):
                alld.append(['_'.join((name, anitem.strval)) for anitem in seq.alphabet])
#
        new_alphabet = []
        for pp in itertools.product(*alld):
            strlist = [jj for jj in pp]
            new_alphabet.append(sep.join(strlist))
#
        # return Sequence(new_s, new_alphabet, check=False)
        return Sequence(new_s, Alphabet(new_alphabet), check=False)
#
    else:
        # return Sequence(new_s, int(new_alen), check=False)
        return Sequence(new_s, Alphabet(int(new_k)), check=False)

def words(seq, wlen, new_alphabet=False):
    """
    Returns a sequence encoded according to the m-words in seq

    .. todo::
        Write the doc of "words"
    """
    assert wlen > 0, 'Word length should be > 0.'
    slen = len(seq)
    lseq = [seq[i:slen-wlen+i+1] for i in range(wlen)]

    return recode(lseq, new_alphabet=new_alphabet)

#def from_iterable(val, valrange):
#    """
#    Map a set of values to symbolic coding (i.e. integers between 0 and k-1)
#    """
#    lrange = list(valrange)
#    symb = [lrange.index(tmp) for tmp in val]
#    return Sequence(symb, len(lrange))

#def visited_states(seq, sort=True):  #, meaning=True, complete=False, ordering=True):
#    """
#    Returns the set of visited symbols ie those that really appear in
#    the sequence.
#
#    :returns: a numpy.ndarray of integers
#
#    .. todo:: 
#       should we had frequencies, etc?
#
#    .. todo:: 
#       should we return a sequence, with alphabet?
#    """
#    freq = S.frequency()
#    # alph_ivals = seq.alphabet.ivals
#    # alph_strvals = seq.alphabet.strvals
#    alphabet = seq.alphabet
#    if sort:
#        lsort = list(np.argsort(freq))
#        lsort.reverse() # decreasing order *in place*!!!!
#        # FIXME: lsort elements have type numpy.int64 which is not directly usable for
#        # indexing Alphabet. See the __index__ method for that.
#        # so here is a local hack which might be generalized if needed...
#        # return [(alph_ivals[idx], freq[idx], alph_strvals[idx]) for idx in lsort]
#        indices = [int(i) for i in lsort]
#        return [(alphabet[idx], freq[idx]) for idx in indices]
#    else:
#        return list(zip(alphabet, freq))
#
#    # alpha = list(range(seq.alen))
##    if seq.alphabet is None:
##        return [(alpha[index], frequencies[index], None) for index in lsort]
##    else:
##        return [(alpha[index], frequencies[index], seq.alphabet[index]) \
##                for index in lsort]

if __name__ == "__main__":
    import doctest
    doctest.testmod()


