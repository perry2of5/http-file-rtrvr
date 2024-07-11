from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from http_file_rtrvr.constants import SupportedHttpMethod
from http_file_rtrvr.constants import FileType


@dataclass
class RetrievalRequest:
    url: str
    save_to: str = ""
    file_type: FileType = FileType.SIMPLE
    method: SupportedHttpMethod = SupportedHttpMethod.GET
    timeout_seconds: int = 5
    accept_type: str | None = None
    content_type: str | None = None
    http_headers: map | None = None
    result_queue_name: str | None = None
