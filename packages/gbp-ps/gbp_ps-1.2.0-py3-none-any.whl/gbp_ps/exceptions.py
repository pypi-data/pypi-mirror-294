"""gbp-ps exceptions"""


class GBPPSException(Exception):
    """Base exception for gbp-ps"""


class RecordNotFoundError(GBPPSException, LookupError):
    """Raised when a record is not found in the repository"""


class RecordAlreadyExists(GBPPSException):
    """Raised when adding a record that already exists in the repository"""


class UpdateNotAllowedError(GBPPSException):
    """Raised when an update is not allowed"""
