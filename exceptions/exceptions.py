class ValueTooSmallError(Exception):
    """Raised when the input value is too small"""
    pass


class InvalidOriginError(Exception):
    """Raised when origin is outside of matrix"""
    pass


class InvalidSubImageDimError(Exception):
    """Raised when the resolution is not divisible by the sub image dimension"""
    pass
