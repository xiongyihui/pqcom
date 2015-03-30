
import sys
import os
import subprocess
import threading
import Queue
import serial
from serial.tools import list_ports
from pqcom_ui import *
import pqcom_setup_ui
import pqcom_about_ui
from PySide.QtGui import *
from PySide.QtCore import *

NORMAL_STRING = 0
HEX_STRING = 1
EXTEND_STRING = 2


script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
worker = None

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', script_path)
    return os.path.join(base_path, relative_path)
    
class AboutDialog(QDialog, pqcom_about_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)

class SetupDialog(QDialog, pqcom_setup_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(SetupDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.ports = None
        self.originalPalette = self.portComboBox.palette()
        
        self.refresh()
        
        self.portComboBox.clicked.connect(self.refresh)
            
    def show(self, hasError=False):
        if hasError:
            p = self.portComboBox.palette()
            p.setColor(QPalette.Text, QColor(255, 0, 0))
            self.portComboBox.setPalette(p)
        else:
            self.refresh()
            
        return self.exec_()
                
    def refresh(self):
        self.portComboBox.setPalette(self.originalPalette)
        ports = list_ports.comports()
        if ports != self.ports:
            self.ports = ports
            self.portComboBox.clear()
            for port in list_ports.comports():
                name = port[0]
                if name.startswith('/dev/ttyACM') or name.startswith('/dev/ttyUSB') or name.startswith('COM'):
                    self.portComboBox.addItem(name)
                
    def get(self):
        port = str(self.portComboBox.currentText())
        baud = int(self.baudComboBox.currentText())
        databits = int(self.dataComboBox.currentText())
        stopbits = int(self.stopbitComboBox.currentText())
        parity = str(self.parityComboBox.currentText())[0]
        
        return (port, baud, databits, stopbits, parity)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowIcon(QIcon(resource_path('img/pqcom-logo.png')))
        
        self.aboutDialog = AboutDialog(self)
        
        self.setupDialog = SetupDialog(self)
        self.actionNew.setIcon(QIcon(resource_path('img/new.svg')))
        self.actionSetup.setIcon(QIcon(resource_path('img/settings.svg')))
        self.actionRun.setIcon(QIcon(resource_path('img/run.svg')))
        self.actionHex.setIcon(QIcon(resource_path('img/hex.png')))
        self.actionClear.setIcon(QIcon(resource_path('img/clear.svg')))
        self.actionAbout.setIcon(QIcon(resource_path('img/about.svg')))
        
        actionEnterSend = QAction('"Enter" to send', self)
        actionEnterSend.setCheckable(True)
        actionCtrlEnterSend = QAction('"Ctrl + Enter" to send', self)
        actionCtrlEnterSend.setCheckable(True)
        shortcutGroup = QActionGroup(self)
        shortcutGroup.addAction(actionEnterSend)
        shortcutGroup.addAction(actionCtrlEnterSend)
        shortcutGroup.setExclusive(True)

        actionUseCR = QAction('EOL - \\r', self)
        actionUseCR.setCheckable(True)
        actionUseLF = QAction('EOL - \\n', self)
        actionUseLF.setCheckable(True)
        actionUseCRLF = QAction('EOL - \\r\\n', self)
        actionUseCRLF.setCheckable(True)
        actionUseCRLF.setChecked(True)
        eolGroup = QActionGroup(self)
        eolGroup.addAction(actionUseCR)
        eolGroup.addAction(actionUseLF)
        eolGroup.addAction(actionUseCRLF)
        eolGroup.setExclusive(True)

        actionAppendEol = QAction('Append extra EOL', self)
        actionAppendEol.setCheckable(True)


        popupMenu = QMenu(self)
        # popupMenu.addAction(actionEnterSend)
        # popupMenu.addAction(actionCtrlEnterSend)
        popupMenu.addAction(actionUseCR)
        popupMenu.addAction(actionUseLF)
        popupMenu.addAction(actionUseCRLF)
        popupMenu.addSeparator()
        popupMenu.addAction(actionAppendEol)

        self.sendButton.setMenu(popupMenu)
        # self.sendButton.setIcon(QIcon(resource_path('img/run.png')))

        p = self.sendButton.palette()
        p.setColor(QPalette.Window, QColor(255, 0, 0))
        self.sendButton.setPalette(self.setupDialog.originalPalette)
        
        self.sendButton.clicked.connect(self.send)
        self.actionSetup.triggered.connect(self.setup)
        self.actionNew.triggered.connect(self.new)
        self.actionRun.toggled.connect(self.run)
        self.actionAbout.triggered.connect(self.aboutDialog.show)
        
        self.actionHex.setVisible(False)
        self.extendRadioButton.setVisible(False)
        
    def new(self):
        args = [sys.executable] + sys.argv
        subprocess.Popen(args)
        
    def send(self):
        data = str(self.sendPlainTextEdit.toPlainText())
        datatype = NORMAL_STRING
        if self.normalRadioButton.isChecked():
            pass
        elif self.hexRadioButton.isChecked():
            datatype = HEX_STRING
        else:
            datatype = EXTEND_STRING
            
        worker.put(data, datatype);
        
    def handle(self):
        self.actionRun.setChecked(False)
        self.setup(True)
        
    def setup(self, hasError=False):
        choice = self.setupDialog.show(hasError)
        if choice == QDialog.Accepted:
            # parameters = self.setupDialog.get()
            # worker.start(parameters)
            self.actionRun.setChecked(True)
        else:
            print('close')
            
    def run(self, is_true):
        parameters = self.setupDialog.get()
        if is_true:
            worker.start(parameters)
            self.setWindowTitle('pqcom - ' + parameters[0] + ' ' + str(parameters[1]) + ' opened')
        else:
            worker.join()
            self.setWindowTitle('pqcom - ' + parameters[0] + ' ' + str(parameters[1]) + ' closed')

    def display(self, text):
        # self.recvTextEdit.append(text)
        self.recvTextEdit.moveCursor(QTextCursor.End)
        self.recvTextEdit.insertPlainText(text)
        self.recvTextEdit.moveCursor(QTextCursor.End)
        
class Worker(QObject):
    received = Signal(str)
    failed = Signal()
    
    def __init__(self):
        super(Worker, self).__init__()
        
        self.serial = None
        self.parameters = None
        self.stopevent = threading.Event()
        self.txqueue = Queue.Queue()
        self.rxqueue = Queue.Queue()
        
        self.txthread = None
        self.rxthread = None
        
    def start(self, parameters):
        self.parameters = parameters
        try:
            self.serial = serial.Serial(port = parameters[0],
                                        baudrate = parameters[1],
                                        bytesize = parameters[2],
                                        stopbits = parameters[3],
                                        timeout  = 0.2)
            if self.stopevent.is_set():
                self.stopevent.clear()
                
                self.txthread = threading.Thread(target=self.send)
                self.rxthread = threading.Thread(target=self.recv)
                self.txthread.start()
                self.rxthread.start()
            else:
                if not self.txthread:
                    self.txthread = threading.Thread(target=self.send)
                    self.rxthread = threading.Thread(target=self.recv)
                    self.txthread.start()
                    self.rxthread.start()
                
        except IOError as e:
            print(e)
            self.failed.emit()
 
    def join(self):
        self.stopevent.set()
        if self.txthread:
            self.txthread.join()
            self.rxthread.join()
        
        if self.serial:
            self.serial.close()
    
    @Slot(str, int)    
    def put(self, data, datatype):
        self.txqueue.put((data, datatype))

        
    def send(self):
        print('tx thread is started')
        while not self.stopevent.is_set():
            try:
                data, datatype = self.txqueue.get(True, 1)
                if datatype == HEX_STRING:
                    data = str(bytearray.fromhex(data))
                elif datatype == EXTEND_STRING:
                    # to do
                    pass
                    
                print('tx:' + data)
                self.serial.write(data)
            except Queue.Empty:
                continue
            except IOError as e:
                self.serial.close()
                self.stopevent.set()
                self.failed.emit()
                
        print('tx thread exits')
            
    def recv(self):
        print('rx thread is started')
        while not self.stopevent.is_set():
            try:
                data = self.serial.read(64)
                
                if data and len(data) > 0:
                    print('rx:' + data)
                    self.received.emit(data)
            except IOError as e:
                self.serial.close()
                self.stopevent.set()
                self.failed.emit()
            
        print('rx thread exits')    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    worker = Worker()
    window = MainWindow()
    
    worker.received.connect(window.display)
    worker.failed.connect(window.handle)
    
    window.show()
    window.setup()
    app.exec_()
    worker.join()
    sys.exit(0)

