from PySide6.QtCore import Signal
from PySide6.QtWidgets import QButtonGroup, QWidget, QPushButton, QApplication, QHBoxLayout
import sys

class TaskFilters(QWidget):
    tskFilter = Signal(int)

    def __init__(self):
        super().__init__()

        ALL = QPushButton("Title")
        ALL.setCheckable(True)

        urgent = QPushButton("URGENT")
        urgent.setCheckable(True)

        medium = QPushButton("MEDIUM")
        medium.setCheckable(True)

        low = QPushButton("LOW")
        low.setCheckable(True)

        buttonGroup = QButtonGroup(self)
        buttonGroup.addButton(ALL, 0)
        buttonGroup.addButton(urgent, 3)
        buttonGroup.addButton(medium, 2)
        buttonGroup.addButton(low, 1)
        buttonGroup.setExclusive(True)
        buttonGroup.idClicked.connect(self.filterEvent)

        layout = QHBoxLayout()
        layout.addWidget(ALL)
        layout.addWidget(urgent)
        layout.addWidget(medium)
        layout.addWidget(low)
        self.setLayout(layout)
        
    def filterEvent(self, id):
        print (f"internal slot pressed: {id}")

        self.tskFilter.emit(id)
        print (f"id emitted: {id}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = TaskFilters()
    widget.show()

    sys.exit(app.exec())
