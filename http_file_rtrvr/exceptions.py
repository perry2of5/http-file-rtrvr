class FileUploadException(Exception):
    pass

    def __init__(
            self,
            upload_url: str,
            message: str,
            cause: Exception | None):
        super(Exception, self).__init__()
        self.upload_url = upload_url
        self.message = message
        self.cause = cause


