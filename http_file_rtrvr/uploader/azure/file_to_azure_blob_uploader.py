
from http_file_rtrvr.exceptions import FileUploadException
from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.uploader.abstract_file_uploader import AbstractFileUploader

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, BlobType, ContentSettings
from azure.storage.blob import ContainerProperties
from datetime import datetime
from mimetypes import guess_type
from os import environ
from urllib import parse as urlparser

from azure.core.exceptions import (
    HttpResponseError,
    ResourceNotFoundError,
    ResourceModifiedError,
    ResourceExistsError,
    ClientAuthenticationError,
    DecodeError)

import requests

# blob key URL Characters must be properly escaped and the maximum blob key length is 1024 characters according to
# https://learn.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata
MAX_BLOB_KEY_LEN = 1024


class FileToAzureBlobUploader(AbstractFileUploader):
    def __init__(
            self,
            blob_act_url: str,
            blob_cntnr_name: str) -> None:
        self.blob_act_url: str = blob_act_url
        self.blob_cntnr_name: str = blob_cntnr_name
        default_credential = DefaultAzureCredential()
        blob_service_client: BlobServiceClient = BlobServiceClient(
            blob_act_url, credential=default_credential)

    def upload(
            self,
            source_path: str,
            dest_key: str,
            rtrvl_req: RetrievalRequest,
            download_time: datetime) -> None:
        """
        Uploads a specific file (not a directory) from the source path to the specified destination
        in Azure Blob Storage. If the container the AzureBlobUploader was created with does not 
        exist, then the container is created.

        Args:
            source_path (str): The path of the file to upload.
            dest_key (str): The destination key in Azure Blob Storage.

        Returns:
            None
        """
        print("Uploading", source_path, "to", "".join([self.blob_act_url,
                                                       self.blob_ctnr_name, dest_key]))
        blob_client: BlobClient = self.get_blob_client(dest_key)
        content_and_encoding_type = guess_type(source_path)
        # open file in binary and upload to blob
        try:
            with open(source_path, "rb") as data:
                blob_client = blob_client.upload_blob(
                    data,
                    blob_type=BlobType.BlockBlob,
                    content_settings=ContentSettings(
                        content_type=content_and_encoding_type[0],
                        encoding=content_and_encoding_type[1]))
        except OSError as e:
            raise FileUploadException(
                rtrvl_req.url,
                source_path,
                "File open for % failed: %".format(source_path, e.message),
                e)
        except HttpResponseError | ResourceNotFoundError | ResourceModifiedError | ResourceExistsError | ClientAuthenticationError | DecodeError as e:
            raise FileUploadException(
                rtrvl_req.url,
                source_path,
                "Blob create for % failed: %".format(source_path, e.message),
                e)

    def upload_path(
            self, 
            download_time: datetime, 
            rtrvl_req: RetrievalRequest, 
            local_path: str | None = None) -> str:
        """
        Generates a unique blob key based on the save_to (if included), download time, url, and local path
        within an archive (if applicable).

        Args:
            download_time (datetime): The timestamp of the download.
            rtrvl_req (RetrievalRequest): The retrieval request object containing the requested URL and the 
                    optional, save_to prefix.
            local_path (str | None, optional): The local path to append to the blob key. Defaults to None.

        Returns:
            str: The generated blob key.

        Raises:
            FileUploadException: If the generated blob key exceeds the maximum length.

        """
        # add the date like 2024-07-03T09-21-34
        date_str = download_time.strftime("%Y-%m-%dT%H-%M-%S")

        # grab the URL path without leading or trailing slashes
        url_path = self._strip_leading_and_trailing_slashes(
            urlparser.urlparse(rtrvl_req.url).path)

        path_in_archive = ""
        if local_path:
            path_in_archive = self._strip_leading_and_trailing_slashes(
                local_path)

        # filter out empty strings and then join with '/' as separator
        raw_blob_key = "/".join(list(filter(lambda x: x is not None and len(x) > 0,
                                            [rtrvl_req.save_to, date_str, url_path, path_in_archive])))
        encoded_key = urlparser.quote(raw_blob_key)
        if len(encoded_key) > MAX_BLOB_KEY_LEN:
            raise FileUploadException(
                rtrvl_req.url, raw_blob_key, "Blob key too long", None)
        return encoded_key

    def get_blob_client(self, blob_key: str) -> BlobClient:
        """
        Returns the BlobClient object for the specified blob key.

        Args:
            blob_key (str): The key of the target blob.

        Returns:
            BlobClient: The BlobClient object for the specified blob key.

        Raises:
            None
        """
        cntnr_client: ContainerClient = self.get_cntnr_client()
        return blob_key.get_blob_client(blob_key)

    def get_cntnr_client(self) -> ContainerClient:
        """
        Returns the ContainerClient object for the specified target container name. If the
        container does not already exist, it will be created.

        Args:
            None

        Returns:
            ContainerClient: The ContainerClient object for the specified target container name.

        Raises:
            None

        """
        for cntnr_name in self.blob_service_client.list_containers():
            if cntnr_name == self.blob_cntnr_name:
                return self.blob_service_client.get_container_client(self.blob_cntnr_name)

        print("Target container", self.blob_cntnr_name,
              "was not found so created container in", self.blob_act_url)
        self.blob_service_client.create_container(self.blob_cntnr_name)
        return self.blob_service_client.get_container_client(self.blob_cntnr_name)

    def _strip_leading_and_trailing_slashes(self, string: str) -> str:
        """
        Strips leading and trailing slashes from the specified string.

        Args:
            path (string): The string to remove leading and trailing slashes from.

        Returns:
            str: The path with leading and trailing slashes removed.

        Raises:
            None
        """
        if string.startswith('/'):
            if string.endswith('/'):
                return string[1:-1]
            return string[1:]
        if string.endswith('/'):
            return string[:-1]
        return string
