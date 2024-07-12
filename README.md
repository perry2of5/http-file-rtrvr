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


Note 1: Interaction diagram was built using plant-uml. Remember to update this URL when you make edits. https://www.plantuml.com/plantuml/png/XLJDRkCs4BxpAGRErLbeLxt4XsBTf4QB_dHhf-cXxc5CZMnY6L8bAGKfyl0TqWDRSWoKHX29vFSp7qVy71E6r3zRrV5_eqs7Bi7IXDRw5xWoC08ULoU8sG-FZrzWPInjtPfIC3HGc0a2MfvVfp04rM327KO27hCl6EEB3ytMRR2bsLH51sesoGTIv999hm05i-pJWVTJ68mMoCWPBsu6FKLaPmKXZYO8hdvFIMblBUbal8imErQHjKLW38ZrXHz-kTsw9nFw-8uT1_LFJpt1U7FPcbEAlKtmw3kZPyVDFAKaNBYz_VOSsm82CL5CPKefPAi39Xe5gqwFC4KEQ4t3UvNp30XcVqWBgAgF5VpeoXgiZznCsoT_elPkGda-3pOZ1xnrUJB7WJOgdks3W_7KML8j_-q3mK_q2a_8TSzX-US6DgGP5UT0INzGxAc2xqFm0QI5ZDl3_OYFN0EPKocr3xxlRkxlyWzk7bRv1p_xlN7mb-_oIQBzMm6FIHNI8GkmPQl4MlQ9_-I_aijAO_U_vRQRi_sme-3Pi0_mSi2Kkppx_YZInVtOvbXScktYC4KsFuFsBd6ja-2O_HCijQOOuO6SeIPFrR3AW5zzWfNlNVD_qJ1K--SkP9Pbq0SpKBmCQdhyRIlfNM-hviHt1JlEJnhkKrMDFB0gh93P6h4BVtJMOvEhoiPmu4NSMG9i4mLOFXqjMkyxw8zR2VNX6278c7YDzMbU8WxbYokpsHxm6EKCCewD-ftrE-dHMjeJP5JVL9NObHg4KWuWSwktjxVofov3bTFPtJKhhE6ckMlRNGtbOlW5xGkozaQZAvInBjS03ekIYuYA7WwokAQuA1XOdmkygl9xZm5PoKba4W3uWK9HgMekxLbiD9H89r4RASPw0GzaUJMxcb9DivIcHWSx0cvI1etvMi-g3krhD17ukKKRptITZoRbDfscAo_db5L9uFA-N3vD8ZcNERh6xW-alu9f0Qqjs0W770YsRaVa83BUKJFFEwAVG-xTNC27T_Uacdxex4HkyUadm0CsVVcIbMheoYN-cQlgd-r_
