#-*- coding:utf-8 -*-
import sys,os, datetime, time;
import global_var
import threading
from PyQt4 import QtCore;
import psutil;

class TaskList(QtCore.QThread):
    def __init__( self, parent = None ):
        super(TaskList, self).__init__(parent);
        self.PidList = []; 
        self.Pid = 0;

    def InitTaskList( self ):
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
                #print (line);
                if line.find( taskname ) != -1:
                    self.Pid = pid;
                            
    def KillByPid( self, pid ):
        if self.Pid != 0:
            try:
                proc = psutil.Process( pid );
                proc.kill();
            except psutil.NoSuchProcess:
                return;
            except psutil.AccessDenied:
                return;
            except psutil.Error:
                return;		

    def doKillTaskMgr( self ):
        while True:
            self.InitTaskList();
            self.GetPidByTaskName( 'taskmgr.exe' );
            if self.Pid != 0:
                #print( 'kill pid:', self.Pid );
                self.KillByPid( self.Pid );
            time.sleep(0.01);
    
    def run(self):
        self.doKillTaskMgr( );

if __name__ == "__main__":
    oTM = TaskList();
    oThread = threading.Thread( target = oTM.doKillTaskMgr(), name = "killtaskmgr" );
    oThread.setDaemon( True );
    oThread.start();
    #TM.GetPidByTaskName( 'taskmgr.exe' );
    print( 'pid:', TM.Pid );
                    
                    
