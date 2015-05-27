#-*- encoding:utf-8 -*-
import sys,os
import configparser;

conf = configparser.ConfigParser();
conf.read( ".\internet_bar.conf" );

# Client Conf
gDir = conf.get( "Client", "dir" );
gUserInfoFile = "%s\%s" % ( gDir, conf.get( "Client", "userinfo" ) );

gUserId = None;
gToken = None;
if os.path.exists( gUserInfoFile ) == True:
    rf = open( gUserInfoFile, "r" );
    data = rf.readlines();
    if len( data ) > 0:
        gUserId = data[-1].strip();
    rf.close();

gTokenFile = "%s%s" % ( gDir, conf.get( "Client", "token" ) );
if os.path.exists( gTokenFile ) == True:
    rf = open( gTokenFile, "r" );
    data = rf.readlines();
    if len( data ) > 0:
        gToken = data[-1].strip();
    rf.close();


# Server Conf
gHost = conf.get( "Server", "host" );
gPort = conf.getint( "Server", "port" );
gIndex = conf.get( "Server", "index" );
gApi = conf.get( "Server", "api" );

