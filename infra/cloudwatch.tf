resource "aws_cloudwatch_metric_alarm" "sqs_age_alarm" {
  alarm_name          = "SQSApproximateAgeOfOldestMessageAlarm-29"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  threshold           = 60  # Terskel i sekunder
  metric_name         = "ApproximateAgeOfOldestMessage"
  namespace           = "AWS/SQS"
  statistic           = "Maximum"
  period              = 60  # Sjekker hvert minutt
  alarm_description   = "Alarm når ApproximateAgeOfOldestMessage overstiger terskelen"
  dimensions = {
    QueueName = aws_sqs_queue.image_generation_queue.name
  }
  alarm_actions = [aws_sns_topic.sqs_age_alarm_topic.arn]
}
