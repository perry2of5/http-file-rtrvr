# $ACR_NAME must be the name of the ACR
# $ACR_TOKEN must be the token name shown in the ACR console (or retrieved with the CLI obviously).
# $ACR_PWD must be the password from the ACR token. Ideally these need to be stored in the Azure Key Vault.

# $ASSIGN_IDENTITY is the id of the managed identify permissions will be retrieved with. I think the identity
# needs to be in the same resource group as the container. The identity can be found with the following command:
# az identity show \
#   --resource-group airflow-container-resource-group-west \
#   --name <identity-name> \
#   --query id \
#   --output tsv

az container create \
    -g airflow-container-resource-group-west \
    --name  testacihttprtrvr9 \
    --image timstestcntnrreg.azurecr.io/http_file_rtrvr:0.0.3 \
    --assign-identity $ASSIGN_IDENTITY \
    --registry-login-server $ACR_NAME.azurecr.io \
    --registry-username $ACR_TOKEN \
    --registry-password "$ACR_PWD" \
    --restart-policy Never \
    --environment-variables \
            'STORAGE_ACCOUNT_URL=https://devtimstoregrp1.blob.core.windows.net' \
            'STORAGE_CONTAINER_NAME=testcontainer' \
            'DOWNLOAD_TEMP_DIR=/tmp/http_rtrvr_temp' \
            'TARGET_RTRVL_URL=https://github.com/perry2of5/http-file-rtrvr/archive/refs/heads/main.zip' \
            'TARGET_RTRVL_SAVE_TO=env_tst_script_aci' \
            'TARGET_RTRVL_FILE_TYPE=archive' \
            'TARGET_RTRVL_TIMEOUT_SECS=30' \
            'TARGET_RTRVL_METHOD=GET' 

