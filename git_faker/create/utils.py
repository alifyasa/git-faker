"""
Utilities to create a git repository
"""

import os
import random
import string


def generate_random_string(length=8):
    """
    Generate random string with certain length
    """

    characters = string.ascii_letters + string.digits  # A-Za-z0-9
    return ''.join(random.choice(characters) for _ in range(length))


def create_folder(repo_path: str):
    """
    Create all folder specified in repo_path.

    If parent doesn't exist, create parent first.
    """

    os.makedirs(repo_path, exist_ok=True)


def get_readme(date: str):
    """
    Base README for git repository
    """

    return f"""
# Simulated Git Repository

{date}
"""
