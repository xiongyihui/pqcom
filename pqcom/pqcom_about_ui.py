# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pqcom_about.ui'
#
# Created: Fri Mar 20 22:33:16 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from util import resource_path, VERSION

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(432, 224)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "pqcom - About", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:16px; margin-bottom:0px; margin-left:16px; margin-right:16px; -qt-block-indent:0; text-indent:0px;\"><br /><img src=\"" + resource_path("img/pqcom-logo-expanded.png") + "\" height=\"64\" /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:16px; margin-bottom:16px; margin-left:16px; margin-right:16px; -qt-block-indent:0; text-indent:0px;\">pqcom, a simple cross platform serial tool.<br /><br />Version:     " + str(VERSION) + "<br />Author:      Yihui Xiong<br />Home:        <a href=\"https://github.com/xiongyihui/pqcom\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/xiongyihui/pqcom</span></a><br />License:     MIT</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
