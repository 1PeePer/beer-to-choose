from fastapi import HTTPException, status

class ParserError(HTTPException):
    """Base exception for parser errors"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class ParserTimeoutError(ParserError):
    """Exception for parser timeout"""
    def __init__(self):
        super().__init__("Parser timeout exceeded")

class ParserConnectionError(ParserError):
    """Exception for parser connection errors"""
    def __init__(self):
        super().__init__("Failed to connect to the source")

class ParserValidationError(ParserError):
    """Exception for parser validation errors"""
    def __init__(self, detail: str):
        super().__init__(f"Validation error: {detail}") 