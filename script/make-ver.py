#! /usr/bin/env python3
#===============================
#
# make-ver
#
#	create all v6.x version data
#
#		> make-ver.py 6
#		make data/v6.0
#		make data/v6.1
#		make data/v6.2
#		...
#
#	create all version data since v5.0
#
#		> make-ver.py
#		make data/v5.0
#		...
#		make data/v6.0
#		...
#
# 2023/12/20 Kuninori Morimoto <kuninori.morimoto.gx@renesas.com>
#===============================
import sys
import os
import lib

#===============================
# kernel_version
#===============================
class kernel_version (lib.base):
    __list = [
        None,	# v0.x	not supported
        None,	# v1.x	not supported
        None,	# v2.x	not supported
        None,	# v3.x	not supported
        20,	# v4.0 - v4.20
        19,	# v5.0 - v5.19
        8,	# v6.0 - v6.8
    ];

    #--------------------
    # make_ver()
    #--------------------
    def make_ver(self):
        for v in range(1, len(self.ver_list)):
            if (os.path.exists("{}/data/{}".format(self.top(), self.ver_list[v]))):
                continue

            print(self.run("{}/script/make-commit-list.sh {} {}".format(self.top(), self.ver_list[v - 1], self.ver_list[v])))

    #--------------------
    # make ver list2
    #--------------------
    def make_ver_list(self, ver):
        if (ver < 5 or
            ver >= len(kernel_version.__list)):
            return []

        prev_ver = kernel_version.__list[ ver - 1 ]
        last_ver = kernel_version.__list[ ver ]

        if (not prev_ver):
            return []

        list = ["v{}.{}".format(ver - 1, prev_ver)]
        for v in range(last_ver + 1):
            list.append("v{}.{}".format(ver, v))
        return list

    #--------------------
    # __init__()
    #--------------------
    def __init__(self, ver = None):

        lst = []
        self.ver_list = []

        if (ver):
            lst = self.make_ver_list(ver)
        else:
            for v in range(5, len(kernel_version.__list)):
                lst.extend(self.make_ver_list(v))

        if (len(lst)):
            # remove duplicate version
            self.ver_list = list(dict.fromkeys(lst))

#====================================
#
# As command
#
#====================================
if __name__=='__main__':
    ver = int(sys.argv[1]) if (len(sys.argv) > 1) else None

    kernel_version(ver).make_ver()
