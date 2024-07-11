from http_file_rtrvr.uploader.abstract_file_tree_uploader import AbstractFileTreeUploader
from http_file_rtrvr.uploader.abstract_file_uploader import AbstractFileUploader
from http_file_rtrvr.retrieval_request import RetrievalRequest

from datetime import datetime
import os

class DirectoryUploader(AbstractFileTreeUploader):
    """
    This class uploads file from a directory using an AbstractFileUploader. It should should succeed
    in uploading all files in the directory or throw an exception.

    Args:
        None

    Attributes:
        None

    Methods:
        upload_directory: Uploads a directory to Azure Blob Storage.

    Usage:
        None: use a subclass such as DirectoryToBlobUploader
    """

    def __init__(self, file_uploader: AbstractFileUploader):
        super().__init__()
        self.file_uploader = file_uploader
        pass

    def upload_file_tree(
            self, 
            file_tree_path: str,
            rtrvl_req: RetrievalRequest,
            download_time: datetime) -> str:
        """
        Uploads the contents of a file tree (directory, zip, etc.) to a blob storage.

        Args:
            directory_path (str): The path of the base directory to be uploaded. Uploads walk 
                    the tree of files and upload all files found replicating the folder structure
                    remotely.
            rtrvl_req (RetrievalRequest): The retrieval request object containing the requested URL
                    and the save_to prefix.
            download_time (datetime): The timestamp of the download.

        Returns:
            the fully-qualified URL of the uploaded root of directory tree in Azure storage
            containers, S3, or whatever.
        """
        self._upload_directory(file_tree_path, rtrvl_req, download_time, "")
        return self.file_uploader.fully_qualified_upload_path(download_time, rtrvl_req, None)


    def _upload_directory(
            self, 
            file_tree_path: str,
            rtrvl_req: RetrievalRequest,
            download_time: datetime,
            context_path: str) -> None:
        print("uploading directory", file_tree_path)
        for file in os.listdir(file_tree_path):
            fq_file_path = os.path.join(file_tree_path, file)
            # If type of file is directory, call the function recursively, otherwise upload.
            if os.path.isdir(fq_file_path):
                print("Recursing into", file)
                self._upload_directory(fq_file_path, rtrvl_req, download_time, os.path.join(context_path, file))
            else:
                print("uploading file", fq_file_path)
                upload_path = self.file_uploader.upload_path(download_time, rtrvl_req, os.path.join(context_path, file))
                self.file_uploader.upload(fq_file_path, upload_path, rtrvl_req, download_time)
