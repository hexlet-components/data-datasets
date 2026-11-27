"""Compare appending rows with replacing the contents of one interval."""

import sqlite3


def open_example() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE orders (id INTEGER, paid_on TEXT)")
    db.execute("CREATE TABLE register (id INTEGER, paid_on TEXT)")
    db.executemany(
        "INSERT INTO orders VALUES (?, ?)",
        [(41, "2026-04-10"), (42, "2026-04-10"), (43, "2026-04-11")],
    )
    db.execute("INSERT INTO register VALUES (43, '2026-04-11')")
    db.commit()
    return db


def append_period(db: sqlite3.Connection, start: str, end: str) -> None:
    db.execute(
        """
        INSERT INTO register (id, paid_on)
        SELECT id, paid_on FROM orders
        WHERE paid_on >= ? AND paid_on < ?
        """,
        (start, end),
    )


def replace_period(db: sqlite3.Connection, start: str, end: str) -> None:
    with db:
        db.execute(
            "DELETE FROM register WHERE paid_on >= ? AND paid_on < ?", (start, end)
        )
        append_period(db, start, end)


def snapshot(db: sqlite3.Connection) -> list[tuple[str, int]]:
    return db.execute(
        "SELECT paid_on, id FROM register ORDER BY paid_on, id"
    ).fetchall()


if __name__ == "__main__":
    for write in (append_period, replace_period):
        with open_example() as db:
            for attempt in (1, 2):
                write(db, "2026-04-10", "2026-04-11")
                print(write.__name__, attempt, snapshot(db))
