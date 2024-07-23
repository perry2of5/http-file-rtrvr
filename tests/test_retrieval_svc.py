from http_file_rtrvr.retrieval_svc import RetrievalSvc
from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.constants import FileType, SvcReturnCode, SupportedHttpMethod
from tests.svc_mocks.always_succeed_file_uploader import AlwaysSucceedFileUploader
from tests.svc_mocks.always_succeed_file_tree_uploader import AlwaysSucceedFileTreeUploader

def test_missing_url_returns_0010():
    no_url_req = RetrievalRequest(
        url=None,
        method=SupportedHttpMethod.GET,
        save_to='some/prefix',
        file_type=FileType.SIMPLE_FILE)
    rtrvl_svc = RetrievalSvc(AlwaysSucceedFileUploader(), AlwaysSucceedFileTreeUploader())
    assert SvcReturnCode.INVALID_REQ == rtrvl_svc.retrieve(no_url_req)


def test_download_example_com_index_html_returns_0000():
    example_com_index_html_url = RetrievalRequest(
        url="https://example.com/index.html",
        method=SupportedHttpMethod.GET,
        timeout_seconds=5,
        save_to='some/prefix',
        file_type=FileType.SIMPLE_FILE)
    rtrvl_svc = RetrievalSvc(AlwaysSucceedFileUploader(), AlwaysSucceedFileTreeUploader())
    assert SvcReturnCode.SUCCESS == rtrvl_svc.retrieve(
        example_com_index_html_url)
