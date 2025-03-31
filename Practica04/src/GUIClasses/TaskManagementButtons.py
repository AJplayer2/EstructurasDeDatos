from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
import sys

class TskMngrButtons(QWidget):
    def __init__(self):
        super().__init__()
        
        complete = QPushButton("COMPLETE")
        delete = QPushButton("DELETE")
        add = QPushButton("ADD")
        save = QPushButton("SAVE")
        load = QPushButton("LOAD")

        layout = QHBoxLayout(self)
        layout.addWidget(complete)
        layout.addWidget(delete)
        layout.addWidget(add)
        layout.addWidget(save)
        layout.addWidget(load)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = TskMngrButtons()
    widget.show()

    sys.exit(app.exec())