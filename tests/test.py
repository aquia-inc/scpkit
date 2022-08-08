"""
Unit tests
"""

import logging
from os.path import join, dirname


import pytest #pylint: disable=import-error

# from dotenv import load_dotenv #pylint: disable=import-error
# from botocore.exceptions import ClientError #pylint: disable=import-error
# from requests.exceptions import HTTPError #pylint: disable=import-error

from scptool.src.util import find_key_in_json, remove_sid #pylint: disable=import-error
from scptool.src.model import SCP 
from scptool.src.merge import sort_list_of_dicts, merge_json

logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('gcp_token_federation').setLevel(logging.DEBUG)
# logging.getLogger('botocore').setLevel(logging.WARNING)
# logging.getLogger('urllib3').setLevel(logging.WARNING)

test_scp_1 = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "test",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "*",
            "Effect": "Deny",
            "Condition": {
                "Null": {
                    "s3:x-amz-server-side-encryption": "true"
                },
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption": [
                        "aws:kms"
                    ]
                }
            }
        },
        {
            "Effect": "Deny",
            "Action": [
                "organizations:LeaveOrganization"
            ],
            "Resource": "*"
        }
    ]
}

test_scp_2 = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "access-analyzer:DeleteAnalyzer",
            "Resource": "*",
            "Effect": "Deny"
        }
    ]
}

TestSCP = SCP("test-scp", test_scp_1)

def test_find_key_in_json():
    found_key = find_key_in_json(test_scp_1, "Statement")
    statement = test_scp_1.get("Statement")
    assert statement == found_key


def test_merge_json():
    merged = merge_json([test_scp_1, test_scp_2])
    assert merged == [
       {
            "Sid": "test",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "*",
            "Effect": "Deny",
            "Condition": {
                "Null": {
                    "s3:x-amz-server-side-encryption": "true"
                },
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption": [
                        "aws:kms"
                    ]
                }
            }
        },
        {
            "Effect": "Deny",
            "Action": [
                "organizations:LeaveOrganization"
            ],
            "Resource": "*"
        },
        {
            "Action": "access-analyzer:DeleteAnalyzer",
            "Resource": "*",
            "Effect": "Deny"
        }
    ]

def test_remove_sid():
    removed = remove_sid(test_scp_1.get("Statement"))
    assert removed == [
        {
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "*",
            "Effect": "Deny",
            "Condition": {
                "Null": {
                    "s3:x-amz-server-side-encryption": "true"
                },
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption": [
                        "aws:kms"
                    ]
                }
            },
        },
        {
            "Effect": "Deny",
            "Action": [
                "organizations:LeaveOrganization"
            ],
            "Resource": "*"
        }
    ]

def test_sort_list_of_dicts():
    sorted = sort_list_of_dicts(test_scp_1.get("Statement"))
    assert sorted == [
        {
            "Effect": "Deny",
            "Action": [
                "organizations:LeaveOrganization"
            ],
            "Resource": "*"
        },
        {
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "*",
            "Effect": "Deny",
            "Condition": {
                "Null": {
                    "s3:x-amz-server-side-encryption": "true"
                },
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption": [
                        "aws:kms"
                    ]
                }
            },
        }
    ]

