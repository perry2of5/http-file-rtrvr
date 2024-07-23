from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.uploader.azure.file_to_azure_blob_uploader import FileToAzureBlobUploader
from http_file_rtrvr.exceptions import FileUploadException
from http_file_rtrvr.uploader.directory_uploader import DirectoryUploader
from http_file_rtrvr.uploader.abstract_file_uploader import AbstractFileUploader
from http_file_rtrvr.constants import FileType, SupportedHttpMethod, SvcReturnCode
import requests


class RetrievalSvc:
    def __init__(self, file_uploader: AbstractFileUploader, dir_uploader: DirectoryUploader) -> None:
        self.file_uploader = file_uploader
        self.dir_uploader = dir_uploader
        pass

    def retrieve(self, retrieval_req: RetrievalRequest) -> SvcReturnCode:
        if retrieval_req.url == None:
            return SvcReturnCode.INVALID_REQ
        else:
            if retrieval_req.method == SupportedHttpMethod.GET:
                return self.get(retrieval_req)
            elif retrieval_req.method == SupportedHttpMethod.POST:
                return self.post(retrieval_req)
            else:
                return SvcReturnCode.OPERATION_UNSUPPORTED

    def get(self, retrieval_req: RetrievalRequest) -> SvcReturnCode:
        # implement get
        response = requests.get(url=retrieval_req.url, timeout=retrieval_req.timeout_seconds,
                headers=retrieval_req.headers)
        return_code = self.derive_return_code(response.status_code)
        if return_code == SvcReturnCode.SUCCESS:
            try:
                if retrieval_req.file_type == FileType.SIMPLE_FILE:
                    self.file_uploader.upload(retrieval_req, response)
                else:
                    self.decompress_and_upload(retrieval_req, response)
            except FileUploadException as e:
                # TODO: need to add logging here and need to export logs to central location
                print("Upload to ", e.upload_url, "failed:", e.message)
                return SvcReturnCode.DOWNLOAD_FAILED
            # save file
            print("save contents here")
        return return_code

    def post(self, retrieval_req: RetrievalRequest) -> SvcReturnCode:
        # implement post
        print('implement post to', retrieval_req.url)
        return SvcReturnCode.OPERATION_UNSUPPORTED

    def derive_return_code(self, http_status_code: int) -> SvcReturnCode:
        if http_status_code >= 200 and http_status_code <= 299:
            # success -- save response and return success
            return SvcReturnCode.SUCCESS
        elif http_status_code == 401:
            return SvcReturnCode.LOGIN_ERROR
        elif http_status_code == 403:
            return SvcReturnCode.ACCESS_DENIED
        elif http_status_code == 404:
            return SvcReturnCode.FILE_NOT_FOUND
        else:
            return SvcReturnCode.UNKNOWN_RETRIEVAL_ERROR

    def _add_header(headers: map, key: str, value: str) -> map:
        if headers == None:
            headers = {key: value}
        else:
            headers.put(key, value)
        return headers
