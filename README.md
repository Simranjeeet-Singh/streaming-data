# Streaming Data Project

## Overview 

The app automates the process of pulling articles from The Guardian API based on search term and sending those articles to an AWS SQS queue.It uses AWS Lambda, API Gateway, and SQS, with infrastructure deployed using Terraform. The app takes the input of search term and date from which to start looking, and then locates the articles using The Guardian API and then takes the Web Title,Publication Date and the article Web Url and posts it to AWS SQS queue.

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Setup Instructions](#setup-instructions)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Usage](#usage)
7. [Cleaning Up](#cleaning-up)

## Features
- Fetches news articles from The Guardian API.
- Sends the articles to AWS SQS using AWS Lambda.
- Easy deployment using Makefile and Terraform.

## Requirements
The local machine must have the following installed so to test project locally and deployment on AWS from the local OS.

- **Python**: 3.9 or above.
- **AWS CLI v2**: To configure AWS credentials locally.
- **Terraform**: v1.7.5 or higher.

The Python packages which are required are divided into two parts. The details of installing them with Make File commands which uses the commands in make file can be found in the Setup Instructions.
- **Python Dependencies**:
  - **Lambda Requirements** (`requirements-lambda.txt`): `requests`, `boto3`.
  - **Testing Requirements** (`requirements-test.txt`): `requests`, `boto3`, `pytest`.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Simranjeeet-Singh/streaming-data.git
cd streaming-data
```

### 2. Setting up local environment

The venv is created using the following make command:

```
make create-venv
```

To activate the local environment run: 

```
. venv/bin/activate
```

Install all dependencies into the venv needed for testing locally:

```
make install-dependencies
```

## Testing

To ensure everything works as expected, you can run the local testing before deployment using the following command:

```
make run-tests
```

## Deployment


### 1. Set Up AWS Credentials

Ensure your AWS credentials are set up correctly by running:

```
aws configure
```

This will prompt you to enter your AWS Access Key, Secret Key, region, etc.

### 2. Provide the Guardian API Key

The project requires a Guardian API key for accessing The Guardian API. You can set this API key while deploying.

If you haven't already, obtain a Guardian API key from The Guardian Open Platform.


### 3. Deploy the Project

To deploy the Lambda function and related AWS infrastructure using Terraform, use the following command:

```
make deploy-lambda guardian_api_key=your-guardian-api-key
```
The api key will become the environment variable for Lambda function.
This will:

    Package the Lambda function and its dependencies.
    Deploy the Lambda function, SQS queue, and API Gateway and stage it using Terraform.
    Set up the Guardian API key in AWS Lambda.

If the guardian api key is not passed through with terraform deployment then it can added/edited from the AWS management console in lambda under configuration section after deployment.

### 4. API Gateway-Invoking from CLI

After deployment, the Terraform script will output the API Gateway URL that can be used to invoke the Lambda function.

```
curl -X POST "<your_api_gateway_url>/articles" -H "Content-Type: application/json" -d '{"search_term": "machine learning", "date_from": "2023-01-01"}'
```
Replace <your_api_gateway_url> with the API gateway URL that will be displayed as output after terraform deployment. The api gateway url can also be obtained from the AWS management console from the api gateway deployed through the project.

### 5. Testing on AWS after cloud deployment

Lambda can be tested from the aws management console by invoking with the json paramters as :
```
{
  "search_term": "machine learning",
  "date_from": "2023-01-01"
}
```

## Usage

After the succesful deployment of the Lambda function, the lambda can be invoke in two ways through the AWS Console and CLI via API Gateway.

## Cleaning up

To clean up and destroy all AWS resources created by the deployment, use the following command:

```
make destroy-lambda
```
## Makefile Overview

```
zip-lambda: Creates a Lambda deployment package.
run-tests: Executes unit tests.
deploy-lambda: Deploys all AWS resources using Terraform.
destroy-lambda: Tears down all infrastructure.
```

## Project Structure

```

streaming-data/
│
├── src/                     # Contains the main Python files and modules
│   ├── main.py              # Entry point for the Lambda function
│   ├── message_broker.py    # SQS handling functionality
│   └── guardian_api.py      # API interaction with The Guardian
│
├── tests/                   # Unit tests
│   ├── test_main.py
│   ├── test_message_broker.py
│   └── test_guardian_api.py
│
├── terraform/               # Terraform configuration files
│   ├── main.tf              # Defines AWS resources (Lambda, SQS, API Gateway)
│   ├── variables.tf         # Defines input variables like API key
│
├── Makefile                 # Automation for build, deploy, test, and clean
├── requirements-test.txt    # Python dependencies for local testing
├── requirements-lambda.txt  # Python dependencies for Lambda 
└── README.md                # Project documentation (this file)
```
### Variables

API_KEY: The Guardian API key used to fetch articles.

AWS_REGION: AWS region for deploying the infrastructure (default: eu-west-2).

### Notes

Guardian API Rate Limits: Be mindful of the Guardian API rate limits, especially when testing.

Security: Do not hardcode sensitive information like API keys or AWS credentials. Always set them via environment variables or Terraform inputs.

