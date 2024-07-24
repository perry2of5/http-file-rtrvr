from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.uploader.azure.file_to_azure_blob_uploader import FileToAzureBlobUploader
from http_file_rtrvr.exceptions import FileDecompressionFailedException, FileUploadException
from http_file_rtrvr.extract.extraction_exception import ExtractionException
from http_file_rtrvr.uploader.directory_uploader import DirectoryUploader
from http_file_rtrvr.uploader.abstract_file_uploader import AbstractFileUploader
from http_file_rtrvr.constants import FileType, SupportedHttpMethod, SvcReturnCode

from http_file_rtrvr.extract.tar_extractor import TarExtractor
from http_file_rtrvr.extract.zip_extractor import ZipExtractor


from shutil import rmtree
from datetime import datetime
import os
import requests
from tarfile import is_tarfile
import tempfile
from urllib import parse as urlparser


class RetrievalSvc:
    def __init__(self, file_uploader: AbstractFileUploader, dir_uploader: DirectoryUploader,
                 download_temp_dir: str) -> None:
        self.file_uploader = file_uploader
        self.dir_uploader = dir_uploader
        self.download_temp_dir = download_temp_dir
        if not os.path.exists(self.download_temp_dir):
            os.makedirs(self.download_temp_dir)
        pass

    def retrieve(self, retrieval_req: RetrievalRequest) -> SvcReturnCode:
        temp_dir: str = None
        try:
            print("creating temp dir under", self.download_temp_dir)
            temp_dir = tempfile.mkdtemp(dir=self.download_temp_dir)
            print("temp dir created: ", temp_dir)
            if retrieval_req.url == None:
                return SvcReturnCode.INVALID_REQ
            else:
                if retrieval_req.method == SupportedHttpMethod.GET:
                    return self._get(temp_dir, retrieval_req)
                elif retrieval_req.method == SupportedHttpMethod.POST:
                    return self._post(temp_dir, retrieval_req)
                else:
                    return SvcReturnCode.OPERATION_UNSUPPORTED
        finally:
            if temp_dir is not None and os.path.exists(temp_dir):
                rmtree(temp_dir)
                print("removed temp dir", temp_dir)

    def _get(self, temp_dir: str, retrieval_req: RetrievalRequest) -> SvcReturnCode:
        # implement get
        download_start_dtm = datetime.now()
        response = requests.get(url=retrieval_req.url, timeout=retrieval_req.timeout_seconds,
                headers=retrieval_req.headers)
        return_code = self._derive_return_code(response.status_code)
        print("response code", return_code, "for", retrieval_req.url)
        if return_code == SvcReturnCode.SUCCESS:
            response.raise_for_status()
            response_file: str = None
            try:                
                # determine if response is text or binary
                response_file = self._save_response(temp_dir, retrieval_req, response)

                if retrieval_req.file_type == FileType.SIMPLE:
                    upload_path = self.file_uploader.upload_path(download_start_dtm, retrieval_req)
                    self.file_uploader.upload(response_file, upload_path, retrieval_req, download_start_dtm)
                else:
                    self._decompress_and_upload(retrieval_req, response_file, temp_dir, download_start_dtm)
            except FileUploadException as e:
                # TODO: need to add logging here and need to export logs to central location
                print("Upload to ", e.upload_url, "failed:", e.message)
                return SvcReturnCode.DOWNLOAD_FAILED
            except FileDecompressionFailedException as e:
                print("Decompression failed for", retrieval_req.url, ":", e.message)
                return SvcReturnCode.DECOMPRESSION_FAILED
            finally:
                if response_file is not None and os.path.exists(response_file):
                    os.remove(response_file)
                    print("removed temp file", response_file)

        return return_code
    
    def _decompress_and_upload(
            self, 
            retrieval_req: RetrievalRequest,
            response_file: str,
            temp_dir: str,
            download_start_dtm: datetime) -> None:
        extract_file_dir: str = None
        try:
            if response_file.lower().endswith(".zip"):
                extract_file_dir = ZipExtractor().extract_to_temp_dir(response_file, temp_dir)
            elif is_tarfile(response_file):
                extract_file_dir = TarExtractor().extract_to_temp_dir(response_file, temp_dir)
            else:
                print("Cannot extract file", response_file)
                raise FileDecompressionFailedException("Unsupported file type for " + response_file)
            print("Uploading files extracted into ", extract_file_dir)
            self.dir_uploader.upload_file_tree(extract_file_dir, retrieval_req, download_start_dtm)
        except FileDecompressionFailedException as e:
            raise e
        except ExtractionException as e:
            raise FileDecompressionFailedException(e.message, e)
        finally:
            if extract_file_dir is not None and os.path.exists(extract_file_dir):
                rmtree(extract_file_dir)
                print("removed temp dir", extract_file_dir)
        pass
    
    def _post(self, temp_dir: str, retrieval_req: RetrievalRequest) -> SvcReturnCode:
        # implement post
        print('implement post to', retrieval_req.url)
        return SvcReturnCode.OPERATION_UNSUPPORTED

    def _save_response(
            self, 
            temp_dir: str, 
            retrieval_req: RetrievalRequest,
            response: requests.Response) -> str:
        # save text response to file
        file_name = urlparser.urlparse(retrieval_req.url).path.split("/")[-1]
        temp_file_path = os.path.join(temp_dir, file_name)

        print("Writing response to", temp_file_path)
        with open(temp_file_path, "wb") as f:
                f.write(response.content)
        return temp_file_path

    def _derive_return_code(self, http_status_code: int) -> SvcReturnCode:
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
