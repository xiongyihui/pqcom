
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
from cStringIO import StringIO
import string
from PySide import QtSvg, QtXml

DEFAULT_EOF = '\n'
TRANS_STRING = ''.join(chr(i) for i in range(0, 0x20) + range(0x80, 0x100))
TRANS_TABLE = string.maketrans(TRANS_STRING, ''.ljust(len(TRANS_STRING), '.'))

worker = None


script_path = os.path.dirname(os.path.realpath(sys.argv[0]))

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

        self.input = StringIO()
        
        self.setWindowIcon(QIcon(resource_path('img/pqcom-logo.png')))
        
        self.aboutDialog = AboutDialog(self)
        
        self.setupDialog = SetupDialog(self)
        parameters = self.setupDialog.get()
        self.setWindowTitle('pqcom - ' + parameters[0] + ' ' + str(parameters[1]))

        self.actionNew.setIcon(QIcon(resource_path('img/new.svg')))
        self.actionSetup.setIcon(QIcon(resource_path('img/settings.svg')))
        self.actionRun.setIcon(QIcon(resource_path('img/run.svg')))
        self.actionHex.setIcon(QIcon(resource_path('img/hex.svg')))
        self.actionClear.setIcon(QIcon(resource_path('img/clear.svg')))
        self.actionAbout.setIcon(QIcon(resource_path('img/about.svg')))

        self.actionUseCR = QAction('EOL - \\r', self)
        self.actionUseCR.setCheckable(True)
        self.actionUseLF = QAction('EOL - \\n', self)
        self.actionUseLF.setCheckable(True)
        self.actionUseCRLF = QAction('EOL - \\r\\n', self)
        self.actionUseCRLF.setCheckable(True)
        self.actionUseCRLF.setChecked(True)
        eolGroup = QActionGroup(self)
        eolGroup.addAction(self.actionUseCR)
        eolGroup.addAction(self.actionUseLF)
        eolGroup.addAction(self.actionUseCRLF)
        eolGroup.setExclusive(True)

        self.actionAppendEol = QAction('Append extra EOL', self)
        self.actionAppendEol.setCheckable(True)


        popupMenu = QMenu(self)
        popupMenu.addAction(self.actionUseCR)
        popupMenu.addAction(self.actionUseLF)
        popupMenu.addAction(self.actionUseCRLF)
        popupMenu.addSeparator()
        popupMenu.addAction(self.actionAppendEol)

        self.sendButton.setMenu(popupMenu)
        # self.sendButton.setIcon(QIcon(resource_path('img/run.png')))

        self.sendButton.clicked.connect(self.send)
        self.actionSetup.triggered.connect(self.setup)
        self.actionNew.triggered.connect(self.new)
        self.actionRun.toggled.connect(self.run)
        self.actionHex.toggled.connect(self.convert)
        self.actionClear.triggered.connect(self.clear)
        self.actionAbout.triggered.connect(self.aboutDialog.show)

        QShortcut(QtGui.QKeySequence("Ctrl+Return"), self.sendPlainTextEdit, self.send)
        
        # self.actionHex.setVisible(False)
        self.extendRadioButton.setVisible(False)
        
    def new(self):
        args = sys.argv
        if args != [sys.executable]:
            args = [sys.executable] + args
        subprocess.Popen(args)
        
    def send(self):
        data = str(self.sendPlainTextEdit.toPlainText())
        if self.normalRadioButton.isChecked():
            if self.actionAppendEol.isChecked():
                data += '\n'
                
            if self.actionUseCRLF.isChecked():
                data = data.replace('\n', '\r\n')
            elif self.actionUseCR.isChecked():
                data = data.replace('\n', '\r')
        elif self.hexRadioButton.isChecked():
            data = str(bytearray.fromhex(data.replace('\n', ' ')))
        else:
            pass
            
        worker.put(data);
        
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
        self.input.write(text)      # store history data

        if self.actionHex.isChecked():
            convertedtext = ''
            buf = StringIO(text)
            line = buf.readline()
            while line:
                if len(line) <= 16:
                    hexpart = ' '.join('{:02X}'.format(ord(c)) for c in line).ljust(52)
                    strpart = line.translate(TRANS_TABLE)

                    convertedtext += hexpart + strpart + '\n'
                    line = buf.readline()
                else:
                    hexpart = ' '.join('{:02X}'.format(ord(c)) for c in line[:16]).ljust(52)
                    strpart = line[:16].translate(TRANS_TABLE)

                    convertedtext += hexpart + strpart + '\n'
                    line = line[16:]
            
            self.recvTextEdit.moveCursor(QTextCursor.End)
            self.recvTextEdit.insertPlainText(convertedtext)
        else: 
            # self.recvTextEdit.append(text)
            self.recvTextEdit.moveCursor(QTextCursor.End)
            self.recvTextEdit.insertPlainText(text)
            self.recvTextEdit.moveCursor(QTextCursor.End)

    def convert(self, is_true):
        text = None
        if is_true:
            convertedtext = ''
            self.input.seek(0, os.SEEK_SET)
            line = self.input.readline()
            while line:
                if len(line) <= 16:
                    hexpart = ' '.join('{:02X}'.format(ord(c)) for c in line).ljust(52)
                    strpart = line.translate(TRANS_TABLE)

                    convertedtext += hexpart + strpart + '\n'
                    line = self.input.readline()
                else:
                    hexpart = ' '.join('{:02X}'.format(ord(c)) for c in line[:16]).ljust(52)
                    strpart = line[:16].translate(TRANS_TABLE)

                    convertedtext += hexpart + strpart + '\n'
                    line = line[16:]
            text = convertedtext
        else:
            text = self.input.getvalue()
        
        self.recvTextEdit.clear()
        self.recvTextEdit.insertPlainText(text)

    def clear(self):
        self.recvTextEdit.clear()
        self.input.truncate(0)
        
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
    def put(self, data):
        self.txqueue.put(data)

        
    def send(self):
        print('tx thread is started')
        while not self.stopevent.is_set():
            try:
                data = self.txqueue.get(True, 1)
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
                data = self.serial.read(1024)
                
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

