# ================================================================
# Remastered Programming Language
# ---------------------------------------------------------------
# Remastered is a programming language made with python.
# Remastered is also a OO (Object Orientated) language and
# easy to use.
# ---------------------------------------------------------------
# Copyright 2017 Christian Barton Randall
# ================================================================

from sys import *
import os

# ================================================================

# ---------------------------------------------------------------
# Custom Functions
# ---------------------------------------------------------------

from functions import lexer, parser

# ================================================================

# ---------------------------------------------------------------
# Main
def main():
	Lexer = lexer.newlexer()
	Parser = parser.newparser()

	fn = argv[1]
	#print(fn)
	f = Lexer.readfile(fn)
	toks = Lexer.Lex(f)
	# print(toks)
	# print("\n\n")
	Parser.parse(toks)


if __name__ == '__main__':
	main()
# ---------------------------------------------------------------

# ================================================================