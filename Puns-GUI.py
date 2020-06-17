#!/usr/local/bin/python3.7

import signal
import sys

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtWidgets import QApplication, QWidget
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
    from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit
    from PyQt5.QtCore import QSize
    from PyQt5 import uic
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

from PunGenerator import *


class PunsGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Determines Initial orientation of GUI
        self.setGeometry(5, 35, 800, 800)
        self.setWindowTitle('PAUL BOT')

        # Test button
        test_button = QPushButton('Test Hypernym of mouse')
        test_button.clicked.connect(PunGenerator)
        h = QHBoxLayout()
        h.addStretch(1)
        h.addWidget(test_button)
        vbox.addLayout(h)

        # Test Input Box
        test_input = QLineEdit('Test')
        h = QHBoxLayout()
        h.addWidget(QLabel('Enter Test: '))
        h.addWidget(test_input)
        vbox.addLayout(h)

        # Test Output on button click

        self.test_output = QLabel('Relationships')
        h = QHBoxLayout()
        h.addWidget(self.test_output)
        vbox.addLayout(h)

        self.show()

    def testClick(self):
        relationships = self.PunGenerator.print_relationships(self, 'mouse')
        relationships, values = zip(*relationships)
        self.test_output.setText('Relationships: {}'.format(*relationships))


if __name__ == '__main__':
    # This line allows control-c in the terminal to kill the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    ex = PunsGUI()
    sys.exit(app.exec_())
