export STORAGE_ACCOUNT_URL=https://devtimstoregrp1.blob.core.windows.net
export STORAGE_CONTAINER_NAME=testcontainer
export DOWNLOAD_TEMP_DIR=/tmp/http_rtrvr_temp
export TARGET_RTRVL_URL=https://github.com/perry2of5/http-file-rtrvr/archive/refs/heads/main.zip
export TARGET_RTRVL_SAVE_TO=env_tst_script_aci
export TARGET_RTRVL_FILE_TYPE=archive
export TARGET_RTRVL_TIMEOUT_SECS=30
export TARGET_RTRVL_METHOD=GET


poetry run python http_file_rtrvr/env_var_http_file_rtrvr.py
