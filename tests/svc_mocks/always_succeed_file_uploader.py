from http_file_rtrvr.uploader.abstract_file_uploader import AbstractFileUploader
from datetime import datetime
from http_file_rtrvr.retrieval_request import RetrievalRequest

class AlwaysSucceedFileUploader(AbstractFileUploader):
    mock_upload_path = "mock.test/file/location.txt"
    # list of tuples indicating the values upload has been called with in time-order
    upload_log = []
    # list of tuples indicating the values upload_path has been called with in time-order
    upload_path_log = []

    def upload(self, local_path: str, blob_key: str):
        self.upload_log.append((local_path, blob_key))
        return
    
    def upload_path(
                self, 
                download_time: datetime, 
                rtrvl_req: RetrievalRequest, 
                local_path: str | None = None) -> str:
        self.upload_path_log.append((download_time, rtrvl_req, local_path))
        return self.mock_upload_path
    
