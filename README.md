# HTTP File Retriever (http-file-rtrvr)
This tool will retrieve a file from an HTTP or HTTPS location. A general flow is shown just below.
![Interaction Diagram](interaction-diagram.png "HTTP File Retriever interaction diagram") (see Note 1).

## Exit Codes
Exit codes are broken into different series where 1xx are access failures, 2xx are file format failures, 3xx are concerns with file contents such as malware, 4xx indicates the files couldn't be uploaded to the staging area for dispatch for further processing (Airbyte), and 5xx indicates errors replying to the system which requested the file retrieval.


| Code | Meaning                                                     |
|------|-------------------------------------------------------------|
| 0000 | Success                                                     |
| 0010 | Invalid Request                                             |
| 0100 | Error Retrieving Credentials                                |
| 0101 | Login Error (OAuth failure, HTTP 401, etc.)                 |
| 0102 | Access Denied (HTTP 403)                                    |
| 0200 | Decompression failed (unsupported format, corrupted, etc.)  |
| 0300 | File, or embedded file, flagged by Anti-malware             |
| 0400 | Upload failed                                               |
| 0500 | Response to source system (Airflow) failed                  |
| 9999 | Operation unsupported                                       |
[Exit codes]


Note 1: Interaction diagram was built using plant-uml. Remember to update this URL when you make edits. https://www.plantuml.com/plantuml/uml/XP91Znen38Nl-HKMlK8lt3XKIojLbNheQcUxFPkCWL53J1rd4FtrDI45Gf6QK_0yVxpd-2afYkPTS1Hrq2EKinna7VW0xS44UFxGY2TVNb-VuVCG25v8PQ2HP78IhwtqeZAAwr5nXOcA_1bJEh3qqE6Q9bUs5-exPQ6MliowXOva77nLLojMxqR_m8g9YuKRiQ9iIE_0zcFsDaXEapRZw3o7G5u7ZWac9LanLbAbkNDr332RVRYcN83Ghqn9Iyb41XXHwMOEc9KlPOxENJw1aIu3C58Tv2ShdKnZI2woDScmsUe2bh-p47ob8xnX3Zg5vO_ESXj1qnH8_NjdromH_0t1yLxVXHDX8tY4cwi3EusPEju51DuCyM-qegjavPyK7SM-SVPjQOrJioOh4ZOpB73OebeOQVFMHxaRMuMVxk0vAaNzh_5shElrVPhcaNholDiBfLIg3m3dK2umxm5FIxB3S40XI1xD6GiG-ksrkvtRk83EOqtmO6m58fHoq9l_oVl0sDTwwKt_ijDy0T_FmgguOYlW2dwmBny3h-ggpEkMkDhkN4yF5lR9G7aN_W00