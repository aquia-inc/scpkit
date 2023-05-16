"""SCPkit
Usage:
    main.py (validate | merge) [--sourcefiles sourcefiles] [--profile profile] [ --outdir outdir] [--validate-after-merge] [--readable] [--console]

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
from docopt import docopt
from .src.validate import validate_policies
from .src.merge import scp_merge
from .src.util import get_files_in_dir

def main():
    arguments = {
        k.lstrip('-'): v for k, v in docopt(__doc__).items()
    }

    arguments['scps'] = get_files_in_dir(arguments["sourcefiles"])

    if arguments.get("merge"):
        scp_merge(**arguments)

    if arguments.get("validate"):
        validate_policies(arguments['scps'], arguments['profile'], arguments['outdir'], arguments['console'])


if __name__ == '__main__':
    main()