#!/bin/zsh

# we need the single quotes in the az command so they are wrapped in the double quotes so they'll be preserved
export AIRFLOW_APP_NAME="'tim-dev-http-dwnld-asb'"

export DPLMNT_SFFX="2024-12-04-v2"

export RESOURCE_GROUP="http-rtrvr-rsrc-grp-${DPLMNT_SFFX}"
export ENVIRONMENT="http-rtrvr-nvrnmnt-${DPLMNT_SFFX}"
export LOCATION="westus"
export JOB_NAME="http-rtrvr-job-${DPLMNT_SFFX}"

export CONTAINER_IMAGE_NAME="http-rtrvr-queue-reader-job:1.0"

# need repeatable ACR name for now.
# export CONTAINER_REGISTRY_NAME="tdpacareg202411130843125399139870"
# this will make an ACR name based off the date and time with a random number appended to the end.
export CONTAINER_REGISTRY_NAME="tdpacareg$(date "+%Y%m%dt%H%M%Srnd")$(head -200 /dev/urandom | cksum | cut -f1 -d " ")"

export IDENTITY_NAME="http-rtrvr-identity-asb-${DPLMNT_SFFX}"

# ASB = Azure Service Bus
export ASB_SUBSCRIPTION=$(az account show --query id --output tsv)
export ASB_NAMESPACE=http-rtrvr-asb-${DPLMNT_SFFX}
export ASB_RESOURCE_GRP=${RESOURCE_GROUP}
export ASB_DWNLD_REQ_QUEUE_NAME=file-rtrvr-request
export ASB_DWNLD_CMPLT_TOPIC_NAME=file-rtrvr-complete
# need to be data owner on the bus to get the number of messages to scale....
export ASB_IAM_ROLE="Azure Service Bus Data Owner"

export STORAGE_ACCOUNT_NAME=devtimstoregrp1
export STORAGE_ACCOUNT_URL=https://${STORAGE_ACCOUNT_NAME}.blob.core.windows.net
export STORAGE_CONTAINER_NAME=testcontainer

# if the identity is already created, you can get the client id by running the following command:
# export IDENTITY_CLIENT_ID=$(az identity show --name "${IDENTITY_NAME}" --resource-group "${RESOURCE_GROUP}" --query clientId --output tsv)