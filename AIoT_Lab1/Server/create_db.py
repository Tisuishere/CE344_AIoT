import sqlite3

conn = sqlite3.connect("iot_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    protocol TEXT NOT NULL,
    timestamp TEXT NOT NULL)
""")

conn.commit()
conn.close()

print("Da tao co so du lieu iot_data.db va bang sensor_data")
