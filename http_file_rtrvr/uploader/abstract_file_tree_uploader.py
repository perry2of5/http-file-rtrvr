import os
from http_file_rtrvr.retrieval_request import RetrievalRequest

from abc import ABC, abstractmethod

from datetime import datetime


class AbstractFileTreeUploader(ABC):
    """
    This abstract class is responsible for uploading a tree of files, such as a directory, to Azure
    Blob Storage. A subclass should succeed in uploading all files in the directory or throw an
    exception.

    Methods:
        upload_file_tree: Uploads a file tree (directory) to Azure Blob Storage. File tree was used since
                we might be uploading a zip file or contents of an SFTP server directory in the future.

    Usage:
        None: use a subclass such as DirectoryToBlobUploader
    """

    def __init__(self):
        pass

    @abstractmethod
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
            None
        """
        pass
