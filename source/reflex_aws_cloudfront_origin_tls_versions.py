""" Module for CloudfrontOriginTlsVersions """

import json
import os

import boto3
from reflex_core import AWSRule


class CloudfrontOriginTlsVersions(AWSRule):
    """
    Reflex rule to enforce minimum Cloudfront origin tls version
    """
    origin_protocol_versions = [
        "TLSv1.2",
        "TLSv1.1",
        "TLSv1",
        "SSLv3",
    ]
    origin_protocol_versions_allowed = [
        "TLSv1.2",
        "TLSv1.1",
    ]
    origin_protocol_versions_not_allowed = [
        "TLSv1",
        "SSLv3",
    ]
    # TODO: Instantiate whatever boto3 client you'll need, if any.
    # Example:
    # client = boto3.client("s3")

    def __init__(self, event):
        super().__init__(event)

    def extract_event_data(self, event):
        """ Extract required event data """
        self.distribution_id = event["detail"]["responseElements"]["distribution"]["id"]
        self.origins = event["detail"]["responseElements"]["distribution"]["distributionConfig"]["origins"]
        self.non_compliant_resources = self.get_tls_versions_from_origins(self.origins)

    def resource_compliant(self):
        """
        Determine if the resource is compliant with your rule.

        Return True if it is compliant, and False if it is not.
        """
        return bool([] == self.non_compliant_resources)

    def remediate(self):
        """
        Fix the non-compliant resource so it conforms to the rule
        """
        # TODO (Optional): Fix the non-compliant resource. This only needs to
        # be implemented for rules that remediate non-compliant resources.
        # Purely detective rules can omit this function.
        pass

    def get_remediation_message(self):
        """ Returns a message about the remediation action that occurred """
        flat_origins = ", ".join(self.non_compliant_resources)
        flat_allowed = ", ".join(self.origin_protocol_versions_allowed)
        return f"Cloudfront distribution {self.distribution_id} custom origin(s) certificate protocol version(s) do not meet the the minimum requirements.  Allowed protocols are: {flat_allowed}.  Non-compliant origins used: {flat_origins}"

    def get_tls_versions_from_origins(self, origins):
        """
        Iterate over origin items with a custom origin.
        Return a list of origins with invalid tls protocols.
        Valid return:
            []
        Invalid:
            [
                {
                    "id": "origin-id-string",
                    "originSslProtocols": ["TLSv1","SSLv3"]
                }
            ]
        """
        origin_items = origins.get("items", None)

        invalid_tls_versions = []

        for origin in origin_items:
            origin_id = origin.get("id", None)
            origin_tls_versions = origin.get("customOriginConfig", None).get(
                "originSslProtocols", None).get("items", None)
            versions = []

            for version in origin_tls_versions:
                if version in self.origin_protocol_versions_not_allowed:
                    versions.append(version)

            if versions:
                invalid_origin = {
                    "id": origin_id,
                    "originSslProtocols": versions
                }
                invalid_tls_versions.append(invalid_origin)
        return invalid_tls_versions


def lambda_handler(event, _):
    """ Handles the incoming event """
    rule = CloudfrontOriginTlsVersions(json.loads(event["Records"][0]["body"]))
    rule.run_compliance_rule()
