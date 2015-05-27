#-*- encoding:utf-8 -*- 
from PyQt4.QtGui import *;
from PyQt4.QtCore import *;
from PyQt4.Qt import *;
from PyQt4 import QtCore, QtGui;
from login import Ui_Dialog;
import sys,os,datetime,time
import socket
import urllib.request;
import urllib.error;
import json
import re
from pyShowMessage import ShowMessage;
from threading import Thread
from pyHeartCheck import HeartCheck;
import global_var;
from pyTaskList import TaskList;
from multiprocessing import Process;
from pyHotKey import *;
from pyProcessProtect import *;
#import qrc_test;

class LoginDlg( QDialog, Ui_Dialog ):
    def __init__( self, parent = None ):
        super( LoginDlg, self ).__init__( parent );
        self.setupUi( self );
        #self.Label_LoginMsg.setEnabled(True);

        # 初始化属性值
        self.Host = global_var.gHost; 
        self.Port = global_var.gPort;
        self.Index = global_var.gIndex;
        self.Api = global_var.gApi;
        self.ID_Card = None;
        self.Pass = None;
        self.Token = None;
        self.LocalIp = socket.gethostbyname( socket.gethostname() );
 
        # 设置对话框没有菜单栏
        self.setWindowState( QtCore.Qt.WindowFullScreen );

		# 设置icon
        self.SysTray = QtGui.QSystemTrayIcon(self);
        self.SysTray.setToolTip( "internet_bar" );
        self.Internet_bar_icon = QtGui.QIcon( "internet_bar.png" );
        self.SysTray.setIcon( self.Internet_bar_icon );

        QObject.connect( self.pushButton_sure, SIGNAL( "clicked()" ), self.clickLogin );
        
        # 创建后台线程，实时去杀掉任务管理器的调用
        self.oTTL = TaskList();
        self.oTTL.start();
        self.oTHC = None;
        self.LastHC = None;
        
        # 创建后台线程，处理捕捉热键事件
        self.oHotKey = HotKey();
        self.oHotKey.start();

        self.oPP = ProcessProtect();
        self.oPP.start();
	
    # 创建托盘菜单
    def CreateMenu( self ):
        self.LOAction = QtGui.QAction( "下机", self );
        self.connect( self.LOAction, SIGNAL( "triggered()"), self.LogOut );
        #self.connect( self.QAction, SIGNAL( "triggered()" ), QtGui.qApp.quit );
        self.CBAction = QtGui.QAction( "查询余额" , self );
        self.connect( self.CBAction, SIGNAL( "triggered()" ), self.CheckBalance );
        self.TrayIconMenu = QtGui.QMenu( self );
        self.TrayIconMenu.addAction( self.LOAction );
        self.TrayIconMenu.addAction( self.CBAction );
        self.SysTray.setContextMenu( self.TrayIconMenu );

    def connect_slot( self, heartcheck ):
        self.connect( heartcheck, QtCore.SIGNAL( 'showdialog' ), self.ShowDialog );
        self.LastHC = heartcheck;

    def LogOut( self ):
        quest = "%s:%d/%s/%s?ip=%s&op=logout&userid=%s&pass=%s&token=%s" % ( self.Host, self.Port, self.Index, self.Api, self.LocalIp, self.ID_Card, self.Pass, self.Token );
        print ("quest:", quest );
        self.ShowDialog( u" " )
        try:
            res = urllib.request.urlopen( quest, timeout = 4 );
        except urllib.error.URLError as e:
            if isinstance( e.reason, socket.timeout ):
                pass;
        except urllib.error.HTTPError as e:
            print( e.code );
        else:
            res = res.read().decode( 'UTF-8' );
            resdata = json.loads( res );
            error = resdata[ 'error' ];
            #关闭心跳检测
            self.oTHC.terminate();
            # 消除菜单按钮
            self.TrayIconMenu.clear();
            #if error == 0:
                #self.ShowDialog( u" " )
				

    def CheckBalance( self ):
        quest = "%s:%d/%s/%s?ip=%s&op=check_balance&userid=%s&pass=%s&token=%s" % ( self.Host, self.Port, self.Index, self.Api, self.LocalIp, self.ID_Card, self.Pass, self.Token );
        print ("quest:", quest );
        try:
            res = urllib.request.urlopen( quest, timeout = 4 );
        except urllib.error.URLError as e:
            if isinstance( e.reason, socket.timeout ):
                pass;
        except urllib.error.HTTPError as e:
            print( e.code );
        else:
            res = res.read().decode( 'UTF-8' );
            resdata = json.loads( res );
            #balance = resdata[ 'balance']; 
            #sMsg = u"还剩%s余额" % balance; 
            Msg = resdata[ 'msg' ];
            error = resdata[ 'error' ];
            if error == 0:
                SM = ShowMessage(self.SysTray,self.Label_LoginMsg);
                SM.ShowTrayMsg( Msg );

    # 锁屏
    def ShowDialog( self, Msg = u"已锁屏幕，请重新登陆" ):
        self.LineEdit_ID_Card.setText( "" );
        self.LineEdit_Pass.setText( "" );
        SM = ShowMessage(self.SysTray, self.Label_LoginMsg);
        SM.ShowLoginDlgMsg( Msg, optype = 1 );
        self.show();
        self.oHotKey = HotKey();
        self.oHotKey.start();
    '''
    def keyPressEvent( self, event ):
        if int(event.modifiers()) == (Qt.ControlModifier+Qt.ShiftModifier):
            return;
        if event.key() == QtCore.Qt.Key_Escape:
            return;
    '''
        
    def clickLogin( self ):
        self.ID_Card = str( self.LineEdit_ID_Card.text() ).strip()
        self.Pass = str( self.LineEdit_Pass.text() ).strip();
        quest = "%s:%d/%s/%s?ip=%s&op=login&userid=%s&pass=%s" % ( self.Host, self.Port, self.Index, self.Api, self.LocalIp, self.ID_Card, self.Pass );
        print ("quest:", quest );
        
        try:
            res = urllib.request.urlopen( quest, timeout = 4 );
        except urllib.error.URLError as e:
            if isinstance( e.reason, socket.timeout ):
                pass;
                # donothing
        except urllib.error.HTTPError as e:
            print (e.code);
        else:
            print ("return");
            res = res.read().decode( 'UTF-8' );
            resdata = json.loads( res );
            resUserId = resdata['userid'];
            bLogin = resdata['logout'];
            error = resdata[ 'error' ];
            msg = resdata[ 'msg' ];
            self.Token = resdata[ 'token' ];
            if error == 0: 
                # 窗口隐藏起来
                self.hide();
                self.CreateMenu();
                self.SysTray.show();

                # 在托盘显示登录成功
                SM = ShowMessage(self.SysTray,self.Label_LoginMsg);
                SM.ShowLoginDlgMsg( Msg = msg, optype = 0 );

                # 写重要信息到本地磁盘
                wf = open( global_var.gUserInfoFile, "a+" );
                wf.write( self.ID_Card );
                wf.write( '\n' );
                wf.close();
                wf = open( global_var.gTokenFile, "a+" );
                if self.Token != None:
                    wf.write( self.Token );
                    wf.write( '\n' );
                wf.close();
                # 登录成功后，关闭热键捕捉
                self.oHotKey.EndHook();
                self.oHotKey.terminate();
                # 余额查询
                time.sleep(2);
                self.CheckBalance();

                # 创建线程，进行心跳检测
                print ("begin heartcheck" );
                if self.LastHC != None:
                    print ( "LastHC no none id:", self.LastHC.ID_Card );
                    self.LastHC.terminate();
                self.oTHC = HeartCheck( self.ID_Card, self.Pass, self.SysTray, self.Token );
                self.connect_slot( self.oTHC );
                self.oTHC.start();

            #TODO 在登录窗口显示密码错误信息
            else:
                SM = ShowMessage(self.SysTray, self.Label_LoginMsg);
                SM.ShowLoginDlgMsg( Msg = msg, optype = 1 );

if __name__ == "__main__":
    app = QApplication( sys.argv );
    dialog = LoginDlg();
    dialog.show();
    app.exec_();

