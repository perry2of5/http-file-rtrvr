from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.uploader.azure.file_to_azure_blob_uploader import FileToAzureBlobUploader
from http_file_rtrvr.constants import FileType

from datetime import datetime
import pytest

class TestBlobKeyGenerationFileToAzureBlobUploader:
    account_url = "https://devtimstoregrp1.blob.core.windows.net"
    cntnr_name = "testcontainer"
    
    def test_upload_path_with_save_to_and_archive_local_path(self):
        uploader = FileToAzureBlobUploader(self.account_url, self.cntnr_name)
        save_to = "save_to_dir"
        download_time = datetime(2023, 3, 9, 8, 7, 1)
        target_url_path = "fake/path/to/archive.zip"
        local_path = "dir1/example1.txt"

        rtrvl_req = RetrievalRequest(
            "http://example.com/" + target_url_path,
            save_to,
            FileType.SIMPLE_FILE)
                                     
        expected_upload_path = "/".join([
            save_to,
            "2023-03-09T08-07-01",
            target_url_path,
            local_path
        ])
        
        upload_path = uploader.upload_path(download_time, rtrvl_req, local_path)
        print("actual:  ", upload_path)
        print("expected:", expected_upload_path)
        assert upload_path == expected_upload_path


    def test_upload_path_with_no_save_to_and_archive_local_path(self):
        uploader = FileToAzureBlobUploader(self.account_url, self.cntnr_name)
        save_to = None
        download_time = datetime(2023, 3, 9, 8, 7, 1)
        target_url_path = "fake/path/to/archive.zip"
        local_path = "dir1/example1.txt"

        rtrvl_req = RetrievalRequest(
            "http://example.com/" + target_url_path,
            save_to,
            FileType.SIMPLE_FILE)
                                     
        expected_upload_path = "/".join([
            "2023-03-09T08-07-01",
            target_url_path,
            local_path
        ])
        
        upload_path = uploader.upload_path(download_time, rtrvl_req, local_path)
        print("actual:  ", upload_path)
        print("expected:", expected_upload_path)
        assert upload_path == expected_upload_path

    def test_upload_path_with_no_save_to_and_no_archive_local_path(self):
        uploader = FileToAzureBlobUploader(self.account_url, self.cntnr_name)
        save_to = None
        download_time = datetime(2023, 3, 9, 8, 7, 1)
        target_url_path = "fake/path/to/archive.zip"
        local_path = None

        rtrvl_req = RetrievalRequest(
            "http://example.com/" + target_url_path,
            save_to,
            FileType.SIMPLE_FILE)
                                     
        expected_upload_path = "/".join([
            "2023-03-09T08-07-01",
            target_url_path
        ])
        
        upload_path = uploader.upload_path(download_time, rtrvl_req, local_path)
        print("actual:  ", upload_path)
        print("expected:", expected_upload_path)
        assert upload_path == expected_upload_path
