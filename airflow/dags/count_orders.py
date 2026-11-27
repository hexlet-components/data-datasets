import csv
from datetime import UTC, datetime
from pathlib import Path

from airflow.sdk import dag, task


@dag(
    dag_id="count_orders",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=UTC),
    catchup=False,
)
def count_orders() -> None:
    @task
    def count_rows() -> None:
        orders = Path(__file__).resolve().parents[1] / "orders.csv"
        with orders.open(encoding="utf-8", newline="") as source:
            rows = sum(1 for _ in csv.DictReader(source))
        print(f"orders={rows}")

    count_rows()


count_orders()
