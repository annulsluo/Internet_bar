#-*- coding:utf-8 -*-
from PyQt4.QtGui import *;
from PyQt4 import QtGui;
from PyQt4.QtCore import *
import sys, os, datetime, time
#from login import Ui_Dialog;
class ShowMessage( ):
    def __init__( self, aSysTray, aLable_LoginMsg = None ):
        self.SysTray = aSysTray;
        self.Label_LoginMsg = aLable_LoginMsg;

    def ShowTrayMsg( self, Msg ):
        self.SysTray.showMessage( u"网吧自助管理系统", Msg, icon = QSystemTrayIcon.Information, msecs = 5000 );

    def ShowLoginDlgMsg( self, Msg, optype ):
        if optype == 0:# 隐藏登录页面提示错误，缩小化窗口并且右下角提示登录成功
            self.Label_LoginMsg.setEnabled( False );
            self.Label_LoginMsg.setText( "" );
            self.ShowTrayMsg( Msg );
        elif optype == 1: #在登录页面显示错误信息
            self.Label_LoginMsg.setEnabled(True);
            pa = QPalette(self.Label_LoginMsg.palette());
            pa.setColor(QPalette.WindowText, QColor('red'));
            self.Label_LoginMsg.setPalette(pa);
            self.Label_LoginMsg.setText( Msg );

if __name__ == "__main__":
    app = QApplication( sys.argv );
    dialog = ShowMessage();
    dialog.show();
    app.exec_();
