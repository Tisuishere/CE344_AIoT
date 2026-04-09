import sqlite3

def save_to_db(device_id, temperature, humidity, protocol, timestamp):
    conn = sqlite3.connect("iot_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sensor_data (device_id, temperature, humidity, protocol, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (device_id, temperature, humidity, protocol, timestamp))
    conn.commit()
    conn.close()