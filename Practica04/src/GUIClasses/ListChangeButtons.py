from PySide6.QtCore import Signal
from PySide6.QtWidgets import QButtonGroup, QWidget, QPushButton, QApplication, QHBoxLayout
import sys

class ListChangeButtons(QWidget):
    buttonPressed = Signal(int)

    def __init__(self):
        super().__init__()

        pending = QPushButton("PENDING")
        pending.setCheckable(True)

        completed = QPushButton("COMPLETED")
        completed.setCheckable(True)

        buttonGroup = QButtonGroup(self)
        buttonGroup.addButton(pending, 1)
        buttonGroup.addButton(completed, 2)
        buttonGroup.setExclusive(True)
        buttonGroup.idClicked.connect(self.intSignal)

        layout = QHBoxLayout()
        layout.addWidget(pending)
        layout.addWidget(completed)

        self.setLayout(layout)

    def intSignal(self, id):
      print (f"internal slot pressed {id}")

      self.buttonPressed.emit(id)
      print (f"signal id emitted: {id}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = ListChangeButtons()
    widget.show()

    sys.exit(app.exec())