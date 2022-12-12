import json
from pathlib import Path

class SCP:
    """Main class for a single Service Control Policy
    """
    def __init__(self, name, content):
        """
        Args:
            name (str): name or short filename for scp
            content (dict): The SCP content
        """
        self.name = name
        self.content = content

    def validate(self, aa_client):
        """Runs the SCP through Access Analyzer validate_policy command and adds findings to self.findings

        Args:
            aa_client ([client]): Authenticated access analyzer boto client to analyze SCPs
        """
        self.findings = aa_client.validate_policy(policyDocument=self.json, policyType="SERVICE_CONTROL_POLICY").get("findings")

    @property
    def json(self):
        """JSON.dumps with no spaces in separators
        Returns:
            str: string of condensed json
        """
        return json.dumps(self.content, separators=(',', ':'))

    @property
    def pretty_json(self):
        """JSON.dumps readable indented SCP
        Returns:
            str: string of readable json
        """
        return json.dumps(self.content, indent=2)

    @property
    def findings_json(self):
        """JSON.dumps readable indented findings
        Returns:
            str: string of readable json
        """
        return json.dumps(self.findings, indent=2)

    def write_findings_for_scp(self, directory):
        p = Path(directory)
        if not p.is_dir():
            p.mkdir()
        with open(f'{p}/{self.name}-findings.json', 'w') as f:
            json.dump(self.findings, f, indent=2)