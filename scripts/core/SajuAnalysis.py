#/usr/local/externs/bin/python
# encoding: utf-8

import sys
import json
import urllib
import itertools
import MySQLdb

import Suri
import Evaluater
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
    f = urllib.urlopen(SAJU_API + '?' + query)
    res = f.read()
    result = json.loads(res)
    return result

def extractNames(qDict):
    family = ''
    k = 'familyName'
    if k in qDict:
        family = qDict[k]
        del qDict[k]
    k = 'firstName'
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
        e = MySQLHelper.MySQLHelper().executeSQL('SELECT jo FROM HanjaName WHERE HanjaName.character = "%s";' % (char))
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
            print 'input text'
            sys.exit()
    text = u'{"gender":"male","location":"seoul","calendar":"solar","year":1987,"month":4,"day":30,"hour":7,"minute":15,"familyName":"李","firstName":"東炫"}'
    #text = unicode(sys.argv[1], 'UTF-8')
    qDict = json.loads(text)

    # 사주오행
    familyName, firstName = extractNames(qDict)
    nameElem = getNameElem('', firstName)
    saju = getSaju(qDict)
    sajuElem = getSajuElem(saju)
    nameElem.extend(sajuElem)
    elemDict = makeElemDict(nameElem)
    print '#사주오행'
    print '오행분포'
    s = '{'
    for k, v in elemDict.iteritems():
        s = s + '"%s":%d,' % (k, v)
    s = s[:-1] + '}'
    print s
    print
    print '부족한 오행'
    weekElem = getWeekElem(elemDict)[0:2]
    for elem in weekElem:
        print elem,
    print
    print

    # 수리오행
    obj = Suri.Suri()
    fa, na = obj.getStrockCounts(familyName, firstName)
    childhood, youth, middleAge, total = obj.fourStatusSuri(fa, na)
    sfe = obj.suriFiveElem(childhood, youth, middleAge)
    ev = Evaluater.Evaluater()
    band = len(sfe)-1
    print '수리오행 점수', ev.evalFiveElem(''.join(sfe)), '(', -band, '~', band, ')'
    print
    syy = obj.suriYinyang(fa, na)
    print '수리음양 점수', ev.evalYinyang(''.join(syy)), '(0 : very good / -1 : good / -2 : soso / -3 : bad)'
    #query = 'SELECT u1 FROM HanjaName WHERE element = "' + weekElem[0] + '" LIMIT 1;'
    #executeSQL(query)
