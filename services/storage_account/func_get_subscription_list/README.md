# Get subscription list function

This folder contains code that will be deployed to function-app in Azure.
The function returns all existing Subscriptions in Azure.

## Dependencies

The following dependencies are required to run the code end deploy to function-app:

- azure-data-tables
- azure-functions
- azure-identity
- azure-keyvault-secrets
- azure-mgmt-subscription
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
