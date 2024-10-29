from http_file_rtrvr.exceptions import FileUploadException
from http_file_rtrvr.retrieval_request import RetrievalRequest
from datetime import datetime
from urllib import parse as urlparser

class AbstractFileUploader:
    def upload(self,
            fq_source_path: str,
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
        pass

    def upload_path(
            self, 
            download_time: datetime, 
            rtrvl_req: RetrievalRequest, 
            archive_path: str | None = None) -> str:
        """
        Generates a unique blob key based on the save_to (if included), download time, url, and local path
        within an archive (if applicable).

        Args:
            download_time (datetime): The timestamp of the download.
            rtrvl_req (RetrievalRequest): The retrieval request object containing the requested URL and the 
                    optional, save_to prefix.
            archive_path (str | None, optional): The optional path to the file within an archive. Defaults to None 
                    because I expect most files will not be in an archive.


        Returns:
            str: The generated blob key.

        Raises:
            FileUploadException: If the generated blob key exceeds the maximum length.

        """
        # add the date like 2024-07-03T09-21-34
        date_str = download_time.strftime("%Y-%m-%dT%H-%M-%S")

        # grab the URL path without leading or trailing slashes
        url_path = ""
        if rtrvl_req.url is not None and len(rtrvl_req.url) > 0:
            url_path = self._strip_leading_and_trailing_slashes(
                    urlparser.urlparse(rtrvl_req.url).path)

        path_in_archive = ""
        if archive_path:
            path_in_archive = self._strip_leading_and_trailing_slashes(archive_path)

        # filter out empty strings and then join with '/' as separator
        raw_blob_key = "/".join(list(filter(lambda x: x is not None and len(x) > 0,
                                            [rtrvl_req.save_to, date_str, url_path, path_in_archive])))
        encoded_key = urlparser.quote(raw_blob_key)
        if len(encoded_key) > self.max_upload_path_length():
            raise FileUploadException(
                rtrvl_req.url, raw_blob_key, "Blob key too long", None)
        return encoded_key    
    
    def max_upload_path_length(self) -> int:
        """
        Returns the maximum length of the upload path for the storage backend.

        Returns:
            int: The maximum length of the upload path.
        """
        pass


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
