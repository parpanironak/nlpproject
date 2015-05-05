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
    for word in wordList:
        word = word.strip()
        hmap[word] = hmap.get(word, 0) + 1.0
    count = 1.0*len(wordList) if len(wordList) > 1 else 1.0

    for word in hmap:
		hmap[word] = hmap.get(word,0)/count;

    return hmap

def createVector(text):
    text = text.lower()
    text = readable_entities(text)
    text = removePunctuations(text)
    text = removeStopWords(text)
    return createCountMap(text.split())

def ipclean(inputfilepath):
    with open(inputfilepath, "r") as f:
        for line in f:
            line = line.strip()
            if line != "=========================================" and line != "+++++++++++++++++++++++++++++++++++++++++":
                m = getMatchObjects(r'\[\[\s*@@\s*\|\s*(.*?)\s*\]\]',line)
                if(len(m) > 1):
                    end = 0
                    for m1 in m:
                        link = "" + line[end + m1.start(): end + m1.end()]
                        tag = m1.group(1).strip()
                        tag = tag[0:1].upper() + tag[1:].lower()
                        sent = ""+ line[0 : end + m1.start()] + " " + line[end + m1.end() :]
                        sent = createVector(sent.strip())
                        end = m1.end()



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
