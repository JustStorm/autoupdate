import urllib.request
import pathlib
import json
import zipfile
import sys
import requests

from shutil import rmtree
ZIP_NAME = 'git_autoupdator.zip'
GITHUB_URL = 'http://github.com/JustStorm/autoupdate.git'

def update(block_num,read_size,total_size,progress_bar_length = 50):
    amount = int(min(block_num*read_size/total_size, 1) * progress_bar_length)
    sys.stdout.write('\r')
    sys.stdout.write(f'>[{amount*"#"}{(progress_bar_length-amount)*" "}]')
    sys.stdout.flush()



def check_version():
    download_file(f'{GITHUB_URL}/releases/latest/download/version.json')
    with open(folder / 'version.json', 'r', encoding='utf-8') as file:
        current = json.loads(file.read())
    with open(temp_folder / 'version.json', 'r', encoding='utf-8') as file:
        latest = json.loads(file.read())
    return (current,latest)

def download_file(url, bar_length=30, silent = True):
    local_filename = temp_folder / url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        total_length = int(r.headers.get('content-length'))
        progr = 0
        last_progr = 0
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if not silent:
                    progr += len(chunk)
                    amount = bar_length*progr//total_length
                    msg = (f">[{amount * '#'}{(bar_length-amount) * ' '}]")
                    if last_progr != amount:
                        amount = last_progr
                        sys.stdout.write('\r'+msg)
                        sys.stdout.flush
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    sys.stdout.write('\n')
    return local_filename


if GITHUB_URL.endswith('.git'):
    GITHUB_URL = GITHUB_URL[:-4]
folder = pathlib.Path(__file__).parent
temp_folder = folder / 'downloads' / "temp"
downloads = folder / 'downloads'
downloads.mkdir(exist_ok=True)
temp_folder.mkdir(exist_ok=True)

print('Checking version...')
current,latest = check_version()

if int(current['id']) > int(latest['id']):
    print(f'Running ahead of latest version:')
    print(f'Current version is {current["version"]} {current["type"]}')
    print(f'Latest avalible version is {latest["version"]} {latest["type"]}')
elif int(current['id']) == int(latest['id']):
    print(f'Up to date! Running {current["version"]} {current["type"]}')
else:
    print(f'New version avalible!')
    print(f'{current["version"]} {current["type"]} --> {latest["version"]} {latest["type"]}')
    download_file(f'{GITHUB_URL}/releases/latest/download/{ZIP_NAME}',silent=False)
    with zipfile.ZipFile(temp_folder / ZIP_NAME, 'r') as zip_ref:
        zip_ref.extractall(folder)
rmtree(temp_folder)