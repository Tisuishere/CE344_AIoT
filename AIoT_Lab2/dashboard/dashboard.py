import sys
import csv
from datetime import datetime
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QProgressBar, QGroupBox, QFileDialog, QMessageBox
)
from db_reader import get_latest_record, get_recent_records
from chart_widget import SensorChart


class IoTDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.group_name = "23521699 - Nguyen Dinh Tu"
        self.temp_threshold = 35.0
        self.hum_threshold = 80.0
        self.current_rows = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)

        self.setWindowTitle("IoT Dashboard Lab2 - Temperature & Humidity Monitor")
        self.setGeometry(100, 100, 1100, 700)
        self.init_ui()
        self.load_data()
        self.update_refresh_interval()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        title = QLabel("DASHBOARD GIÁM SÁT NHIỆT ĐỘ - ĐỘ ẨM THEO THỜI GIAN THỰC")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: navy;")

        group_label = QLabel(f"{self.group_name}")
        group_label.setAlignment(Qt.AlignCenter)
        group_label.setStyleSheet("font-size: 20px; color: #334155; font-weight: 600;")

        title_wrap = QVBoxLayout()
        title_wrap.addWidget(title)
        title_wrap.addWidget(group_label)

        main_layout.addLayout(title_wrap)

        top_layout = QHBoxLayout()
        info_group = QGroupBox("Thông tin hiện tại")
        info_layout = QGridLayout()
        self.lbl_device = QLabel("Device ID: ---")
        self.lbl_temp = QLabel("Temperature: --- °C")
        self.lbl_hum = QLabel("Humidity: --- %")
        self.lbl_protocol = QLabel("Protocol: ---")
        self.lbl_time = QLabel("Timestamp: ---")
        self.lbl_status = QLabel("Status: Waiting data...")
        self.temp_bar = QProgressBar()
        self.temp_bar.setRange(0, 100)
        self.hum_bar = QProgressBar()
        self.hum_bar.setRange(0, 100)
        info_layout.addWidget(self.lbl_device, 0, 0)
        info_layout.addWidget(self.lbl_protocol, 0, 1)
        info_layout.addWidget(self.lbl_temp, 1, 0)
        info_layout.addWidget(self.lbl_hum, 1, 1)
        info_layout.addWidget(self.temp_bar, 2, 0)
        info_layout.addWidget(self.hum_bar, 2, 1)
        info_layout.addWidget(self.lbl_time, 3, 0, 1, 2)
        info_layout.addWidget(self.lbl_status, 4, 0, 1, 2)
        info_group.setLayout(info_layout)
        control_group = QGroupBox("Điều khiển")
        control_layout = QVBoxLayout()
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["ALL", "TCP", "UDP", "MQTT"])
        self.protocol_combo.currentTextChanged.connect(self.load_data)

        self.refresh_combo = QComboBox()
        self.refresh_combo.addItem("2 giay", 2000)
        self.refresh_combo.addItem("5 giay", 5000)
        self.refresh_combo.currentIndexChanged.connect(self.update_refresh_interval)

        self.btn_refresh = QPushButton("Làm mới")
        self.btn_refresh.clicked.connect(self.load_data)

        self.btn_export_csv = QPushButton("Xuat CSV")
        self.btn_export_csv.clicked.connect(self.export_csv)

        control_layout.addWidget(QLabel("Chọn giao thức:"))
        control_layout.addWidget(self.protocol_combo)
        control_layout.addWidget(QLabel("Chu ky cap nhat:"))
        control_layout.addWidget(self.refresh_combo)
        control_layout.addWidget(self.btn_refresh)
        control_layout.addWidget(self.btn_export_csv)
        control_layout.addStretch()
        control_group.setLayout(control_layout)
        top_layout.addWidget(info_group, 3)
        top_layout.addWidget(control_group, 1)
        main_layout.addLayout(top_layout)
        self.chart = SensorChart()
        main_layout.addWidget(self.chart)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Device ID", "Temperature", "Humidity", "Protocol", "Timestamp"]
        )
        main_layout.addWidget(self.table)
        central_widget.setLayout(main_layout)

    def load_data(self):
        protocol = self.protocol_combo.currentText()
        latest = get_latest_record(protocol)
        rows = get_recent_records(20, protocol)
        self.current_rows = rows
        if latest:
            device_id, temp, hum, proto, ts = latest
            self.lbl_device.setText(f"Device ID: {device_id}")
            self.lbl_temp.setText(f"Temperature: {temp:.2f} °C")
            self.lbl_hum.setText(f"Humidity: {hum:.2f} %")
            self.lbl_protocol.setText(f"Protocol: {proto}")
            self.lbl_time.setText(f"Timestamp: {ts}")
            self.temp_bar.setValue(max(0, min(100, int(temp))))
            self.hum_bar.setValue(max(0, min(100, int(hum))))
            self.update_warning_state(temp, hum)
        else:
            self.lbl_status.setText("Status: No data found")
            self.lbl_status.setStyleSheet("font-weight: bold; color: #6b7280;")
            self.temp_bar.setValue(0)
            self.hum_bar.setValue(0)
            self.temp_bar.setStyleSheet("")
            self.hum_bar.setStyleSheet("")
        self.table.setRowCount(len(rows))
        timestamps, temps, hums = [], [], []
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

            timestamps.append(row[4].split(" ")[1] if " " in row[4] else row[4])
            temps.append(row[1])
            hums.append(row[2])

        if rows:
            self.chart.plot_data(timestamps, temps, hums)

    def export_csv(self):
        if not self.current_rows:
            QMessageBox.warning(self, "Thong bao", "Khong co du lieu de xuat CSV.")
            return

        default_name = f"sensor_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Luu file CSV",
            default_name,
            "CSV Files (*.csv);;All Files (*)",
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["device_id", "temperature", "humidity", "protocol", "timestamp"])
                writer.writerows(self.current_rows)

            QMessageBox.information(self, "Thanh cong", f"Da xuat CSV: {file_path}")
        except OSError as exc:
            QMessageBox.critical(self, "Loi", f"Khong the xuat CSV.\n{exc}")

    def update_refresh_interval(self):
        interval_ms = self.refresh_combo.currentData()
        if interval_ms is None:
            interval_ms = 2000
        self.timer.start(int(interval_ms))

    def update_warning_state(self, temp, hum):
        temp_alert = temp > self.temp_threshold
        hum_alert = hum > self.hum_threshold

        if temp_alert or hum_alert:
            reasons = []
            if temp_alert:
                reasons.append(f"Temp>{self.temp_threshold:.0f}C")
                self.temp_bar.setStyleSheet("QProgressBar::chunk { background-color: #d9534f; }")
            else:
                self.temp_bar.setStyleSheet("QProgressBar::chunk { background-color: #2e7d32; }")

            if hum_alert:
                reasons.append(f"Hum>{self.hum_threshold:.0f}%")
                self.hum_bar.setStyleSheet("QProgressBar::chunk { background-color: #d9534f; }")
            else:
                self.hum_bar.setStyleSheet("QProgressBar::chunk { background-color: #2e7d32; }")

            self.lbl_status.setText(f"Status: Warning ({', '.join(reasons)})")
            self.lbl_status.setStyleSheet("font-weight: bold; color: #c62828;")
        else:
            self.temp_bar.setStyleSheet("QProgressBar::chunk { background-color: #2e7d32; }")
            self.hum_bar.setStyleSheet("QProgressBar::chunk { background-color: #2e7d32; }")
            self.lbl_status.setText("Status: Connected / Data loaded")
            self.lbl_status.setStyleSheet("font-weight: bold; color: #1b5e20;")


def main():
    app = QApplication(sys.argv)
    window = IoTDashboard()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()