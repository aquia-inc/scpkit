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


def write_json(content, directory):
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
            json.dump(scp, f, separators=(',', ':'))


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


def remove_sid(sids):
    """Removes Sid key from each sid if it exists. Sid is not necessary and thus takes up unneeded space in an SCP.
    Args:
        sids (list): List of Sids
    Returns:
        [List]: List of Sids with the Sid key removed regardless of case.
    """
    for sid in sids:
        for k in list(sid):
            if k.lower() == 'sid':
                sid.pop(k, None)
    return sids
