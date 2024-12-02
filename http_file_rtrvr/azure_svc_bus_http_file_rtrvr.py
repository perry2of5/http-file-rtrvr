# import library to read environment variables
import os
from json import loads, dumps

# import library to convert string to dictionary
from ast import literal_eval

from datetime import datetime

from http_file_rtrvr.retrieval_svc import RetrievalSvc, RetrievalRequest, RetrievalResponse, SvcReturnCode
from http_file_rtrvr.constants import FileType, SupportedHttpMethod
from http_file_rtrvr.uploader.azure.file_to_azure_blob_uploader import FileToAzureBlobUploader
from http_file_rtrvr.uploader.directory_uploader import DirectoryUploader

import asyncio

from azure.identity import DefaultAzureCredential
from azure.servicebus import AutoLockRenewer, ServiceBusClient, ServiceBusMessage, ServiceBusReceiver

MESSAGE_BATCH_SIZE = 1

def lock_renewal_failure_callback(renewable, error):
    print("Lock renewal failure:", error)

message_lock_renewer = AutoLockRenewer(
    max_lock_renewal_duration=15*60,
    max_workers=4,
    on_lock_renew_failure=lock_renewal_failure_callback
)

def main():
    print("Starting Azure Service Bus HTTP file retriever at", datetime.now())
    try:
        print("Processing environment variables at", datetime.now())
        storage_account_url = os.environ.get('STORAGE_ACCOUNT_URL')
        storage_container_name = os.environ.get('STORAGE_CONTAINER_NAME')
        download_temp_dir = os.environ.get('DOWNLOAD_TEMP_DIR')
        svc_bus_fqn = os.environ.get('SVC_BUS_FQN')
        queue_name = os.environ.get('QUEUE_NAME')
        
        if storage_account_url is None or storage_container_name is None:
            print("Missing storage account URL or container name")
            return
        if download_temp_dir is None:
            print("Missing download temp directory")
            return 
        if svc_bus_fqn is None or queue_name is None:
            print("Missing service bus fully qualified namespace or queue name")
            return

        print("Looking for messages in queue", queue_name, "and saving downloads to", storage_account_url,
               storage_container_name)

        print("Getting default Azure Credential")
        credential = DefaultAzureCredential(logging_enable=True)
        print("Connecting to service bus")
        servicebus_client = ServiceBusClient(svc_bus_fqn, credential, logging_enable=True)

        file_uploader = FileToAzureBlobUploader(storage_account_url, storage_container_name)
        dir_uploader = DirectoryUploader(file_uploader)
        rtrvl_svc = RetrievalSvc(file_uploader, dir_uploader, download_temp_dir)

        with servicebus_client:
            process_messages(servicebus_client, queue_name, rtrvl_svc)
    except Exception as e:
        print("failure at", datetime.now())
        print("failure: ", e)
        print(type(e))

def process_messages(servicebus_client: ServiceBusClient, queue_name: str, rtrvl_svc: RetrievalSvc):
    """
    Process messages from a Service Bus queue. If no message is received within 60 seconds,
    the function will return.

    Args:
        queue_name (str): The name of the queue to process messages from.
        servicebus_client (ServiceBusClient): The client object for the Service Bus.
        receiver (ServiceBusReceiver): The receiver object for the queue.
        rtrvl_svc (RetrievalSvc): The retrieval service object.

    Returns:
        None
    """
    receiver = servicebus_client.get_queue_receiver(
            queue_name=queue_name, prefetch_count=MESSAGE_BATCH_SIZE, auto_lock_renewer=message_lock_renewer)
    with receiver:
        num_processed = 1
        while num_processed > 0:
            num_processed = 0
            print("Waiting for messages at", datetime.now())
            received_msgs = receiver.receive_messages(max_message_count=MESSAGE_BATCH_SIZE, max_wait_time=60)
            if 0 == len(received_msgs):
                print("No messages received.")
            else:
                for msg in received_msgs:
                    num_processed += 1
                    try:
                        rtrvl_result = process_rtrvl_msg(rtrvl_svc, msg, servicebus_client)
                        if rtrvl_result.status == SvcReturnCode.SUCCESS:
                            print("Message processed successfully at", datetime.now())
                            receiver.complete_message(msg)
                        else:
                            print("Message processing failed at", datetime.now(),
                                    "with status", rtrvl_result.status)
                            receiver.abandon_message(msg)
                    except Exception as e:
                        print("Message processing failure at", datetime.now(), e)
    print("Finished processing messages at", datetime.now())

def process_rtrvl_msg(
        rtrvl_svc: RetrievalSvc,
        msg: ServiceBusMessage,
        servicebus_client: ServiceBusClient) -> RetrievalResponse:
    print(str(msg))
    rtrvl_req = parse_msg_body(msg)
    print('Processing retrieval request...', msg.message_id)
    rtrvl_result = rtrvl_svc.retrieve(rtrvl_req)
    print('URL retrieved for message', msg.message_id)
    if msg.reply_to is not None:
        send_response(msg, rtrvl_result, servicebus_client)
    print("finished", msg.message_id, "at", datetime.now(), "with status", rtrvl_result.status.value)
    return rtrvl_result

def parse_msg_body(msg: ServiceBusMessage) -> RetrievalRequest:
    msg_req = loads(str(msg))

    rtrvl_req = RetrievalRequest(
                url=msg_req.get('url'),
                method=SupportedHttpMethod[msg_req.get('method', 'GET').upper()],
                timeout_seconds=int(msg_req.get('timeout_secs', '10')),
                save_to=msg_req.get('save_to'),
                file_type=FileType[msg_req.get('file_type', 'SIMPLE').upper()]
            )
    target_rtrvl_http_headers_str = msg_req.get('http_headers', None)
    if target_rtrvl_http_headers_str is not None and len(target_rtrvl_http_headers_str) > 0:
        rtrvl_req.http_headers = literal_eval(target_rtrvl_http_headers_str)
    return rtrvl_req

def send_response(
        msg: ServiceBusMessage,
        rtrvl_result: RetrievalResponse,
        servicebus_client: ServiceBusClient
    ):
    if msg.reply_to is None:
        if msg.message_id is None:
            print("No reply_to or message_id in message")
            return
        else:
            print("No reply_to in message", msg.message_id) 
            return
    elif msg.message_id is None:
        print("No message_id in message")
        return
    # check if msg.reply_to_type is topic ignoring case
    if (msg.application_properties is None or 
            msg.application_properties.get('reply_to_type') != 'topic'):
        send_response_queue(msg.reply_to, msg.message_id, rtrvl_result, servicebus_client)
    else:
        send_response_topic(msg.reply_to, msg.message_id, rtrvl_result, servicebus_client)

def send_response_topic(
        topic_name: str,
        correlation_id: str, 
        rtrvl_result: RetrievalResponse,
        servicebus_client: ServiceBusClient
    ):
    sender = servicebus_client.get_topic_sender(topic_name=topic_name)
    with sender:
        try:
            json = dumps(rtrvl_result, default=vars)
            message = ServiceBusMessage(json)
            message.correlation_id = correlation_id
            sender.send_messages(message)
            print("Sent response to", topic_name)
        except Exception as e:
            print("Failed to send response to", topic_name, ":", e)
    print("response sent", message.message_id)


def send_response_queue(
        queue_name: str,
        correlation_id: str,
        rtrvl_result: RetrievalResponse,
        servicebus_client: ServiceBusClient
    ):
    sender = servicebus_client.get_queue_sender(queue_name=queue_name)
    with sender:
        try:
            json = dumps(rtrvl_result, default=vars)
            message = ServiceBusMessage(json)
            message.correlation_id = correlation_id
            sender.send_messages(message)
            print("Sent response to", queue_name)
        except Exception as e:
            print("Failed to send response to", queue_name, ":", e)
    print("response sent", message.message_id)

if __name__ == "__main__":
    main()