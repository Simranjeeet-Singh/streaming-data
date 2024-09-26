resource "aws_lambda_function" "guardian_lambda" {
  function_name = "guardian-article-lambda"
  handler       = "src.main.lambda_handler"
  runtime       = "python3.8"
  role          = aws_iam_role.lambda_execution_role.arn
  filename      = "lambda_package.zip"  # We will create this package later

  environment {
    variables = {
      GUARDIAN_API_KEY = "your-api-key-here"
      SQS_QUEUE_NAME   = aws_sqs_queue.guardian_articles_queue.name
    }
  }
}

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
          "sqs:GetQueueUrl"
        ],
        "Resource": aws_sqs_queue.guardian_articles_queue.arn
      }
    ]
  })
}
