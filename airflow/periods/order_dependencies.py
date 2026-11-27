"""Two tasks sharing a table on a single-machine Airflow installation."""

import os
import sqlite3
from pathlib import Path

from airflow.sdk import DAG, task


def connect() -> sqlite3.Connection:
    home = Path(os.environ.get("AIRFLOW_HOME", "~/airflow")).expanduser()
    return sqlite3.connect(home / "course_order_dependencies.sqlite")


@task
def load_orders() -> None:
    with connect() as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, amount INTEGER)"
        )
        db.executemany(
            "INSERT OR REPLACE INTO orders VALUES (?, ?)", [(41, 500), (42, 700)]
        )


@task
def sales_total() -> None:
    with connect() as db:
        total = db.execute("SELECT SUM(amount) FROM orders").fetchone()[0]
        print(f"revenue={total}")


@task
def order_count() -> None:
    with connect() as db:
        count = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        print(f"orders={count}")


with DAG(dag_id="order_dependencies", schedule=None):
    load = load_orders()
    total = sales_total()
    load >> total
