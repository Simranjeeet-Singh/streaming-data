# Streaming Data Project

## Overview 

The app automates the process of pulling articles from The Guardian API based on search term and sending those articles to an AWS SQS queue.It uses AWS Lambda, API Gateway, and SQS, with infrastructure deployed using Terraform. The app takes the input of search term and starting date, and then locates the articles using The Guardian API and then sends the Web Title,Publication Date and the article Web Url to an AWS SQS queue.

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Setup Instructions](#setup-instructions)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Usage](#usage)
7. [Cleaning Up](#cleaning-up)
8. [Makefile Overview](#makefile-overview)
9. [Project Structure](#project-structure)
10. [Notes](#notes)

## Features
- Fetches news articles from The Guardian API.
- Sends the articles to AWS SQS using AWS Lambda.
- Easy deployment using Makefile and Terraform.

## Requirements

### AWS Acoount
You will need an **AWS Account** to set up the infrastructure. If you don't already have an account, you can create one here: [AWS Account Sign-Up](https://aws.amazon.com/free).

### The Guardian API Key
To fetch news articles, you need a **Guardian API Key**. Register for a developer API key at [The Guardian Open Platform](https://open-platform.theguardian.com/access/).

### Software Requirements
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

Create the virtual environment using the following Makefile command:

```
make create-venv
```

To activate the virtual environment, run:

```
. venv/bin/activate
```

Install all dependencies into the virtual environment needed for testing locally:

```
make install-dependencies
```

## Testing

To ensure everything works as expected, you can run the local testing before deployment using the following command:

```
make run-tests
```
Ensure that you have activated the virtual environment (. venv/bin/activate) before running the tests.

## Deployment


### 1. Set Up AWS Credentials

Ensure your AWS credentials are set up correctly by running:

```
aws configure
```

This will prompt you to enter your AWS Access Key, Secret Key, region, etc.


### 2. Deploy the Project

To deploy the Lambda function and related AWS infrastructure using Terraform, use the following command:

```
make deploy-lambda guardian_api_key=your-guardian-api-key
```
The api key will become the environment variable for Lambda function.
This command will:

- Package the Lambda function and its dependencies.
- Deploy the Lambda function, SQS queue, and API Gateway and stage it using Terraform.
- Set up the Guardian API key in AWS Lambda.

If the guardian api key is not passed through with terraform deployment then it can added/edited from the AWS management console in lambda under configuration section after deployment.

### 3. API Gateway-Invoking from CLI

After deployment, the Terraform script will output the API Gateway URL that can be used to invoke the Lambda function using curl command stated in this section.
The api gateway URL will be like : 

```https://<api-id>.execute-api.<aws-region>.amazonaws.com/prod
```
The <api-id> can also be obtained from the AWS management console, and 'prod' is the stage name set up in the project.
The following command invokes lambda function:

```
curl -X POST "<your_api_gateway_url>/articles" -H "Content-Type: application/json" -d '{"search_term": "machine learning", "date_from": "2023-01-01"}'
```
Replace <your_api_gateway_url> with the API gateway URL that will be displayed as output after terraform deployment. The value for "search_term" and "date_from" is user input.

### 4. Testing on AWS after cloud deployment

Lambda can be tested from the aws management console by invoking with the json event. The guardian api key has to be provided as enviornment variable before testing with json event.

## Usage

After successfully deploying the Lambda function, it can be invoked in two ways:

- **AWS Console**: Test the Lambda directly via the "Test" button.
- **API Gateway via CL**: Use the API Gateway URL output to send a POST request.

## Cleaning up

To clean up and destroy all AWS resources created by the deployment, use the following command:

```
make destroy-lambda
```
## Makefile Overview

- **create-venv**: Creates a virtual environment for isolated Python dependencies.
- **install-dependencies**: Installs all dependencies required for local testing.
- **zip-lambda**: Packages Lambda deployment and its dependencies.
- **run-tests**: Executes unit tests.
- **deploy-lambda**: Deploys all AWS resources using Terraform.
- **destroy-lambda**: Tears down all infrastructure.

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

- guardian_api_key: The Guardian API key used to fetch articles.

- aws_region: AWS region for deploying the infrastructure (default: eu-west-2).

### Notes

Guardian API Rate Limits: Be mindful of the Guardian API rate limits, especially when testing.

Security: Do not hardcode sensitive information like API keys or AWS credentials. Use environment variables or Terraform inputs instead.

