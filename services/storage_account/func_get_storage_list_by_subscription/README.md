# Get storage list by subscription function

This folder contains code that will be deployed to function-app in Azure.
The function receives the name of the subscription and returns all the storage in it.

## Dependencies

The following dependencies are required to run the code end deploy to function-app:

- azure-functions
- azure-identity
- azure-mgmt-storage
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
