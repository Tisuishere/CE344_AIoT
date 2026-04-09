from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SensorChart(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)

    def plot_data(self, timestamps, temperatures, humidities):
        self.ax.clear()
        self.ax.plot(timestamps, temperatures, marker='o', label='Temperature (°C)')
        self.ax.plot(timestamps, humidities, marker='s', label='Humidity (%)')
        self.ax.set_title("Temperature and Humidity History")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.ax.legend()
        self.ax.grid(True)
        self.ax.tick_params(axis='x', rotation=30)
        self.figure.tight_layout()
        self.draw()