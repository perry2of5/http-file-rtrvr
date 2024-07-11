from http_file_rtrvr.retrieval_svc import RetrievalSvc
from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.constants import SvcReturnCode
from http_file_rtrvr.constants import SupportedHttpMethod


def test_missing_url_returns_0010():
    no_url_req = RetrievalRequest(url=None, method=SupportedHttpMethod.GET)
    assert SvcReturnCode.INVALID_REQ == RetrievalSvc().retrieve(no_url_req)


def test_download_example_com_index_html_returns_0000():
    example_com_index_html_url = RetrievalRequest(
        url="https://example.com/index.html",
        method=SupportedHttpMethod.GET,
        timeout_seconds=5)
    assert SvcReturnCode.SUCCESS == RetrievalSvc().retrieve(
        example_com_index_html_url)
