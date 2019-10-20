# The art of PostgreSQL

## Setup

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
```
