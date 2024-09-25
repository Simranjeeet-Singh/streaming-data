resource "aws_sqs_queue" "guardian_articles_queue" {
  name = "guardian-articles-queue"
}

resource "aws_iam_user" "sqs_user" {
  name = "sqs-user"
}

resource "aws_iam_user_policy" "sqs_user_policy" {
  name   = "SQSUserPolicy"
  user   = aws_iam_user.sqs_user.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "sqs:SendMessage",
        Resource = aws_sqs_queue.guardian_articles_queue.arn
      }
    ]
  })
}