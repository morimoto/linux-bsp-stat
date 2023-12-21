#! /usr/bin/env python3
#===============================
#
# lib
#
# 2023/12/12 Kuninori Morimoto <kuninori.morimoto.gx@renesas.com>
#===============================
import os
import re
import subprocess

#===============================
# print_base
#===============================
class print_base:
    #--------------------
    # __del__()
    #--------------------
    def __del__(self):
        self.file.close()

    #--------------------
    # __init__()
    #--------------------
    def __init__(self, bsp_title, suffix):
        self.file = open("{}.{}".format(bsp_title, suffix), "w", encoding="UTF-8")

#===============================
# base
#===============================
class base:
    __top = os.path.abspath("{}/..".format(os.path.dirname(__file__)))

    #--------------------
    # top
    #--------------------
    def top(self):
        return base.__top

    #--------------------
    # chomp
    #--------------------
    def chomp(self, text):
        return re.sub(r"\n$", r"", text);

    #--------------------
    # tolist()
    #--------------------
    def tolist(self, string):
        if (len(string) > 0):
            return string.split('\n');

        return [];

    #--------------------
    # run2()
    #
    # run command and get result as plane text
    #--------------------
    def run2(self, command):

        # Ughhhh
        # I don't like python external command !!
        # (ノ `Д´)ノ  go away !!
        child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = child.communicate()

        return self.chomp(stdout.decode("utf-8")), child.returncode;

    #--------------------
    # run()
    #--------------------
    def run(self, command):
        return self.run2(command)[0]

    #--------------------
    # run1()
    #
    # run command and get result as list
    #--------------------
    def runl(self, command):

        # call run() and exchange result as array
        #
        # "xxxxxxx
        #  yyyyyyy
        #  zzzzzzz"
        # ->
        # ["xxxxxxx",
        #  "yyyyyyy",
        #  "zzzzzzz"]
        return self.tolist(self.run(command));

