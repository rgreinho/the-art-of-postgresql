from pathlib import Path

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
    c.run("./setup/minikube-setup.sh")
    c.run("./setup/pgsql-setup.sh")


@task
def mrd(c):
    """Setup the Motor Race Database."""
    db_archive = "f1db_postgres.sql.gz"
    # hostname = os.environ["PGHOST"]
    # port = os.environ["PGPORT"]
    # username = os.environ["PGUSER"]
    # password = os.environ["PGPASSWORD"]
    dbname = "f1db"
    c.run(f"createdb {dbname}", warn=True)
    p = Path(".tmp")
    p.mkdir(exist_ok=True)
    with c.cd(".tmp"):
        c.run(f"curl -sLO http://ergast.com/downloads/{db_archive}")
        c.run(f"gzip -d {db_archive}", warn=True)
        c.run(
            "curl -sLO https://raw.githubusercontent.com/lanyrd/mysql-postgresql-converter/master/db_converter.py"
        )
        c.run(f"python2 db_converter.py f1db_postgres.sql {dbname}.psql")
        c.run(f"psql {dbname} < {dbname}.psql")


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
