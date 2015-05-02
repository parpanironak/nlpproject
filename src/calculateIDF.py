#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string


INPUT_DATA_DIR = "./corpus_data"
OUTPUT_DATA_DIR = "./tagger_data"
NLTK_DATA_DIR = "./nltk_data"
NLTK_CORPUS_DIR = "./nltk_corpus"

try:
    os.environ['NLTK_DATA'] = NLTK_DATA_DIR
    import nltk.data
    from nltk.corpus import stopwords
except ImportError:
    sys.stderr.write("{0} depends on python {1} module. Run 'pip install {1}' from a shell.\n".format(sys.argv[0], "nltk"))
    exit(1)



cachedStopWords = stopwords.words("english")
table = string.maketrans("","")

def removePunctuations(s):
    return s.translate(table, string.punctuation)

def removeStopWords(text):
	return ' '.join([word for word in text.split() if word not in cachedStopWords])

def getRawTextFromXMLDocTag(absFilePath):
	print 
	if os.path.isfile(absFilePath) and absFilePath.endswith(".xml"):
		e = ET.parse(absFilePath).getroot()
		if e.tag == "doc":
			return e.text
		else:
			print "no doc tag"
			return None
	else:
		print "doesnotexit"
		return None

def extract_sentences(rawText):
    try:
        nltk.data.find('tokenizers/punkt.zip')
    except LookupError:
        nltk.download('punkt', download_dir = NLTK_DATA_DIR)
    
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        
    tokenized_text = tokenizer.tokenize(rawText)
    sentences = []
    for textblob in tokenized_text:
        sentences.extend(textblob.split('\n\n'))
    return sentences

def documentWordSet(sentList):	
	if not isinstance(sentList , list):
		return None
        
	pattern = re.compile(r"\[\[[^\[\]]*? \| ([^\[\]]*?)\]\]")
	wordList = set()	
	for entityFileLine in sentList:			
		tempLine = pattern.sub(r"\1", entityFileLine)
		partialWordList = removeStopWords(removePunctuations(tempLine.strip())).split()
		wordList = wordList | set([x.lower() for x in partialWordList])
	return wordList
	


def calculateIDF(ipDirectory):
	hmap = {}
	for i in os.listdir(ipDirectory):
		if i.endswith(".xml"): 
			absFilePath = ipDirectory + "/" + i
			rawXMLText = getRawTextFromXMLDocTag(absFilePath)
			docWordSet = documentWordSet(extract_sentences(str(rawXMLText)))
			for docWord in docWordSet:
				hmap[docWord] = hmap.get(docWord,0) + 1		
		else:
			continue

	return hmap

print calculateIDF("/home/rap450/nlp/shellscripts")

