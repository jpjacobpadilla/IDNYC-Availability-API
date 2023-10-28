class HttpRequestError(Exception):
    """Custom exception for HTTP request errors."""
    
    def __init__(self, status_code: int):
        super().__init__(f'The HTTP request responded with a status code of {status_code}')