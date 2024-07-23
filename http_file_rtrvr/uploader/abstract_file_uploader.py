from http_file_rtrvr.exceptions import FileUploadException
from http_file_rtrvr.retrieval_request import RetrievalRequest

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, BlobType, ContentSettings
from azure.storage.blob import ContainerProperties
from datetime import datetime
from mimetypes import guess_type
from os import environ
from urllib import parse as urlparser


class AbstractFileUploader():
    def upload(
            self,
            source_path: str,
            dest_key: str,
            rtrvl_req: RetrievalRequest,
            download_time: datetime) -> None:
        """
        Uploads a specific file (not a directory) from the local source path to some data set storage location.
        If the location exists, the uploader should create it if possible.

        Args:
            source_path (str): The path of the file to upload.
            dest_key (str): The destination key in Azure Blob Storage.

        Returns:
            None
        """
        pass

    def upload_path(
                self, 
                download_time: datetime, 
                rtrvl_req: RetrievalRequest, 
                local_path: str | None = None) -> str:
            """
            Generates the upload path for a file based on the download time, retrieval request, and local path.
            Specifically, the save_to from the retrieval request, the date & time the download occurred, the
            path portion of the downloaded url, and if applicable, the path of the file in the downloaded archive.

            Args:
                download_time (datetime): The time when the file was downloaded.
                rtrvl_req (RetrievalRequest): The retrieval request object containing information about the file.
                        The save_to and path portion of the URL are used.
                local_path (str | None, optional): The local path of the file. Defaults to None.

            Returns:
                str: The upload path for the file.

            """
            pass
