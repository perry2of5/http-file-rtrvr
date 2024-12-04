# HTTP File Retriever (http-file-rtrvr)
This tool will retrieve a file from an HTTP or HTTPS location. A general flow is shown just below. Please be advised <i><b><u>the service does not currently include anti-virus</u></b></i> although it appears in the diagram which reflects a desired state rather than the current state.<br><br>
![Interaction Diagram](interaction-diagram.png "HTTP File Retriever interaction diagram") (see Note 1).

<u><b><i>WARNING WARNING WARING - no anti-virus is currently included even though it appears in the diagram above as a desired feature</u></b></i><br>

## Environment Variables
The service expects to retrieve credentials from the Azure Container it is running in or from the Azure CLI when running locally for debugging. It still needs to know the following and for now they are passed in as environment variables. To debug in VSCode you can use "envFile": "${workspaceFolder}/some/path/asb/.env" in the launch.json where the some/path/asb part is a random subdirectory.

| Resource               | Variable                  | When         | Description                                                      |
|------------------------|---------------------------|--------------|------------------------------------------------------------------|
| Storage Account URL    | STORAGE_ACCOUNT_URL       | Always       | The Azure storage account to save the data to blobs within.      |
| Storage Container Name | STORAGE_CONTAINER_NAME    | Always       | Container name within the storage account to save blobs to.      |
| Temp Folder            | DOWNLOAD_TEMP_DIR         | Always       | Local folder to save files in temporarily.                       |
| Servce Bus Namespace   | SVC_BUS_FQN               | Svc Bus Only | Fully Qualified Service Bus name. e.g., tim-dev-airflow-azure-msg-bus.servicebus.windows.net |
| Request Queue          | QUEUE_NAME                | Svc Bus Only | Name of queue download requests will arrive on.                  |
| Request URL            | TARGET_RTRVL_URL          | Env Var Svc  | URL to retrieve file from                                        |
| Request SAVE_TO        | TARGET_RTRVL_SAVE_TO      | Env Var Svc  | Prefix to save blob under                                        |
| Request File Type      | TARGET_RTRVL_FILE_TYPE    | Env Var Svc  | Type of file - Simple or Archive (zip, tar, tgz, etc)            |
| Request Timeout Secs.  | TARGET_RTRVL_TIMEOUT_SECS | Env Var Svc  | Timeout for web request to URL                                   |
| Request HTTP Method    | TARGET_RTRVL_METHOD       | Env Var Svc  | HTTP GET for now. In the future POST and possibly others.        |
| Request HTTP Headers   | TARGET_RTRVL_HTTP_HEADERS | Env Var Svc  | HTTP Headers to send with the request                            |


## Request Format
Requests over messaging should be sent as JSON.

    {
        "method": "GET",
        "url": "http://example.com/index.html",
        "save_to": "some/prefix/for/files",
        "timeout_seconds": 5
    }

The file retrieved from above request will be written to:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<i>&lt;storage account&gt;/&lt;storage container&gt;/some/prefix/for/files/&lt;yyyy-MM-ddTHH-mm-ss>/index.html</i><br>
where the storage account and container come from the environment when the service is started and the date-time is from when the download was started.

The following fields are mandatory:
- url: URL of the simple file or archive to download.
- save_to: prefix of blob to save to within the storage container. This will have the date and time of the download appended to it and the file will be saved under that.
- 

The following fields are optional:
- method: defaults to GET. Valid options are GET or POST
- timeout_seconds: integer seconds, defaults to 5 seconds
- file_type: the type of the resource to download can be a SIMPLE file or an ARCHIVE file. Future work could add support for downloading a directory from FTP or SFTP or something.
- http_headers: a map of HTTP headers to send with the request to the URL. These are parsed into a map from json or the environment variable using "literal_eval".

### Response destination
Response destination is controlled using the standard ```reply_to``` header and the application-specific ```reply_to_type``` header. The ```reply_to_type``` header may be either "topic" or "queue" and is assumed to be a queue if not specified. 

## Response format

    {
        "source_url": "http://example.com/index.html",
        "status": "0000",
        "file_type": "simple",
        "method": "GET",
        "save_to_key": "some/prefix/for/files/2024-12-03T21-20-52/index.html",
        "saved_to_fqn": "https://devtimstoregrp1.blob.core.windows.net/testcontainer/some/prefix/for/files/2024-12-03T21-20-52/index.html"
    }


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

# Build Directions
Build the docker image with the following. Removing the --no-cache speeds up the build, but seems to occasionally miss changes to the files (I'm probably doing it wrong).

    docker build --no-cache -t ${CONTAINER_REGISTRY_NAME}.azurecr.io/http_file_rtrvr:0.0.4 .

Login to Azure Container Registry in CLI so Docker can use the credentials to upload:

    az acr login --name ${CONTAINER_REGISTRY_NAME}

Upload the docker image to ACR 

    docker push ${CONTAINER_REGISTRY_NAME}.azurecr.io/http_file_rtrvr:0.0.4

# References

Note 1: Interaction diagram was built using plant-uml. Remember to update this URL when you make edits. https://www.plantuml.com/plantuml/uml/XLLDR-Cs4BtpLmoSQn9eLxt4XsBLJOqk-j5TU-iUwXx6qiWMof0gIIb8aH_VqNXWIrgtIoE0n7apx_7DY7aN4uRKFLbZMdveogP5bs1HDA6s_ddd7ejF2nWlZ82deFcxeuvqUn68NsFQETbTJ3CuE4V7rhj8CxYYOpjLyyFdpnzXrLY6hoc5XdeA2r1qpVlh5FfWAaounqZ2y15ZVFQXshaDrdCzPQ1gatmWGourwKLL5LqwCfv2tvIqc9-QWvk-d6I8CibGHPECXE50oPJUMYfJurs4nUaKmhs0UKBCPthuvMxdjateufTTwAUM5bi853ixRu62rnJ166qTtDrzEpHb2TesST7mYqJEbixYoAVeCT78StD-X6bYZxQf66kSvuJG78vf2Lds9eCFJcAmFfLcKLtovzBUJKkUMyLQjFSxDsmEJg6DXdUxu62qDQ8qnJzT8FYHNc2BxCqj5BzlO4ECJl4MA9NtXZLby7q8Fe1EL-CEy7vKZrm5GqrZp27uhhrv_p3yuEPnDVpW9tze7FpXsw79QFyqm6jo2XsU9LY1ggk2K_t9_qLkO1gh_tMOo5kM7_OKF0jcZSz7JDHJ67I_KMfHFvOv9jSvdFTQQEKPIkyIkJGnZgk_XQ8iAKPu9DTGDMpbyXd2Bpx1odUk-ferd5hwfpOCLOfG7fkUujoeQVlhMZR_QwogSps1JORhRPQD-9W1LiYPrHKMSLebms-jzLZ9oLWSzfo4Uqk0TQ80nVOaqthVGdU24fP7KIMHB_J6_Bm_SXH6wpIMtrc_rudCTHZ7eEoRB5DnevF8Ejkkxpf5UWCOXSWXAxhssRw-ligVcRklRTm_L2lCuQPwgEjz3d8J_Ops6GF1faGd536NwmBxfPYdMbKczXfSKrnA3gmlwgwoVEem83CvclhdUmh2akNio9FAg2XHcPHjn1Zp9O-1vQYe-fzMwFIpiZq1JxCaLPUePrQ7zYKs4VYvHXilvLeVcpJCinatP6AzEZmuCBzNY-t4aYijcW_iHVwupWPxWiYLjFNtyA46j5Om4OuSthazaHEGe-eM8ajJD2I_S_g__dvwRR3S4DkhqpEzqdd1ffEBmd26PEAffBcU_eu5T4_sNm00
