# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pqcom_setup.ui'
#
# Created: Sat Mar 14 19:43:28 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(236, 218)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.portComboBox = CustomComboBox(Dialog)
        self.portComboBox.setEditable(True)
        self.portComboBox.setObjectName("portComboBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.portComboBox)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.baudComboBox = QtGui.QComboBox(Dialog)
        self.baudComboBox.setEditable(True)
        self.baudComboBox.setObjectName("baudComboBox")
        self.baudComboBox.addItem("")
        self.baudComboBox.addItem("")
        self.baudComboBox.addItem("")
        self.baudComboBox.addItem("")
        self.baudComboBox.addItem("")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.baudComboBox)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.stopbitComboBox = QtGui.QComboBox(Dialog)
        self.stopbitComboBox.setObjectName("stopbitComboBox")
        self.stopbitComboBox.addItem("")
        self.stopbitComboBox.addItem("")
        self.stopbitComboBox.addItem("")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.stopbitComboBox)
        self.dataComboBox = QtGui.QComboBox(Dialog)
        self.dataComboBox.setEditable(True)
        self.dataComboBox.setObjectName("dataComboBox")
        self.dataComboBox.addItem("")
        self.dataComboBox.addItem("")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dataComboBox)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.parityComboBox = QtGui.QComboBox(Dialog)
        self.parityComboBox.setObjectName("parityComboBox")
        self.parityComboBox.addItem("")
        self.parityComboBox.addItem("")
        self.parityComboBox.addItem("")
        self.parityComboBox.addItem("")
        self.parityComboBox.addItem("")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.parityComboBox)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Open)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "pqcom", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Port Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Baud Rate", None, QtGui.QApplication.UnicodeUTF8))
        self.baudComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "115200", None, QtGui.QApplication.UnicodeUTF8))
        self.baudComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "57600", None, QtGui.QApplication.UnicodeUTF8))
        self.baudComboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "38400", None, QtGui.QApplication.UnicodeUTF8))
        self.baudComboBox.setItemText(3, QtGui.QApplication.translate("Dialog", "19200", None, QtGui.QApplication.UnicodeUTF8))
        self.baudComboBox.setItemText(4, QtGui.QApplication.translate("Dialog", "9600", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Stop Bits", None, QtGui.QApplication.UnicodeUTF8))
        self.stopbitComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.stopbitComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "1.5", None, QtGui.QApplication.UnicodeUTF8))
        self.stopbitComboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.dataComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "8", None, QtGui.QApplication.UnicodeUTF8))
        self.dataComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "7", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Data Bits", None, QtGui.QApplication.UnicodeUTF8))
        self.parityComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.parityComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "Even", None, QtGui.QApplication.UnicodeUTF8))
        self.parityComboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "Odd", None, QtGui.QApplication.UnicodeUTF8))
        self.parityComboBox.setItemText(3, QtGui.QApplication.translate("Dialog", "Mark", None, QtGui.QApplication.UnicodeUTF8))
        self.parityComboBox.setItemText(4, QtGui.QApplication.translate("Dialog", "Space", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Parity", None, QtGui.QApplication.UnicodeUTF8))
        
class CustomComboBox(QtGui.QComboBox):
    clicked = QtCore.Signal()
    
    def __init__(self, parent):
        super(CustomComboBox, self).__init__(parent)
        
    def showPopup(self):
        self.clicked.emit()
        super(CustomComboBox, self).showPopup()

