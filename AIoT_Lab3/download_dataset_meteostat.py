from datetime import datetime
import meteostat as ms
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Tải dữ liệu thời tiết từ Meteostat theo giờ")
parser.add_argument('--lat', type=float, default=21.0285, help='Latitude của địa điểm (default: BTTH)')
parser.add_argument('--lon', type=float, default=105.8542, help='Longitude của địa điểm (default: BTTH)')
parser.add_argument('--location_name', type=str, default='btth', help='Tên địa điểm (dùng trong tên file output)')
parser.add_argument('--start', type=str, default='2025-01-01', help='Ngày bắt đầu (YYYY-MM-DD)')
parser.add_argument('--end', type=str, default='2025-12-31', help='Ngày kết thúc (YYYY-MM-DD)')
parser.add_argument('--elevation', type=int, default=15, help='Độ cao của điểm đo (mét)')
args = parser.parse_args()
# Đang lấy vị trí Hà nội
print(f"Tải dữ liệu từ vị trí: ({args.lat}, {args.lon}) - {args.location_name}")
print(f"Khoảng thời gian: {args.start} -> {args.end}")

point = ms.Point(args.lat, args.lon, args.elevation)
start = datetime.strptime(args.start, '%Y-%m-%d')
end = datetime.strptime(args.end, '%Y-%m-%d').replace(hour=23, minute=59)

# Tìm các trạm gần nhất
print("Tìm trạm khí tượng ...")
stations = ms.stations.nearby(point, limit=10)
print(f"Tìm thấy {len(stations)} trạm trong khu vực")

# Lấy dữ liệu theo giờ
print("Tải dữ liệu theo giờ...")
ts = ms.hourly(stations, start, end)
df = ms.interpolate(ts, point).fetch()
df = df.reset_index()

# Chọn các cột cần thiết
cols = [c for c in ["time", "temp", "rhum", "pres"] if c in df.columns]
df = df[cols].dropna().sort_values("time")

# Lưu vào file
Path("data").mkdir(exist_ok=True)
output_file = f"data/weather_{args.location_name}_hourly.csv"
df.to_csv(output_file, index=False)

print(f"Tải thành công! Số bản ghi: {len(df)}")
print(f"Lưu vào: {output_file}")