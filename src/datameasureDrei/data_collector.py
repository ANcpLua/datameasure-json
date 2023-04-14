import time
from datetime import datetime
import requests
from PyQt5.QtCore import QObject, QTimer, pyqtSignal, QThread


class DataCollector(QObject):
    data_received = pyqtSignal(list)

    def __init__(self, config):
        """Collects data from a server at regular intervals."""
        # initialize data collector
        super(DataCollector, self).__init__()
        self.thread = None
        self.url = config.get('server_url', 'http://127.0.0.1:7744/datameasure/data1')
        self.hello_url = config.get('hello_url', 'http://127.0.0.1:7744/hello')
        self.polling_interval = int(config.get('polling_interval', 10))
        self._running = False
        self.prev_counter = None
        self.sum_gauge = 0
        self.count_gauge = 0

        # create a timer to print gauge value every 10 seconds
        self.print_timer = QTimer()
        self.print_timer.timeout.connect(self.print_gauge)
        self.print_timer.start(10000)  # 10 seconds

    def start(self):
        """Starts the data collection thread."""
        if not self._running:
            self._running = True
            self.thread = QThread()
            self.moveToThread(self.thread)
            self.thread.started.connect(self.collect_data)
            self.thread.start()

    def stop(self):
        """Stops the data collection thread."""
        if self._running:
            self._running = False
            self.thread.quit()
            self.thread.wait()

    def collect_data(self):
        """Collects data from the server at regular intervals."""
        while self._running:
            try:
                response = requests.get(self.url)
                response.raise_for_status()
                data = response.json()
                counter = data.get('data', 0)
                gauge, status = self.calculate_gauge_and_status(counter)
                if status is not None:
                    self.data_received.emit([datetime.now(), counter, gauge, status])
            except requests.exceptions.RequestException as e:
                print(f"Error collecting data: {e}")
            time.sleep(self.polling_interval)

    def calculate_gauge_and_status(self, counter):
        """Calculates the gauge and status based on the counter value."""
        if self.prev_counter is None:
            self.prev_counter = counter
            return 0, "OK"

        diff = counter - self.prev_counter
        if diff < 0:
            diff += 1024
        self.prev_counter = counter

        self.sum_gauge += diff
        self.count_gauge += 1
        long_term_avg = self.sum_gauge / self.count_gauge

        """(difficult) If the reported gauge value is changing more than +/- 10% of the long term average of the 
        value the wrong values shall not be reported (difficult) if the reported gauge value is changing more than 
        +/- 10% of the long term average and the counter is less than 200: This    shall be reported as a reboot and 
        wrong values shall not be reported"""
        if abs(diff - long_term_avg) > long_term_avg * 0.1:
            if diff < long_term_avg and counter < 200:
                return diff, "Reboot"
            else:
                return None, None

        return diff, "OK"

    def print_gauge(self):
        """Prints the average gauge value."""
        if self.count_gauge > 0:
            avg_gauge = self.sum_gauge / self.count_gauge
            print(f"Average bottles/second: {avg_gauge}")
