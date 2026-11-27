"""Read the orders for one interval. All timestamps are UTC."""

import sqlite3
import sys
from datetime import date, timedelta

import pendulum
from airflow.sdk import CronDataIntervalTimetable, DAG, get_current_context, task


def select_orders(start: str, end: str) -> list[int]:
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE orders (id INTEGER, paid_at TEXT)")
        db.executemany(
            "INSERT INTO orders VALUES (?, ?)",
            [
                (40, "2026-04-09 23:59:59"),
                (41, "2026-04-10 00:00:00"),
                (42, "2026-04-10 23:59:59"),
                (43, "2026-04-11 00:00:00"),
            ],
        )
        rows = db.execute(
            """
            SELECT id FROM orders
            WHERE paid_at >= :start AND paid_at < :end
            ORDER BY id
            """,
            {"start": start, "end": end},
        )
        return [row[0] for row in rows]


with DAG(
    dag_id="orders_period",
    schedule=CronDataIntervalTimetable("@daily", timezone="UTC"),
    start_date=pendulum.datetime(2026, 4, 9, tz="UTC"),
    catchup=False,
):

    @task
    def show_orders() -> None:
        context = get_current_context()
        start = context["data_interval_start"].strftime("%Y-%m-%d %H:%M:%S")
        end = context["data_interval_end"].strftime("%Y-%m-%d %H:%M:%S")
        print(select_orders(start, end))

    show_orders()


if __name__ == "__main__":
    day = date.fromisoformat(sys.argv[1])
    next_day = day + timedelta(days=1)
    print(select_orders(f"{day} 00:00:00", f"{next_day} 00:00:00"))
