# -*- coding: utf-8 -*-

from PySide6 import QtCore, QtWidgets

class ComboBox(QtWidgets.QComboBox):
    clicked = QtCore.Signal()

    def showPopup(self):
        self.clicked.emit()
        super(ComboBox, self).showPopup()
