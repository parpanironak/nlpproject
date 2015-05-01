#!/usr/bin/python

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string

table = string.maketrans("","")

def removePunctuations(s):
    return s.translate(table, string.punctuation)

def createCountMap(wordList):
	hmap = {};
	if not isinstance(word , list)
		return None
		ema
	for word in wordList:
		if hamp.has_key(word):
			hmap[word] = hmap[word] + 1
		else:
			hmap[word] = 1
			
	return hmap

def methodd(tag, entity, odir):
	
	termFrequencyVector = {}
	pattern = r"(?i)\[\[%s \\| %s\]\]" % entity, tag
	entityFilePath = odir + "/corpus/" + tag + "/" + entity + ".txt"
	if(os.path.isfile(entityFilePath)):	
		wordList = []	
		with open(entityFilePath) as entityFile:
			entityFileLine = entityFile.readline()
			if entityFileLine == "<doc>" or entityFileLine == "</doc>" :
				
				tempList = re.split(pattern, entityFileLine)
				for temp in tempList:
					partialWordList = removePunctuations(temp.strip()).split()
					wordList = wordList + [x.lower() for x in partialWordList]
		
		
		
	 
	
	
