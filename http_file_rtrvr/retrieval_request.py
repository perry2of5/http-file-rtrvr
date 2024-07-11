from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from http_file_rtrvr.http_method import SupportedHttpMethod


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RetrievalRequest:
    url: str
    method: SupportedHttpMethod = SupportedHttpMethod.GET
    timeout_seconds: int = 5
