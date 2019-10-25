from pathlib import Path
import os

from invoke import task
from nox.virtualenv import VirtualEnv

# Configuration values.
VENV = "venv"


@task
def clean(c):
    """Clean up the environment."""
    c.run("minikube delete")


@task(default=True)
def setup(c):
    """Setup the student environment."""
    c.run("python3 -m venv venv")
    _, venv_bin, _ = get_venv(VENV)
    pip = venv_bin / "pip"
    c.run(f"{pip.resolve()} install -U pip setuptools")
    c.run(f"{pip.resolve()} install -r requirements.txt -r requirements-dev.txt")
    c.run("./setup/minikube-setup.sh", warn=True)
    c.run("./setup/pgsql-setup.sh", warn=True)
    c.run("./setup/mysql-setup.sh", warn=True)


@task
def mrdb(c):
    """Setup the Motor Race Database."""
    mysql_hostname = os.environ["MYSQL_HOST"]
    mysql_port = os.environ["MYSQL_PORT"]
    mysql_username = "mysql"
    mysql_password = os.environ["MYSQL_PWD"]
    pg_hostname = os.environ["PGHOST"]
    pg_port = os.environ["PGPORT"]
    pg_username = os.environ["PGUSER"]
    pg_password = os.environ["PGPASSWORD"]

    db_archive = "f1db.sql.gz"
    dbname = "f1db"
    c.run(f"createdb {dbname}", warn=True)
    p = Path(".tmp")
    p.mkdir(exist_ok=True)
    with c.cd(".tmp"):
        c.run(f"curl -sLO http://ergast.com/downloads/{db_archive}")
        c.run(f"gzip -d {db_archive}", warn=True)
        c.run(
            f"mycli mysql://root:{mysql_password}@{mysql_hostname}:{mysql_port}/mysql --no-warn -e 'create database {dbname}'",
            warn=True,
        )
        c.run(
            f"mycli mysql://root:{mysql_password}@{mysql_hostname}:{mysql_port}/{dbname} --no-warn < {dbname}.sql",
            warn=True,
        )
        c.run(
            f"pgloader mysql://root:{mysql_password}@{mysql_hostname}:{mysql_port}/{dbname} "
            f"postgresql://{pg_username}:{pg_password}@{pg_hostname}:{pg_port}/{dbname}",
            warn=True,
        )


def get_venv(venv):
    """
    Return `Path` objects from the venv.
    :param str venv: venv name
    :return: the venv `Path`, the `bin` folder `Path` within the venv, and if specified, the `Path` object of the
        activate script within the venv.
    :rtype: a tuple of 3 `Path` objects.
    """
    location = Path(venv)
    venv = VirtualEnv(location.resolve())
    venv_bin = Path(venv.bin)
    activate = venv_bin / "activate"
    return venv, venv_bin, activate
