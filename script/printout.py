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
    # finish()
    #--------------------
    def finish(self):
        return
    #--------------------
    # print()
    #--------------------
    def print(self, bsp_subject, upstream_commit, from_kernel_ver):
        print("{:<9s} / {:<}".format(from_kernel_ver, bsp_subject))

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
    def print(self, bsp_subject, upstream_commit, from_kernel_ver):
        self.file.write("{:<9s} / {:<}\n".format(from_kernel_ver, bsp_subject))

#===============================
# printout html
#===============================
class html(lib.print_base):
    #--------------------
    # finish()
    #--------------------
    def finish(self):
        self.file.write("</table>\n")
        self.file.write("</html>\n")
        super().finish()

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
    def print(self, bsp_subject, upstream_commit, from_kernel_ver):
        self.file.write("<tr><td>{}</td><td>".format(from_kernel_ver))
        if (from_kernel_ver != "Local"):
            self.file.write("<a href=\"https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id={}\">{}</a>".format(upstream_commit, bsp_subject))
        else:
            self.file.write(bsp_subject)

        self.file.write("</td></tr>\n")
