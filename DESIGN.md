# Design Notes

## Why do we have to trigger the rule so much?

Since event.responseElements.distribution.distributionConfig.origins.items is an array, cloudwatch event rule patterns do not allow us to match inside the array.  This logic must be handled inside the python lambda logic.

Alternatively, we could adapt our standard rule pattern to leverage eventbridge, which is new at the time of this writting.

```json
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
    ],
    "responseElements": {
      "distribution": {
        "distributionConfig": {
          "origins":{
            "items":[
              {
                "customOriginConfig": {
                  "originSslProtocols": {
                    "items": [
                      "TLSv1",
                      "SSLv3"
                    ]
                  }
                }
              }
            ]
          }
        }
      }
    }
  }
}
```

