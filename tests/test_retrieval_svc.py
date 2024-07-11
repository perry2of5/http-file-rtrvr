from http_file_rtrvr.retrieval_svc import RetrievalSvc
from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.svc_return_code import SvcReturnCode


def test_missing_url_returns_0010():
    no_url_req = RetrievalRequest(url=None)
    assert SvcReturnCode.INVALID_REQ == RetrievalSvc().retrieve(no_url_req)
