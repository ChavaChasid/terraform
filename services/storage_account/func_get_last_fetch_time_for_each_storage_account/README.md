# Get last fetch time for-each storage account function

This folder contains code that will be deployed to function-app in Azure.
The function extracts data from Log analytics and returns the last usage time for each storage account.
Later on in the automation, these data are used to check if the Storge account is in use.

## Dependencies

The following dependencies are required to run the code end deploy to function-app:

- azure-functions
- azure-identity
- azure-monitor-query
- black
- pytest
- pytest-cov
- python-dotenv

These dependencies exist in the 'requirements.txt' file.

## Running the code

The code is automatically run using CI CD processes through workflow.

## Tests

The code has undergone in-depth TEST tests with respect to end situations,
the tests are also automatically run in the CI CD process through workflow.
