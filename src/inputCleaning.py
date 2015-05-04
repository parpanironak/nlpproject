#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, getopt
import os
reload(sys)  
sys.setdefaultencoding('utf8')
import re
try:
    import config
except ImportError:
    sys.stderr.write("Error: missing file utils.py\n")
    exit(1)
    
try:
    os.environ['NLTK_DATA'] = config.NLTK_DATA_DIR
    import nltk.data
except ImportError:
    sys.stderr.write("{0} depends on python {1} module. Run 'pip install {1}' from a shell.\n".format(sys.argv[0], "nltk"))
    exit(1)
    
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

from inputExtractPages import clean

def ipclean(inputfile):
	text = ""
	with open(inputfile, "r") as tf:
		for line in tf:
			line = clean(line)
			tokenized_text = tokenizer.tokenize(line)
			print '\n=========================================\n'.join(tokenized_text)
			print '+++++++++++++++++++++++++++++++++++++++++'

def main(argv):

   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"i:",["ifile="])

   except getopt.GetoptError:
      print 'test.py -i <inputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         inputfile = arg

   if inputfile != '':
		ipclean(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
