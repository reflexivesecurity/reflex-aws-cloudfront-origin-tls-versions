# reflex-aws-cloudfront-origin-tls-versions

A Reflex rule to enforce minimum Cloudfront origin TLS version.

To learn more about CloudFront, see [the AWS Documentation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html).

## Getting Started
To get started using Reflex, check out [the Reflex Documentation](https://docs.cloudmitigator.com/).

## Usage
To use this rule either add it to your `reflex.yaml` configuration file:  
```
rules:
  aws:
    - cloudfront-origin-tls-versions:
        version: latest
```

or add it directly to your Terraform:  
```
module "cloudfront-origin-tls-versions" {
  source            = "git::https://github.com/reflexivesecurity/reflex-aws-cloudfront-origin-tls-versions.git?ref=latest"
  sns_topic_arn     = module.central-sns-topic.arn
  reflex_kms_key_id = module.reflex-kms-key.key_id
}
```

Note: The `sns_topic_arn` and `reflex_kms_key_id` example values shown here assume you generated resources with `reflex build`. If you are using the Terraform on its own you need to provide your own valid values.

## Configuration
This rule has no configuration options.

## Contributing
If you are interested in contributing, please review [our contribution guide](https://docs.cloudmitigator.com/about/contributing.html).

## License
This Reflex rule is made available under the MPL 2.0 license. For more information view the [LICENSE](https://github.com/reflexivesecurity/reflex-aws-cloudfront-origin-tls-versions/blob/master/LICENSE) 
