resource "aws_lambda_function" "image_processor" {
  function_name = "image_processor_lambda_29"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_sqs.lambda_handler"
  runtime       = "python3.8"
  timeout       = 30  # Timeout configured for longer image processing time

  filename = data.archive_file.lambda_zip.output_path

  environment {
    variables = {
      BUCKET_NAME = "pgr301-couch-explorers"
    }
  }

  depends_on = [aws_iam_role_policy.lambda_sqs_s3_bedrock_policy]
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.image_generation_queue.arn
  function_name    = aws_lambda_function.image_processor.arn
  enabled          = true
}
