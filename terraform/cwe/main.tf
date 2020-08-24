module "cwe" {
  source           = "git::https://github.com/cloudmitigator/reflex-engine.git//modules/cwe?ref=v2.0.1"
  name        = "CloudfrontOriginTlsVersions"
  description = "Reflex rule to enforce minimum Cloudfront origin tls version"

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

}
