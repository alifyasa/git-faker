import os


def create_folder(repo_path: str):
    os.makedirs(repo_path, exist_ok=True)
