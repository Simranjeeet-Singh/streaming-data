output "sqs_queue_url" {
  value = aws_sqs_queue.guardian_articles_queue.url
}