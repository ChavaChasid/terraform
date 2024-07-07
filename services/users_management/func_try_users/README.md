# Add user function

This folder contains code that will be deployed to the function-app in Azure - the code gets the details of a new user to add in Azure and runs a function to add him.

## Dependencies

The following dependencies are required to run the code end deploy to function-app:

- azure-functions
- azure-cli
- python-dotenv
- requests
- msal

These dependencies exist in the 'requirements.txt' file.

## Running the code

The code is automatically run using CI CD processes through workflow.

## Tests

The code has undergone in-depth TEST tests with respect to end situations, the tests are also automatically run in the CI CD process through workflow.
