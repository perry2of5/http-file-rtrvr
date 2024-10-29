docker run \
    -v ~/.azure:/home/svcuser/.azure \
    --env PYTHONPATH=. \
    --env STORAGE_ACCOUNT_URL=https://devtimstoregrp1.blob.core.windows.net \
    --env STORAGE_CONTAINER_NAME=testcontainer \
    --env DOWNLOAD_TEMP_DIR=/tmp/http_rtrvr_temp \
    --env TARGET_RTRVL_URL=https://example.com/index.html \
    --env TARGET_RTRVL_SAVE_TO=env_tst_script_docker \
    --env TARGET_RTRVL_FILE_TYPE=simple \
    --env TARGET_RTRVL_TIMEOUT_SECS=20 \
    --env TARGET_RTRVL_METHOD=GET \
    --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID \
    --env AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET \
    --env AZURE_TENANT_ID=$AZURE_TENANT_ID \
    timstestcntnrreg.azurecr.io/http_file_rtrvr:0.0.3
