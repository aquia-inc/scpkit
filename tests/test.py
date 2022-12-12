"""
Unit tests
"""

import pytest #pylint: disable=import-errors

from scpkit.src.util import find_key_in_json
from scpkit.src.merge import sort_list_of_dicts, merge_json, combine_similar_sids


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


def test_find_key_in_json():
    found_key = find_key_in_json(test_scp_1, "Statement")
    statement = test_scp_1.get("Statement")
    assert statement == found_key


def test_merge_json():
    merged = merge_json([test_scp_1, test_scp_2])
    expected = []
    expected.extend(test_scp_1.get("Statement"))
    expected.extend(test_scp_2.get("Statement"))
    assert merged == expected


# manipulates dictionary - affects subsequent tests
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
            },
        }
    ]

def test_combine_similar_sids():
    test_data = [{
                    "Action": ["access-analyzer:DeleteAnalyzer"],
                    "Resource": ["*"],
                    "Effect": "Deny"
                },
                {
                    "Effect": "Deny",
                    "Action": [
                        "organizations:LeaveOrganization"
                    ],
                    "Resource": ["*"]
                },
                {
                    "Sid": "test",
                    "Action": [
                        "s3:PutObject"
                    ],
                    "Resource": ["*"],
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
                }
                ]
    result = [{
                    "Action": [
                        "s3:PutObject"
                    ],
                    "Resource": ["*"],
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
                    "Action": ["access-analyzer:DeleteAnalyzer",
                        "organizations:LeaveOrganization"],
                    "Resource": ["*"],
                    "Effect": "Deny"
                }
                ]
    scps = combine_similar_sids(test_data)
    assert result == scps
