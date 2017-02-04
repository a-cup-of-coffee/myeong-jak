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
import datetime

import Initializer
import YinyangFiveElem
import Evaluater
import Suri
import RecommandName
import MySQLHelper

fp = open('./SAJU_API');
SAJU_API = fp.readline()
fp.close()

def makeQuery(qDict):
    query = ''
    for qKey, qValue in qDict.iteritems():
        query = '%s%s=%s&' % (query, qKey, qValue)
    return query

def getSaju(qDict):
    query = makeQuery(qDict)
    query = query.encode('utf-8')
    f = urllib.urlopen(SAJU_API + '?' + query)
    res = f.read()
    result = json.loads(res)
    return result

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

def getSajuElem(saju):
    result = saju['result']
    elemList = []
    elemList.extend(getOneju(result['y']))
    elemList.extend(getOneju(result['m']))
    elemList.extend(getOneju(result['d']))
    elemList.extend(getOneju(result['h']))
    return elemList

def getNameElem(fa, fi):
    elemList = []
    for char in (fa + fi):
        e = MySQLHelper.MySQLHelper().executeFetchoneSQL('SELECT jo FROM HanjaName WHERE HanjaName.character = "%s";' % (char))
        elem = chiToHan(e)
        elemList.append(elem)
    return elemList

def chiToHan(c):
    if c == u'火':
        return u'화'
    if c == u'水':
        return u'수'
    if c == u'木':
        return u'목'
    if c == u'金':
        return u'금'
    if c == u'土':
        return u'토'

def getOneju(oneju):
    return [oneju['ch']['han'], oneju['ji']['han']]

def makeElemDict(elemList):
    eDict = getInitElemDict()
    for elem in elemList:
        if elem in eDict:
            eDict[elem] += 1
    return eDict

def getInitElemDict():
    d = dict()
    d[u'화'] = 0
    d[u'수'] = 0
    d[u'목'] = 0
    d[u'금'] = 0
    d[u'토'] = 0
    return d

def getWeekElem(elemDict):
    tups = makeDictToTuples(elemDict)
    sortedTups = sorted(tups, key=lambda x:x[0])
    weekElemDeepList = map(lambda x: x[1], sortedTups)[0:2]
    weekElemChain = itertools.chain(*weekElemDeepList)
    return list(weekElemChain)

def makeDictToTuples(elemDict):
    rDict = getReverseDict(elemDict)
    tups = []
    for k in rDict.keys():
        tups.append((k, rDict[k]))
    return tups

def getReverseDict(elemDict):
    rDict = dict()
    for k, v in elemDict.iteritems():
        if v in rDict:
            rDict[v].append(k)
        else:
            rDict[v] = [k]
    return rDict

def tester(chance):
	koreanRange = xrange(ord(u'가'), ord(u'힣') + 1)
	for ch in koreanRange:
		if random.random() > chance:
			continue
		char = unichr(ch)
		a = getInitial(char)
		print char, ''.join(a), '\t', ''.join(getYinyangFiveElem(a))

def getInitial(char):
	ini = Initializer.Initializer()
	return ini.getInitial(char)

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

def korYinyang(qDict):
        fiveElem, fiveElemOnlyHead, yinyang = korParse(qDict)
	ev = Evaluater.Evaluater()
        d = dict()
        d['score'] = ev.evalYinyang(''.join(yinyang))
        d['result'] = ' '.join(yinyang)
        d['socre_max'] = 0
        d['socre_min'] = -3
        print json.dumps(d, ensure_ascii=False)

def korFiveElem(qDict):
        fiveElem, fiveElemOnlyHead, yinyang = korParse(qDict)
	ev = Evaluater.Evaluater()
	band = len(fiveElem)-1
        d = dict()
        d['score'] = ev.evalFiveElem(''.join(fiveElemOnlyHead))
        d['result'] = ' '.join(fiveElemOnlyHead)
	band = len(fiveElemOnlyHead)-1
        d['socre_max'] = band
        d['socre_min'] = -band
        print json.dumps(d, ensure_ascii=False)
        '''
	print '#발음오행'
        print '\t' + ' '.join(fiveElem)
        print '\t', ev.evalFiveElem(''.join(fiveElem)), '(', -band, '~', band, ', 초성종성 사용)'
        print '\t' + ' '.join(fiveElemOnlyHead)
	band = len(fiveElemOnlyHead)-1
	print '\t', ev.evalFiveElem(''.join(fiveElemOnlyHead)), '(', -band, '~', band, ', 초성만 사용)'
        '''

def chiNumFiveElem(qDict):
        familyName, firstName = extractHanjaNames(qDict)
        obj = Suri.Suri()
        fa, na = obj.getStrockCounts(familyName, firstName)
        childhood, youth, middleAge, total = obj.fourStatusSuri(fa, na)
        sfe = obj.suriFiveElem(childhood, youth, middleAge)
        ev = Evaluater.Evaluater()
        band = len(sfe)-1
        d = dict()
        d['score'] = ev.evalFiveElem(''.join(sfe))
        d['result'] = ' '.join(sfe)
        d['score_max'] = band
        d['score_min'] = -band
        print json.dumps(d, ensure_ascii=False)
        '''
        print '\t점수', ev.evalFiveElem(''.join(sfe)), '(', -band, '~', band, ')'
        syy = obj.suriYinyang(fa, na)
        print '\t점수', ev.evalYinyang(''.join(syy)), '(0 : very good / -1 : good / -2 : soso / -3 : bad)'
        '''
def chiNumFourStatus(qDict):
        familyName, firstName = extractHanjaNames(qDict)
        obj = Suri.Suri()
        fa, na = obj.getStrockCounts(familyName, firstName)
        childhood, youth, middleAge, total = obj.fourStatusSuri(fa, na)
        d = dict()
        s = dict()
        s['원격'] = childhood
        s['형격'] = youth
        s['이격'] = middleAge
        s['정격'] = total
        d['score'] = -1
        d['result'] = s
        d['score_max'] = -1
        d['score_min'] = -1
        print json.dumps(d, ensure_ascii=False)

def chiNumYinyang(qDict):
        familyName, firstName = extractHanjaNames(qDict)
        obj = Suri.Suri()
        fa, na = obj.getStrockCounts(familyName, firstName)
        syy = obj.suriYinyang(fa, na)
        ev = Evaluater.Evaluater()
        d = dict()
        d['score'] = ev.evalYinyang(''.join(syy))
        d['result'] = ' '.join(syy)
        d['score_max'] = 0
        d['score_min'] = -3
        print json.dumps(d, ensure_ascii=False)

def korSajuFiveElem(qDict):
        familyName, firstName = extractHanjaNames(qDict)
        nameElem = getNameElem('', firstName)
        print json.dumps(nameElem, ensure_ascii=False)
        saju = getSaju(qDict)
        sajuElem = getSajuElem(saju)
        nameElem.extend(sajuElem)
        elemDict = makeElemDict(nameElem)
        s = dict()
        for k, v in elemDict.iteritems():
            s[k] = v
        d = dict()
        d['score'] = -1
        d['result'] = s
        d['score_max'] = -1
        d['score_min'] = -1
        print json.dumps(d, ensure_ascii=False)
        '''
        print '\t부족한 오행'
        weekElem = getWeekElem(elemDict)[0:2]
        print '\t\t',
        for elem in weekElem:
            print elem,
        '''
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

def recommandName(qDict):
        familyName = qDict['familyNameHangul']
        familyNameHanja, firstNameHanja = extractHanjaNames(qDict)
        obj = Suri.Suri()
        fa, na = obj.getStrockCounts(familyNameHanja, firstNameHanja)
        familyCount = fa[0]
        goodCountSet = getGoodCountSet(familyCount)

        # 발음오행 기준으로 한글 후보생성
        rn = RecommandName.RecommandName()
        ev = Evaluater.Evaluater()
        fiveElem, fiveElemOnlyHead, yinyang = korParse(qDict)
        ssElemList = rn.getSangSaeng(fiveElemOnlyHead[0])
        recomNameList = []
        tempCnt = 0
        recomMax = 1
        for ss in ssElemList:
            nl = rn.getNameListForKor(ss)
            for name in nl:
                recom = dict()
                #chance = random.random()
                #if chance > 0.01:
                #   continue
                # white name filter
                '''
                isWhite = rn.isWhiteName(name)
                if isWhite == False:
                    continue
                '''
                candiNameDict = dict()
                candiNameDict['familyNameHangul'] = familyName
                candiNameDict['firstNameHangul'] = ''.join(name)
                fiveElem, fiveElemOnlyHead, yinyang = korParse(candiNameDict)
                # 발음오행
                feScore = ev.evalFiveElem(''.join(fiveElemOnlyHead))
                if feScore < 0:
                    continue
                recom['korFiveElem'] = feScore
                # 발음음양
                yyScore = ev.evalYinyang(''.join(yinyang))
                if yyScore == -3:
                    continue
                recom['korYinyang'] = yyScore
                # 81수리 기반으로 한자 후보생성
                hanjaNameList = getRecomHanjaNameList(familyCount, name, goodCountSet)
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
                    recom['chiNumYinyang'] = syScore
                    # 81 수리
                    childhood, youth, middleAge, total = obj.fourStatusSuri(fa, na)
                    chiNumFourStatus = dict()
                    chiNumFourStatus[u'원격'] = childhood
                    chiNumFourStatus[u'형격'] = youth
                    chiNumFourStatus[u'이격'] = middleAge
                    chiNumFourStatus[u'정격'] = total
                    recom['chiNumFourStatus'] = chiNumFourStatus
                    # 수리오행
                    sfe = obj.suriFiveElem(childhood, youth, middleAge)
                    sfScore = ev.evalFiveElem(''.join(sfe))
                    if sfScore  < 1:
                        continue
                    recom['chiNumFiveElem'] = sfScore
                    # 사주
                    # familyNameHanja, firstNameHanja
                    saju = getSaju(qDict)
                    sajuElem = getSajuElem(saju)
                    sajuElemDict = makeElemDict(sajuElem)
                    sajuElemStd = calStd(sajuElemDict)
                    nameElem = getNameElem('', firstNameHanja)
                    nameElemDict = makeElemDict(nameElem)
                    fullElemDict = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), [nameElemDict, sajuElemDict])
                    fullElemStd = calStd(fullElemDict)
                    if fullElemStd > sajuElemStd:
                        continue
                    recom = copy.deepcopy(recom)
                    recom['sajuElem'] = sajuElemDict
                    recom['nameElem'] = nameElemDict
                    recom['fullElem'] = fullElemDict
                    recom['firstNameHanja'] = firstNameHanja
                    recom['firstNameHangul'] = ''.join(name)
                    recomNameList.append(recom)
                    tempCnt = tempCnt + 1
                    if tempCnt > recomMax:
                        break
                if tempCnt > recomMax:
                    break
            if tempCnt > recomMax:
                break
        s = json.dumps(recomNameList, ensure_ascii=False)
        print 1
        print urllib.quote(s.encode('utf-8'))
        print s

def calStd(d):
        cnt = len(d)
        s = sum(d.values())
        avg = float(s) / float(cnt)
        var = sum(map(lambda x: math.pow(x - avg, 2) , d.values())) / cnt
        std = math.sqrt(var)
        return std
        
if __name__ == "__main__":
	#tester(0.001)
        if len(sys.argv) < 2:
                print 'input text'
                sys.exit()
        #text = u'{"gender":"male","location":"seoul","calendar":"solar","year":1987,"month":4,"day":30,"hour":7,"minute":15,"familyNameHanja":"李","firstNameHanja":"東炫","familyNameHangul":"이","firstNameHangul":"동현"}'
        #text = u'{"gender":"male","location":"seoul","calendar":"solar","year":1987,"month":4,"day":30,"hour":7,"minute":15,"familyNameHanja":"李","firstNameHanja":"瑙尹","familyNameHangul":"이","firstNameHangul":"노윤"}'
        text = u'{"gender":"male","location":"seoul","calendar":"solar","year":1987,"month":4,"day":30,"hour":7,"minute":15,"familyNameHanja":"李","familyNameHangul":"이"}'
        #text = unicode(sys.argv[1], 'UTF-8')
        op = u'recommand_name'
        #op = u'chi_num_five_elem'
        #op = unicode(sys.argv[1], 'UTF-8')
        #text = unicode(sys.argv[2], 'UTF-8')
        qDict = json.loads(text)

        if op == 'kor_five_elem':
            korFiveElem(qDict)
        elif op == 'kor_yinyang':
            korYinyang(qDict)
        elif op == 'chi_num_five_elem':
            chiNumFiveElem(qDict)
        elif op == 'chi_num_four_status':
            chiNumFourStatus(qDict)
        elif op == 'chi_num_yinyang':
            chiNumYinyang(qDict)
        elif op == 'kor_saju_five_elem':
            korSajuFiveElem(qDict) 
        elif op == 'recommand_name':
            recommandName(qDict)
