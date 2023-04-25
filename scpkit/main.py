"""SCPkit
Usage:
    main.py (validate | merge) [--sourcefiles sourcefiles] [--profile profile] [ --outdir outdir] [--validate-after-merge] [--readable]

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --sourcefiles sourcefiles   Directory path to SCP files in json format
    --outdir outdir             Directory to write new SCP files [Default: ./]
    --profile profile           AWS profile name
    --validate-after-merge      Validate the policies after merging them
    --readable                  Leave indentation and some whitespace to make the SCPs readable
"""
from docopt import docopt
from .src.validate import validate_policies
from .src.merge import scp_merge, get_files_in_dir

def main():
    arguments = {
        k.lstrip('-'): v for k, v in docopt(__doc__).items()
    }

    arguments['scps'] = get_files_in_dir(arguments["sourcefiles"])

    if arguments.get("merge"):
        scp_merge(**arguments)

    if arguments.get("validate"):
        validate_policies(arguments['scps'], arguments['profile'], arguments['outdir'])


if __name__ == '__main__':
    main()