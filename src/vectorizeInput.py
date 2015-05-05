#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, getopt
import os
reload(sys)
sys.setdefaultencoding('utf8')
import re


def getMatchObjects(pattern, line):
	lis = []
	
	m = re.search(pattern, line)
	while m != None:
		lis.append(m);
		m = re.search(pattern, line[m.end():])
		
	return lis
	
def ipclean(inputfilepath):
	
	with open(inputfilepath) as f:
		for line in f:
			if line.strip() != "=========================================" and line.strip() != "+++++++++++++++++++++++++++++++++++++++++":
				m = getMatchObjects(r'\[\[@@\s*\|(.*?)\]\]',line)
				for m1 in m:
					print line[m1.start():m1.end()]


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"i:",["ifile="])

    except getopt.GetoptError:
       print 'test.py -i <inputfile>'
       exit(1)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg

    if inputfile != '':
        ipclean(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
