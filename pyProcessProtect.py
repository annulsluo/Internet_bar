#-*- coding:utf-8 -*-
import sys, os, time;
import threading;
import psutil;
import win32process;
from PyQt4 import QtCore;

class ProcessProtect( QtCore.QThread ):
    def __init__( self, parent = None ):
        super( ProcessProtect, self ).__init__( parent );
        self.PidList = []; 
        self.Pid = 0;

    def InitPidInfo( self ):
        self.PidList = psutil.get_pid_list();
	
    def GetPidByTaskName( self, taskname ):
        self.Pid = 0;
        for pid in self.PidList:
            try:
                proc = psutil.Process( pid );
            except psutil.NoSuchProcess:
                continue;
            except psutil.AccessDenied:
                continue;
            except psutil.Error:
                continue;
            else:
                line = str(proc.name);
                if line.find( taskname ) != -1:
                    self.Pid = pid;

    def doProcessProtect( self ):
        dir = os.getcwd();
        exe = '%s\Monitor\pyMonitor.exe' % ( dir );
        cmdline = '%s %s' % ( exe, dir );
        while True:
            self.InitPidInfo();
            self.GetPidByTaskName( 'pyMonitor.exe' );
            if self.Pid == 0:
                win32process.CreateProcess( exe, cmdline, None, None, 0, win32process.CREATE_NO_WINDOW, None, None, win32process.STARTUPINFO() );
            time.sleep( 1 );
 
    def run( self ):
        self.doProcessProtect();

if __name__ == "__main__":
    PI = ProcessProtect();
    PI.doProcessProtect();
