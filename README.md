Streaming Data Project
Project Overview

This project retrieves articles from The Guardian API based on user-defined search terms and posts them to an AWS SQS queue using AWS Lambda and API Gateway. The project is designed to be deployed on AWS infrastructure using Terraform for infrastructure management.
Key Features

    Fetches up to 10 articles from The Guardian API.
    Publishes articles in JSON format to an AWS SQS queue.
    Fully deployable using Terraform and AWS Lambda.
    Supports user input via API Gateway, ideal for integration into larger data platforms.

Requirements

    Python 3.9 or above.
    AWS Account with appropriate IAM permissions for Lambda, SQS, and API Gateway.
    Terraform v1.0 or later installed on your local machine.
    The Guardian API key.

Installation and Setup
1. Clone the Repository

bash

git clone https://github.com/Simranjeeet-Singh/streaming-data.git
cd streaming-data

2. Environment Setup

Ensure your system has pip and Python 3.9+. Install the necessary Python dependencies:

bash

pip install -r requirements.txt

3. Configure AWS Credentials

Ensure that your AWS credentials are configured properly. This can be done by using the AWS CLI:

bash

aws configure

4. Set Up API Key and Deploy

The deployment process requires the Guardian API key. To deploy the project, you can pass the key via the CLI using the following make command:

bash

make deploy-lambda API_KEY=your_guardian_api_key

This will:

    Install dependencies.
    Package the Lambda function.
    Deploy the infrastructure via Terraform.

5. Running Tests

To ensure everything is working as expected, you can run the tests using the following command:

bash

make run-tests

6. Destroy Resources

To clean up and remove the infrastructure created by Terraform, use:

bash

make destroy-lambda

How It Works

    Lambda Function: The Lambda function fetches articles from The Guardian API using search terms, then pushes the articles to an SQS queue.
    API Gateway: API Gateway is used to trigger the Lambda function, passing in user-defined search terms as a POST request.
    SQS: Articles are published in JSON format to the SQS queue for further consumption by downstream systems.

Project Structure

bash

.
├── Makefile                # Automation commands for deployment and testing
├── requirements.txt        # Python dependencies
├── src/
│   ├── main.py             # Lambda function handler
│   ├── guardian_api.py      # API logic to fetch Guardian articles
│   ├── message_broker.py    # SQS message sending logic
├── terraform/
│   ├── main.tf             # Terraform configuration for AWS resources
│   └── variables.tf        # Terraform input variables
├── tests/                  # Unit tests for the project
└── lambda_package.zip      # Zipped Lambda package (generated)

API Example

You can invoke the deployed Lambda function via API Gateway. The API expects the following POST request:

bash

curl -X POST https://<API_GATEWAY_URL>/articles -d '{"search_term": "machine learning", "date_from": "2023-01-01"}'

License

This project is open-source and available under the MIT License.

This README ensures the user has clear step-by-step instructions on setting up, deploying, testing, and destroying the project infrastructure. It also emphasizes the use of environment variables and includes clear instructions for the API usage.
