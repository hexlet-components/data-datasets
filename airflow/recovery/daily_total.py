from csv import DictReader
from pathlib import Path

import pendulum
from airflow.sdk import CronDataIntervalTimetable, dag, get_current_context, task


@dag(
    schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC"),
    start_date=pendulum.datetime(2025, 4, 10, tz="UTC"),
    end_date=pendulum.datetime(2025, 4, 12, tz="UTC"),
    catchup=False,
)
def daily_total() -> None:
    @task
    def write_total() -> None:
        day = get_current_context()["data_interval_start"].date().isoformat()
        folder = Path.home() / "airflow-course-recovery"
        with (folder / f"{day}.csv").open() as source:
            total = sum(int(row["amount"]) for row in DictReader(source))
        (folder / f"{day}.txt").write_text(f"{total}\n")
        print(f"day={day} total={total}")

    write_total()


daily_total()
