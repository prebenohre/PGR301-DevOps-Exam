output "sqs_queue_url" {
  description = "URL for SQS-køen som Lambda leser fra"
  value       = aws_sqs_queue.image_generation_queue.id
}

output "lambda_function_arn" {
  description = "ARN for Lambda-funksjonen med nytt navn"
  value       = aws_lambda_function.image_processor.arn
}
