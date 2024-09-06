class CustomException(Exception):
    """
    Custom exception for handling specific errors.

    Args:
        detail (str): Detail message of the exception.
        code (int): Error code associated with the exception.
    """

    def __init__(self, detail: str, code: int):
        self.detail = detail
        self.code = code

    def __str__(self):
        return f"{self.detail} (Code: {self.code})"
