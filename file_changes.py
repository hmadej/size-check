import os, sys
import subprocess
import re
from markdown import *

PATTERN = re.compile('(\d{1,8})[^b|^m]*(master|branch)\/(.*)')
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
    branch_name = os.environ['branch'] if 'branch' in os.environ else 'branch'
    master_name = os.environ['main'] if 'master' in os.environ else 'master'
    master_sizes = get_directory_sizes(master_name, sys.argv[1:])
    branch_sizes = get_directory_sizes(branch_name, sys.argv[1:])
    print(make_table(master_sizes, branch_sizes))
