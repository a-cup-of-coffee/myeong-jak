#/usr/local/externs/bin/python
# encoding: utf-8

import random
import sys
import json
import urllib
import itertools
import MySQLdb
import math
import copy
import time

import Initializer
import YinyangFiveElem
import Evaluater
import Suri
import RecommandName
import MySQLHelper

fp = open('./SAJU_API');
SAJU_API = fp.readline()
fp.close()

def getInitial(char):
    ini = Initializer.Initializer()
    return ini.getInitial(char)

def getGoodCount(familyCount, baseCount):
    tmp = baseCount - familyCount
    if tmp > 0:
        return str(tmp)
    return str(tmp + 81)

def getGoodCountSet(familyCount):
    gcl = MySQLHelper.MySQLHelper().executeSQL('SELECT num FROM 81suri WHERE score = 1;')
    gcl = map(lambda x:x[0], gcl)
    #gcl = map(lambda x:getGoodCount(familyCount, x[0]), gcl)
    gcSet = set(gcl)
    return gcSet

def getYinyangFiveElem(initial):
        yy = YinyangFiveElem.YinyangFiveElem()
        return yy.getYinyangFiveElem(initial)

def korParse(qDict):
    familyHangul, firstHangul = extractHangulNames(qDict)
    hangulName = familyHangul + firstHangul
    fiveElem = []
    fiveElemOnlyHead = []
    yinyang = []
    for char in hangulName:
            ini = getInitial(char)
            yy = getYinyangFiveElem(ini)
            fiveElem.append(yy[0])
            fiveElemOnlyHead.append(yy[0])
            yinyang.append(yy[1])
            if len(yy) > 2:
                    fiveElem.append(yy[2])
    return fiveElem, fiveElemOnlyHead, yinyang

def extractHanjaNames(qDict):
    family = ''
    k = 'familyNameHanja'
    if k in qDict:
        family = qDict[k]
        del qDict[k]
    k = 'firstNameHanja'
    first = ''
    if k in qDict:
        first = qDict[k]
        del qDict[k]
    return family, first

def extractHangulNames(qDict):
    family = ''
    k = 'familyNameHangul'
    if k in qDict:
        family = qDict[k]
        del qDict[k]
    k = 'firstNameHangul'
    first = ''
    if k in qDict:
        first = qDict[k]
        del qDict[k]
    return family, first

def getRecomHanjaNameList(familyCount, name, goodCountSet):
    hanjaNameList = []
    gcs = map(lambda x:getGoodCount(familyCount, x), goodCountSet)
    fst = MySQLHelper.MySQLHelper().executeSQL('SELECT HanjaName.character, HanjaName.hs FROM HanjaName WHERE u1 = "%s" AND hs IN ("%s");' % (name[0], '","'.join(gcs)))
    snd = MySQLHelper.MySQLHelper().executeSQL('SELECT HanjaName.character, HanjaName.hs FROM HanjaName WHERE u1 = "%s" AND hs IN ("%s");' % (name[1], '","'.join(gcs)))
    if len(fst) < 1 or len(snd) < 1:
        return hanjaNameList
    for f in fst:
        for s in snd:
            if f[1] + s[1] in goodCountSet:
                hanjaNameList.append(unicode(f[0] + s[0], 'utf-8'))
    return hanjaNameList
    #print json.dumps(fst, ensure_ascii=False)

if __name__ == "__main__":
    print time.ctime(time.time())
    result = MySQLHelper.MySQLHelper().executeSQL('TRUNCATE TABLE NameCandidate;')
    ev = Evaluater.Evaluater()
    yy = YinyangFiveElem.YinyangFiveElem()
    result = MySQLHelper.MySQLHelper().xecuteSQL('SELECT familyname, familyname_hanja FROM FamilyName;')
    familyList = map(lambda x: [unicode(x[0], 'utf-8'), unicode(x[1], 'utf-8')], result) 
    result = MySQLHelper.MySQLHelper().executeSQL('SELECT DISTINCT first1, first2 FROM WhiteName;')
    hangulList = map(lambda x: [unicode(x[0], 'utf-8'), unicode(x[1], 'utf-8')], result)
    for idx, fl in enumerate(familyList):
        familyName = fl[0]
        print idx, '/', len(familyList), time.ctime(time.time())
        familyNameHanja = fl[1]
        obj = Suri.Suri()
        fa, na = obj.getStrockCounts(familyNameHanja, "")
        familyCount = fa[0]
        goodCountSet = getGoodCountSet(familyCount)
        for hl in hangulList:
            if len(hl) < 2 or len(''.join(hl)) < 2:
                continue
            candiNameDict = dict()
            candiNameDict['familyNameHangul'] = familyName
            candiNameDict['firstNameHangul'] = ''.join(hl)
            fiveElem, fiveElemOnlyHead, yinyang = korParse(candiNameDict)
            # 발음오행
            feScore = ev.evalFiveElem(''.join(fiveElemOnlyHead))
            if feScore < 0:
                continue
            #recom['korFiveElem'] = feScore
            # 발음음양
            yyScore = ev.evalYinyang(''.join(yinyang))
            if yyScore == -3:
                continue
            #recom['korYinyang'] = yyScore
            # 81수리 기반으로 한자 후보생성
            hanjaNameList = getRecomHanjaNameList(familyCount, ''.join(hl), goodCountSet)
            if len(hanjaNameList) < 1:
                continue
            for firstNameHanja in hanjaNameList:
                obj = Suri.Suri()
                fa, na = obj.getStrockCounts(familyNameHanja, firstNameHanja)
                # 수리음양
                syy = obj.suriYinyang(fa, na)
                ev = Evaluater.Evaluater()
                syScore = ev.evalYinyang(''.join(syy))
                if syScore == -3:
                    continue
                #recom['chiNumYinyang'] = syScore
                # 81 수리
                childhood, youth, middleAge, total = obj.fourStatusSuri(fa, na)
                fs = [childhood, youth, middleAge, total]
                fs = map(lambda x: str(x), fs)
                #chiNumFourStatus = dict()
                #chiNumFourStatus[u'원격'] = childhood
                #chiNumFourStatus[u'형격'] = youth
                #chiNumFourStatus[u'이격'] = middleAge
                #chiNumFourStatus[u'정격'] = total
                #recom['chiNumFourStatus'] = chiNumFourStatus
                # 수리오행
                sfe = obj.suriFiveElem(childhood, youth, middleAge)
                sfScore = ev.evalFiveElem(''.join(sfe))
                if sfScore  < 1:
                    continue
                #recom['chiNumFiveElem'] = sfScore
                sql = 'INSERT INTO NameCandidate (familyNameHanja, firstNameHanja, familyNameHangul, firstNameHangul, korFiveElem, korYinyang, chiNumFiveElem, chiNumFourStatus, chiNumYinyang) VALUES ("%s", "%s", "%s", "%s", %d, %d, %d, "%s", %d);' % (familyNameHanja, firstNameHanja, familyName, "".join(hl), feScore, yyScore, sfScore, ",".join(fs), syScore)
                result = MySQLHelper.MySQLHelper().executeSQL(sql)
