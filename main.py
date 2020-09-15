from markdown import make_tables
from file_changes import get_directory_sizes
import urllib3
from json import dumps
import sys, os


if __name__ == '__main__':
    master_sizes = get_directory_sizes('main', sys.argv[1:])
    branch_sizes = get_directory_sizes('branch', sys.argv[1:])
    table = {'body': make_tables(master_sizes, branch_sizes)}
    
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    REPO_NAME = os.environ['REPO_NAME']
    PR_NUMBER = os.environ['PR_NUMBER']
  
    url = f'https://api.github.com/repos/{REPO_NAME}/issues/{PR_NUMBER}/comments'
    http = urllib3.PoolManager()
    r = http.request(
        'POST',
        url,
        headers={
            "Authorization": f'token {ACCESS_TOKEN}',
            "User-Agent": "Mozilla",
        },
        body= dumps(table).encode('utf-8')
    )