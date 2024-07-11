from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.svc_return_code import SvcReturnCode
from http_file_rtrvr.http_method import SupportedHttpMethod
import requests


class RetrievalSvc:

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
        response = requests.get(url=retrieval_req.url,
                                timeout=retrieval_req.timeout_seconds)
        return_code = self.derive_return_code(response.status_code)
        if return_code == SvcReturnCode.SUCCESS:
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
