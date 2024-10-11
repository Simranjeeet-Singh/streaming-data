provider "aws" {
  region = var.region
}

# Create IAM role for Lambda
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [{
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      }
    }]
  })
}

# Attach permissions to Lambda role
resource "aws_iam_role_policy" "lambda_execution_policy" {
  name   = "lambda_execution_policy"
  role   = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "sqs:SendMessage",
          "sqs:GetQueueUrl",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage"
        ],
        "Resource": aws_sqs_queue.guardian_articles_queue.arn
      }
    ]
  })
}

# Create SQS Queue
resource "aws_sqs_queue" "guardian_articles_queue" {
  name = "guardian-articles-queue"
}

# SQS Queue policy
resource "aws_sqs_queue_policy" "guardian_articles_queue_policy" {
  queue_url = aws_sqs_queue.guardian_articles_queue.id

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": [
          "SQS:SendMessage",
          "SQS:GetQueueUrl"
        ],
        "Resource": aws_sqs_queue.guardian_articles_queue.arn,
        "Condition": {
          "ArnEquals": {
            "aws:SourceArn": aws_lambda_function.guardian_lambda.invoke_arn
          }
        }
      }
    ]
  })
}

# Lambda function
resource "aws_lambda_function" "guardian_lambda" {
  function_name = "guardian-article-lambda"
  handler       = "main.lambda_handler"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_execution_role.arn
  filename      = "../lambda_package.zip"  # Add packaging step for your function
  environment {
    variables = {
      GUARDIAN_API_KEY = var.guardian_api_key
      SQS_QUEUE_NAME   = aws_sqs_queue.guardian_articles_queue.name
    }
  }
}

# API Gateway REST API
resource "aws_api_gateway_rest_api" "guardian_api" {
  name = "guardian-api"
}

# API Gateway resource (for Lambda trigger)
resource "aws_api_gateway_resource" "articles" {
  rest_api_id = aws_api_gateway_rest_api.guardian_api.id
  parent_id   = aws_api_gateway_rest_api.guardian_api.root_resource_id
  path_part   = "articles"
}

# API Gateway method
resource "aws_api_gateway_method" "get_articles" {
  rest_api_id   = aws_api_gateway_rest_api.guardian_api.id
  resource_id   = aws_api_gateway_resource.articles.id
  http_method   = "POST"
  authorization = "NONE"
}

# API Gateway integration with Lambda
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.guardian_api.id
  resource_id             = aws_api_gateway_resource.articles.id
  http_method             = aws_api_gateway_method.get_articles.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.guardian_lambda.invoke_arn
}

# API Gateway deployment
resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.guardian_api.id
  stage_name  = "prod"  # Name this stage appropriately for deployment
  depends_on  = [aws_api_gateway_integration.lambda_integration]
}

# Grant API Gateway permission to invoke Lambda
resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.guardian_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.guardian_api.execution_arn}/*/*"
}

# Output API Gateway URL after deploying
output "api_gateway_url" {
  value = aws_api_gateway_deployment.deployment.invoke_url
  description = "URL for accessing the deployed API Gateway endpoint."
}
