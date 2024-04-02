"""
Create Git Repository

Contains the function create_simulated_repository which creates a git repository
based on the simulation result
"""

from git_faker.create.git import git_init, git_add_all, git_commit
from git_faker.create.utils import get_readme, create_folder


def create_simulated_repository(sim_result_path: str, repo_path: str):
    """
    Given simulation result file path and repository path, create
    a git repository on repository path based on the simulation result
    """

    create_folder(repo_path)
    git_init(repo_path)

    with open(sim_result_path, "r", encoding="utf-8") as sim_result:
        while True:

            if not sim_result.readable():
                break

            commit_date = sim_result.readline()

            if len(commit_date) == 0:
                break

            with open(f"{repo_path}/README.md", "w", encoding="utf-8") as repo_file:
                repo_file.write(get_readme(commit_date))

            git_add_all(repo_path)
            git_commit(commit_date, repo_path, f"Update {commit_date}")
