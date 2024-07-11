from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from http_file_rtrvr.constants import SupportedHttpMethod


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RetrievalRequest:
    url: str
    method: SupportedHttpMethod = SupportedHttpMethod.GET
    timeout_seconds: int = 5
