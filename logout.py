#-*- encoding:utf-8 -*-
import urllib.request;
import urllib.error;
import json;
import socket;
import sys, os, datetime, time;
import global_var;

class Logout():
    def __init__( self, Pass ):
        self.Host = global_var.gHost;
        self.Port = global_var.gPort;
        self.Index = global_var.gIndex;
        self.Api = global_var.gApi;
        self.ID_Card = global_var.gUserid;
        self.Pass = Pass;
        self.LocalIp = socket.gethostbyname( socket.gethostname() );
        self.Token = global_var.gToken; # 
        
        self.quest = "%s:%d/%s/%s?ip=%s&op=logout&userid=%s&pass=%s&token=%s" % ( self.Host, self.Port, self.Index, self.Api, self.LocalIp, self.ID_Card, self.Pass, self.Token );
        #
    def doLogout():
        try:
            res = urllib.request.urlopen( self.quest, timeout = 5 );
        except rllib.error.URLError, e:
            if isinstance( e.reason, socket.timeout ):
                pass;
        except urllib.error.HTTPError, e:
            print (e.code);
        else:
            res = res.read().decode( 'UTF-8' );
            resdata = json.loads( res );
            resUserId = resdata['userid'];
            bLogout = resdata['logout'];
            if bLogout == True:
                pass;
                #if gUserId = resUserId:
                    #TODO LockScreen

if __name__ == "__main__":
    ologout = Logout();
    


