import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

 
def main():
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()
	button = QtWidgets.QPushButton("Hello, PyQt!")
	button.clicked.connect(on_click)
	window.setCentralWidget(button)

	window.show()
	app.exec_()

@pyqtSlot()
def on_click(self):
	print('PyQt5 button click')
if __name__ == '__main__':
    main()
