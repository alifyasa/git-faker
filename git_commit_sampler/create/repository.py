from git_commit_sampler.create.git import git_init, git_add_all, git_commit
from git_commit_sampler.create.rw_file import create_folder
from git_commit_sampler.create.utils import get_readme


def create_simulated_repository(sim_result_path: str, repo_path: str):

    create_folder(repo_path)
    git_init(repo_path)

    with open(sim_result_path, "r") as sim_result:
        while True:

            if not sim_result.readable():
                break

            commit_date = sim_result.readline()

            if len(commit_date) == 0:
                break

            with open(f"{repo_path}/README.md", "w") as repo_file:
                repo_file.write(get_readme(commit_date))
            
            git_add_all(repo_path)
            git_commit(commit_date, repo_path, f"Update {commit_date}")