# **Services**

This project is responsible for automations in Azure in order to maintain proper resource management in the cloud.

This project is divided into several function-apps, each of which is responsible for a separate part of the process - the automatic.

The construction of the architecture was done in the form of division into folders according to topics so that each subfolder is deployed to a function-app.

## **Subscription-management**

The Azure environment is managed according to subscriptions that help manage permissions and resources efficiently so that a clear separation can be made between environments. To automatically generate financial optimization of the resources in the cloud, regular monitoring is required so that no subscriptions remain unused.

The automation that will be scheduled at every fixed period of time will locate subs that have not been used in the recent period and will send an alert to the direct manager's email in order for him to check the need for this sub. The summary of the alerts sent will be sent to the cloud domain manager to optimize the follow-up of the treatment.

## **Storage-managment**

Managing a cloud environment requires proper management both technically and in terms of financial management. The cloud storage accounts are resources with great potential for creating unnecessary financial anomalies. The purpose of the finOps automation is to automatically generate financial optimization of the resources in the cloud.

The automation that will be scheduled at any fixed period of time will monitor and check all storage accounts. In the event that an account stores data that is not in use or information is not extracted from it, that is to say the storage is not useful - The function-app send an alert to the email of the owner of the subscription in order for him to check the need for this account, thus avoiding wasting money. The summary of the alerts sent will be sent to the administrator of the cloud domain in order to optimize the follow-up of the treatment.

## Dependencies

The following dependencies are required to run the code end deploy to function-app:

- azure-functions
- azure-cli
- azure-identity
- azure-data-tables
- azure-storage-blob
- azure-mgmt-monitor
- azure-mgmt-consumption
- azure-mgmt-resource
- azure-mgmt-storage
- azure-keyvault-secrets
- pytest
- pytest_mock
- ruff
- python-dateutil
- pytest-cov
- python-dotenv
- pytz
- requests
- openpyxl

These dependencies exist in the 'requirements.txt' file.

## Running the code

process is activated using Logic-app, which is automatically scheduled every month and activates the first function-app, which activates the following ones.
The construction of the various resources in Azure was done using Terraform, which is responsible for building resources in Azure.
The code is automatically deployed to the various functions-app through the CI/CD process.

## Tests

The code has undergone in-depth TEST tests with respect to end situations.
