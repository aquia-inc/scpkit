import json
from pathlib import Path
import yaml
from .util import get_filepaths_in_dir

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
        # self.aa_client = aa_client
        # self.validate()

    def validate(self, aa_client):
        """Runs the SCP through Access Analyzer validate_policy command and adds findings to self.findings

        Args:
            aa_client ([type]): [description]
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


class ConfigFile:
    """Config file generation and update for selecting SCPs
    """

    def __init__(self, conf_file_location):
        self.conf_file_location = conf_file_location
        self.conf = {}
        # self.load_config()


    def create_config(self,filepath):
        scps = get_filepaths_in_dir(filepath)
        scpconfigs = [ self.SCPConfig(path=scp, enabled=True, name=scp.name) for scp in scps]
        pass

    def load_config(self):
        with open(self.conf_file_location) as f:
            self.conf = yaml.safe_load(f)

        self.scpconfig = [ self.SCPConfig() for scp in self.conf ]


    def update_config(self):
        pass


    def write_config(self):
        pass


    class SCPConfig:
        """[summary]
        """

        def __init__(self, path: Path, enabled: bool, name, variables: list = None):
            self.name = name
            self.path = path
            self.enabled = enabled
            self.variables = variables




