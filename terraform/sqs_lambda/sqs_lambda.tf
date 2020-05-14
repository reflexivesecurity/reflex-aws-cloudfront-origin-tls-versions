module "sqs_lambda" {

  function_name   = "CloudfrontOriginTlsVersions"
  source_code_dir = "${path.module}/source"
  handler         = "reflex_aws_cloudfront_origin_tls_versions.lambda_handler"
  lambda_runtime  = "python3.7"
  environment_variable_map = {
    SNS_TOPIC = var.sns_topic_arn
  }

  queue_name    = "CloudfrontOriginTlsVersions"
  delay_seconds = 0

  target_id = "CloudfrontOriginTlsVersions"

  sns_topic_arn  = var.sns_topic_arn
  sqs_kms_key_id = var.reflex_kms_key_id
}
