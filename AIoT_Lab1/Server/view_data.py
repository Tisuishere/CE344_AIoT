import argparse
import sqlite3
from typing import Iterable, List, Tuple

DB_PATH = "iot_data.db"


def fetch_rows(limit: int, protocol: str | None, descending: bool) -> List[Tuple]:
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()

	where_clause = ""
	params: List[object] = []
	if protocol:
		where_clause = "WHERE protocol = ?"
		params.append(protocol.upper())

	order = "DESC" if descending else "ASC"
	query = f"""
		SELECT id, device_id, temperature, humidity, protocol, timestamp
		FROM sensor_data
		{where_clause}
		ORDER BY id {order}
		LIMIT ?
	"""
	params.append(limit)

	cursor.execute(query, params)
	rows = cursor.fetchall()
	conn.close()
	return rows


def print_table(headers: Iterable[str], rows: List[Tuple]) -> None:
	headers = list(headers)
	if not rows:
		print("Khong co du lieu trong bang sensor_data voi bo loc hien tai.")
		return

	str_rows = [tuple(str(cell) for cell in row) for row in rows]
	widths = [len(h) for h in headers]

	for row in str_rows:
		for i, cell in enumerate(row):
			if len(cell) > widths[i]:
				widths[i] = len(cell)

	separator = "+-" + "-+-".join("-" * w for w in widths) + "-+"
	header_line = "| " + " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))) + " |"

	print(separator)
	print(header_line)
	print(separator)
	for row in str_rows:
		line = "| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(row))) + " |"
		print(line)
	print(separator)


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Xem du lieu da luu trong iot_data.db (bang sensor_data)."
	)
	parser.add_argument(
		"-n",
		"--limit",
		type=int,
		default=20,
		help="So dong toi da can hien thi (mac dinh: 20).",
	)
	parser.add_argument(
		"-p",
		"--protocol",
		choices=["TCP", "UDP", "MQTT", "tcp", "udp", "mqtt"],
		help="Loc theo protocol: TCP, UDP, MQTT.",
	)
	parser.add_argument(
		"--oldest-first",
		action="store_true",
		help="Hien thi du lieu cu truoc (mac dinh la moi nhat truoc).",
	)

	args = parser.parse_args()

	if args.limit <= 0:
		raise SystemExit("limit phai la so nguyen duong")

	rows = fetch_rows(
		limit=args.limit,
		protocol=args.protocol,
		descending=not args.oldest_first,
	)

	print_table(
		headers=["id", "device_id", "temperature", "humidity", "protocol", "timestamp"],
		rows=rows,
	)


if __name__ == "__main__":
	main()
