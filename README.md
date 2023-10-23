# SCPkit
[![GitHub Super-Linter](https://github.com/aquia-inc/scpkit/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/aquia-inc/scpkit/actions/workflows/linter.yaml)

## Overview

This project provides a Python module to aid in Service Control Policy (SCP) management in AWS accounts.

SCPs have a current limit of 5 total per entity, and a size limit on each of 5120 characters. This tool will merge selected SCPs into the fewest amount of policies, and optionally remove whitespace characters as they count toward the character limit.


```mermaid
  stateDiagram-v2
      [SCPTool] --> Validate
      [SCPTool] --> Merge
      [SCPTool] --> Visualize
      Merge --> Validate
      Validate --> [*]
      Merge --> [*]
      Visualize --> [*]
```
## Using SCPkit
SCPkit can be installed from PyPI
```
pip install scpkit
```

### Validating a directory of SCPs
Validating a directory requires active AWS credentials through a profile or environment. SCPkit will recursively search the directory for json files and validate them with [Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html)'s [ValidatePolicy API](https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ValidatePolicy.html).
```
scpkit validate --sourcefiles /path/to/scps --profile yourawsprofile --outdir /path/to/findings
```

### Merging a directory of SCPs
Merging a directory of SCPs does not require active AWS credentials, but can optionally validate after merging.
```
scpkit merge --sourcefiles /path/to/scps --outdir /path/to/directory
```
Optional validation with output locally:
```
scpkit merge --sourcefiles /path/to/scps --outdir /path/to/directory --validate-after-merge --profile yourawsprofile
```

### Creating a visualization of an AWS Organization, OUs, Accounts, and SCPs
Creating this visualization requires you be authenticated with either the Org management account, or a delegated administrator. See the [AWS Documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_delegate_policies_example_view_accts_orgs.html) page for more info on delegating Organizations.

This will output a graph pdf and graphviz data file in the specified directory (or local directory, if outdir is not specified.)

```
scpkit visualize --profile yourawsprofile --outdir ./org-graph
```
Accounts are presented as ellipses, organizational units are rectangles, and SCPs are trapezoids.

![Visualization of an Organization](./visualize-org.png)

The full CLI is documented through docopt
```
"""SCPkit
Usage:
    main.py (validate | merge | visualize) [--sourcefiles sourcefiles] [--profile profile] [ --outdir outdir] [--validate-after-merge] [--readable] [--console]

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --sourcefiles sourcefiles   Directory path to SCP files in json format or a single SCP file
    --outdir outdir             Directory to write new SCP files [Default: ./]
    --profile profile           AWS profile name
    --validate-after-merge      Validate the policies after merging them
    --readable                  Leave indentation and some whitespace to make the SCPs readable
    --console                   Adds Log to console
"""
```

## Local development
From the root of the folder:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m scpkit.main validate --sourcefiles ./scps --profile yourawsprofile
```
Install as a package
```
python3 -m venv .venv
source .venv/bin/activate
pip install -U git+https://github.com/aquia-inc/scpkit.git
```

## References
This project would not be possible without the contributions of the following:
* https://summitroute.com/blog/2020/03/25/aws_scp_best_practices/
* https://github.com/ScaleSec/terraform_aws_scp
* https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples.html
* https://asecure.cloud/l/scp/
* https://github.com/aws-samples/service-control-policy-examples
