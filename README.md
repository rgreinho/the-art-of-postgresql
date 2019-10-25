# The art of PostgreSQL

## Getting started

### Requirements

You must have [invoke](https://docs.pyinvoke.org/en/1.3/) installed in order to run the tasks:

```bash
pip install invoke
```

You may also need to execute `bootstrap-osx.sh` to ensure you have all the tools installed on your machine:

```bash
./setup/bootstrap-osx.sh
```

### Setup

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

Source the environment variables with:

```bash
eval $(./setup/pgsql-connect.sh)
eval $(./setup/mysql-connect.sh)
```

Display the connection strings with:

```bash
./setup/pgsql-connect.sh
./setup/mysql-connect.sh
```

## Other tasks

### mrdb

Setup the Motor Race Database:

```bash
inv mrdb
```
