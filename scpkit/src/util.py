import json
import boto3
from pathlib import Path
from .model import SCP


def load_json(filepath):
    """Loads json content from files
    Args:
        filepath (str): Path to a file containing json
    Returns:
        [dict]: JSON loaded from the file
    """
    with open(filepath) as f:
        data = json.load(f)
    return data


def write_json(content, directory, readable=False):
    """Writes json to a file
    Args:
        content (dict): JSON to write
        directory ([type]): File output location
    """
    i = 0
    for scp in content:
        i = i + 1
        p = Path(directory)
        if not p.is_dir():
            p.mkdir()
        with open(f'{p}/scp-{i}.json', 'w') as f:
            if readable:
                json.dump(scp, f, indent=2)
            else:
                json.dump(scp, f, separators=(',', ':'))


def dump_json(content, readable=False):
    """Dumps json to a string with either indent 2 or smashed together and no whitespace

    Args:
        content (dict): SCP
        readable (bool, optional): If true, adds indent=2 to json, otherwise smashes it all together. Defaults to False.

    Returns:
        str: SCP
    """
    if readable:
        return json.dumps(content, indent=2)
    else:
        return json.dumps(content)


def get_files_in_dir(filepath):
    """Loads all JSON files from a directory
    Args:
        filepath (str): Folder that contains JSON files or an individual json file
    Returns:
        [list]: list of JSON content from all files
    """

    p = Path(filepath)

    if not p.exists():
        raise FileNotFoundError(f"The file {p} does not exist.")

    if p.is_dir(): 
        p = list(p.glob('**/*.json'))
    elif p.is_file():
        p = [p]
    else:
        raise Exception

    all_content = [ SCP(name=file.name, content=load_json(file)) for file in p ]
    return all_content


def find_key_in_json(content, key_to_find):
    """Recursive function to find a key 
    Args:
        content ([dict]): IAM Policy document
        key_to_find ([str]): str of key to find, example: 'Statement'
    Returns:
        [list]: Contents of "key_to_find"
    """
    for key, value in content.items():
        if key.lower() == key_to_find.lower():

            # Normalize Statement content into a list. It is valid to not be a list.
            if type(content[key]) is not list:
                content[key] = [content[key]]
            return content[key]

        # If we havent found the content and the value is not a str, iterate through.
        elif type(value) is not str:
            find_key_in_json(content[key], key_to_find)


def make_actions_and_resources_lists(content):
    """Makes Actions and Resources values lists if they are not lists.

    Args:
        content (list): List of SIDs

    Returns:
        list: List of SIDs that have actions and resources in list format rather than string
    """
    for sid in content:
        if sid.get("Action") and type(sid.get("Action")) is not list:
            sid["Action"] = [sid.get("Action")]
        if sid.get("NotAction") and type(sid.get("NotAction")) is not list:
            sid["NotAction"] = [sid.get("NotAction")]
        # no such thing as NotResource in SCPs - https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_syntax.html#scp-elements-table
        if type(sid.get("Resource")) is not list:
            sid["Resource"] = [sid.get("Resource")]
    return content


def create_session(profile=None):
    """Creates a boto session

    Args:
        profile (string): AWS profile name

    Returns:
        [object]: Authenticated Boto3 session
    """
    if profile:
        return boto3.Session(profile_name=profile)
    else:
        return boto3.Session()


def create_client(session, service):
    """Creates a service client from a boto session

    Args:
        session (object): Authenicated boto3 session
        service (string): service name to create the client for

    Returns:
        [object]: client session for specific aws service (eg. accessanalyzer)
    """
    return session.client(service)


def paginate(service, method, **method_args):
    """Paginates through the results of a method.

    Args:
        service (boto3.client): The AWS service client.
        method (str): The name of the method to paginate.
        method_args (dict): The arguments to pass to the method.

    Returns:
        list: A list of paginated results.
    """
    paginator = service.get_paginator(method)
    results = paginator.paginate(**method_args)
    return results