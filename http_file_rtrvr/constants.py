from enum import Enum

# These enums inherit from str and Enum so that the objects that use them can be serialized to JSON
# without writing a custom encoder. The str inheritance allows the enum to be serialized as a string.

class SvcReturnCode(str, Enum):
    SUCCESS = '0000'
    INVALID_REQ = '0010'
    ERR_RTRV_CREDS = '0100'
    LOGIN_ERROR = '0101'
    ACCESS_DENIED = '0102'
    FILE_NOT_FOUND = '0103'
    UNKNOWN_RETRIEVAL_ERROR = '0199'
    DECOMPRESSION_FAILED = '0200'
    MALWARE_FLAGGED = '0300'
    DOWNLOAD_FAILED = '0400'
    RESPONSE_FAILED = '0500'
    UPLOAD_FAILED = '0501'
    OPERATION_UNSUPPORTED = '9999'


class SupportedHttpMethod(str, Enum):
    GET = 'GET'
    POST = 'POST'

class FileType(str, Enum):
    SIMPLE = 'simple'
    ARCHIVE = 'archive'
