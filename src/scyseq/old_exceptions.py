"""
This is the exception handling for symbolic sequences
"""
# scyseq/exceptions.py

class ScySeqError(Exception):
    """Base exception for all errors raised by the scyseq library."""
    pass


# === Erreurs liées à l'alphabet ===
class AlphabetError(ScySeqError):
    """Base exception for alphabet-related issues."""
    pass

class InvalidSymbolError(AlphabetError):
    """Raised when an invalid symbol is used."""
    pass

class EmptyAlphabetError(AlphabetError):
    """Raised when attempting to use an empty alphabet."""
    pass


# === Erreurs liées aux séquences ===
class SequenceError(ScySeqError):
    """Base exception for sequence-related issues."""
    pass

class SequenceParseError(SequenceError):
    """Raised when parsing a sequence fails."""
    pass

class SymbolMismatchError(SequenceError):
    """Raised when a sequence contains symbols not in the alphabet."""
    pass

#FIXME: How can we get the expression that call  

class Error(Exception):
    """
    This exception does nothing. 

    I found "Exception handling" in "Python tutorial" and just copied the
    examples.

    .. todo::
       Understand better "Exception handling" chapter and make better
       exception handling in the whole package.  
    """ 
    pass

class ShapeError(Error):
    """
    This exception is used when the length of the alphabet causes an error.
    """
    def __init__(self, message):
        """
        Init the exception

        .. todo::
           Can we deal with the expression as in the "Python tutorial"
        """
        self.message = message
        #self.expression = expression
    def  __str__(self):
        return self.message

class SymbolError(Error):
    """
    This exception is used when the length of the alphabet causes an error.
    """
    def __init__(self, message):
        """
        Init the exception

        .. todo::
           Can we deal with the expression as in the "Python tutorial"
        """
        self.message = message
        #self.expression = expression
    def  __str__(self):
        return self.message

class AlphabetError(Error):
    """
    This exception is used when the length of the alphabet causes an error.
    """
    def __init__(self, message):
        """
        Init the exception

        .. todo::
           Can we deal with the expression as in the "Python tutorial"
        """
        self.message = message
        #self.expression = expression
    def  __str__(self):
        return self.message

class LengthError(Error):
    """
    This exception is used when the length of the sequence causes an error.
    """
    def __init__(self, message):
        self.message = message
    def  __str__(self):
        return self.message

class DictionaryError(Error):
    """
    This exception is used when the dictionary causes an error.
    """
    def __init__(self, message):
        self.message = message
    def  __str__(self):
        return self.message

