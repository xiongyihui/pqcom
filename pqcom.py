
import sys
import serial
from serial.tools import list_ports
from pqcom_ui import *
from pqcom_setup_ui import *
from PySide.QtGui import *
from PySide.QtCore import *



class SetupDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(SetupDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.refresh()
        
        self.portComboBox.clicked.connect(self.refresh)
                
    def refresh(self):
        print('refresh')
        self.portComboBox.clear()
        for port in list_ports.comports():
            name = port[0]
            if name.startswith('/dev/ttyACM') or name.startswith('/dev/ttyUSB') or name.startswith('com'):
                self.portComboBox.addItem(port[0])
                
    def get(self):
        port = str(self.portComboBox.currentText())
        baud = int(self.baudComboBox.currentText())
        databits = int(self.dataComboBox.currentText())
        stopbits = int(self.stopbitComboBox.currentText())
        parity = str(self.parityComboBox.currentText())
        
        return (port, baud, databits, stopbits, parity)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    def display(self, text):
        self.recvTextEdit.append(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    dialog = SetupDialog(window)
    choice = dialog.exec_()
    if choice == QDialog.Accepted:
        print dialog.get()
        app.exec_()
    else:
        print('close')

    sys.exit(0)

