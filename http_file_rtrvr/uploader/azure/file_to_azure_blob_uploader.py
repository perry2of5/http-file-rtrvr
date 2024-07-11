from http_file_rtrvr.exceptions import FileUploadException
from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.uploader.abstract_file_uploader import AbstractFileUploader

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, BlobType, ContentSettings
from datetime import datetime
from mimetypes import guess_type
from urllib import parse as urlparser

from pathlib import Path

from azure.core.exceptions import (HttpResponseError, DecodeError)

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
        self.blob_service_client: BlobServiceClient = BlobServiceClient(
            blob_act_url, credential=DefaultAzureCredential())

    def upload(
            self,
            fq_source_path: str,
            dest_key: str,
            rtrvl_req: RetrievalRequest,
            download_time: datetime) -> str:
        """
        Uploads a specific file (not a directory) from the source path to the specified destination
        in Azure Blob Storage. If the container the AzureBlobUploader was created with does not
        exist, then the container is created.

        Args:
            fq_source_path (str): The fully-qualified path of the file to upload.
            dest_key (str): The destination key in Azure Blob Storage.
            rtrvl_req (RetrievalRequest): The retrieval request object containing the requested URL
                    and the save_to prefix.
            download_time (datetime): The timestamp of the download.

        Returns:
            None

        Raises:
            FileUploadException: If the file cannot be uploaded to Azure Blob Storage.
            ResourceExistsError: If the blob already exists.
            ClientAuthenticationError: If the client cannot authenticate to Azure.
        """
        fq_dest_path = self.fully_qualified_upload_path(download_time, rtrvl_req)
        print("Uploading", fq_source_path, "to", fq_dest_path)
        blob_client: BlobClient = self.get_blob_client(dest_key)
        print("Got blob client for dest_key", dest_key)
        content_and_encoding_type = guess_type(fq_source_path)
        print("guessed encoding: ", content_and_encoding_type)
        # open file in binary and upload to blob
        try:
            print("opening", fq_source_path, "to upload")
            with open(fq_source_path, "rb") as data:
                print("starting upload to ", dest_key)
                blob_client.upload_blob(
                    data,
                    blob_type="BlockBlob",
                    content_settings=ContentSettings(
                        content_type=content_and_encoding_type[0],
                        encoding=content_and_encoding_type[1]))
                print("uploaded")
                return fq_dest_path
        except OSError as e:
            raise FileUploadException(
                rtrvl_req.url,
                "File open for {} failed: {}".format(fq_source_path, e.errno),
                e)
        except HttpResponseError as e:
            # HttpResponseError is the parent class of ResourceNotFoundError, ResourceModifiedError,
            # ClientAuthenticationError, ResourceExistsError, and DecodeError. Converting to a
            # locally defined exception for when we expand this to upload to other services besides
            # Azure storage.
            raise FileUploadException(
                    rtrvl_req.url,
                    "Blob create for {} failed: {}".format(fq_source_path, e.message),
                    e)
        
    def fully_qualified_upload_prefix(self) -> str:
        return self.blob_act_url + '/' + self.blob_cntnr_name


    def max_upload_path_length(self) -> int:
            """
            Returns the maximum length of the upload path for the Azure Blob storage backend.

            Returns:
                int: The maximum length of the upload path.
            """
            return MAX_BLOB_KEY_LEN

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
        return cntnr_client.get_blob_client(blob_key)

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
        for cntnr in self.blob_service_client.list_containers():
            if cntnr.name == self.blob_cntnr_name:
                print("found", cntnr.name)
                return self.blob_service_client.get_container_client(self.blob_cntnr_name)
            else:
                print("container", cntnr.name, "does not match", self.blob_cntnr_name)

        print("Target container", self.blob_cntnr_name,
              "was not found so created container in", self.blob_act_url)
        self.blob_service_client.create_container(self.blob_cntnr_name)
        return self.blob_service_client.get_container_client(self.blob_cntnr_name)
