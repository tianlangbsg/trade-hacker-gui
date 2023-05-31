import random
import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView
from PySide6.QtCore import QTimer, Signal

class MainWindow(QMainWindow):
    refresh_signal = Signal()

    def __init__(self):
        super().__init__()

        self.table = QTableView()
        self.setCentralWidget(self.table)

        self.model = QStandardItemModel()
        self.table.setModel(self.model)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(1000)

        self.refresh_signal.connect(self.refresh_table)

    def on_timeout(self):
        self.refresh_signal.emit()

    def refresh_table(self):
        self.model.clear()
        for i in range(3):
            items = [QStandardItem(str(random.randint(1,9))), QStandardItem(str(random.randint(1,9) * 2))]
            self.model.appendRow(items)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
