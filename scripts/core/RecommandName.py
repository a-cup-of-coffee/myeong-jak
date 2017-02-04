#/usr/local/externs/bin/python
# encoding: utf-8

import random
import json

import MySQLHelper
import Initializer
import Evaluater
import YinyangFiveElem

class RecommandName:
	class __RecommandName:
                sangSaengDict = None
                fiveElemToInitDict = None
                allNameDict = None

		def __init__(self):
			self.sangSaengDict = self.initSangSaengDict()
			self.fiveElemToInitDict = self.initFiveElemToInitDict()
                        self.allNameDict = self.initAllNameDict()

                def initSangSaengDict(self):
                        sd = dict()
                        sd[u'화'] = [u'목', u'화', u'금', u'토']
                        sd[u'수'] = [u'금', u'화', u'수', u'목']
                        sd[u'목'] = [u'수', u'화', u'수', u'토']
                        sd[u'금'] = [u'토', u'수', u'목', u'금']
                        sd[u'토'] = [u'화', u'화', u'수', u'금']
                        return sd

                def initFiveElemToInitDict(self):
                        fd = dict()
                        fd[u'화'] = [u'ㄴ', u'ㄷ', u'ㄹ', u'ㅌ']
                        fd[u'수'] = [u'ㅁ', u'ㅂ', u'ㅍ']
                        fd[u'목'] = [u'ㄱ', u'ㅋ']
                        fd[u'금'] = [u'ㅅ', u'ㅈ', u'ㅊ']
                        fd[u'토'] = [u'ㅇ', u'ㅎ']
                        return fd

                def initAllNameDict(self):
			ad = dict()
			ad[u'화'] = []
			ad[u'수'] = []
			ad[u'목'] = []
			ad[u'금'] = []
			ad[u'토'] = []
			obj = MySQLHelper.MySQLHelper()
			ev = Evaluater.Evaluater()
                        '''
			result = obj.executeSQL('SELECT DISTINCT u1 FROM HanjaName ORDER BY u1 ASC;')
			hangulList = map(lambda x: unicode(x[0], 'utf-8'), result)
			cnt = 0
			for first in hangulList:
			    fIni = self.getInitial(first)
			    if len(fIni) < 2:
				continue
			    fElem = self.getYinyangFiveElem(fIni)
			    for last in hangulList:
				lIni = self.getInitial(last)
				if len(lIni) < 2:
				    continue
				lElem = self.getYinyangFiveElem(lIni)
				score = ev.evalFiveElem(fElem[0] + lElem[0])
				if score > -1:
				    ad[fElem[0]].append([first, last])
				    #print first, last, fIni[0], lIni[0], fElem[0], lElem[0], score
				    cnt = cnt + 1
			#print json.dumps(self.allNameDict, ensure_ascii=False)
			return ad
                        '''
			result = obj.executeSQL('SELECT DISTINCT first1, first2 FROM WhiteName ORDER BY rand();')
			hangulList = map(lambda x: [unicode(x[0], 'utf-8'), unicode(x[1], 'utf-8')], result)
                        for name in hangulList:
                            fIni = self.getInitial(name[0])
                            if len(fIni) < 2:
                                continue
                            fElem = self.getYinyangFiveElem(fIni)
                            lIni = self.getInitial(name[1])
                            if len(lIni) < 2:
                                continue
                            lElem = self.getYinyangFiveElem(lIni)
                            score = ev.evalFiveElem(fElem[0] + lElem[0])
                            if score > -1:
                                ad[fElem[0]].append(name)
                        return ad
                        

                def isWhiteName(self, name):
                    obj = MySQLHelper.MySQLHelper()
                    result = obj.executeSQL('SELECT count(*) FROM WhiteName WHERE first1="%s" && first2="%s" LIMIT 1;' % (name[0], name[1]))
                    if result[0][0] > 0:
                        return True
                    return False

		def getNameListForKor(self, fiveElem):
			if fiveElem in self.allNameDict:
				return self.allNameDict[fiveElem]
			return []
                        
		def getInitial(self, char):
			ini = Initializer.Initializer()
			return ini.getInitial(char)

		def getYinyangFiveElem(self, initial):
			yy = YinyangFiveElem.YinyangFiveElem()
			return yy.getYinyangFiveElem(initial)

                def getSangSaeng(self, char):
                        if char in self.sangSaengDict:
                            return self.sangSaengDict[char]
                        return []

                def convertFiveElemToInit(self, char):
                        if char in self.fiveElemToInitDict:
                                return self.fiveElemToInitDict[char]
                        return []

	instance = None
	def __init__(self):
		if not RecommandName.instance:
			RecommandName.instance = RecommandName.__RecommandName()
	def __getattr__(self, name):
		return getattr(self.instance, name)

if __name__ == "__main__":
	tester(0.5)
