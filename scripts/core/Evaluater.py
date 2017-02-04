#/usr/local/externs/bin/python
# encoding: utf-8

import random

class Evaluater:
	class __Evaluater:
		fiveElemDict = None
		yinyangDict = None
		def __init__(self):
			self.fiveElemDict = self.initFiveElemDict()
			self.yinyangDict = self.initYinyangDict()

		def initFiveElemDict(self):
			fd = dict()
			fd[u'목수'] = 1
			fd[u'수금'] = 1
			fd[u'금토'] = 1
			fd[u'토화'] = 1
			fd[u'화목'] = 1
			fd[u'목금'] = -1
			fd[u'금화'] = -1
			fd[u'화수'] = -1
			fd[u'수토'] = -1
			fd[u'토목'] = -1
			return fd

		def initYinyangDict(self):
			yd = dict()
			yd[u'음'] = -1
			yd[u'양'] = 1
			return yd

		def evalFiveElem(self, text):
			score = 0
			for i in range(len(text) - 1):
				elem = text[i:i+2]
				score = score + self.fiveElemDict.get(elem, 0)
			return score

		def evalYinyang(self, text):
			score = 0
			for ch in text:
				score = score + self.yinyangDict.get(ch, 0)
			return -abs(score)

		def getEvaluater(self, initialRow):
			yf = []
			for i in initialRow:
				yf.append(self.yfDict.get(i, i))
			return yf

	instance = None
	def __init__(self):
		if not Evaluater.instance:
			Evaluater.instance = Evaluater.__Evaluater()
	def __getattr__(self, name):
		return getattr(self.instance, name)

if __name__ == "__main__":
	pass
