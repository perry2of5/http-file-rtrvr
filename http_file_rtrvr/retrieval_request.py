from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from http_file_rtrvr.constants import SupportedHttpMethod
from http_file_rtrvr.constants import FileType


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RetrievalRequest:
    url: str
    save_to: str = ""
    file_type: FileType = FileType.SIMPLE_FILE
    method: SupportedHttpMethod = SupportedHttpMethod.GET
    timeout_seconds: int = 5
    accept_type: str | None = None
    content_type: str | None = None
    headers: map | None = None
