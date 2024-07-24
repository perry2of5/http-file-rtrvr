# Anti-Virus
## No Anti-Virus is currently included
<u><b><i>WARNING WARNING WARING - no anti-virus is currently included</u></b></i><br>
I envision using clam or one of the variants of it to provide anti-virus in the future. Right now, the implementation depends on the store the file is uploaded to blocking access to the file until a clean scan result is obtained by Microsoft Defender for Storage or similar.

## Microsoft Defender for Storage + Malware Scanning
As of 2024-07-11, there is no free tier for malware scanning costs are:
- Microsoft Defender for Storage $10 / month / storage account
- Malware Scanning for $0.15 / GB scanned + read costs, event costs, etc. Scanning triggered by BlobCreated events such as
  + initial uploading of new blobs
  + overwriting existing blobs
  + finalizing changes to blobs through specific operations

By default, scanning is capped at 5,000 GB (5TB) per month. We may need to increase this depending on expected data throughput.

Limitations:
- Scan throughput rate limit: Malware Scanning can process up to 2 GB per minute for each storage account. If the rate of file upload momentarily exceeds this threshold for a storage account, the system attempts to scan the files in excess of the rate limit. If the rate of file upload consistently exceeds this threshold, some blobs won't be scanned.
- Blob scan limit: Malware Scanning can process up to 2,000 files per minute for each storage account. If the rate of file upload momentarily exceeds this threshold for a storage account, the system attempts to scan the files in excess of the rate limit. If the rate of file upload consistently exceeds this threshold, some blobs won't be scanned.
- Blob size limit: The maximum size limit for a single blob to be scanned is 2 GB. Blobs that are larger than the limit won't be scanned.


Scan results can be provided by:
- blob index tags (can be manipulated so cannot be depended on)
- Defender for Cloud security alerts
- Event Grid events
  + fastest results
  + lowest latency
  + multiple processors possible:
    - Function App (previously called Azure Function) – use a serverless function to run code for automated response like move, delete or quarantine.
    - Webhook – to connect an application.
    - Event Hubs & Service Bus Queue – to notify downstream consumers
- Log Analytics -- definitely want this for audits, but not for file http_file_rtrvr

Based on this, we probably want to use event grid to get scan results. We could have a similar messaging configuration if we write our own virus scanning using clam or something similar.

### Setting up event handling
Generally need follow these steps
1. block access to un-scanned files and infected files.
2. set up custom topic.
3. configure Microsoft Defender for Cloud -> Storage -> Send scan results to topic....
4. override default setting if needed:
   - Enable/disable the Malware Scanning or the Data sensitivity threat detection features.
   - Configure custom settings for Malware Scanning.
   - Disable Microsoft Defender for Storage on specific storage accounts
5. process scan events.
  


## Handling AV Response
When an AV scan completes, we'll get a message on a queue. Since the file downloaded might be an archive with multiple files, we need to see if any given AV response is the final response for the download file or archive.

For this, we need to determine if the current response creates the need for a notification to Airflow. For this we could use:
- RDBMS
- Azure Cosmos with transaction batches to ensure we only send back completion to Airflow once with a message containing all updates. https://lennilobel.wordpress.com/2020/10/04/transactions-in-azure-cosmos-db-with-the-net-sdk/
- AWS Dynamo DB with DynamoDB transactions to ensure we only send the completion back once. https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html
