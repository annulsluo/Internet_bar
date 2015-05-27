# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Sun Feb  1 03:54:26 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(500, 300)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        self.pushButton_sure = QtGui.QPushButton(Dialog)
        desktop = QtGui.QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        print( "width %d, height %d", width, height )
        #self.pushButton_sure.setGeometry(QtCore.QRect(150, 170, 91, 31))
        mywidth = ( width / 2) - 100
        myheight = ( height / 2 ) + 10
        self.pushButton_sure.setGeometry(QtCore.QRect( mywidth, myheight, 91, 31 ))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_sure.setFont(font)
        self.pushButton_sure.setObjectName(_fromUtf8("pushButton_sure"))
        self.Label_ID_Card = QtGui.QLabel(Dialog)
        #self.Label_ID_Card.setGeometry(QtCore.QRect(80, 80, 61, 31))
        self.Label_ID_Card.setGeometry(QtCore.QRect(mywidth - 70, myheight - 90, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label_ID_Card.setFont(font)
        self.Label_ID_Card.setObjectName(_fromUtf8("Label_ID_Card"))
        self.Label_Pass = QtGui.QLabel(Dialog)
        #self.Label_Pass.setGeometry(QtCore.QRect(80, 120, 61, 31))
        self.Label_Pass.setGeometry(QtCore.QRect(mywidth - 70, myheight - 50, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label_Pass.setFont(font)
        self.Label_Pass.setObjectName(_fromUtf8("Label_Pass"))
        self.Label_LoginMsg = QtGui.QLabel(Dialog)
        self.Label_LoginMsg.setEnabled(False)
        #self.Label_LoginMsg.setGeometry(QtCore.QRect(150, 150, 181, 20))
        self.Label_LoginMsg.setGeometry(QtCore.QRect(mywidth, myheight - 20, 181, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Andalus"))
        font.setPointSize(10)
        self.Label_LoginMsg.setFont(font)
        self.Label_LoginMsg.setText(_fromUtf8(""))
        self.Label_LoginMsg.setObjectName(_fromUtf8("Label_LoginMsg"))
        self.LineEdit_ID_Card = QtGui.QLineEdit(Dialog)
        #self.LineEdit_ID_Card.setGeometry(QtCore.QRect(150, 80, 181, 31))
        self.LineEdit_ID_Card.setGeometry(QtCore.QRect(mywidth, myheight - 90, 181, 31))
        self.LineEdit_ID_Card.setObjectName(_fromUtf8("LineEdit_ID_Card"))
        self.LineEdit_Pass = QtGui.QLineEdit(Dialog)
        #self.LineEdit_Pass.setGeometry(QtCore.QRect(150, 120, 181, 31))
        self.LineEdit_Pass.setGeometry(QtCore.QRect(mywidth, myheight - 50, 181, 31))
        self.LineEdit_Pass.setEchoMode(QtGui.QLineEdit.Password)
        self.LineEdit_Pass.setObjectName(_fromUtf8("LineEdit_Pass"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "网吧自助管理系统", None))
        self.pushButton_sure.setText(_translate("Dialog", "确定", None))
        self.Label_ID_Card.setText(_translate("Dialog", "身份证：", None))
        self.Label_Pass.setText(_translate("Dialog", "密码：", None))

