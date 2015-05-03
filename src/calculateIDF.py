#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string
import math

import unicodedata
import sys



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

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

def removeUPunctuations(text):
    return text.translate(tbl)


cachedStopWords = stopwords.words("english")
table = string.maketrans("","")

#def removePunctuations(s):
#    return s.translate(table, string.punctuation)


def removeStopWords(text):
    return ' '.join([word for word in text.split() if word not in cachedStopWords])


def getRawTextFromXMLDocTag(absFilePath):
    if os.path.isfile(absFilePath) and absFilePath.endswith(".xml"):
		try:
#			e = ET.parse(absFilePath).getroot()
#			if e.tag == "doc":
#				return e.text
#			else:
#				print "no doc tag"
#				return None
			xmldoc = u'';
			flag = True
			with codecs.open(absFilePath ,'r', encoding='utf-8',errors='replace') as document:
				for line in document:
					if flag and (re.match(r'<doc.*?>',line.strip()) is not None):
						flag = False
					elif not flag and not line.strip() == "</doc>":
						xmldoc += u'\n'
						xmldoc += line
					elif not flag and line.strip() == "</doc>":
						flag = True;
			
			return xmldoc						
		except  Exception,e: 
			f = open("error.txt" , "a")
			f.write(str(absFilePath))
			f.write("\n")
			f.write(str(e))
			f.write("\n")
			f.close()
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
    if not isinstance(sentList, list):
        return []
    pattern = re.compile(r"\[\[\s*([^\[\]|]+)\s*\|\s*([^\[\]|]+)\s*\]\]")
    wordList = set()
    for entityFileLine in sentList:
        tempLine = pattern.sub(r"\1", entityFileLine)
        partialWordList = removeStopWords(removeUPunctuations(tempLine.strip())).split()
        wordList = wordList | set([x.lower() for x in partialWordList])
    return wordList


def calculateIDF(ipDirectory):
	hmap = {}
	totalFiles = 0
	for i in os.listdir(ipDirectory):			
		totalFiles = totalFiles + 1
		absFilePath = ipDirectory + "/" + str(i)
		rawXMLText = getRawTextFromXMLDocTag(absFilePath)
		docWordSet = documentWordSet(extract_sentences(unicode(rawXMLText)))
		for docWord in docWordSet:
			hmap[docWord] = hmap.get(docWord, 0) + 1
				
	return hmap, totalFiles

def normalizeIDF(hmap, totalFiles):
	
	totalFiles = 1.0*totalFiles
	for docWord in hmap:
		hmap[docWord] = math.log(totalFiles/(hmap.get(docWord, 1)))
	return hmap

def usage():
    sys.stderr.write('createRawCorpus.py -i <inputdirectory> -o <outputdirectory>\n')

def writeToFile(hmap, odir):

	outputFilePath = odir + "/idf/wordIDF.txt"
	dir = os.path.dirname(outputFilePath)
	if not os.path.exists(dir):
		os.makedirs(dir)
	outputFile = codecs.open(outputFilePath, "w", "utf-8")

	for word in hmap:
		outputFile.write(word)
		outputFile.write('\t')
		outputFile.write(str(hmap.get(word)))
		outputFile.write('\n')

	outputFile.close()

def main():
    print "start"
    inputdir = ''
    outputdir = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"i:o:",["idir=","odir="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--idir"):
			inputdir = arg
        if opt in ("-o", "--odir"):
			outputdir = arg

    if inputdir != "" and outputdir != "":
		print "calculating idf"
		hmap, totalFiles = calculateIDF(inputdir)
		print "normalizing idf"
		hmap = normalizeIDF(hmap, totalFiles)
		print "storing idf"
		writeToFile(hmap, outputdir)
    else:
        usage()
        sys.exit(2)


if __name__ == "__main__":
   main()



#hmap = { "ronak": 200, "parpani": 300 }
#writeToFile(hmap, "/home/rap450/nlp/check")
#print normalizeIDF(hmap, 500);
#print math.log(500.0/300.0)
#print math.log(500.0/200.0)
