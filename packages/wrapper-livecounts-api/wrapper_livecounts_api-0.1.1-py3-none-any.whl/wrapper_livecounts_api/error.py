class TiktokError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RequestApiError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
