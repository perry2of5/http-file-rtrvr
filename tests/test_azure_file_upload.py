from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.uploader.azure.file_to_azure_blob_uploader import FileToAzureBlobUploader
from http_file_rtrvr.constants import FileType

from datetime import datetime
import pytest

class TestBlobUploadingInFileToAzureBlobUploader:
    account_url = "https://devtimstoregrp1.blob.core.windows.net"
    cntnr_name = "testcontainer"
    
    def test_blob_key_with_save_to_and_archive_local_path(self):
        uploader = FileToAzureBlobUploader(self.account_url, self.cntnr_name)
