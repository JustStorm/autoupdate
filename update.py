import pathlib
import git
import os

dir_path = pathlib.Path(__file__).parent

local_repo = git.Repo(dir_path)

for i in local_repo.config_reader():
    print(i)


print(dir_path)