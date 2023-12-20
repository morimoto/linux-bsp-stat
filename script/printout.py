#! /usr/bin/env python3
#===============================
#
# printout
#
# 2023/12/12 Kuninori Morimoto <kuninori.morimoto.gx@renesas.com>
#===============================
import lib

#===============================
# printout plane
#===============================
class plane:
    #--------------------
    # print()
    #--------------------
    def print(self, bsp_subject, bsp_commit, upstream_commit, from_kernel_ver):
        print("{:<9s} / ".format(from_kernel_ver), end="")
        if (bsp_commit):
            print("{} / ".format(bsp_commit), end="")
        print("{:<}".format(bsp_subject))

#===============================
# printout txt
#===============================
class txt(lib.print_base):
    #--------------------
    # __init__()
    #--------------------
    def __init__(self, bsp_title):
        super().__init__(bsp_title, "txt")

    #--------------------
    # print()
    #--------------------
    def print(self, bsp_subject, bsp_commit, upstream_commit, from_kernel_ver):
        self.file.write("{:<9s} / ".format(from_kernel_ver))
        if (bsp_commit):
            self.file.write("{} / ".format(bsp_commit))
        self.file.write("{:<}\n".format(bsp_subject))


#===============================
# printout html
#===============================
class html(lib.print_base):
    #--------------------
    # __del__()
    #--------------------
    def __del__(self):
        self.file.write("</table>\n")
        self.file.write("</html>\n")
        super().__del__()

    #--------------------
    # __init__()
    #--------------------
    def __init__(self, bsp_title):
        super().__init__(bsp_title, "html")
        self.file.write("<html>\n")
        self.file.write("<table  border=\"1\">\n")
    #--------------------
    # print()
    #--------------------
    def print(self, bsp_subject, bsp_commit, upstream_commit, from_kernel_ver):
        self.file.write("<tr><td>{}</td><td>".format(from_kernel_ver))
        if (bsp_commit):
            self.file.write("{}</td><td>".format(bsp_commit))
        if (from_kernel_ver == "Local"):
            self.file.write(bsp_subject)
        else:
                self.file.write("<a href=\"https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id={}\">{}</a>".format(upstream_commit, bsp_subject))
        self.file.write("</td></tr>\n")
