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
def export_orders() -> None:
    @task
    def export() -> str:
        context = get_current_context()
        day = context["data_interval_start"].date().isoformat()
        folder = Path.home() / "airflow-course-recovery"
        destination = folder / "exports" / context["run_id"] / f"{day}.csv"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((folder / f"{day}.csv").read_bytes())
        return str(destination)

    @task
    def count_rows(path: str) -> None:
        with Path(path).open() as source:
            count = sum(1 for row in DictReader(source))
        print(f"path={path} rows={count}")

    count_rows(export())


export_orders()
