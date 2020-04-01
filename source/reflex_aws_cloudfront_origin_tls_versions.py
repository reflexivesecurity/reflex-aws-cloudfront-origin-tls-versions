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

    def __init__(self, event):
        super().__init__(event)

    def extract_event_data(self, event):
        """ Extract required event data """
        self.distribution_id = event["detail"]["responseElements"]["distribution"]["id"]
        self.origins = event["detail"]["responseElements"]["distribution"]["distributionConfig"]["origins"]
        self.non_compliant_resources = self.get_tls_versions_from_origins(self.origins)
        self.non_compliant_resources_str = self.convert_origins_string(self.non_compliant_resources)

    def resource_compliant(self):
        """
        Determine if the resource is compliant with your rule.

        Return True if it is compliant, and False if it is not.
        """
        return bool([] == self.non_compliant_resources)

    def get_remediation_message(self):
        """ Returns a message about the remediation action that occurred """
        flat_allowed = ", ".join(self.origin_protocol_versions_allowed)
        return f"Cloudfront distribution {self.distribution_id} custom origin(s) certificate protocol version(s) do not meet the the minimum requirements.  Allowed protocols are: {flat_allowed}.  Non-compliant origins used: {self.non_compliant_resources_str}"

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
            origin_tls_versions = origin.get("customOriginConfig", {}).get("originSslProtocols", {}).get("items", [])
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


    @staticmethod
    def convert_origins_string(origins):
        origins_string = "Origins: "

        for origin in origins:
            origins_string += " id: "+str(origin.get("id",""))
            origins_string += " "+"".join(origin.get("originSslProtocols",""))

        return origins_string

def lambda_handler(event, _):
    """ Handles the incoming event """
    rule = CloudfrontOriginTlsVersions(json.loads(event["Records"][0]["body"]))
    rule.run_compliance_rule()
