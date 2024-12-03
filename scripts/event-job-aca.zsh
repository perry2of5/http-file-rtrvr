#!/bin/zsh

source ${0:a:h}/env-vars.zsh

az group create --name ${RESOURCE_GROUP} --location ${LOCATION}

# identity to access queues and storage:
az identity create --resource-group ${RESOURCE_GROUP} --name ${IDENTITY_NAME} --output json
export IDENTITY_CLIENT_ID=$(az identity show --name ${IDENTITY_NAME} --resource-group "${RESOURCE_GROUP}" \
    --query clientId --output tsv)
export IDENTITY_ID=$(az identity show --name ${IDENTITY_NAME} --resource-group "${RESOURCE_GROUP}" \
    --query id --output tsv)

# ###### Create Service Bus Namespace and Queues ######
az servicebus namespace create --resource-group ${RESOURCE_GROUP} --name ${ASB_NAMESPACE} --location ${LOCATION}
export ASB_NAMESPACE_SCOPE=$(az servicebus namespace show --resource-group ${RESOURCE_GROUP} \
    --name ${ASB_NAMESPACE} --query id --output tsv)
# grant identity access to the namespace - otherwise KEDA can't monitor the number of messages in the queue.
# It will appear to work until it is idle for a while and then it will stop scaling according to various
# posts on the internet.
az role assignment create --role "${ASB_IAM_ROLE}" --assignee "${IDENTITY_CLIENT_ID}" \
    --scope "${ASB_NAMESPACE_SCOPE}"

# request queue
az servicebus queue create --resource-group ${RESOURCE_GROUP} --namespace-name ${ASB_NAMESPACE} \
    --name ${ASB_DWNLD_REQ_QUEUE_NAME}
# get connection string for download request queue
export ASB_CONN_STR=$(az servicebus namespace authorization-rule keys list --resource-group ${RESOURCE_GROUP} \
    --namespace-name ${ASB_NAMESPACE} --name RootManageSharedAccessKey --query primaryConnectionString --output tsv)
# Get scope of the request queue
export ASB_REQ_Q_SCOPE=$(az servicebus queue show --name ${ASB_DWNLD_REQ_QUEUE_NAME} \
    --namespace-name ${ASB_NAMESPACE} --resource-group ${ASB_RESOURCE_GRP} --query id --output tsv)
# grant identity access to request queue
az role assignment create --role "${ASB_IAM_ROLE}" --assignee ${IDENTITY_CLIENT_ID} \
    --scope "${ASB_REQ_Q_SCOPE}"

# reply topic
az servicebus topic create --resource-group ${RESOURCE_GROUP} --namespace-name ${ASB_NAMESPACE} \
    --name ${ASB_DWNLD_CMPLT_TOPIC_NAME}
export ASB_RESP_TOPIC_SCOPE=$(az servicebus topic show --name ${ASB_DWNLD_CMPLT_TOPIC_NAME} \
    --namespace-name ${ASB_NAMESPACE} --resource-group ${ASB_RESOURCE_GRP} --query id --output tsv)
az role assignment create --role "${ASB_IAM_ROLE}" --assignee ${IDENTITY_CLIENT_ID} \
    --scope "${ASB_RESP_TOPIC_SCOPE}"

# Grant access to reply topic and request queue to the airflow app
export AIRFLOW_APP_ID=$(az ad app list --filter "displayName eq ${AIRFLOW_APP_NAME}" --query '[0].appId' --output tsv)
az role assignment create --role "${ASB_IAM_ROLE}" --assignee ${AIRFLOW_APP_ID} \
    --scope "${ASB_RESP_TOPIC_SCOPE}"
az role assignment create --role "${ASB_IAM_ROLE}" --assignee ${AIRFLOW_APP_ID} \
    --scope "${ASB_REQ_Q_SCOPE}"



# create storage account to store downloaded files in
az storage account create --name ${STORAGE_ACCOUNT_NAME} --resource-group ${RESOURCE_GROUP} \
    --location ${LOCATION} --sku Standard_RAGRS --kind StorageV2 --min-tls-version TLS1_2 \
    --allow-blob-public-access false
export STORAGE_ACCOUNT_SCOPE=$(az storage account blob-service-properties show \
    --account-name ${STORAGE_ACCOUNT_NAME} --resource-group ${RESOURCE_GROUP} --query id --output tsv)
# grant identity access to storage account
az role assignment create --role "Storage Blob Data Contributor" --assignee ${IDENTITY_CLIENT_ID} \
    --scope "${STORAGE_ACCOUNT_SCOPE}"


# create container registry
az acr create --name "${CONTAINER_REGISTRY_NAME}" --resource-group "${RESOURCE_GROUP}" \
    --location "${LOCATION}" --sku Basic --admin-enabled true
# Build docker image for job to run.
az acr build --registry "${CONTAINER_REGISTRY_NAME}" \
    --image "${CONTAINER_IMAGE_NAME}"  "https://github.com/perry2of5/http-file-rtrvr.git"


az containerapp env create --name ${ENVIRONMENT} --resource-group ${RESOURCE_GROUP} --location ${LOCATION}

# The AZURE_CLIENT_ID environment variable tells the python azure-identify library to look for the user-managed identity
# https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#specify-a-user-assigned-managed-identity-with-defaultazurecredential
az containerapp job create --name "${JOB_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --environment "${ENVIRONMENT}" \
    --trigger-type "Event" \
    --replica-timeout "1800" \
     --replica-retry-limit 2 \
    --min-executions "0" \
    --max-executions "1" \
    --polling-interval "300" \
    --scale-rule-name "scale-q-${ASB_DWNLD_REQ_QUEUE_NAME}" \
    --scale-rule-type "azure-servicebus" \
    --scale-rule-metadata \
        "namespace=${ASB_NAMESPACE}" \
        "queueName=${ASB_DWNLD_REQ_QUEUE_NAME}" \
        "messageCount=1" \
    --scale-rule-auth "connection=connection-string-secret" \
    --secrets \
        "connection-string-secret=${ASB_CONN_STR}" \
    --image "${CONTAINER_REGISTRY_NAME}.azurecr.io/${CONTAINER_IMAGE_NAME}" \
    --cpu "0.5" \
    --memory "1Gi" \
    --registry-server "${CONTAINER_REGISTRY_NAME}.azurecr.io" \
    --env-vars \
        "STORAGE_ACCOUNT_URL=${STORAGE_ACCOUNT_URL}" \
        "STORAGE_CONTAINER_NAME=${STORAGE_CONTAINER_NAME}" \
        "DOWNLOAD_TEMP_DIR=/home/svcuser/tmp/http_rtrvr_temp" \
        "SVC_BUS_FQN=${ASB_NAMESPACE}.servicebus.windows.net" \
        "QUEUE_NAME=${ASB_DWNLD_REQ_QUEUE_NAME}" \
        "AZURE_CLIENT_ID=${IDENTITY_CLIENT_ID}" \
    --mi-user-assigned "${IDENTITY_ID}"

# az containerapp job identity assign --name "${JOB_NAME}" --resource-group "${RESOURCE_GROUP}" \
#     --user-assigned "${IDENTITY_NAME}"


# az containerapp job delete --name "$JOB_NAME" --resource-group "$RESOURCE_GROUP"
# az containerapp env delete --name ${ENVIRONMENT} --resource-group ${RESOURCE_GROUP} --location ${LOCATION}