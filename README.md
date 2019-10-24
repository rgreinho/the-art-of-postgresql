# The art of PostgreSQL

## Setup

You need to have [invoke](https://docs.pyinvoke.org/en/1.3/) installed in order to run the tasks.

```bash
pip install invoke
```

Prepare the environment with:

```bash
inv
```

This will spin up a minikube, install and configure a postgresql instance.

Then active the venv:

```bash
source venv/bin/activate
```

## Connect

```bash
eval $(./setup/pgsql-connect.sh)
./setup/pgsql-connect.sh
```
