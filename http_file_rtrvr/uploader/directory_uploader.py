from http_file_rtrvr.uploader.abstract_file_tree_uploader import AbstractFileTreeUploader
from http_file_rtrvr.uploader.abstract_file_uploader import AbstractFileUploader

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
        super(AbstractFileTreeUploader).__init__()
        self.file_uploader = file_uploader
        pass

    def upload_file_tree(self, file_tree_path: str):
        """
        Uploads the contents of a file tree (directory, zip, etc.) to a blob storage.

        Args:
            directory_path (str): The path of the base directory to be uploaded. Uploads walk 
            the tree of files and upload all files found replicating the folder structure
            remotely.

        Returns:
            None
        """
        for file in os.listdir(file_tree_path):
            file_path = os.path.join(file_tree_path, file)
            # If type of file is directory, call the function recursively, otherwise upload.
            if os.path.isdir(file_path):
                self.upload_directory(file_path)
            else:
                self.blob_uploader.upload_file(file_path, file)

