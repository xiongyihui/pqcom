#!/usr/bin/env python3

"""
+------------------------------------------------------------------+
| pq                      pqcom                              - + x |
+------------------------------------------------------------------+
| + | > | = | H | X | i |                                          |
+------------------------------------------------------------------+
| |   |   |   |   |   |                                            |
| |   |   |   |   |   +---> Open about dialog                      |
| |   |   |   |   |                                                |
| |   |   |   |   +-------> Clear received message                 |
| |   |   |   |                                                    |
| |   |   |   +-----------> Enable/Disable Hex View                |
| |   |   |                                                        |
| |   |   +---------------> Open settings dialog                   |
| |   |                                                            |
| |   +-------------------> Open/Close serial port                 |
| |                                                                |
| +-----------------------> Open a new window                      |
|                                                                  |
|                                                                  |
|                                                                  |
|                                                                  |
|                                                                  |
|                                                                  |
+------------------------------------------------------------------+
|                                                                  |
|  Keyboard Shortcut                                               |
|      Ctrl + Enter: Send                                          |
|                                                                  |
+------------------------------------------------------------------+
| + Normal | O Hex | O Extended | * | History |  | # Repeat | Send |
+------------------------------------------------------------------+
"""

import sys
import os
import subprocess
import threading
from time import sleep
import pickle

from PyQt5.QtGui import QIcon, QKeySequence, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QAction, QActionGroup, QMenu, QShortcut
from PyQt5.QtCore import Qt, pyqtSignal as Signal
# from PyQt5 import QtSvg

from pqcom import serial_bus
from pqcom import pqcom_translator as translator
from pqcom import setup_ui
from pqcom import about_ui
from pqcom import main_ui
from pqcom.util import resource_path


PQCOM_DATA_FILE = os.path.join(os.path.expanduser('~'), '.pqcom_data3')
ICON_LIB = {'N': 'img/normal.svg', 'H': 'img/0x.svg', 'E': 'img/ex.svg'}

DEFAULT_EOF = '\n'
serial = None


class AboutDialog(QDialog, about_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)


class SetupDialog(QDialog, setup_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(SetupDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.ports = []
        self.refresh()

        self.portComboBox.clicked.connect(self.refresh)

    def show(self, warning=False):
        if warning:
            self.portComboBox.setStyleSheet('QComboBox {color: red;}')
        else:
            self.refresh()

        return self.exec_()

    def refresh(self):
        self.portComboBox.setStyleSheet('QComboBox {color: black;}')
        ports = serial_bus.get_ports()
        if ports != self.ports:
            self.ports = ports
            self.portComboBox.clear()
            for port in ports:
                self.portComboBox.addItem(port)

    def get(self):
        port = str(self.portComboBox.currentText())
        baud = int(self.baudComboBox.currentText())
        bytebits = int(self.dataComboBox.currentText())
        stopbits = int(self.stopbitComboBox.currentText())
        parity = str(self.parityComboBox.currentText())

        return port, baud, bytebits, stopbits, parity


class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    serial_failed = Signal()
    data_received = Signal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.collections = []
        try:
            saved = open(PQCOM_DATA_FILE, 'rb')
            self.collections = pickle.load(saved)
            saved.close()
        except IOError:
            pass

        self.input_history = ''
        self.output_history = []
        self.repeater = Repeater()

        self.setWindowIcon(QIcon(resource_path('img/pqcom-logo.png')))

        self.aboutDialog = AboutDialog(self)

        self.setupDialog = SetupDialog(self)
        port, baud, bytebits, stopbits, parity = self.setupDialog.get()
        self.setWindowTitle('pqcom - ' + port + ' ' + str(baud))

        self.actionNew.setIcon(QIcon(resource_path('img/new.svg')))
        self.actionSetup.setIcon(QIcon(resource_path('img/settings.svg')))
        self.actionRun.setIcon(QIcon(resource_path('img/run.svg')))
        self.actionHex.setIcon(QIcon(resource_path('img/hex.svg')))
        self.actionClear.setIcon(QIcon(resource_path('img/clear.svg')))
        self.actionPin.setIcon(QIcon(resource_path('img/pin.svg')))
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

        self.outputHistoryActions = []
        self.outputHistoryMenu = QMenu(self)
        self.outputHistoryMenu.addAction('None')
        self.historyButton.setMenu(self.outputHistoryMenu)

        self.collectActions = []
        self.collectMenu = QMenu(self)
        self.collectMenu.setTearOffEnabled(True)
        if not self.collections:
            self.collectMenu.addAction('None')
        else:
            for item in self.collections:
                icon = QIcon(resource_path(ICON_LIB[item[0]]))
                action = self.collectMenu.addAction(icon, item[1])
                self.collectActions.append(action)

        self.collectButton.setMenu(self.collectMenu)
        self.collectButton.setIcon(QIcon(resource_path('img/star.svg')))

        self.collectMenu.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.connect(self.collectMenu, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                    #  self.on_collect_context_menu)
        self.collectContextMenu = QMenu(self)
        self.removeCollectionAction = QAction('Remove', self)
        self.removeAllCollectionsAction = QAction('Remove all', self)
        self.collectContextMenu.addAction(self.removeCollectionAction)
        self.collectContextMenu.addAction(self.removeAllCollectionsAction)

        self.activeCollectAction = None

        self.removeCollectionAction.triggered.connect(self.remove_collection)
        self.removeAllCollectionsAction.triggered.connect(self.remove_all_collections)

        self.sendButton.clicked.connect(self.send)
        self.repeatCheckBox.toggled.connect(self.repeat)
        self.actionSetup.triggered.connect(self.setup)
        self.actionNew.triggered.connect(self.new)
        self.actionRun.toggled.connect(self.run)
        self.actionHex.toggled.connect(self.convert)
        self.actionClear.triggered.connect(self.clear)
        self.actionPin.toggled.connect(self.pin)
        self.actionAbout.triggered.connect(self.aboutDialog.show)
        self.outputHistoryMenu.triggered.connect(self.on_history_item_clicked)
        self.collectButton.clicked.connect(self.collect)
        self.collectMenu.triggered.connect(self.on_collect_item_clicked)

        self.serial_failed.connect(self.handle_serial_error)
        self.data_received.connect(self.display)

        QShortcut(QKeySequence('Ctrl+Return'), self.sendPlainTextEdit, self.send)

        def gen_shortcut_callback(n):
            def on_shortcut():
                self.send_collection(n - 1)

            return on_shortcut

        for i in range(1, 10):
            QShortcut(QKeySequence('Ctrl+' + str(i)), self, gen_shortcut_callback(i))

        # self.extendRadioButton.setVisible(False)
        self.periodSpinBox.setVisible(False)

    def new(self):
        save = open(PQCOM_DATA_FILE, 'wb')
        pickle.dump(self.collections, save)
        save.close()

        args = sys.argv
        if args != [sys.executable]:
            args = [sys.executable] + args
        subprocess.Popen(args)

    def send(self):
        if self.repeatCheckBox.isChecked():
            if self.sendButton.text().find('Stop') >= 0:
                self.repeater.stop()
                self.sendButton.setText('Start')
                return

        raw = str(self.sendPlainTextEdit.toPlainText())
        data = raw
        form = 'N'
        if self.normalRadioButton.isChecked():
            if self.actionAppendEol.isChecked():
                data += '\n'

            if self.actionUseCRLF.isChecked():
                data = data.replace('\n', '\r\n')
            elif self.actionUseCR.isChecked():
                data = data.replace('\n', '\r')
        elif self.hexRadioButton.isChecked():
            form = 'H'
            data = translator.from_hex_string(data)
        else:
            form = 'E'
            data = translator.from_extended_string(data)

        if self.repeatCheckBox.isChecked():
            self.repeater.start(data, self.periodSpinBox.value())
            self.sendButton.setText('Stop')
        else:
            serial.write(data)

        # record history
        record = [form, raw, data]
        if record in self.output_history:
            self.output_history.remove(record)

        self.output_history.insert(0, record)

        self.outputHistoryActions = []
        self.outputHistoryMenu.clear()
        for item in self.output_history:
            icon = QIcon(resource_path(ICON_LIB[item[0]]))

            action = self.outputHistoryMenu.addAction(icon, item[1])
            self.outputHistoryActions.append(action)

    def repeat(self, is_true):
        if is_true:
            self.periodSpinBox.setVisible(True)
            self.sendButton.setText('Start')
        else:
            self.periodSpinBox.setVisible(False)
            self.sendButton.setText('Send')
            self.repeater.stop()

    def on_history_item_clicked(self, action):
        try:
            index = self.outputHistoryActions.index(action)
        except ValueError:
            return

        form, raw, data = self.output_history[index]
        if form == 'H':
            self.hexRadioButton.setChecked(True)
        elif form == 'E':
            self.extendRadioButton.setChecked(True)
        else:
            self.normalRadioButton.setChecked(True)

        self.sendPlainTextEdit.clear()
        self.sendPlainTextEdit.insertPlainText(raw)
        self.send()

    def collect(self):
        if not self.collections:
            self.collectMenu.clear()
        raw = str(self.sendPlainTextEdit.toPlainText())
        form = 'N'
        if self.hexRadioButton.isChecked():
            form = 'H'
        elif self.extendRadioButton.isChecked():
            form = 'E'

        item = [form, raw]
        if item in self.collections:
            return

        self.collections.append(item)
        icon = QIcon(resource_path(ICON_LIB[form]))
        action = self.collectMenu.addAction(icon, raw)
        self.collectActions.append(action)

    def on_collect_context_menu(self, point):
        self.activeCollectAction = self.collectMenu.activeAction()
        self.collectContextMenu.exec_(self.collectMenu.mapToGlobal(point))

    def on_collect_item_clicked(self, action):
        try:
            index = self.collectActions.index(action)
        except ValueError:
            return
        self.send_collection(index)

    def send_collection(self, index):
        if len(self.collections) > index:
            form, raw = self.collections[index]
            if form == 'H':
                self.hexRadioButton.setChecked(True)
            elif form == 'E':
                self.extendRadioButton.setChecked(True)
            else:
                self.normalRadioButton.setChecked(True)

            self.sendPlainTextEdit.clear()
            self.sendPlainTextEdit.insertPlainText(raw)
            self.send()

    def remove_collection(self):
        try:
            index = self.collectActions.index(self.activeCollectAction)
        except ValueError:
            return

        del self.collectActions[index]
        del self.collections[index]

        self.collectMenu.clear()
        for item in self.collections:
            icon = QIcon(resource_path(ICON_LIB[item[0]]))
            action = self.collectMenu.addAction(icon, item[1])
            self.collectActions.append(action)

        save = open(PQCOM_DATA_FILE, 'wb')
        pickle.dump(self.collections, save)
        save.close()

    def remove_all_collections(self):
        self.collectMenu.clear()
        self.collections = []
        self.collectActions = []
        self.collectMenu.addAction('None')

        save = open(PQCOM_DATA_FILE, 'wb')
        save.close()
        pickle.dump(self.collections, save)

    def on_serial_failed(self):
        if self.sendButton.text().find('Stop') >= 0:
            self.repeater.stop()
            self.sendButton.setText('Start')
        self.serial_failed.emit()

    def handle_serial_error(self):
        self.actionRun.setChecked(False)
        self.setup(True)

    def on_data_received(self):
        self.data_received.emit()

    def setup(self, warning=False):
        choice = self.setupDialog.show(warning)
        if choice == QDialog.Accepted:
            if self.actionRun.isChecked():
                self.actionRun.setChecked(False)
            self.actionRun.setChecked(True)

    def run(self, is_true):
        port, baud, bytebits, stopbits, parity = self.setupDialog.get()
        if is_true:
            serial.start(port, baud, bytebits, stopbits, parity)
            self.setWindowTitle('pqcom - ' + port + ' ' + str(baud) + ' opened')
        else:
            if self.sendButton.text().find('Stop') >= 0:
                self.repeater.stop()
                self.sendButton.setText('Start')
            serial.join()
            self.setWindowTitle('pqcom - ' + port + ' ' + str(baud) + ' closed')

    def display(self):
        data = serial.read()
        self.input_history += data  # store history data

        if self.actionHex.isChecked():
            data = translator.to_hex_prefix_string(data)

        self.recvTextEdit.moveCursor(QTextCursor.End)
        self.recvTextEdit.insertPlainText(data)
        self.recvTextEdit.moveCursor(QTextCursor.End)

    def convert(self, is_true):
        if is_true:
            text = translator.to_hex_prefix_string(self.input_history)
        else:
            text = self.input_history

        self.recvTextEdit.clear()
        self.recvTextEdit.insertPlainText(text)
        self.recvTextEdit.moveCursor(QTextCursor.End)

    def pin(self, is_true):
        if is_true:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)

        self.show()

    def clear(self):
        self.recvTextEdit.clear()
        self.input_history = ''

    def closeEvent(self, event):
        save = open(PQCOM_DATA_FILE, 'wb')
        pickle.dump(self.collections, save)
        save.close()

        event.accept()


class Repeater(object):
    def __init__(self):
        self.stop_event = threading.Event()
        self.period = 1
        self.thread = None

    def set_period(self, period):
        self.period = period

    def start(self, data, period):
        self.stop_event.clear()
        self.period = period
        self.thread = threading.Thread(target=self.repeat, args=(data,))
        self.thread.start()

    def stop(self):
        self.stop_event.set()

    def repeat(self, data):
        print('repeater thread is started')
        while not self.stop_event.is_set():
            serial.write(data)
            sleep(self.period)
        print('repeater thread exits')

def main():
    global serial

    app = QApplication(sys.argv)
    window = MainWindow()
    serial = serial_bus.SerialBus(window.on_data_received, window.on_serial_failed)

    window.show()
    window.setup()
    app.exec_()
    serial.join()
    sys.exit(0)

if __name__ == '__main__':
    main()
