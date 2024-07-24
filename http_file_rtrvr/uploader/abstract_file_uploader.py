from http_file_rtrvr.retrieval_request import RetrievalRequest
from datetime import datetime

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