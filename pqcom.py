
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
from util import resource_path, TRANS_TABLE, TRANS_STRING
import string
from PySide import QtSvg, QtXml
from time import sleep

DEFAULT_EOF = '\n'
txqueue = Queue.Queue()
rxqueue = Queue.Queue()
    
class AboutDialog(QDialog, pqcom_about_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

class SetupDialog(QDialog, pqcom_setup_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(SetupDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        self.ports = None
        self.refresh()
        
        self.portComboBox.clicked.connect(self.refresh)
            
    def show(self, hasError=False):
        if hasError:
            self.portComboBox.setStyleSheet('QComboBox {color: red;}')
        else:
            self.refresh()
            
        return self.exec_()
                
    def refresh(self):
        self.portComboBox.setStyleSheet('QComboBox {color: black;}')
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

        self.inputHistory = ''
        self.outputHistory = []
        self.repeater = Repeater()
        
        self.setWindowIcon(QIcon(resource_path('img/pqcom-logo.png')))
        
        self.aboutDialog = AboutDialog(self)
        
        self.setupDialog = SetupDialog(self)
        parameters = self.setupDialog.get()
        self.setWindowTitle('pqcom - ' + parameters[0] + ' ' + str(parameters[1]))

        self.actionNew.setIcon(QIcon(resource_path('img/new.png')))
        self.actionSetup.setIcon(QIcon(resource_path('img/settings.png')))
        self.actionRun.setIcon(QIcon(resource_path('img/run.png')))
        self.actionHex.setIcon(QIcon(resource_path('img/hex.png')))
        self.actionClear.setIcon(QIcon(resource_path('img/clear.png')))
        self.actionAbout.setIcon(QIcon(resource_path('img/about.png')))

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
        # self.sendButton.setStyleSheet('QToolButton {border: 1px outset rgb(29, 153, 243);}')
        # self.sendButton.setStyleSheet('QToolButton {border: 1px outset rgb(218, 68, 83);}')
        # self.sendButton.setIcon(QIcon(resource_path('img/run.png')))
        
        self.outputHistoryActions = []
        self.outputHistoryMenu = QMenu(self)
        self.historyButton.setMenu(self.outputHistoryMenu)

        self.sendButton.clicked.connect(self.send)
        self.repeatCheckBox.toggled.connect(self.repeat)
        self.actionSetup.triggered.connect(self.setup)
        self.actionNew.triggered.connect(self.new)
        self.actionRun.toggled.connect(self.run)
        self.actionHex.toggled.connect(self.convert)
        self.actionClear.triggered.connect(self.clear)
        self.actionAbout.triggered.connect(self.aboutDialog.show)
        self.outputHistoryMenu.triggered.connect(self.prev)

        QShortcut(QtGui.QKeySequence('Ctrl+Return'), self.sendPlainTextEdit, self.send)
        
        self.extendRadioButton.setVisible(False)
        self.periodSpinBox.setVisible(False)
        # self.historyButton.setVisible(False)
        
    def new(self):
        args = sys.argv
        if args != [sys.executable]:
            args = [sys.executable] + args
        subprocess.Popen(args)
        
    def send(self):
        if self.repeatCheckBox.isChecked():
            if str(self.sendButton.text()) == 'Stop':
                self.repeater.stop()
                self.sendButton.setText('Start')
                return
            
        raw = str(self.sendPlainTextEdit.toPlainText())
        data = raw
        type = ''
        if self.normalRadioButton.isChecked():
            if self.actionAppendEol.isChecked():
                data += '\n'
                
            if self.actionUseCRLF.isChecked():
                data = data.replace('\n', '\r\n')
            elif self.actionUseCR.isChecked():
                data = data.replace('\n', '\r')
        elif self.hexRadioButton.isChecked():
            type = 'HEX'
            data = str(bytearray.fromhex(data.replace('\n', ' ')))
        else:
            pass
            
        if self.repeatCheckBox.isChecked():
            self.repeater.start(data, self.periodSpinBox.value())
            self.sendButton.setText('Stop')
        else:
            txqueue.put(data);
            
        # record history
        record = [type, raw, data]
        try:
            self.outputHistory.remove(record)
        except ValueError as e:
            pass
        self.outputHistory.insert(0, record)
        
        self.outputHistoryActions = []
        self.outputHistoryMenu.clear()
        for item in self.outputHistory:
            text = item[1]
            if item[0]:
                text = item[0] + ':' + text
            action = self.outputHistoryMenu.addAction(text)
            self.outputHistoryActions.append(action)
        
    def repeat(self, isTrue):
        if isTrue:
            self.periodSpinBox.setVisible(True)
            self.sendButton.setText('Start')
        else:
            self.periodSpinBox.setVisible(False)
            self.sendButton.setText('Send')
            
    def prev(self, action):
        index = self.outputHistoryActions.index(action)
        type, raw, data = self.outputHistory[index]
        if type == 'HEX':
            self.hexRadioButton.setChecked(True)
        else:
            self.normalRadioButton.setChecked(True)
            
        self.sendPlainTextEdit.clear()
        self.sendPlainTextEdit.insertPlainText(raw)
        
    def handle(self):
        self.actionRun.setChecked(False)
        self.setup(True)
        
    def setup(self, hasError=False):
        choice = self.setupDialog.show(hasError)
        if choice == QDialog.Accepted:
            if self.actionRun.isChecked():
                self.actionRun.setChecked(False)
            self.actionRun.setChecked(True)
        else:
            print('close')
            
    def run(self, isTrue):
        parameters = self.setupDialog.get()
        if isTrue:
            worker.start(parameters)
            self.setWindowTitle('pqcom - ' + parameters[0] + ' ' + str(parameters[1]) + ' opened')
        else:
            worker.join()
            self.setWindowTitle('pqcom - ' + parameters[0] + ' ' + str(parameters[1]) + ' closed')

    def display(self):
        if rxqueue.empty():
            return
          
        data = rxqueue.get()
        self.inputHistory += data      # store history data

        if self.actionHex.isChecked():
            data = self.hex(data)
        else:
            pass
            #data = data.translate(TRANS_TABLE)
            
        self.recvTextEdit.moveCursor(QTextCursor.End)
        self.recvTextEdit.insertPlainText(data)
        self.recvTextEdit.moveCursor(QTextCursor.End)

    def convert(self, is_true):
        text = None
        if is_true:
            text = self.hex(self.inputHistory)
        else:
            text = self.inputHistory
            #text = self.inputHistory.translate(TRANS_TABLE)
        
        self.recvTextEdit.clear()
        self.recvTextEdit.insertPlainText(text)
        self.recvTextEdit.moveCursor(QTextCursor.End)
        
    def hex(self, data):
        convertedtext = ''
        bytesindex = 0
        hexpart = ''
        strpart = ''
        while bytesindex < len(data):
            ch = data[bytesindex]
            if ch == '\n':
                hexpart += '0A' + ' '
                strpart += '.'
                
                convertedtext += hexpart.ljust(52) + strpart + '\n'
                hexpart = ''
                strpart = ''
            elif ch == '\r':
                hexpart += '0D' + ' '
                strpart += '.'
                
                if ((bytesindex + 1) < len(data)) and (data[bytesindex + 1] == '\n'):
                    hexpart += '0A' + ' '
                    strpart += '.'
                    bytesindex += 1

                convertedtext += hexpart.ljust(52) + strpart + '\n'
                hexpart = ''
                strpart = ''
            else:
                hexpart += '{:02X}'.format(ord(ch)) + ' '
                if ch < '\x20' or ch > '\x7F':
                    ch = '.'
                strpart += ch
                
            if len(strpart) >= 16:
                convertedtext += hexpart.ljust(52) + strpart + '\n'
                hexpart = ''
                strpart = ''
                
            bytesindex += 1
            
        if strpart:
            convertedtext += hexpart.ljust(52) + strpart + '\n'
            
        return convertedtext

    def clear(self):
        self.recvTextEdit.clear()
        self.inputHistory = ''
        
class Repeater():
    def __init__(self):
        self.stopevent = threading.Event()
        
    def setPeriod(self, period):
        self.period = period
        
    def start(self, data, period):
        self.stopevent.clear()
        self.data = data
        self.period = period
        self.thread = threading.Thread(target=self.repeat)
        self.thread.start()
        
    def stop(self):
        self.stopevent.set()
        
    def repeat(self):
        print('repeater thread is started')
        while not self.stopevent.is_set():
            worker.put(self.data)
            sleep(self.period)
        print('repeater thread exits')
        
class Worker(QObject):
    received = Signal()
    failed = Signal()
    
    def __init__(self, txqueue, rxqueue):
        super(Worker, self).__init__()
        
        self.serial = None
        self.parameters = None
        self.stopevent = threading.Event()
        self.txqueue = txqueue
        self.rxqueue = rxqueue
        
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
            self.stopevent.set()   
            self.txthread = threading.Thread(target=self.send)
            self.rxthread = threading.Thread(target=self.recv)
            self.stopevent.clear()
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
    
    @Slot(str)    
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
                    self.rxqueue.put(data)
                    self.received.emit()
            except IOError as e:
                self.serial.close()
                self.stopevent.set()
                self.failed.emit()
            
        print('rx thread exits')    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    worker = Worker(txqueue, rxqueue)
    window = MainWindow()
    
    worker.received.connect(window.display)
    worker.failed.connect(window.handle)
    
    window.show()
    window.setup()
    app.exec_()
    worker.join()
    sys.exit(0)

