from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from http_file_rtrvr.constants import FileType, SupportedHttpMethod, SvcReturnCode


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class RetrievalResponse:
    source_url: str
    status: SvcReturnCode
    file_type: FileType
    method: SupportedHttpMethod
    saved_to: str = ""