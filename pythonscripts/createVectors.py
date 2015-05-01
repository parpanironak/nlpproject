#!/usr/bin/python

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string
from nltk.corpus import stopwords

cachedStopWords = stopwords.words("english")
table = string.maketrans("","")

def removePunctuations(s):
    return s.translate(table, string.punctuation)

def removeStopWords(text)
	return ''.join([word for word in text.split() if word not in cachedStopWords])

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

def createTermFrequencyVector(tag, entity, odir):

	entityFilePath = odir + "/corpus/" + tag + "/" + entity + ".txt"
	if(os.path.isfile(entityFilePath)):	
		pattern = r"(?i)\[\[%s \\| %s\]\]" % entity, tag
		wordList = []	
		with open(entityFilePath) as entityFile:
			entityFileLine = entityFile.readline()
			if entityFileLine != "<doc>" and entityFileLine != "</doc>" :				
				tempList = re.split(pattern, entityFileLine)
				for temp in tempList:
					partialWordList = removeStopWords(removePunctuations(temp.strip())).split()
					wordList = wordList + [x.lower() for x in partialWordList]
		return createCountMap(wordList)
	
	else:
		return None
		
		
	 
print removeStopWords("ronak is strong");	
	
