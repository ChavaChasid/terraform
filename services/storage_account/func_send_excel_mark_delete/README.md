# Send Email and mark for delete function

This folder contains code that will be deployed to function-app in Azure.
The function receives the list of notifications sent,
exports the data to an Excel table and sends the Excel to the main administrator.
In addition, the function receives a list of storage accounts that exist in the current test,
and records in the Deletion table the storage accounts that existed in the previous test and now no longer exist.

## Dependencies

The following dependencies are required to run the code end deploy to function-app:

- azure-core
- azure-data-tables
- azure-functions
- azure-identity
- azure-keyvault-secrets
- azure-mgmt-storage
- azure-mgmt-monitor
- azure-storage-blob
- black
- pandas
- pytest
- pytest-cov
- python-dotenv
- openpyxl

These dependencies exist in the 'requirements.txt' file.

## Running the code

The code is automatically run using CI CD processes through workflow.

## Tests

The code has undergone in-depth TEST tests with respect to end situations,
the tests are also automatically run in the CI CD process through workflow.
