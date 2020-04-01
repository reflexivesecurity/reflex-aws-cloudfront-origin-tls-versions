module "reflex_aws_cloudfront_origin_tls_versions" {
  source           = "git::https://github.com/cloudmitigator/reflex-engine.git//modules/cwe_lambda?ref=v0.5.4"
  rule_name        = "CloudfrontOriginTlsVersions"
  rule_description = "Reflex rule to enforce minimum Cloudfront origin tls version"

  event_pattern = <<PATTERN
{
  "source": [
    "aws.cloudfront"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "cloudfront.amazonaws.com"
    ],
    "eventName": [
      "UpdateDistribution",
      "CreateDistribution"
    ]
  }
}
PATTERN

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
