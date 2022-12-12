from .util import write_json, find_key_in_json, load_json, make_actions_and_resources_lists, dump_json
from copy import deepcopy
from pathlib import Path
from .model import SCP
from .validate import validate_policies
from itertools import groupby

def sort_list_of_dicts(content):
    """Sorts a list of dictionaries
    Args:
        content ([list]): List containing dictionaries
    Returns:
        [list]: Sorted list of dictionaries
    """
    content.sort(key=lambda x: sum(len(str(v)) + len(str(k))
                 for k, v in x.items()))
    return content


def merge_json(json_blobs):
    """Combines all of the JSON in an array into one large array. Finds the Statement key in each JSON file and returns that.
    Args:
        json_blobs (list): list of json dicts
    Returns:
        [list]: List of all SIDs across all JSON files.
    """
    content = [item for blob in json_blobs for item in find_key_in_json(
        blob, 'Statement')]
    return content


def make_policies(content, readable, max_size: int = 5120):
    """Combines the policies in order, counts the bytes, and starts a new file when it goes over the limit.
        Theres probably a better way to do this with permutations, but that could also be resource intensive.

    Args:
        content (list): List of Sid dictionaries (in order of smallest to largest preferred)
        max_size (int, optional): Max byte count. Defaults to 5120.
    Returns:
        list: List of condensed SCP documents.
    """
    file_list = []
    stage = {"Version": "2012-10-17", "Statement": []}
    total_chars = 0

    for sid in content:

        # Get the number of characters for the Sid
        chars = len((dump_json(sid, readable=readable)).encode('utf-8'))

        # If the total number of characters plus the sid exceeds the max, make a new policy document
        if (total_chars + chars) > max_size:
            file_list.append(deepcopy(stage))
            stage = {"Version": "2012-10-17", "Statement": []}
            total_chars = 0

        # Keep a running tally of the total characters, append the Sid to the policy doc and remove it from the content.
        total_chars = total_chars+chars
        stage['Statement'].append(sid)

    if total_chars > 0:
        file_list.append(stage)
    return file_list


def scp_merge(**kwargs):
    """This is the main function that grabs the files, transforms, and writes new files.
    """
    all_scps = [ scp.content for scp in kwargs['scps'] ]

    merged_scps = merge_json(all_scps)

    cleaned_scps = make_actions_and_resources_lists(merged_scps)

    # combine statements with same condition+resource+effect
    merged_scps = combine_similar_sids(cleaned_scps)

    sort_list_of_dicts(merged_scps)

    new_policies = make_policies(merged_scps, readable=kwargs.get("readable"))

    write_json(new_policies, kwargs['outdir'], readable=kwargs.get("readable"))

    if kwargs.get("validate-after-merge"):
        scps = [ SCP(name=i, content=scp) for i, scp in enumerate(new_policies, 1) ]
        validate_policies(scps, kwargs['profile'], kwargs['outdir'])


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


def combine_similar_sids(content):
    """Combines SIDs that have the same Resource, Effect, and Condition (if exists)

    Args:
        content (list): List of SCP dictionaries

    Returns:
        list: List of SCP dictionaries minimized where possible.
    """
    # groupby works best when dicts are sorted, this sorts by condition, resource, and effect
    content.sort(key= lambda x: (x.get("Condition") is not None, x['Resource'], x["Effect"]), reverse=True)

    # groups the sids that have the same condition, resource, and effect
    grouped_data = groupby(content, key=lambda x: (x["Resource"], x["Effect"], x.get("Condition")))

    merged_content = []

    # walk through the groups
    for (resource, effect, condition), group in grouped_data:
        new_dict = {"Effect":effect, "Resource":resource}


        if condition is not None:
            new_dict["Condition"] = condition

        # handling combining actions
        new_dict["Action"] = []
        new_dict["NotAction"] = []
        for g in list(group):
            if g.get("NotAction"):
                new_dict.pop("Action", None)
                for action in g.get("NotAction"):
                    new_dict["NotAction"].append(action)
            else:
                new_dict.pop("NotAction", None)
                for action in g.get("Action"):
                    new_dict["Action"].append(action)
        merged_content.append(new_dict)

    return merged_content
