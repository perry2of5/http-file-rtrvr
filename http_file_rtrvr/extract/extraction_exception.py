class ExtractionException(Exception):
    def __init__(self, message, cause=None):
        self.message = message
        self.cause = cause
        super(Exception, self).__init__(message, cause)

 