# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pqcom.ui'
#
# Created: Sat Mar 14 19:35:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(558, 508)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.recvTextEdit = QtGui.QTextEdit(self.centralwidget)
        self.recvTextEdit.setReadOnly(True)
        self.recvTextEdit.setObjectName("recvTextEdit")
        self.verticalLayout.addWidget(self.recvTextEdit)
        self.sendPlainTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendPlainTextEdit.sizePolicy().hasHeightForWidth())
        self.sendPlainTextEdit.setSizePolicy(sizePolicy)
        self.sendPlainTextEdit.setMinimumSize(QtCore.QSize(0, 32))
        self.sendPlainTextEdit.setMaximumSize(QtCore.QSize(16777215, 128))
        self.sendPlainTextEdit.setBaseSize(QtCore.QSize(0, 0))
        self.sendPlainTextEdit.setObjectName("sendPlainTextEdit")
        self.verticalLayout.addWidget(self.sendPlainTextEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtGui.QRadioButton(self.centralwidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.hexRadioButton = QtGui.QRadioButton(self.centralwidget)
        self.hexRadioButton.setObjectName("hexRadioButton")
        self.horizontalLayout.addWidget(self.hexRadioButton)
        self.extendRadioButton = QtGui.QRadioButton(self.centralwidget)
        self.extendRadioButton.setObjectName("extendRadioButton")
        self.horizontalLayout.addWidget(self.extendRadioButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.sendButton = QtGui.QPushButton(self.centralwidget)
        self.sendButton.setAutoDefault(False)
        self.sendButton.setDefault(False)
        self.sendButton.setFlat(False)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "pqcom", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("MainWindow", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.hexRadioButton.setText(QtGui.QApplication.translate("MainWindow", "Hex", None, QtGui.QApplication.UnicodeUTF8))
        self.extendRadioButton.setText(QtGui.QApplication.translate("MainWindow", "Extend", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("MainWindow", "Send", None, QtGui.QApplication.UnicodeUTF8))

