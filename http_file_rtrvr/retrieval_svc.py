from http_file_rtrvr.retrieval_request import RetrievalRequest
from http_file_rtrvr.svc_return_code import SvcReturnCode


class RetrievalSvc:

    def retrieve(self, retrieval_req: RetrievalRequest) -> SvcReturnCode:
        if retrieval_req.url == None:
            return SvcReturnCode.INVALID_REQ
        else:
            # TODO
            return SvcReturnCode.OPERATION_UNSUPPORTED
