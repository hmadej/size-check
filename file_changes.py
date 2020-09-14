import os, sys
import subprocess
import re
from markdown import *


BRANCH_name = os.environ['branch'] if 'branch' in os.environ else 'branch'
MASTER_name = os.environ['main'] if 'main' in os.environ else 'master'
PATTERN = re.compile(f'(\d{1,8})[^{BRANCH_name[0]}|^{MASTER_name[0]}]*({BRANCH_name}|{MASTER_name})\/(.*)')
CLI_ARGS = ['du', '-k', '-d', '1']
# group 1 is size as an integer, group 3 is filepath

'''
Run cli tool DU to get directory size information
convert stdout string information into a dict
'''
def get_directory_size(path):
    try:
        if os.path.exists(path):
            stdout = str(subprocess.run(
                [*CLI_ARGS, path],
                capture_output=True
            ).stdout, 'utf-8')

            return {
                matches.group(3): int(matches.group(1))
                for line in stdout.split('\n')
                if (matches := PATTERN.match(line))
            }
        else:
            print(f'No {path} exists')
            return {}
    except Exception as e:
        print(e)
        return {}


def get_directory_sizes(source_dir, list_dir):
    return {
        fp: get_directory_size(f'./{source_dir}/{fp}')
        for fp in list_dir
    }


if __name__ == '__main__':
    master_sizes = get_directory_sizes(MASTER_name, sys.argv[1:])
    branch_sizes = get_directory_sizes(BRANCH_name, sys.argv[1:])
    print(make_table(master_sizes, branch_sizes))