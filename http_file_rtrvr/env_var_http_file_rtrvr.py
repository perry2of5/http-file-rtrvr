# import library to read environment variables
import os

# import library to convert string to dictionary
import ast

from datetime import datetime

from http_file_rtrvr.retrieval_svc import RetrievalSvc, RetrievalRequest
from http_file_rtrvr.constants import FileType, SupportedHttpMethod
from http_file_rtrvr.uploader.azure.file_to_azure_blob_uploader import FileToAzureBlobUploader
from http_file_rtrvr.uploader.directory_uploader import DirectoryUploader

def main():
    print("Starting environment variable based HTTP file retriever...", datetime.now())
    try:
        print("Processing environment variables...")
        storage_account_url = os.environ.get('STORAGE_ACCOUNT_URL')
        storage_container_name = os.environ.get('STORAGE_CONTAINER_NAME')
        download_temp_dir = os.environ.get('DOWNLOAD_TEMP_DIR')
        target_rtrvl_url = os.environ.get('TARGET_RTRVL_URL')
        target_rtrvl_save_to = os.environ.get('TARGET_RTRVL_SAVE_TO')
        # convert file type into enum value, defaulting to SIMPLE (i.e., not an archive)
        target_rtrvl_file_type = FileType[os.environ.get('TARGET_RTRVL_FILE_TYPE', 'SIMPLE').upper()]
        target_rtrvl_timeout_secs = int(os.environ.get('TARGET_RTRVL_TIMEOUT_SECS', '10'))
        target_rtrvl_method = SupportedHttpMethod[os.environ.get('TARGET_RTRVL_METHOD', 'GET').upper()]

        target_rtrvl_http_headers_str = os.environ.get('TARGET_RTRVL_HTTP_HEADERS')
        target_rtrvl_http_headers = None
        if target_rtrvl_http_headers_str is not None and len(target_rtrvl_http_headers_str) > 0:
            target_rtrvl_http_headers = ast.literal_eval(target_rtrvl_http_headers_str)

        file_uploader = FileToAzureBlobUploader(storage_account_url, storage_container_name)
        dir_uploader = DirectoryUploader(file_uploader)
        rtrvl_svc = RetrievalSvc(file_uploader, dir_uploader, download_temp_dir)

        rtrvl_req = RetrievalRequest(
            url=target_rtrvl_url,
            method=target_rtrvl_method,
            timeout_seconds=target_rtrvl_timeout_secs,
            save_to=target_rtrvl_save_to,
            file_type=target_rtrvl_file_type,
            http_headers=target_rtrvl_http_headers
        )
        print('Processing retrieval request...', rtrvl_req)

        svc_rtrn_cd = rtrvl_svc.retrieve(rtrvl_req)
        print("finished at", datetime.now(), "with status", svc_rtrn_cd.status.value)
    except Exception as e:
        print("failure at", datetime.now(), e)


if __name__ == "__main__":
    main()