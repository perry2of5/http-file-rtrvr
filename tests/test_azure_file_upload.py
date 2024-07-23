from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.uploader.azure.file_to_azure_blob_uploader import FileToAzureBlobUploader
from http_file_rtrvr.uploader.directory_uploader import DirectoryUploader
from http_file_rtrvr.constants import FileType

from datetime import datetime
import pytest
from pathlib import Path
import os

class TestBlobUploadingInFileToAzureBlobUploader:
    account_url = "https://devtimstoregrp1.blob.core.windows.net"
    cntnr_name = "testcontainer2"
    
    def test_upload_local_file(self):
        """
        This test uploads a local file to Azure Blob Storage. It should show up in the container as:
        /python/files/2024-07-23T09-03-05/perry2of5/http-file-rtrvr/blob/main/tests/test_azure_file_upload.py
        """
        uploader = FileToAzureBlobUploader(self.account_url, self.cntnr_name)
        upload_dtm = datetime(2024, 7, 23, 9, 3, 5)
        rtrvl_req = RetrievalRequest(
            "https://github.com/perry2of5/http-file-rtrvr/blob/main/tests/test_azure_file_upload.py",
            "python/files")
        blob_key = uploader.upload_path(upload_dtm, rtrvl_req)
        print(Path.cwd().absolute)
        target_file = os.path.join(os.path.dirname(__file__), 'test_azure_file_upload.py')
        print("target_file:", target_file)
        uploader.upload(target_file, blob_key, rtrvl_req, upload_dtm)

    def test_upload_directory(self):
        """
        This test uploads all files in a directory to Azure Blob Storage. Files in the directory should show 
        up in the container as:
        directory/files/2024-07-23T09-03-05/some/archive.zip/*
        """
        uploader = FileToAzureBlobUploader(self.account_url, self.cntnr_name)
        dir_uploader = DirectoryUploader(uploader)
        upload_dtm = datetime(2024, 7, 23, 9, 3, 5)
        rtrvl_req = RetrievalRequest(
            url="https://example.com/some/archive.zip",
            save_to="directory/files")
        target_dir = os.path.dirname(__file__)
        print("target_dir:", target_dir)
        dir_uploader.upload_file_tree(target_dir, rtrvl_req, upload_dtm)
        
