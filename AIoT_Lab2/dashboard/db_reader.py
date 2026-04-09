from pathlib import Path
import sqlite3
from typing import List, Optional, Tuple


Record = Tuple[str, float, float, str, str]

DB_PATH = Path(__file__).resolve().parents[2] / "AIoT_Lab1" / "Server" / "iot_data.db"


def _get_connection() -> sqlite3.Connection:
	return sqlite3.connect(DB_PATH)


def get_latest_record(protocol: str = "ALL") -> Optional[Record]:
	"""Return the newest sensor record, optionally filtered by protocol."""
	if not DB_PATH.exists():
		return None

	try:
		with _get_connection() as conn:
			cursor = conn.cursor()
			if protocol and protocol.upper() != "ALL":
				cursor.execute(
					"""
					SELECT device_id, temperature, humidity, protocol, timestamp
					FROM sensor_data
					WHERE protocol = ?
					ORDER BY id DESC
					LIMIT 1
					""",
					(protocol.upper(),),
				)
			else:
				cursor.execute(
					"""
					SELECT device_id, temperature, humidity, protocol, timestamp
					FROM sensor_data
					ORDER BY id DESC
					LIMIT 1
					"""
				)

			row = cursor.fetchone()
			return row if row else None
	except sqlite3.Error:
		return None


def get_recent_records(limit: int = 20, protocol: str = "ALL") -> List[Record]:
	"""Return recent sensor records sorted from oldest to newest."""
	if not DB_PATH.exists():
		return []

	safe_limit = max(1, int(limit))

	try:
		with _get_connection() as conn:
			cursor = conn.cursor()
			if protocol and protocol.upper() != "ALL":
				cursor.execute(
					"""
					SELECT device_id, temperature, humidity, protocol, timestamp
					FROM (
						SELECT id, device_id, temperature, humidity, protocol, timestamp
						FROM sensor_data
						WHERE protocol = ?
						ORDER BY id DESC
						LIMIT ?
					)
					ORDER BY id ASC
					""",
					(protocol.upper(), safe_limit),
				)
			else:
				cursor.execute(
					"""
					SELECT device_id, temperature, humidity, protocol, timestamp
					FROM (
						SELECT id, device_id, temperature, humidity, protocol, timestamp
						FROM sensor_data
						ORDER BY id DESC
						LIMIT ?
					)
					ORDER BY id ASC
					""",
					(safe_limit,),
				)

			return cursor.fetchall()
	except sqlite3.Error:
		return []
