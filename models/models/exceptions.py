class DataDoesNotExist(Exception):
    """Raised if no data found in corresponding table"""
    pass

class ValidationError(Exception):
    """Raised when validation error occurs"""
    pass