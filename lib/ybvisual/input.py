#!/usr/bin/env python

#import readchar
import curses
import os


#Keyboard class
class Keyboard:
    window = None
    last_key = ''
    @staticmethod
    def IsKeyPressed(key):
        if(Keyboard.last_key==ord(str(key))):
            return True
        else:
            return False
    @staticmethod
    def CheckInput():
        #We need to use the curses library        
        Keyboard.window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        Keyboard.window.keypad(1)
        Keyboard.window.addstr(0,0,"Keyboard active - checking for user input",curses.A_REVERSE)
        key = Keyboard.window.getch()
        print key
        Keyboard.last_key = key
        os.system('clear')
        Keyboard.window.erase()
        Keyboard.window.refresh()
    @staticmethod
    def Restore():
        curses.nocbreak()
        Keyboard.window.keypad(0)
        curses.echo()
        curses.endwin()
        #Finally - clear the terminal
        os.system('clear')
        