#! /usr/bin/env python3
#===============================
#
# linux
#
# 2023/12/12 Kuninori Morimoto <kuninori.morimoto.gx@renesas.com>
#===============================
import os
import re
import lib
import sys
import importlib
import yaml
import optparse

#===============================
# linux
#===============================
class linux (lib.base):
    #--------------------
    # git_subject
    #--------------------
    def git_subject(self, commit):
        return self.run("git -C {} log -1 --format=%s {}".format(self.linux_path, commit))

    #--------------------
    # cherry_pick_commit()
    #--------------------
    def cherry_pick_commit(self, commit):
        log = self.run("git -C {} log -1 {} | grep \"cherry picked from commit\"".format(self.linux_path, commit))
        m = re.search("cherry picked from commit ([0-f]+)", log)

        if (not m):
            return None

        return m.group(1)

    #--------------------
    # cherry_pick_from()
    #--------------------
    def cherry_pick_from(self, upstream_commit):
        if (not upstream_commit):
            return "Local"

        ret = self.run("cd {}/data; grep -l {} *".format(self.top, upstream_commit))
        if (not ret):
            ret = "Local"

        return ret

    #--------------------
    # __init__()
    #--------------------
    def __init__(self, linux_path, commit_to, commit_from = None):

        if (not os.path.exists(linux_path)):
            raise Exception("Linux not exist")

        self.linux_path		= linux_path
        self.top		= os.path.abspath("{}/..".format(os.path.dirname(__file__)))
        self.bsp_title		= commit_to.replace('/', '-')	# topic/bsp -> topic-bsp
        self.printout_way	= []

        if (not commit_from):
            ver_log = self.runl("git -C {} show {}:Makefile | head -n 4".format(linux_path, commit_to))
            commit_from = "v{}.{}.{}".format(ver_log[1].split(" = ")[1],
                                             ver_log[2].split(" = ")[1],
                                             ver_log[3].split(" = ")[1])

        self.bsp_commit_list = self.runl("git -C {} log --oneline --format=%H {}..{}".format(linux_path, commit_from, commit_to))

    #--------------------
    # add_print()
    #--------------------
    def add_print(self, way):
        if (way == "txt"):
            self.printout_way.append(importlib.import_module("printout").txt(self.bsp_title))
        if (way == "html"):
            self.printout_way.append(importlib.import_module("printout").html(self.bsp_title))
        if (way == "plane"):
            self.printout_way.append(importlib.import_module("printout").plane())

    #--------------------
    # printout
    #--------------------
    def printout(self):
        for bsp_commit in self.bsp_commit_list:
            upstream_commit	= self.cherry_pick_commit(bsp_commit)
            from_kernel_ver	= self.cherry_pick_from(upstream_commit)
            for way in self.printout_way:
                way.print(self.git_subject(bsp_commit), upstream_commit, from_kernel_ver)

#====================================
#
# As command
#
#====================================
if __name__=='__main__':

    parser = optparse.OptionParser()
    parser.add_option("-t", "--text", action="store_true", default=False, dest="text")
    parser.add_option("-H", "--html", action="store_true", default=False, dest="html")
    (options, args) = parser.parse_args()

    cwd = os.getcwd()

    # Linux dir should have...
    if (not os.path.exists("{}/.git".format(cwd))	or
        not os.path.exists("{}/Makefile".format(cwd))	or
        not os.path.exists("{}/Kbuild".format(cwd))	or
        not os.path.exists("{}/Kconfig".format(cwd))	or
        not os.path.exists("{}/MAINTAINERS".format(cwd))):
        sys.exit("You need to use this command from Linux dir")

    ver_from	= None
    ver_to	= None
    if (len(args) == 1):
        ver_to   = args[0]
    elif (len(args) == 2):
        ver_from = args[0]
        ver_to   = args[1]
    else:
        sys.exit("commit_from / commit_to are required")

    lx = linux("/home/morimoto/WORK/linux", ver_to, ver_from)

    cnt = 0
    if (options.text):
        lx.add_print("txt")
        cnt += 1
    if (options.html):
        lx.add_print("html")
        cnt += 1

    if (cnt == 0):
        lx.add_print("plane")

    lx.printout()
