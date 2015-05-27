#-*- coding:utf-8 -*-
import sys,os, datetime, time;
import win32gui, win32api, win32con;
from ctypes import wintypes
import ctypes
from ctypes import *
from ctypes.wintypes import *
import pythoncom;
import win32con;
from PyQt4 import QtCore;
import platform;

LRESULT = c_long;
class KBDLLHOOKSTRUCT( Structure ):
    _fields_ = [
        ( 'vkCode', DWORD ),
        ( 'scanCode', DWORD ),
        ( 'flags', DWORD ),
        ( 'time', DWORD ),
        ( 'dwExtraInfo', DWORD ),
        ]
HOOKPROC = WINFUNCTYPE( LRESULT, c_int, WPARAM, LPARAM );
HC_ACTION = 0;

class HotKey( QtCore.QThread ):
    def __init( self, parent = None ):
        super( HotKey, self ).__init( parent );
        self.keyHookID = 0;
    
    def keyHookFunc( self, code, wParam, lParam ):
        if code != win32con.HC_ACTION:
            return ctypes.windll.user32.CallNextHookEx( 0, code, wParam, lParam );
        kbd = KBDLLHOOKSTRUCT.from_address( lParam );
        print( "key %d\n" % kbd.vkCode );
        if wParam == win32con.WM_KEYDOWN or wParam == win32con.WM_SYSKEYDOWN:
            '''
            hotkey = ( kbd.vkCode == win32con.VK_LWIN or kbd.vkCode == win32con.VK_RWIN ) or \
                (win32api.GetAsyncKeyState( win32con.VK_LWIN ) < 0 or win32api.GetAsyncKeyState( win32con.VK_RWIN ) < 0 ) and kbd.vkCode == win32con.VK_L )

            '''
            if (win32api.GetAsyncKeyState( win32con.VK_LWIN ) < 0 or win32api.GetAsyncKeyState( win32con.VK_RWIN ) < 0 ) and kbd.vkCode == win32con.VK_L:
                print ( "win+L\n" ); 
                return True;
            if kbd.vkCode == win32con.VK_LWIN or kbd.vkCode == win32con.VK_RWIN:
                print ( "hookfunc win\n" );
                return True;

            if kbd.flags & win32con.LLKHF_ALTDOWN:
                print( "hookfunc alt\n" );
                return True;

            if kbd.vkCode == win32con.VK_TAB and (kbd.flags & win32con.LLKHF_ALTDOWN ):
                print ( "hookfunc tab+alt\n" );
                return True;

            ctrl_pressed = win32api.GetKeyState( win32con.VK_CONTROL ) & 0x8000;
            if kbd.vkCode == win32con.VK_DELETE and ctrl_pressed and ( kbd.flags & win32con.LLKHF_ALTDOWN ):
                print ( "hookfunc ctrl+alt+del\n" );
                return True;

            if ctrl_pressed and ( kbd.flags & win32con.LLKHF_ALTDOWN ):
                print ( "hookfunc ctrl+alt\n" );
                return True;

            if kbd.vkCode == win32con.VK_ESCAPE and (kbd.flags & win32con.LLKHF_ALTDOWN):
                print ( "hookfunc alt+esc\n" );
                return True;

            if kbd.vkCode == win32con.VK_ESCAPE and ctrl_pressed:
                print ( "hookfunc ctrl+esc\n" );
                return True;
            if (kbd.vkCode == win32con.VK_LSHIFT or kbd.vkCode == win32con.VK_RSHIFT ) and ctrl_pressed: 
                print ( "hookfunc shift+ctrl\n" );
                return True;
            if kbd.vkCode == win32con.VK_ESCAPE:
                print ( "hookfunc esc\n" );
                return True;
            if ctrl_pressed:
                print ( "hookfunc ctrl\n" );
                return True;
        return ctypes.windll.user32.CallNextHookEx( 0, code, wParam, lParam );
        
    def HookFunc( self ):
        c_khook = HOOKPROC( self.keyHookFunc );
        splatform = platform.platform();
        hwnd = None;
        if splatform.find( "XP" ) != -1:
            hwnd = ctypes.windll.kernel32.GetModuleHandleW( None );
        elif splatform.find( "Windows-7" ) != -1:
            hwnd = 0;
        self.keyHookID = ctypes.windll.user32.SetWindowsHookExW( win32con.WH_KEYBOARD_LL, c_khook, hwnd, 0 ); # 为了兼容64位版本，把第三个参数给废除了
        if self.keyHookID == 0:
            print( "could not set hook\n" );
        win32gui.PumpMessages();
    
    def EndHook( self ):
        ctypes.windll.user32.UnhookWindowsHookEx( self.keyHookID );
        print( "could not unhook key hook %s\n" % self.keyHookID );
    
    def run( self ):
        self.keyHookID = 0;
        self.HookFunc();

if __name__ == "__main__":
    oHotKey = HotKey();
    oHotKey.HookFunc();
    

