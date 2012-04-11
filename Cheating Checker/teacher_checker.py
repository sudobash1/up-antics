#!/usr/bin/python

import os, sys
import re


path = os.getcwd()
for name in os.listdir(path):
    
    if((re.match(".*\.py$",name)) and (name != "teacher_checker.py")):
        if(os.path.isfile(name)):
            file = open(name, "r")
            content = file.read()
            #string which imports Game
            s = "import Game"
            index = content.find(s)
            if (index != -1):
                print "Student has imported Game.py in", name 


