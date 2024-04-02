import random
import string

def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits  # A-Za-z0-9
    return ''.join(random.choice(characters) for _ in range(length))

random_string = generate_random_string(8)
print(random_string)

def get_readme(date: str):
    return f"""
# Simulated Git Repository

{date}
"""