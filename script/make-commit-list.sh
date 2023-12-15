#! /bin/bash
#===============================
#
# make-commit-list
#
# ex)
#	> cd ${LINUX}
#	> ${linux-bsp-stat}/script/make-commit-list.sh v6.1 v6.2
#	> ls ${linux-bsp-stat}/data
#	... v6.2
#
# 2023/12/13 Kuninori Morimoto <kuninori.morimoto.gx@renesas.com>
#===============================
TOP=`readlink -f "$0" | xargs dirname | xargs dirname`

FROM=$1
TO=$2

[ x${FROM} = x -o x${TO} = x ] && echo "need FROM and TO" && exit

TO_TXT=`echo "${TO}" | sed "s/\//-/g"`

git log --format=%H ${FROM}..${TO} > ${TOP}/data/${TO_TXT}
