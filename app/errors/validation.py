# app/errors/validation.py


# class ValidationError(Exception):
#     """ """

class ValidationError(Exception):
    """
    """
    def __init__(self, message: str, hint: str | None = None):
        self.message = message
        self.hint = hint
        super().__init__(message)
