data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda_sqs.py"  
  output_path = "${path.module}/lambda_function_payload.zip"
}
