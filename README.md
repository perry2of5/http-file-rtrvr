# HTTP File Retriever (http-file-rtrvr)
This tool will retrieve a file from an HTTP or HTTPS location. A general flow is shown just below.
![Interaction Diagram](interaction-diagram.png "HTTP File Retriever interaction diagram") (see Note 1).

## Request Format
Requests should be sent as JSON.

    {
        "method": "GET",
        "url": "http://example.com/some/file",
        "timeout_seconds": 5
    }

The following fields are mandatory:
- url

The following fields are optional:
- method: defaults to GET. Valid options are GET or POST
- timeout_seconds: integer seconds, defaults to 5 seconds


## Exit Codes
Exit codes are broken into different series where 1xx are access failures, 2xx are file format failures, 3xx are concerns with file contents such as malware, 4xx indicates the files couldn't be uploaded to the staging area for dispatch for further processing (Airbyte), and 5xx indicates errors replying to the system which requested the file retrieval.


| Code | Meaning                                                     |
|------|-------------------------------------------------------------|
| 0000 | Success                                                     |
| 0010 | Invalid Request                                             |
| 0100 | Error Retrieving Credentials                                |
| 0101 | Login Error (OAuth failure, HTTP 401, etc.)                 |
| 0102 | Access Denied (HTTP 403)                                    |
| 0103 | File Not Found (HTTP 404)                                   |
| 0199 | Unknown Retrieval Error                                     |
| 0200 | Decompression failed (unsupported format, corrupted, etc.)  |
| 0300 | File, or embedded file, flagged by Anti-malware             |
| 0400 | Upload Failed                                               |
| 0500 | Response to source system (Airflow) failed                  |
| 9999 | Operation unsupported                                       |
[Exit codes]


Note 1: Interaction diagram was built using plant-uml. Remember to update this URL when you make edits. https://www.plantuml.com/plantuml/uml/XLLDR-Cs4BtpLmoSQn9eLxt4XsBLJOqk-j5TU-iUwXx6qiWMof0gIIb8aH_VqNXWIrgtIoE0n7apx_7DY7aN4uRKFLbZMdveogP5bs1HDA6s_ddd7ejF2nWlZ82deFcxeuvqUn68NsFQETbTJ3CuE4V7rhj8CxYYOpjLyyFdpnzXrLY6hoc5XdeA2r1qpVlh5FfWAaounqZ2y15ZVFQXshaDrdCzPQ1gatmWGourwKLL5LqwCfv2tvIqc9-QWvk-d6I8CibGHPECXE50oPJUMYfJurs4nUaKmhs0UKBCPthuvMxdjateufTTwAUM5bi853ixRu62rnJ166qTtDrzEpHb2TesST7mYqJEbixYoAVeCT78StD-X6bYZxQf66kSvuJG78vf2Lds9eCFJcAmFfLcKLtovzBUJKkUMyLQjFSxDsmEJg6DXdUxu62qDQ8qnJzT8FYHNc2BxCqj5BzlO4ECJl4MA9NtXZLby7q8Fe1EL-CEy7vKZrm5GqrZp27uhhrv_p3yuEPnDVpW9tze7FpXsw79QFyqm6jo2XsU9LY1ggk2K_t9_qLkO1gh_tMOo5kM7_OKF0jcZSz7JDHJ67I_KMfHFvOv9jSvdFTQQEKPIkyIkJGnZgk_XQ8iAKPu9DTGDMpbyXd2Bpx1odUk-ferd5hwfpOCLOfG7fkUujoeQVlhMZR_QwogSps1JORhRPQD-9W1LiYPrHKMSLebms-jzLZ9oLWSzfo4Uqk0TQ80nVOaqthVGdU24fP7KIMHB_J6_Bm_SXH6wpIMtrc_rudCTHZ7eEoRB5DnevF8Ejkkxpf5UWCOXSWXAxhssRw-ligVcRklRTm_L2lCuQPwgEjz3d8J_Ops6GF1faGd536NwmBxfPYdMbKczXfSKrnA3gmlwgwoVEem83CvclhdUmh2akNio9FAg2XHcPHjn1Zp9O-1vQYe-fzMwFIpiZq1JxCaLPUePrQ7zYKs4VYvHXilvLeVcpJCinatP6AzEZmuCBzNY-t4aYijcW_iHVwupWPxWiYLjFNtyA46j5Om4OuSthazaHEGe-eM8ajJD2I_S_g__dvwRR3S4DkhqpEzqdd1ffEBmd26PEAffBcU_eu5T4_sNm00
