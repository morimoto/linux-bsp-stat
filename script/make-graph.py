#! /usr/bin/env python3
#===============================
#
# make-graph
#
# 2023/12/13 Kuninori Morimoto <kuninori.morimoto.gx@renesas.com>
#===============================
import lib
import sys
import os

#===============================
# make_graph
#===============================
class make_graph (lib.base):

    #--------------------
    # __init__()
    #--------------------
    def __init__(self, file_array):

        pdf_name = "graph.pdf"

        if (os.path.exists(pdf_name)):
            sys.exit("You alreay have {}".format(pdf_name))

        tmp = ""
        for file in file_array:
            if (not file.endswith(".txt")):
                sys.exit("It needs xxx.txt".format(file))

            if (not os.path.exists(file)):
                sys.exit("{} is not exist".format(file))
            tmp += " {}".format(file)

        ver_array = self.runl("cat {} | cut -d \"/\" -f 1 | sort | uniq | sed 's/ *$//'".format(tmp))

        # we want to have...
        #	Local		v6.2
        #	v6.2	->	v6.3
        #	v6.3		v6.4
        #	v6.4		Local
        if ("Local" in ver_array):
            ver_array.remove("Local")
            ver_array.append("Local")

        dir = "/tmp/make-graph-{}".format(os.getpid())
        self.run("mkdir {}".format(dir))

        # create object files
        for ver in ver_array:
            for file in file_array:
                num = self.run("grep {} {} | wc -l".format(ver, file))
                self.run("echo \"{} {}\" >> {}/{}".format(file, num, dir, ver))

        # create gnuplot file
        with open("{}/gnuplot".format(dir), mode='w') as f:
            f.write("set terminal pdf size 20cm,12cm\n"\
                    "set output \"{}\"\n"\
                    "set title \"patch statistic\"\n"\
                    "set offset 0, 2, 1, 0\n"\
                    "set style data histograms\n"\
                    "set style histogram rowstacked\n"\
                    "set style fill solid border rgb \"black\"\n"\
                    "set grid y\n"\
                    "set boxwidth 0.5\n"\
                    "set xtics rotate by -20\n"\
                    "set key bottom outside\n"\
                    "\n"
                    "plot \\\n".format(pdf_name))

            for ver in ver_array:
                f.write("\"{}/{}\"	using 2:xticlabels(1) title \"{}\",\\\n".format(dir, ver, ver))


        # make graph
        self.run("gnuplot {}/gnuplot".format(dir))

        # remove work dir
        self.run("rm -fr {}".format(dir))

#====================================
#
# As command
#
#====================================
if __name__=='__main__':

    # remote command name
    sys.argv.pop(0)

    make_graph(sys.argv)
