import os
import sys
from PyQt6.QtWidgets import QApplication
from .ui import MainUI

def main():
    app = QApplication(sys.argv)
    w = MainUI()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()