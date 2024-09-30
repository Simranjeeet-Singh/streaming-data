Streaming Data Project
Overview

This project fetches articles from The Guardian API and publishes them to AWS SQS. It uses AWS Lambda and API Gateway for serverless architecture and Terraform for infrastructure deployment.
Features

    Fetches up to 10 recent articles from The Guardian API using a search term.
    Publishes article data to an AWS SQS queue.
    Automates infrastructure setup using Terraform and Makefile.

Prerequisites

    Python 3.x
    AWS Account and configured AWS CLI
    Terraform installed
    Guardian API key (free-tier available)

Setup Instructions
1. Clone the Repository

bash

git clone <your-forked-repo-url>
cd streaming-data

2. Install Python Dependencies

Create a virtual environment and install dependencies:

bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Configure AWS and Guardian API

Ensure AWS CLI is configured:

bash

aws configure

Set the Guardian API key in the environment:

bash

export GUARDIAN_API_KEY=<your-guardian-api-key>

4. Deploy with Terraform

Use the provided Makefile to zip the Lambda package and apply Terraform:

bash

make deploy-lambda

Terraform will provision:

    An AWS Lambda function
    SQS Queue
    API Gateway to trigger Lambda

5. Interacting with the API

Use the API Gateway to trigger Lambda and fetch articles. Example using curl:

bash

curl -X POST "<api_gateway_url>/articles" -d '{"search_term": "machine learning", "date_from": "2023-01-01"}'

6. Check SQS for Messages

You can check your AWS SQS queue for messages containing article details.
Example SQS Message:

json

{
    "webPublicationDate": "2023-01-01T12:34:56Z",
    "webTitle": "An Example Article",
    "webUrl": "https://www.theguardian.com/example-article"
}

7. Running Tests

Use pytest to run the unit tests:

bash

pytest

8. Cleaning Up

Destroy the infrastructure when finished:

bash

cd terraform
terraform destroy

Common Issues

    Error: API key not set: Ensure that GUARDIAN_API_KEY is set in your environment.
    Error: Terraform not initialized: Run terraform init inside the terraform/ directory before applying.

Contributions

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Push your changes and create a pull request.
