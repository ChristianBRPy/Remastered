import sys, os, time, platform, glob

class newlexer():
	def __init__(self, *args, **kwargs):
		return None

	def readfile(self, filename):
		f = open(filename, 'r')
		fc = f.read()
		f.close()
		return fc+"\n"

	def Lex(self, fc):
		fc = list(fc)
		toks = []
		tok = ""
		strstate = 0
		string = ""
		editstate = 0
		editcode = ""
		commentstate = 0
		voidstate = 0
		voidname = ""
		voidcount = 0
		paramstate = 0
		param = ""
		varstate = 0
		varname = ""
		newconststate = 0
		conststate = 0
		constname = ""
		constcode = 0

		for char in fc:
			tok += char
			if tok == " ":
				if strstate == 1:
					string += tok
				elif editstate == 1:
					editcode += tok

				if varstate == 1:
					varstate = 0
					toks.append("VAR:"+varname)
					varname = ""

				tok = ""
			elif tok == "\n":
				if varstate == 1:
					varstate = 0
					toks.append("VAR:"+varname)
					varname = ""
				if editstate == 1:
					editcode += "\n"
				tok = ""
				commentstate = 0
			elif tok == "\t":
				tok = ""
			elif commentstate == 1:
				tok = ""
			elif tok.lower() == "new":
				toks.append("VARCONSTANT")
				tok = ""
				newconststate = 1
			elif tok.lower() == "const":
				toks.append("CONSTANT")
				tok = ""
				conststate = 1
			elif tok.lower() == "void":
				toks.append("VOID")
				tok = ""
				voidstate = 1
			elif tok.lower() == "@inc":
				toks.append("inc")
				tok = ""
			elif tok.lower() == "printscreen":
				toks.append("PRINTSCREEN")
				tok = ""
			elif tok[len(tok)-1] == "=":
				d = tok[0:len(tok)-1]
				if d[len(d)-1] == " ":
					d = tok[0:len(tok)-2]
				toks.append("SET")
				toks.append(d)
				tok = ""
			elif tok == "{":
				tok = ""
			elif tok == "}":
				if voidcount == 1:
					voidcount = 0
					toks.append("ENDVOID")
				elif constcode == 1:
					toks.append("CONSTEND")
					constcode = 0
				tok = ""
			elif tok == "(":
				if conststate == 1:
					conststate = 0
					constcode = 1
					toks.append("NAME:"+constname)
					constname = ""
				if voidstate == 1:
					toks.append("NAME:"+voidname)
					voidname = ""
				toks.append("STARTPARAMS")
				tok = ""
				paramstate = 1
			elif tok == ")":
				if param != "":
					toks.append(param)
					param = ""
				if voidstate == 1:
					voidstate = 0
					voidcount = 1
				if varstate == 1:
					varstate = 0
					toks.append("VAR:"+varname)
					varname = ""
				toks.append("ENDPARAMS")
				tok = ""
				paramstate = 0
			elif tok == "," and paramstate == 1 and voidstate == 1:
				if varstate == 1:
					varstate = 0
					toks.append("VAR:"+varname)
					varname = ""
				tok = ""
			elif varstate == 1:
				varname += tok
				tok = ""
			elif conststate == 1:
				constname += tok
				tok = ""
			# elif paramstate == 1 and voidstate == 1:
			# 	param += tok
			# 	tok = ""
			elif tok == "#":
				commentstate = 1
				tok = ""
			elif tok == "$":
				varstate = 1
				tok = ""
			elif tok == "\"":
				if strstate == 0:
					strstate = 1
				elif strstate == 1:
					strstate = 0
					toks.append("STRING:"+string)
					string = ""
				tok = ""
			elif strstate == 1:
				string += tok
				tok = ""
			elif voidstate == 1:
				voidname += tok
				tok = ""
			elif editstate == 1:
				if tok != ";" and tok != ":":
					editcode += tok
				tok = ""

		return toks