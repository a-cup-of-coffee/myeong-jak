#/usr/local/externs/bin/python
# encoding: utf-8

import random

class Initializer:
	class __Initializer:
		charDict = None
		jamoDict = None
		def __init__(self):
			self.charDict = self.initCharToHangulJamo()
			self.jamoDict = self.initHangulJamoToHangulCompatibilityJamo()
		def initCharToHangulJamo(self):
			# https://en.wikipedia.org/wiki/Hangul_Jamo_(Unicode_block)
			cd = dict()
			koreanRange = xrange(ord(u'가'), ord(u'힣') + 1)
			for char in koreanRange:
				head = (char - 0xAC00) / (21 * 28) + 0x1100
				body = ((char - 0xAC00) / 28) % 21 + 0x1161
				tail = (char - 0xAC00) % 28 + 0x11A7 
				cd[unichr(char)] = [head, body, tail]
			return cd
		def initHangulJamoToHangulCompatibilityJamo(self):
			# https://en.wikipedia.org/wiki/Hangul_Compatibility_Jamo
			jd = dict()
			# head
			jd[0x1100] = unichr(0x3131)
			jd[0x1101] = unichr(0x3132)
			jd[0x1102] = unichr(0x3134)
			jd[0x1103] = unichr(0x3137)
			jd[0x1104] = unichr(0x3138)
			jd[0x1105] = unichr(0x3139)
			jd[0x1106] = unichr(0x3141)
			jd[0x1107] = unichr(0x3142)
			jd[0x1108] = unichr(0x3143)
			jd[0x1109] = unichr(0x3145)
			jd[0x110A] = unichr(0x3146)
			jd[0x110B] = unichr(0x3147)
			jd[0x110C] = unichr(0x3148)
			jd[0x110D] = unichr(0x3149)
			jd[0x110E] = unichr(0x314A)
			jd[0x110F] = unichr(0x314B)
			jd[0x1110] = unichr(0x314C)
			jd[0x1111] = unichr(0x314D)
			jd[0x1112] = unichr(0x314E)
			# body
			jd[0x1161] = unichr(0x314F)
			jd[0x1162] = unichr(0x3150)
			jd[0x1163] = unichr(0x3151)
			jd[0x1164] = unichr(0x3152)
			jd[0x1165] = unichr(0x3153)
			jd[0x1166] = unichr(0x3154)
			jd[0x1167] = unichr(0x3155)
			jd[0x1168] = unichr(0x3156)
			jd[0x1169] = unichr(0x3157)
			jd[0x116A] = unichr(0x3158)
			jd[0x116B] = unichr(0x3159)
			jd[0x116C] = unichr(0x315A)
			jd[0x116D] = unichr(0x315B)
			jd[0x116E] = unichr(0x315C)
			jd[0x116F] = unichr(0x315D)
			jd[0x1170] = unichr(0x315E)
			jd[0x1171] = unichr(0x315F)
			jd[0x1172] = unichr(0x3160)
			jd[0x1173] = unichr(0x3161)
			jd[0x1174] = unichr(0x3162)
			jd[0x1175] = unichr(0x3163)
			# tail
			jd[0x11A7] = ''
			jd[0x11A8] = unichr(0x3131)
			jd[0x11A9] = unichr(0x3132)
			jd[0x11AA] = unichr(0x3133)
			jd[0x11AB] = unichr(0x3134)
			jd[0x11AC] = unichr(0x3135)
			jd[0x11AD] = unichr(0x3136)
			jd[0x11AE] = unichr(0x3137)
			jd[0x11AF] = unichr(0x3139)
			jd[0x11B0] = unichr(0x313A)
			jd[0x11B1] = unichr(0x313B)
			jd[0x11B2] = unichr(0x313C)
			jd[0x11B3] = unichr(0x313D)
			jd[0x11B4] = unichr(0x313E)
			jd[0x11B5] = unichr(0x313F)
			jd[0x11B6] = unichr(0x3140)
			jd[0x11B7] = unichr(0x3141)
			jd[0x11B8] = unichr(0x3142)
			jd[0x11B9] = unichr(0x3144)
			jd[0x11BA] = unichr(0x3145)
			jd[0x11BB] = unichr(0x3146)
			jd[0x11BC] = unichr(0x3147)
			jd[0x11BD] = unichr(0x3148)
			jd[0x11BE] = unichr(0x314A)
			jd[0x11BF] = unichr(0x314B)
			jd[0x11C0] = unichr(0x314C)
			jd[0x11C1] = unichr(0x314D)
			jd[0x11C2] = unichr(0x314E)
			return jd
		def getInitial(self, uni_char):
			initial = []
			c = self.charDict.get(uni_char, uni_char)
			for ci in c:
				i = self.jamoDict.get(ci, uni_char)
				initial.append(i)
			return initial

	instance = None
	def __init__(self):
		if not Initializer.instance:
			Initializer.instance = Initializer.__Initializer()
	def __getattr__(self, name):
		return getattr(self.instance, name)

def tester(chance):
	ini = Initializer()
	koreanRange = xrange(ord(u'가'), ord(u'힣') + 1)
	for ch in koreanRange:
		if random.random() > chance:
			continue
		char = unichr(ch)
		a = ini.getInitial(char)
		print char, ''.join(a)

if __name__ == "__main__":
	tester(0.001)
