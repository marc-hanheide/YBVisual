#!/usr/bin/env python

import readchar



class Keyboard:
    last_key = ''
    @staticmethod
    def IsKeyPressed(key):
        if(Keyboard.last_key==key):
            return True
        else:
            return False
    @staticmethod
    def CheckInput():
        char = readchar.readchar()
        print char
        Keyboard.last_key = char
