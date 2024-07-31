import urllib.request
import pathlib
import json

ZIP_NAME = 'git_autoupdator.zip'
GITHUB_URL = 'https://github.com/JustStorm/autoupdate.git'



if GITHUB_URL.endswith('.git'):
    GITHUB_URL = GITHUB_URL[:-4]
folder = pathlib.Path(__file__).parent
urllib.request.urlretrieve(f'{GITHUB_URL}/releases/latest/download/version.json', folder / 'download' / 'version.json')
with open(folder / 'version.json', 'r', encoding='utf-8') as file:
    current_version_data = json.loads(file.read())

with open(folder / 'download' / 'version.json', 'r', encoding='utf-8') as file:
    latest_version_data = json.loads(file.read())

if int(current_version_data['id']) > int(latest_version_data['id']):
    print(f'Running ahead of latest version:\n\
          Current is {current_version_data["version"]} {current_version_data["type"]}\n\
          Latest avalible version is {latest_version_data["version"]} {latest_version_data["type"]}')
elif int(current_version_data['id']) == int(latest_version_data['id']):
    print(f'Up to date! Running {current_version_data["version"]} {current_version_data["type"]}')
else:
    print(f'New version avalible!\n\
          {current_version_data["version"]} {current_version_data["type"]} --> {latest_version_data["version"]} {latest_version_data["type"]}')
    urllib.request.urlretrieve(f'{GITHUB_URL}/releases/latest/download/{ZIP_NAME}', folder / 'download' / ZIP_NAME)
    