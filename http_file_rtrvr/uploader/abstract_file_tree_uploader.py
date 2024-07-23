import os
from http_file_rtrvr.retrieval_request import RetrievalRequest

from datetime import datetime


class AbstractFileTreeUploader():
    """
    This abstract class is responsible for uploading a tree of files, such as a directory, to Azure
    Blob Storage. A subclass should succeed in uploading all files in the directory or throw an
    exception.

    Args:
        None

    Attributes:
        None

    Methods:
        upload_directory: Uploads a directory to Azure Blob Storage.

    Usage:
        None: use a subclass such as DirectoryToBlobUploader
    """

    def __init__(self):
        pass

    def upload_file_tree(
            self, 
            file_tree_path: str,
            rtrvl_req: RetrievalRequest,
            download_time: datetime) -> None:
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
