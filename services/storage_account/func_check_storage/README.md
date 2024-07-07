# Test storages function

This folder contains code that will be deployed to function-app in Azure.
The function receives data belonging to the particular storage on which the test is performed,
Checks whether the capacity has increased since the previous test and whether data was retrived from it in X last time,
sending an alert if necessary.
She records all the findings in the documentation table.
and returns the list of storages that the supervisors have been notified about.

## Dependencies

The following dependencies are required to run the code end deploy to function-app:

- azure-data-tables
- azure-core
- azure-functions
- azure-identity
- azure-keyvault-secrets
- azure-mgmt-storage
- azure-mgmt-monitor
- black
- pandas
- pytest
- pytest-cov
- python-dotenv

These dependencies exist in the 'requirements.txt' file.

## Running the code

The code is automatically run using CI CD processes through workflow.

## Tests

The code has undergone in-depth TEST tests with respect to end situations,
the tests are also automatically run in the CI CD process through workflow.
