import pathlib
import git
import os

dir_path = pathlib.Path(__file__).parent

local_repo = git.Repo(dir_path)
orig = local_repo.remotes.origin
orig.fetch()

orig.pull('master')