import argparse
import random
import sqlite3
import time
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "AIoT_Lab1" / "Server" / "iot_data.db"
PROTOCOLS = ("TCP", "UDP", "MQTT")


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            protocol TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()


def generate_row(device_id: str) -> tuple[str, float, float, str, str]:
    temperature = round(random.uniform(24.0, 40.0), 2)
    humidity = round(random.uniform(40.0, 90.0), 2)
    protocol = random.choice(PROTOCOLS)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return device_id, temperature, humidity, protocol, timestamp


def insert_row(conn: sqlite3.Connection, row: tuple[str, float, float, str, str]) -> None:
    conn.execute(
        """
        INSERT INTO sensor_data (device_id, temperature, humidity, protocol, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        row,
    )
    conn.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Insert random sensor rows for dashboard monitoring")
    parser.add_argument("--device", default="DEV_01", help="Device ID to write")
    parser.add_argument("--interval", type=float, default=2.0, help="Seconds between inserts")
    parser.add_argument("--count", type=int, default=0, help="Number of rows to insert (0 = infinite)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.interval <= 0:
        raise ValueError("--interval must be > 0")
    if args.count < 0:
        raise ValueError("--count must be >= 0")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        ensure_table(conn)

        print(f"DB: {DB_PATH}")
        print("Start inserting data. Press Ctrl+C to stop.")

        inserted = 0
        while args.count == 0 or inserted < args.count:
            row = generate_row(args.device)
            insert_row(conn, row)
            inserted += 1

            device_id, temperature, humidity, protocol, timestamp = row
            print(
                f"[{inserted}] {device_id} | {temperature:.2f} C | {humidity:.2f}% | "
                f"{protocol} | {timestamp}"
            )

            if args.count == 0 or inserted < args.count:
                time.sleep(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
