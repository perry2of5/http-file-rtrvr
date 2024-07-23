import os

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
            pass

