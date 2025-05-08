# -*- encoding:utf8 -*-
"""
This is the exception handling for symbolic sequences
"""

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

