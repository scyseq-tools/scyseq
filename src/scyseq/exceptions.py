"""
Exception classes for the scyseq library.
"""

# FIXME: this is just to avoid forgetting the __all__ at the end... (and save
# time for the next time...)
_PUBLIC_API_ = [
    "ScyseqError",
    "SymbolError", "SymbolDefinitionError", "SymbolAccessError",
    "AlphabetError", "AlphabetAccessError", "InvalidSymbolError", "EmptyAlphabetError",
    "SequenceError", "SequenceParseError", "SymbolMismatchError",
]

class ScyseqError(Exception):
    """Base exception for all errors raised by the scyseq library."""
    pass

# === Symbol-related errors ===

class SymbolError(ScyseqError):
    """Base exception for symbol-related issues."""
    pass

class SymbolDefinitionError(SymbolError):
    """Exception raised when a symbol cannot be defined."""
    def __init__(self, value, msg):
        super().__init__(msg)
        self.value = value

class SymbolAccessError(SymbolError):
    """Exception raised when a symbol cannot be accessed."""
    def __init__(self, msg):
        super().__init__(msg)

# === Alphabet-related errors ===

class AlphabetError(ScyseqError):
    """Base exception for alphabet-related issues."""
    pass

class AlphabetAccessError(AlphabetError):
    """Exception raised when an alphabet cannot be accessed."""
    def __init__(self, msg):
        super().__init__(msg)

class InvalidSymbolError(AlphabetError):
    """Raised when an invalid symbol is used in an alphabet or sequence."""
    def __init__(self, symbol, alphabet):
        msg = f"Symbol '{symbol}' is not part of the allowed alphabet: {alphabet}"
        super().__init__(msg)
        self.symbol = symbol
        self.alphabet = alphabet


class EmptyAlphabetError(AlphabetError):
    """Raised when attempting to use an empty alphabet."""
    def __init__(self):
        super().__init__("The alphabet must not be empty.")


# === Sequence-related errors ===

class SequenceError(ScyseqError):
    """Base exception for sequence-related issues."""
    pass


class SequenceParseError(SequenceError):
    """Raised when parsing a sequence fails due to invalid format."""
    def __init__(self, sequence, message="Unable to parse sequence."):
        super().__init__(f"{message} Input: {sequence}")
        self.sequence = sequence


class SymbolMismatchError(SequenceError):
    """Raised when a sequence contains symbols not in the defined alphabet."""
    def __init__(self, sequence, invalid_symbols):
        msg = f"Sequence contains invalid symbols: {invalid_symbols}"
        super().__init__(msg)
        self.sequence = sequence
        self.invalid_symbols = invalid_symbols


__all__ = _PUBLIC_API_

