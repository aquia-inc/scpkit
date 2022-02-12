# scpkit
[![GitHub Super-Linter](https://github.com/aquia-inc/scpkit/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

## What it is

This project is intended to accomplish two things

1. Create a collection of validated Service Control Policies that an AWS administrator may want to apply to their Org
2. With the current limit of 5 SCPs and a size limit on each of 5120 bytes, multiple SCPs need to be condensed into fewer policies. This tool will merge selected SCPs into the fewest amount of policies, and optionally remove whitespaces characters as they count toward the byte limit.


```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements
python main.py [commands]
```
setup.py will be added once stabilized.

Collection of SCPs generated in part from:
* https://summitroute.com/blog/2020/03/25/aws_scp_best_practices/
* https://github.com/ScaleSec/terraform_aws_scp
* https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples.html
* https://asecure.cloud/l/scp/
