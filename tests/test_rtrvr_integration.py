# Integration tests.

from http_file_rtrvr.retrieval_svc import RetrievalSvc
from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.constants import FileType, SvcReturnCode, SupportedHttpMethod
from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.uploader.azure.file_to_azure_blob_uploader import FileToAzureBlobUploader
from http_file_rtrvr.uploader.directory_uploader import DirectoryUploader
from http_file_rtrvr.constants import FileType

account_url = "https://devtimstoregrp1.blob.core.windows.net"
cntnr_name = "testcontainer"

class TestSingleFileIntegration:

    def test_download_example_com_index_html_returns_0000(self):
        example_com_index_html_url = RetrievalRequest(
            url="https://example.com/index.html",
            method=SupportedHttpMethod.GET,
            timeout_seconds=10,
            save_to='int_single_test',
            file_type=FileType.SIMPLE)
        file_uploader_svc = FileToAzureBlobUploader(account_url, cntnr_name)
        rtrvl_svc = RetrievalSvc(file_uploader_svc, DirectoryUploader(file_uploader_svc))
        print("retrieving")
        rtrvl_result = rtrvl_svc.retrieve(example_com_index_html_url)
        assert SvcReturnCode.SUCCESS == rtrvl_result


class TestArchiveDownloadIntegration:

    def test_download_archive_returns_00000(self):
        example_com_index_html_url = RetrievalRequest(
            url="https://github.com/perry2of5/http-file-rtrvr/archive/refs/heads/main.zip",
            method=SupportedHttpMethod.GET,
            timeout_seconds=30,
            save_to='int_arch_test',
            file_type=FileType.ARCHIVE)
        file_uploader_svc = FileToAzureBlobUploader(account_url, cntnr_name)
        rtrvl_svc = RetrievalSvc(file_uploader_svc, DirectoryUploader(file_uploader_svc))
        print("retrieving")
        rtrvl_result = rtrvl_svc.retrieve(example_com_index_html_url)
        assert SvcReturnCode.SUCCESS == rtrvl_result

