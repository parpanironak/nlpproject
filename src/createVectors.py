#!/usr/bin/env python2

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

def removeStopWords(text):
	return ' '.join([word for word in text.split() if word not in cachedStopWords])

def createCountMap(wordList):
    hmap = {};
    if not isinstance(wordList , list):
        return None
    for word in wordList:
        hmap[word] = hmap.get(word, 0) + 1.0
    count = 1.0*len(wordList) if len(wordList) > 1 else 1.0
    
    for word in hmap:
		hmap[word] = hmap.get(word,0)/count;
    
    return hmap


def createTermFrequencyVector(tag, entity, odir):
	entityFilePath = odir + "/corpus/" + tag + "/" + entity + ".txt"
	if(os.path.isfile(entityFilePath)):	
		pattern = re.compile(r"(?i)\[\[{0} \| {1}\]\]".format(entity, tag))
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


