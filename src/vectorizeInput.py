#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, getopt
import os
reload(sys)
sys.setdefaultencoding('utf8')
import re
import nltk
import unicodedata
import string
import math

NLTK_DATA_DIR = "./nltk_data"
TEST_FILE = '/home/rap450/nlp/shellscripts'

try:
    os.environ['NLTK_DATA'] = NLTK_DATA_DIR
    import nltk.data
    try:
        nltk.data.find('stopwords')
    except LookupError:
        nltk.download('stopwords', download_dir = NLTK_DATA_DIR)
    from nltk.corpus import stopwords
except ImportError:
    sys.stderr.write("{0} depends on python {1} module. Run 'pip install {1}' from a shell.\n".format(sys.argv[0], "nltk"))
    exit(1)

#tags = ["Barcelona", "Chinese" "Dutch", "Finnish", "Greek", "Italian", "Latin", "Milan", "PST", "Public", "Scottish", "Swedish", "Turkish" ]
tags = ["Barcelona"]

cachedStopWords = stopwords.words("english")

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

table = string.maketrans("","")
def removePunctuations(s):
    return s.translate(table, string.punctuation)

def removeUPunctuations(text):
    print tbl
    return text.translate(tbl)


def removeStopWords(text):
	return ' '.join([word for word in text.split() if word not in cachedStopWords])

def getMatchObjects(pattern, line):
    lis = []
    m = re.search(pattern, line)
    while m != None:
        lis.append(m);
        line = line[m.end():]
        m = re.search(pattern, line)
        if m == None:
            return lis


    return lis

def readable_entities(text):
    return re.sub(r'\[\[\s*[^\[\]|]+\s*\|\s*([^\[\]|]+)\s*\]\]', r'\1', text)

def createCountMap(wordList):
    hmap = {};
    if not isinstance(wordList , list):
        return None
    maxcount = 1.0
    for word in wordList:
        hmap[word] = hmap.get(word, 0) + 1.0
        if maxcount < hmap[word]:
			maxcount = hmap[word]
    count = 1.0*len(wordList) if len(wordList) > 1 else 1.0

    for word in hmap:
		#hmap[word] = hmap.get(word,0)/count
		hmap[word] = hmap.get(word,0)/maxcount

    return hmap

def createVector(text):
    text = text.lower()
    text = readable_entities(text)
    text = removePunctuations(text)
    text = removeStopWords(text)
    return createCountMap(text.split())

def comapare(entityMap, sentvec):
	
	hmap = {}
	totalEntityCount = len(entityMap)
	maxval = 1.0
	for dim in sentvec:
		count = 0
		for entity in entityMap:
			if dim in entityMap[entity]:
				count = count + 1		
		hmap[dim] = math.log(1.0*totalEntityCount/count)
		maxval = hmap[dim] if hmap[dim] > maxval else maxval
		
	for dim in sentvec:
		hmap[dim] = hmap[dim] / maxval
	
	score = 0.0
	entitScoreMap = {}
	maxentity = None
	for entity in entityMap:
		for dim in sentvec:
			if dim in entityMap[entity]:
				score = score + sentvec[dim] * entityMap[entity][dim] * hmap[dim]
		entitScoreMap[entity] = score	
	
	maxentity = None
	for entity in entitScoreMap:
		if maxentity == None:
			maxentity = entity
		else:
			maxentity = entity if entitScoreMap[entity] > entitScoreMap[maxentity] else maxentity
			
	return maxentity
	
def disambiguate(inputfilepath, entitymap):
    with open(inputfilepath, "r") as f:
        for line in f:
            line = line.strip()
            if line != "=========================================" and line != "+++++++++++++++++++++++++++++++++++++++++":
                m = getMatchObjects(r'\[\[\s*@@\s*\|\s*(.*?)\s*\]\]',line)
                if(len(m) > 0):
                    end = 0
                    for m1 in m:
                        link = "" + line[end + m1.start(): end + m1.end()]
                        tag = m1.group(1).strip()
                        tag = tag[0:1].upper() + tag[1:].lower()
                        sent = ""+ line[0 : end + m1.start()] + " " + line[end + m1.end() :]
                        sentvec = createVector(sent.strip())
                        if tag in tags:
							print line
							print comapare(entitymap[tag], sentvec):
						else:
							print line
							print "cannot identify %s" % m1.group(0)
						print "========================================="
                        end = m1.end()
                else:
					print line
					print "No tags to disambiguate"
					print "========================================="
					
def loadEntiyVector(entity, tag, odir):
	
	fpath = odir + "/vectors/" + tag + "/" + entity.strip() + ".txt"
	hmap = {}
	with open(fpath, "r") as f:
		for line in f:				
			word, score = f.readLine().rstrip("\t", 2)
			socre = float(score)
			hmap[word] = score
			
	return hmap

def loadVectors(odir):
	
    hmap = {}
    for tag in tags:
		fpath = odir + "/tags/" + tag + ".txt"
		innerhmap = {}
		with open(fpath, "r") as f:
			for line in f:				
				entity = f.readLine().strip()
				innerhmap[entity] = loadEntiyVector(entity, odir)
			
		hmap[tag] = innerhmap 

	return hmap

def main(argv):
    inputfile = ''
    directory = ""
    try:
        opts, args = getopt.getopt(argv,"i:d:",["ifile=", "dir="])

    except getopt.GetoptError:
       print 'test.py -i <inputfile>'
       exit(1)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        if opt in ("-d", "--dir"):
            inputfile = arg

    if inputfile != '' and direcotry != "":
		hamp = loadVectors(odir):
        disambiguate(inputfile, hmap)

if __name__ == "__main__":
    main(sys.argv[1:])
