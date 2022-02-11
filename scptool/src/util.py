import json
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


def write_json(content, directory):
    """[summary]
    Args:
        content ([type]): [description]
        directory ([type]): [description]
    """
    i = 0
    for scp in content:
        i = i + 1
        with open(f'scp-{i}.json', 'w') as f:
            json.dump(scp, f, separators=(',', ':'))


def get_files_in_dir(folder):
    """Loads all JSON files from a directory
    Args:
        folder (str): Folder that contains JSON files
    Returns:
        [list]: list of JSON content from all files
    """

    p = Path(folder)
    all_content = [ SCP(name=file.name, content=load_json(file)) for file in list(p.glob('**/*.json')) ]
    return all_content


def find_key_in_json(content, key_to_find):
    """Recursive function to find a key 
    Args:
        content ([dict]): IAM Policy document
        key_to_find ([str]): str of key to find, example: 'Statement'
    Returns:
        [list]: [description]
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