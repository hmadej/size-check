import os, sys
import subprocess
import re


PATTERN = re.compile('(\d{1,8}).*(branch|main)\/(.*)')
DEPTH = int(os.environ['depth']) if 'depth' in os.environ else 1
CLI_ARGS = ['du', '-k', '-d', DEPTH]
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
        directory: get_directory_size(f'./{source_dir}/{directory}')
        for directory in list_dir
    }