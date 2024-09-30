
# Streaming Data Project

## Project Overview
The **Streaming Data Project** retrieves articles from The Guardian API using a search term and optionally a date. It posts the results (up to 10 articles) to an AWS SQS queue for consumption by other applications. 

The project uses Terraform for infrastructure deployment, AWS Lambda to handle the processing, and an API Gateway to trigger the Lambda function.

## Requirements
Before you begin, ensure you have the following installed:

- **Python** (version 3.9 or higher)
- **AWS CLI** with properly configured credentials
- **Terraform** (version 1.0+)
- **Make** (for running the deployment commands)

## Installation and Setup

### 1. Clone the Repository
First, clone the project repository to your local machine and navigate to the project directory:
```bash
git clone https://github.com/Simranjeeet-Singh/streaming-data.git
cd streaming-data
```

### 2. Install Dependencies

Install the Python dependencies specified in the requirements.txt file:

```
pip install -r requirements.txt
```

### 3. Set Up AWS Credentials

Ensure your AWS credentials are set up correctly by running:

```
aws configure
```

This will prompt you to enter your AWS Access Key, Secret Key, region, etc.

### 4. Provide the Guardian API Key

The project requires a Guardian API key for accessing The Guardian API. You can set this API key while deploying.

If you haven't already, obtain a Guardian API key from The Guardian Open Platform.
### 5. Deploy the Project

To deploy the Lambda function and related AWS infrastructure using Terraform, use the following command:

```
make deploy-lambda API_KEY=your_guardian_api_key
```
The api key will become the environment variable for Lambda function which can also be changed from the console directly after deployment.
This will:

    Package the Lambda function and its dependencies.
    Deploy the Lambda function, SQS queue, and API Gateway using Terraform.
    Set up the Guardian API key in AWS Lambda.

### 6. Test Lambda Invocation

You can test your deployed Lambda function using AWS API Gateway:

```
curl -X POST <api_gateway_url> -d '{"search_term": "machine learning", "date_from": "2023-01-01"}'
```
Replace <api_gateway_url> with the actual URL generated from the deployment.
### 7. Run Tests

To ensure everything works as expected, you can run the tests using the following command:

```
make run-tests
```
### 8. Destroy Resources

To clean up and destroy all AWS resources created by the deployment, use the following command:

```
make destroy-lambda
```
### Project Structure

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
│   └── outputs.tf           # Defines output for resources like SQS URL
│
├── Makefile                 # Automation for build, deploy, test, and clean
├── requirements.txt         # Python dependencies
├── module-requirements.txt  # Additional Project Modules
└── README.md                # Project documentation (this file)
```
### Variables

API_KEY: The Guardian API key used to fetch articles.

AWS_REGION: AWS region for deploying the infrastructure (default: eu-west-2).

### Notes

Guardian API Rate Limits: Be mindful of the Guardian API rate limits, especially when testing.

Security: Do not hardcode sensitive information like API keys or AWS credentials. Always set them via environment variables or Terraform inputs.

