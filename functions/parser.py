from tkinter import *
from tkinter.filedialog import *
import importlib, os

functions = {}
constructors = {}

const_list = []
constfunctions = []

class newparser(object):
	def __init__(self):
		super(newparser, self).__init__()
	def makeRunLambda(self, num):
		return lambda params: newparser.voidparse(newparser, functions[num]["name"], functions[num]["function"], params, False, None)
	def makeConstRunLambda(self, const, num, name, constid):
		return lambda params: newparser.voidparse(newparser, name, num["function"], params, True, constfunctions[constid][name])
	def makeConstLambda(self, num):
		return lambda params: newparser.constparse(newparser, constructors[num]["function"], constructors[num]["name"], params)
	def printscreen(self, param, varchar):
		if param[0:3] == "INT":
			print(param[4:])
		elif param[0:3] == "VAR":
			self.printscreen(self, varchar[param[4:]], varchar)
		elif param[0:6] == "STRING":
			print(param[7:])
		elif param[0:7] == "BOOLEAN":
			print(param[8:])
	def include(self, pkg):
		if pkg[0:7] == "python_":
			importlib.import_module(pkg[8:])
			print(pkg[8:])
		# elif os.path.isfile(os.path.join(os.path.join(os.getcwd(), "lib"), pkg)):
		# 	self.import_rema(os.path.join(os.path.join(os.getcwd(), "lib"), pkg))
		# elif os.path.isfile(os.path.join(os.getcwd() pkg)):
		# 	self.import_rema(os.path.join(os.getcwd(), pkg))
	def parse(self, toks):
		i = 0
		varchar = {}
		global functions
		global const_list
		const_list = []
		while i<len(toks):
			if toks[i] == "PRINTSCREEN":
				params = 0
				paramlist = []
				if toks[i+1] == "STARTPARAMS":
					if toks[i+2] == "ENDPARAMS":
						void(0)
					else:
						while(toks[i+2+params] != "ENDPARAMS"):
							paramlist.append(toks[i+2+params])
							params += 1
						self.printscreen(paramlist[0])
				i+=3+params
			elif toks[i] == "INC":
				params = 0
				paramlist = []
				if toks[i+1] == "STARTPARAMS":
					if toks[i+2] == "ENDPARAMS":
						void(0)
					else:
						while(toks[i+2+params] != "ENDPARAMS"):
							paramlist.append(toks[i+2+params])
							params += 1
						self.include(paramlist[0])
				i+=3+params
			elif toks[i]+" "+toks[i+1][0:4] == "VOID NAME":
				functions[toks[i+1][5:]] = {}
				functions[toks[i+1][5:]]["name"] = toks[i+1][5:]
				functions[toks[i+1][5:]]["type"] = "void"
				functions[toks[i+1][5:]]["params"] = []
				functions[toks[i+1][5:]]["function"] = []

				params = 0

				if toks[i+2] == "STARTPARAMS":
					if toks[i+3] != "ENDPARAMS":
						while toks[i+3+params] != "ENDPARAMS":
							functions[toks[i+1][5:]]["params"].append(toks[i+3+params])

							params += 1

				codeblocks = 0

				while toks[i+4+params+codeblocks] != "ENDVOID":
					functions[toks[i+1][5:]]["function"].append(toks[i+4+params+codeblocks])					
					codeblocks += 1
					functions[toks[i+1][5:]]["runfunction"] = self.makeRunLambda(toks[i+1][5:])
				i += 4+params+codeblocks
			elif toks[i]+" "+toks[i+1][0:4] == "CONSTANT NAME":
				constructors[toks[i+1][5:]] = {}
				constructors[toks[i+1][5:]]["name"] = toks[i+1][5:]
				constructors[toks[i+1][5:]]["type"] = "const"
				constructors[toks[i+1][5:]]["params"] = []
				constructors[toks[i+1][5:]]["function"] = []
				constfunctions.append({"name":toks[i+1][5:]})
				nm = ""
				for letter in toks[i+1][5:]:
					nm += str(letter)
				#print(nm)
				const_list += [nm]

				params = 0

				if toks[i+2] == "STARTPARAMS":
					if toks[i+3] != "ENDPARAMS":
						while toks[i+3+params] != "ENDPARAMS":
							constructors[toks[i+1][5:]]["params"].append(toks[i+3+params])

							params += 1

				codeblocks = 0

				while toks[i+4+params+codeblocks] != "CONSTEND":
					constructors[toks[i+1][5:]]["function"].append(toks[i+4+params+codeblocks])					
					codeblocks += 1
					constructors[toks[i+1][5:]]["runfunction"] = self.makeConstLambda(toks[i+1][5:])
				i += 4+params+codeblocks
			i+=1
		#print(functions)

		#print(const_list)
		#print("\n")
		for constructor in const_list:
			#print(constructors[constructor])
			constructors[constructor]["runfunction"]([])
		i2 = 0
		#print(constfunctions)
		while i2 < len(constfunctions):
			constfunctions[i2][constfunctions[i2]["funcname"]]["runfunction"]([])
			i2 += 1
		functions['main']["runfunction"]([])
	def voidparse(self, name, toks, params, inConst, Const):
		#print(toks)
		i = 0
		q = -1
		varchar = {}
		global functions
		if not inConst:
			for param in functions[name]["params"]:
				q+=1
				param = param[4:]
				varchar[param] = params[q]
		else:
			for param in Const["params"]:
				q+=1
				param = param[4:]
				varchar[param] = params[q]
		while i<len(toks):
			#print(toks[i])
			if toks[i] == "PRINTSCREEN":
				params = 0
				paramlist = []
				if toks[i+1] == "STARTPARAMS":
					if toks[i+2] == "ENDPARAMS":
						void(0)
					else:
						while(toks[i+2+params] != "ENDPARAMS"):
							if toks[i+2+params] == "VARIABLE":
								paramlist.append(varchar[toks[i+3+params]])
								params += 2
							else:
								paramlist.append(toks[i+2+params])
								params += 1
						self.printscreen(self, paramlist[0], varchar)
				i+=2+params
			elif toks[i] == "SET":
				varchar[toks[i+1]] = toks[i+2]
			elif toks[i]+" "+toks[i+1][0:4] == "VOID NAME":
				funcparams = []
				paramnum = 0
				if toks[i+2] == "STARTPARAMS":
					if toks[i+3] != "ENDPARAMS":
						while toks[i+3+paramnum] != "ENDPARAMS":
							funcparams.append(toks[i+3+paramnum])
							paramnum += 1
					functions[toks[i+1][5:]]["runfunction"](funcparams)

				i += 3+paramnum
			i+=1
	def constparse(self, toks, cname, params):
		i = 0
		name = cname
		varchar = {}
		jq = 0
		for cf in constfunctions:
			if cf["name"] == name:
				func = jq
			jq += 1
		q = 0
		#print(toks)
		#print(constructors[name]["functions"])
		# for param in constructors[name]["params"]:
		# 	param = param[4:]
		#  	varchar[param] = params[q]
		#  	q+=1
		#print(str(len(toks)))
		while i<int(len(toks)):
			#print(toks[i])
			if toks[i] == "PRINTSCREEN":
				params = 0
				paramlist = []
				if toks[i+1] == "STARTPARAMS":
					if toks[i+2] == "ENDPARAMS":
						void(0)
					else:
						while(toks[i+2+params] != "ENDPARAMS"):
							paramlist.append(toks[i+2+params])
							params += 1
						self.printscreen(paramlist[0])
				i+=3+params
			elif toks[i]+" "+toks[i+1][0:4] == "VOID NAME":
				constfunctions[func][toks[i+1][5:]] = {}
				constfunctions[func]["funcname"] = toks[i+1][5:]
				constfunctions[func][toks[i+1][5:]]["name"] = toks[i+1][5:]
				constfunctions[func][toks[i+1][5:]]["type"] = "void"
				constfunctions[func][toks[i+1][5:]]["params"] = []
				constfunctions[func][toks[i+1][5:]]["function"] = []

				params = 0

				if toks[i+2] == "STARTPARAMS":
					if toks[i+3] != "ENDPARAMS":
						while toks[i+3+params] != "ENDPARAMS":
							constfunctions[func][toks[i+1][5:]]["params"].append(toks[i+3+params])

							params += 1

				codeblocks = 0

				while toks[i+4+params+codeblocks] != "ENDVOID":
					constfunctions[func][toks[i+1][5:]]["function"].append(toks[i+4+params+codeblocks])					
					codeblocks += 1
					constfunctions[func][toks[i+1][5:]]["runfunction"] = self.makeConstRunLambda(self, name, constfunctions[func][toks[i+1][5:]], toks[i+1][5:], func)
				i += 4+params+codeblocks
			i+=1