# Git Faker

Simulate git commit using non-homogenenous poisson process and create a git repository based on simulation result.

## Initializing Environment

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Project

```sh
python -m git_faker
```

## Formatting and Linting

Formatting using `black`:

```sh
black git_faker
```

Linting using `pylint`:

```sh
pylint git_faker
```
