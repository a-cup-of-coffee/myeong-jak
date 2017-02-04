#/usr/local/externs/bin/python
# encoding: utf-8

import random

class YinyangFiveElem:
	class __YinyangFiveElem:
		yfDict = None
		def __init__(self):
			self.yfDict = self.initYFDict()
		def initYFDict(self):
			# http://thoughts.chkwon.net/naming-children/
			# https://namu.wiki/w/%EB%AA%A8%EC%9D%8C%EC%A1%B0%ED%99%94#s-2
			hd = dict()
			hd[u'ㄱ'] = u'목'
			hd[u'ㄲ'] = u'목'
			hd[u'ㄴ'] = u'화'
			hd[u'ㄷ'] = u'화'
			hd[u'ㄸ'] = u'화'
			hd[u'ㄹ'] = u'화'
			hd[u'ㅁ'] = u'수'
			hd[u'ㅂ'] = u'수'
			hd[u'ㅃ'] = u'수'
			hd[u'ㅅ'] = u'금'
			hd[u'ㅆ'] = u'금'
			hd[u'ㅇ'] = u'토'
			hd[u'ㅈ'] = u'금'
			hd[u'ㅉ'] = u'금'
			hd[u'ㅊ'] = u'금'
			hd[u'ㅋ'] = u'목'
			hd[u'ㅌ'] = u'화'
			hd[u'ㅍ'] = u'수'
			hd[u'ㅎ'] = u'토'

			hd[u'ㅏ'] = u'양'
			hd[u'ㅐ'] = u'양'
			hd[u'ㅑ'] = u'양'
			hd[u'ㅒ'] = u'양'
			hd[u'ㅓ'] = u'음'
			hd[u'ㅔ'] = u'음'
			hd[u'ㅕ'] = u'음'
			hd[u'ㅖ'] = u'음'
			hd[u'ㅗ'] = u'양'
			hd[u'ㅘ'] = u'양'
			hd[u'ㅙ'] = u'양'
			hd[u'ㅚ'] = u'양'
			hd[u'ㅛ'] = u'양'
			hd[u'ㅜ'] = u'음'
			hd[u'ㅝ'] = u'음'
			hd[u'ㅞ'] = u'음'
			hd[u'ㅟ'] = u'음'
			hd[u'ㅠ'] = u'음'
			hd[u'ㅡ'] = u'음'
			hd[u'ㅢ'] = u'음'
			hd[u'ㅣ'] = u'중'
			return hd
		def getYinyangFiveElem(self, initialRow):
			yf = []
			for i in initialRow:
				yf.append(self.yfDict.get(i, i))
			return yf
	instance = None
	def __init__(self):
		if not YinyangFiveElem.instance:
			YinyangFiveElem.instance = YinyangFiveElem.__YinyangFiveElem()
	def __getattr__(self, name):
		return getattr(self.instance, name)

def tester(chance):
	yf = YinyangFiveElem()
	koreanRange = xrange(ord(u'ㄱ'), ord(u'ㅣ') + 1)
	for ch in koreanRange:
		if random.random() > chance:
			continue
		char = unichr(ch)
		print char, ''.join(yf.getYinyangFiveElem(char))

if __name__ == "__main__":
	tester(0.5)
