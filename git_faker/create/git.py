import subprocess
import os
from datetime import datetime


def git_init(repo_path: str):
    subprocess.run(["git", "-C", repo_path, "init", "-b", "main"], check=True)


def git_add_all(repo_path: str):
    subprocess.run(["git", "-C", repo_path, "add", "."], check=True)


def git_commit(
        commit_date: str,
        repo_path: str,
        commit_message: str = "Initial commit"):
    formatted_date = datetime.strptime(
        commit_date.strip(), "%Y-%m-%d %H:%M:%S.%f")
    iso_date = formatted_date.isoformat()
    env = os.environ.copy()
    env['GIT_COMMITTER_DATE'] = iso_date
    env['GIT_AUTHOR_DATE'] = iso_date
    subprocess.run(["git", "-C", repo_path, "commit", "-m",
                   commit_message], env=env, check=True)
