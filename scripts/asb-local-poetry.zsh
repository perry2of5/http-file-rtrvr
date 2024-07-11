#!/bin/zsh

source ${0:a:h}/env-vars.zsh

export DOWNLOAD_TEMP_DIR=/tmp
export SVC_BUS_FQN=${ASB_NAMESPACE}.servicebus.windows.net
export QUEUE_NAME=${ASB_DWNLD_REQ_QUEUE_NAME}


# assign the local azure CLI user access to the necessary components.
export CURRENT_USER_NAME=$(az ad signed-in-user show --query "userPrincipalName" --output tsv)
export USER_ID=$(az ad signed-in-user show --query "id" --output tsv)

export STORAGE_ACCOUNT_SCOPE=$(az storage account show \
    --name ${STORAGE_ACCOUNT_NAME} --resource-group ${RESOURCE_GROUP} --query id --output tsv)

az role assignment create --role "Storage Blob Data Contributor" --assignee ${CURRENT_USER_NAME} \
    --scope "${STORAGE_ACCOUNT_SCOPE}"

export ASB_REQ_Q_SCOPE=$(az servicebus queue show --name ${ASB_DWNLD_REQ_QUEUE_NAME} \
    --namespace-name ${ASB_NAMESPACE} --resource-group ${ASB_RESOURCE_GRP} --query id --output tsv)
export ASB_RESP_Q_SCOPE=$(az servicebus queue show --name ${ASB_DWNLD_CMPLT_QUEUE_NAME} \
    --namespace-name ${ASB_NAMESPACE} --resource-group ${ASB_RESOURCE_GRP} --query id --output tsv)

az role assignment create --role "Azure Service Bus Data Owner" --assignee ${USER_ID} \
    --scope "${ASB_REQ_Q_SCOPE}"
az role assignment create --role "Azure Service Bus Data Owner" --assignee ${USER_ID} \
    --scope "${ASB_RESP_Q_SCOPE}"


# now run the darn thing :)
poetry run python http_file_rtrvr/azure_svc_bus_http_file_rtrvr.py
