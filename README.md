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


Note 1: Interaction diagram was built using plant-uml. Remember to update this URL when you make edits. https://www.plantuml.com/plantuml/uml/ZPF1SXCn38RlVWfDkBPCsd3AWMcWT61WeDCjvPABiwia7XmhoF9cmjEZTJRfceOPVDee-dzzbkIRA9ObRRp184xsaC_CyTBJ3iuS6y4U_YqKeu-FZ_TmvppEmmCAEsoHHqV5KkCFmYsRnefTs8XPSszZt14tyr3P9OxAAZLZKmanbdLcITQQZzowMYMPHqDLMx_aoNazH-4jbbSeVndhZyjvU7ASukZCfLjJa_TOYwCGONIuQWOyanqdnlHjWilBjyyDc0BZhuHHSaYJrA-rWeCMcTCdbChMUjTehWca0dQhjKnXFBuQmwUG_uE7WxVQ9g6JDONIyxcrIjFFQXwwODSGwwFHQE80Wz2WffdzJepm6VVmP9EN2vZzgA12pPPu0IZrQwDGO_Z0J0pzDhYmWlS3FmmDT9x6q5PU-SvunNOFWqy3UWhmVj9JyBHouTZAdDSZ2_t4q9aFWRzrItEXnBn09cKaXjtQIhUZ7UeLVCb-6NX0DgpTxqmvlxvH-Hjg2e91YbQf-JNCwXfZX5iC3fikDCaF1RwIm1sbqFntCygnBfSv-AzrQR2cpPQrz1bjxb6vIDSwijkJnb60EwjkZJ6UQ0ksUnyRwtUM4M9jzTR4WBPUvw9dXjLEeTAy71tEA8krHlBoacAY5CSg3GhMSY98Mq-swPNPDO8Gp1mlzkeGAN6DyIL8d4pX-q6RHKEMthEaAHVzdQT5l-EJutg_KShUCZTfECA3StahFL2bl0V6D7ZcrT-eGThuFm00
