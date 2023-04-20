import sys
import configparser
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, \
    QTableWidget, QTableWidgetItem

from data_collector import DataCollector


class MainWindow(QMainWindow):
    def __init__(self, config):
        super(MainWindow, self).__init__()

        self.stop_button = None
        self.start_button = None
        self.hello_url_input = None
        self.table = None
        self.hello_url_label = None
        self.url_input = None
        self.url_label = None
        self.data_collector = DataCollector(config)
        self.setup_ui()
        self.start_data_collection()

    """ gui """
    def setup_ui(self):
        # create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # create labels and input fields
        self.url_label = QLabel("Server URL:")
        self.url_input = QLineEdit(self.data_collector.url)
        self.hello_url_label = QLabel("Hello URL:")
        self.hello_url_input = QLineEdit(self.data_collector.hello_url)

        # create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Counter", "Gauge", "Status"])

        # create start and stop buttons
        self.start_button = QPushButton("Start Data Collection")
        self.start_button.clicked.connect(self.start_data_collection)
        self.stop_button = QPushButton("Stop Data Collection")
        self.stop_button.clicked.connect(self.stop_data_collection)

        # add all widgets to the layout
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.hello_url_label)
        layout.addWidget(self.hello_url_input)
        layout.addWidget(self.table)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        # set layout for the central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_data_collection(self):
        # start data collection and connect data_received signal to update_table slot
        self.data_collector.start()
        self.data_collector.data_received.connect(self.update_table)

    def stop_data_collection(self):
        # stop data collection
        self.data_collector.stop()

    def update_table(self, data):
        # insert a new row into the table and add the data to the row
        row = self.table.rowCount()
        self.table.insertRow(row)

        for i, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            self.table.setItem(row, i, item)


def main():
    # set up logging and read configuration file
    logging.basicConfig(filename='app.log', level=logging.INFO)
    config = configparser.ConfigParser()
    config.read('config.ini')

    # create application, window and show the window
    app = QApplication(sys.argv)
    window = MainWindow(config['settings'])
    window.show()

    # start the application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
