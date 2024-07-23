from enum import Enum


class SvcReturnCode(Enum):
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
    OPERATION_UNSUPPORTED = '9999'


class SupportedHttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'

class FileType(Enum):
    SIMPLE_FILE = 'simple'
    ZIP_FILE = 'zip'
    TAR_FILE = 'tar'
    GZIP_FILE = 'gz'
    GZIPPED_TAR_FILE = 'tgz'
