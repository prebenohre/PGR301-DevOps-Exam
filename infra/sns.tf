resource "aws_sns_topic" "sqs_age_alarm_topic" {
  name = "sqs-age-alarm-topic-29"
}

resource "aws_sns_topic_subscription" "alarm_email_subscription" {
  topic_arn = aws_sns_topic.sqs_age_alarm_topic.arn
  protocol  = "email"
  endpoint  = var.alarm_email
}
