# reflex-aws-cloudfront-origin-tls-versions

Reflex rule to enforce minimum Cloudfront origin tls version

## Usage
To use this rule either add it to your `reflex.yaml` configuration file:  
```
rules:
  - reflex-aws-cloudfront-origin-tls-versions:
      version: latest
```

or add it directly to your Terraform:  
```
...

module "reflex-aws-cloudfront-origin-tls-versions" {
  source           = "github.com/cloudmitigator/reflex-aws-cloudfront-origin-tls-versions"
}

...
```

## License
This Reflex rule is made available under the MPL 2.0 license. For more information view the [LICENSE](https://github.com/cloudmitigator/reflex-aws-cloudfront-origin-tls-versions/blob/master/LICENSE) 
