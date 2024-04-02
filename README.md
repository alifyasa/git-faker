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

## References

 1. [https://dspace.cuni.cz/bitstream/handle/20.500.11956/101040/120308816.pdf?sequence=1](https://dspace.cuni.cz/bitstream/handle/20.500.11956/101040/120308816.pdf?sequence=1)
