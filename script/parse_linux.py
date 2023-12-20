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
        return self.run("git log -1 --format=%s {}".format(commit))

    #--------------------
    # cherry_pick_commit()
    #--------------------
    def cherry_pick_commit(self, commit):
        log = self.run("git log -1 {} | grep \"cherry picked from commit\"".format(commit))
        if (len(log)):
            m = re.search("cherry picked from commit ([0-f]+)", log)
            if (m):
                return m.group(1)

        log = self.run("git log -1 {} | grep \"commit [0-f]* upstream\.\"".format(commit))
        if (len(log)):
            m = re.search("commit ([0-f]+) upstream.", log)
            if (m):
                return m.group(1)

        log = self.run("git log -1 {} | grep \"Upstream commit:* [0-f]*\"".format(commit))
        if (len(log)):
            m = re.search("Upstream commit[:]? ([0-f]+)", log)
            if (m):
                return m.group(1)

        return None

    #--------------------
    # cherry_pick_from()
    #--------------------
    def cherry_pick_from(self, upstream_commit):
        if (not upstream_commit):
            return "Local"

        # Base kernel version
        f = self.commit_from.split(".")

        # Avoid old base kernel version
        #
        # ex)
        #	v6.8.12 BSP
        #	data/v6.1,
        #	data/v6.2, ...
        #
        ver_list_orig = self.runl("cd {}/data; ls".format(self.top))
        ver_list_tgt = []
        for ver in ver_list_orig:
            # ver  : v6.1	v6.3-rc2
            # v[0] : v6		v6
            # v[1] : 1		3-rc2
            v = ver.split(".")

            # FIXME
            #
            # We want to avoid below case too ?
            #
            # ex)
            #	v6.8.12 BSP
            #	data/v6.12,
            #	data/v6.13,
            #	...
            #	data/v7.xx

            if (v[0] > f[0] or
                ((v[0] == f[0] and v[1] > f[1]))):
                ver_list_tgt.append(ver)

        # check version via ver_list_tgt
        for ver in ver_list_tgt:
            ret = self.run("cd {}/data; grep -l {} {}".format(self.top, upstream_commit, ver))
            if (ret):
                return ret

        return "Local"

    #--------------------
    # __init__()
    #--------------------
    def __init__(self, commit_to, commit_from = None):

        self.top		= os.path.abspath("{}/..".format(os.path.dirname(__file__)))
        self.bsp_title		= commit_to.replace('/', '-')	# topic/bsp -> topic-bsp
        self.printout_way	= []

        if (not commit_from):
            ver_log = self.runl("git show {}:Makefile | head -n 4".format(commit_to))
            commit_from = "v{}.{}.{}".format(ver_log[1].split(" = ")[1],
                                             ver_log[2].split(" = ")[1],
                                             ver_log[3].split(" = ")[1])

        self.commit_from = commit_from
        self.bsp_commit_list = self.runl("git log --oneline --format=%H {}..{}".format(commit_from, commit_to))

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
    def printout(self, with_bsp_commit):
        for bsp_commit in self.bsp_commit_list:
            upstream_commit	= self.cherry_pick_commit(bsp_commit)
            from_kernel_ver	= self.cherry_pick_from(upstream_commit)
            for way in self.printout_way:
                way.print(self.git_subject(bsp_commit),
                          bsp_commit if (with_bsp_commit) else None,
                          upstream_commit, from_kernel_ver)

#====================================
#
# As command
#
#====================================
if __name__=='__main__':

    parser = optparse.OptionParser()
    parser.add_option("-t", "--text",	action="store_true", default=False, dest="text")
    parser.add_option("-H", "--html",	action="store_true", default=False, dest="html")
    parser.add_option("-p", "--plane",	action="store_true", default=False, dest="plane")
    parser.add_option("-b", "--bsp",	action="store_true", default=False, dest="bsp")
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

    lx = linux(ver_to, ver_from)

    cnt = 0
    if (options.text):
        lx.add_print("txt")
        cnt += 1
    if (options.html):
        lx.add_print("html")
        cnt += 1

    if (cnt == 0 or
        options.plane):
        lx.add_print("plane")

    lx.printout(options.bsp)
