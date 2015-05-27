#-*- encoding:utf-8 -*-
import urllib.request;
import urllib.error;
import json;
import socket;
import sys, os, datetime, time;
import global_var;
from pyShowMessage import ShowMessage;
from PyQt4 import QtCore;

class HeartCheck(QtCore.QThread):
    def __init__( self, ID_Card, Pass, aSysTray, aToken, parent = None ):
        super(HeartCheck, self).__init__(parent);
        self.Host = global_var.gHost;
        self.Port = global_var.gPort;
        self.Index = global_var.gIndex;
        self.Api = global_var.gApi;
        #self.ID_Card = global_var.gUserId;
        self.ID_Card = ID_Card;
        print ( "id_car: ", ID_Card );
        print ("pass: ", Pass );
        self.Pass = Pass;
        self.LocalIp = socket.gethostbyname( socket.gethostname() );
        self.Token = aToken; #
        self.SysTray = aSysTray;
        #self.Signal = aSignal;
        
        self.quest = "%s:%d/%s/%s?ip=%s&op=check&userid=%s&pass=%s&token=%s" % ( self.Host, self.Port, self.Index, self.Api, self.LocalIp, self.ID_Card, self.Pass, self.Token );
        #print self.quest;

    def doHeartCheck(self):
        testcnt = 0;
        while True:
            print ("HeartCheck quest: ", self.quest);
            try:
                res = urllib.request.urlopen( self.quest, timeout = 5 );
            except urllib.error.URLError as e:
                if isinstance( e.reason, socket.timeout ):
                    pass;
            except urllib.error.HTTPError as e:
                print (e.code);
            else:
                res = res.read().decode( 'UTF-8' );
                resdata = json.loads( res );
                resUserId = resdata['userid'];
                bLock = resdata['lock'];
                bShowTips = resdata[ 'showtips' ];
                Pos = resdata[ 'pos' ];
                Msg = resdata[ 'msg' ];
                if bLock == True:
                 #   if gUserId == resUserId:
                    print ("Heart Check lock");
                    self.emit( QtCore.SIGNAL( 'showdialog' ) );
                if bShowTips == True:
                    SM = ShowMessage( self.SysTray );
                    SM.ShowTrayMsg( Msg );
            time.sleep( 30 );

    def run(self):
        self.doHeartCheck();

if __name__ == "__main__":
    HC = HeartCheck();
    HC.doHeartCheck();
