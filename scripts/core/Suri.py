#/usr/local/externs/bin/python
# encoding: utf-8

import sys
import MySQLHelper
import Evaluater

class Suri:
	suriElem = None
	def __init__(self):
		self.suriElem = dict()
		self.suriElem[1] = u'목'
		self.suriElem[2] = u'목'
		self.suriElem[3] = u'화'
		self.suriElem[4] = u'화'
		self.suriElem[5] = u'토'
		self.suriElem[6] = u'토'
		self.suriElem[7] = u'금'
		self.suriElem[8] = u'금'
		self.suriElem[9] = u'수'
		self.suriElem[0] = u'수'
		
	def getSC(self, char):
		obj = MySQLHelper.MySQLHelper()
		result = obj.executeSQL('SELECT count FROM HanjaName WHERE HanjaName.character = "' + char + '";')
		if len(result) > 0:
			return result[0][0]
		return None
	def getStrockCounts(self, family, name):
		fa = []
		na = []
		for t in family:
			fa.append(self.getSC(t))
		for t in name:
			na.append(self.getSC(t))
		return fa, na
	def fourStatusSuri(self, familySC, nameSC):
		family = reduce(lambda x, y: x + y, familySC)
		childhood = self.getSuri([nameSC[0], nameSC[-1]])
		youth = self.getSuri([family, nameSC[0]])
		middleAge = self.getSuri([family, nameSC[-1]])
		total = self.getSuri([family, nameSC[0], nameSC[-1]])
                '''
		print '#사격수리'
		print '\t성 획수', familySC, '이름 획수', nameSC
		print '\t원격(초년운)', childhood	
		print '\t형격(청년운)', youth	
		print '\t이격(장년운)', middleAge
		print '\t정격(전체운)', total
                '''
		return childhood, youth, middleAge, total
	def suriFiveElem(self, childhood, youth, middleAge):
		mid = middleAge % 10
		you = youth % 10
		chi = childhood % 10
                '''
		print '#수리오행'
		print '\t이격', mid, '형격', you, '원격', chi
		print '\t', self.suriElem[mid], self.suriElem[you], self.suriElem[chi]
                '''
		return [self.suriElem[mid], self.suriElem[you], self.suriElem[chi]]
	def suriYinyang(self, familySC, nameSC):
		syy = []
		for sc in familySC + nameSC:
			if sc % 2 == 0:
				syy.append(u'음')
			else:
				syy.append(u'양')
                '''
		print '#수리음양'
		print '\t' + ' '.join(syy)
                '''
		return syy
	def getSuri(self, strockCounts):
		return reduce(lambda x, y: x+ y, strockCounts)
		
if __name__ == '__main__':
	if len(sys.argv) < 3:
                print 'input text'
                sys.exit()
        family = unicode(sys.argv[1], 'UTF-8')
        name = unicode(sys.argv[2], 'UTF-8')
	
	print '0'
	obj = Suri()
	fa, na = obj.getStrockCounts(family, name)
	childhood, youth, middleAge, total = obj.fourStatusSuri(fa, na)
	sfe = obj.suriFiveElem(childhood, youth, middleAge)
	ev = Evaluater.Evaluater()
	band = len(sfe)-1
	print '수리오행 점수', ev.evalFiveElem(''.join(sfe)), '(', -band, '~', band, ')'
	print 
	syy = obj.suriYinyang(fa, na)
	print '수리음양 점수', ev.evalYinyang(''.join(syy)), '(0 : very good / -1 : good / -2 : soso / -3 : bad)'
	
