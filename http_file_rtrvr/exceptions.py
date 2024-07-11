class FileUploadException(Exception):
    def __init__(
            self,
            upload_url: str,
            message: str,
            cause: Exception | None = None):
        super().__init__()
        self.upload_url = upload_url
        self.message = message
        self.cause = cause

class FileDecompressionFailedException(Exception):
    def __init__(
            self,
            message: str,
            cause: Exception | None = None):
        super().__init__(message, cause)
        self.message = message
        self.cause = cause
