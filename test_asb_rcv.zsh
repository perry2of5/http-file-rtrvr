export STORAGE_ACCOUNT_URL=https://devtimstoregrp1.blob.core.windows.net
export STORAGE_CONTAINER_NAME=testcontainer
export DOWNLOAD_TEMP_DIR=/tmp/http_rtrvr_temp

export SVC_BUS_FQN=tim-dev-airflow-azure-msg-bus.servicebus.windows.net
export QUEUE_NAME=file-download-request

# {
# "url": "https://example.com/index.html",
# "save_to":"json_rtvrl_test",
# "file_type":"simple",
# "result_queue_name": "tdp-test-queue"
# }
# {"url": "https://example.com/index.html","save_to": "json_rtvrl_test","file_type": "simple"}

# {
# "url": "https://github.com/perry2of5/http-file-rtrvr/archive/refs/heads/main.zip",
# "save_to":"json_rtvrl_test",
# "file_type":"archive"
# }

poetry run python http_file_rtrvr/azure_svc_bus_http_file_rtrvr.py
