"""SCPtool
Usage:
    main.py [validate | merge] [--sourcefiles sourcefiles] [--profile profile] [ --outdir outdir] [--keep-sids]

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --sourcefiles sourcefiles   Directory path to SCP files in json format
    --outdir outdir             Directory to write new SCP files
    --profile profile           AWS profile name
    --keep-sids                 Keeps Sids for metadata purposes

"""
from docopt import docopt
from .src.validate import validate_policies
from .src.merge import scp_merge, get_files_in_dir

def main():
    arguments = {
        k.lstrip('-'): v for k, v in docopt(__doc__, version='SCPtool v0.01').items()
    }

    arguments['scps'] = get_files_in_dir(arguments["sourcefiles"])

    if arguments.get("validate"):
        validate_policies(arguments['scps'], arguments['profile'])

    elif arguments.get("merge"):
        scp_merge(**arguments)


if __name__ == '__main__':
    main()