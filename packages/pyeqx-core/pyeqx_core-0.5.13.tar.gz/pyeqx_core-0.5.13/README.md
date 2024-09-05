# data-driven-core

## pre-requisites

to setup virtual environment to execute unit tests, it has to setup virtual env and install dependencies

```bash
# setup virtual env
python3.11 -m venv .venv

# activate virtual env
source .venv/bin/activate

# install dependencies
pip install delta-spark pyspark pandas retrying minio requests

# install dependencies (If you want to publish)
pip install twine
```

## tests

to execute unit test run this command at root of the project

```bash
python3 -m unittest discover test -p "**.py"
```

## build

```bash
python3 setup.py sdist bdist_wheel
```

## publish to gitlab

```bash
python3 -m twine upload --repository-url https://gitlab.com/api/v4/projects/<project_id>/packages/pypi/ --username gitlab-ci-token --password <access_token> dist/*

# Replace <project_id> with the ID of your GitLab project
```

## install from gitlab

```bash
pip install pyeqx-core --index-url https://__token__:<access_token>@gitlab.com/api/v4/projects/<project_id>/packages/pypi/simple

# Replace <project_id> with the ID of your GitLab project
```
