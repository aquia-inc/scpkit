import json
from pathlib import Path


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


def get_filepaths_in_dir(folder):
    """Loads all JSON filepaths from a directory
    Args:
        folder (str): Folder that contains JSON files
    Returns:
        [list]: list of JSON files in a directory
    """

    p = Path(folder)
    all_content = [ file for file in list(p.glob('**/*.json')) ]
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