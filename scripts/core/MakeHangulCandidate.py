#/usr/local/externs/bin/python
# encoding: utf-8

import MySQLHelper
import Initializer
import Evaluater
import YinyangFiveElem

def getInitial(char):
        ini = Initializer.Initializer()
        return ini.getInitial(char)

def getYinyangFiveElem(initial):
        yy = YinyangFiveElem.YinyangFiveElem()
        return yy.getYinyangFiveElem(initial)

obj = MySQLHelper.MySQLHelper()
ev = Evaluater.Evaluater()
result = obj.executeSQL('SELECT DISTINCT u1 FROM HanjaName ORDER BY u1 ASC;')
hangulList = map(lambda x: unicode(x[0], 'utf-8'), result)
cnt = 0
for first in hangulList:
    fIni = getInitial(first)
    if len(fIni) < 2:
        continue
    fElem = getYinyangFiveElem(fIni)
    for last in hangulList:
        lIni = getInitial(last)
        if len(lIni) < 2:
            continue
        lElem = getYinyangFiveElem(lIni)
        score = ev.evalFiveElem(fElem[0] + lElem[0])
        if score > 0:
            print first, last, fIni[0], lIni[0], fElem[0], lElem[0], score
            cnt = cnt + 1
print cnt
