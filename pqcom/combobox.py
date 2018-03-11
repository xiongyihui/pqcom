# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

class ComboBox(QtWidgets.QComboBox):
    clicked = QtCore.pyqtSignal()

    def showPopup(self):
        self.clicked.emit()
        super(ComboBox, self).showPopup()
