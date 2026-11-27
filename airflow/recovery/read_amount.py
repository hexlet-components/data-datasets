from datetime import timedelta
from pathlib import Path

from airflow.sdk import dag, task
from airflow.sdk.exceptions import AirflowFailException


@dag(schedule=None)
def read_amount() -> None:
    @task(retries=2, retry_delay=timedelta(minutes=2))
    def read_source() -> None:
        source = Path.home() / "airflow-course-recovery" / "incoming.txt"
        value = source.read_text().strip()
        try:
            amount = int(value)
        except ValueError as error:
            raise AirflowFailException(f"Invalid amount: {value!r}") from error
        print(f"amount={amount}")

    read_source()


read_amount()
