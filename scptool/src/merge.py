from .util import get_files_in_dir, remove_sid, write_json, dump_scp_to_json, find_key_in_json
from copy import deepcopy

def sort_list_of_dicts(content):
    """[summary]
    Args:
        content ([type]): [description]
    Returns:
        [type]: [description]
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


def make_policies(content, max_characters: int = 10000): # TODO: make this bytes
    """Combines the policies in order, counts the characters, and starts a new file when it goes over the limit.
    Args:
        content (list): List of Sid dictionaries (in order of smallest to largest preferred)
        max_characters (int, optional): Max character count. Defaults to 10000.
    Returns:
        list: List of condensed SCP documents.
    """
    file_list = []
    stage = {"Version": "2012-10-17", "Statement": []}
    total_chars = 0

    for sid in content:

        # Get the number of characters for the Sid
        chars = len(dump_scp_to_json(sid))

        # If the total number of characters plus the sid exceeds the max, make a new policy document
        if (total_chars + chars) > max_characters:
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
    all_scps = get_files_in_dir(kwargs['sourcefiles'])
    merged_scps = merge_json(all_scps)
    if not kwargs['keep-sids']:
        remove_sid(merged_scps)
    sort_list_of_dicts(merged_scps)
    new_policies = make_policies(merged_scps)
    write_json(new_policies, kwargs['outdir'])