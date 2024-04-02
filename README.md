# Git Faker

Sampling git commits based on non-homogeneous poisson process with custom lambda function

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

## Linting

```sh
pylint git_faker
```

```sh
autopep8 --in-place --recursive --aggressive --aggressive git_faker
```
