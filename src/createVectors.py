#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string
import unicodedata

try:
    import utils, config
except ImportError:
    sys.stderr.write("Error: missing file utils.py, config.py\n")
    exit(1)

table = string.maketrans("","")

TEST_FILE = '/home/rap450/nlp/shellscripts'

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                    if unicodedata.category(unichr(i)).startswith('P'))


def removeUPunctuations(text):
    return text.translate(tbl)


def removePunctuations(s):
    return s.translate(table, string.punctuation)


def removeStopWords(text):
    return ' '.join([word for word in text.split() if word not in utils.cachedStopWords])


def createCountMap(wordList):
    hmap = {};
    if not isinstance(wordList , list):
        return None
    for word in wordList:
        hmap[word] = hmap.get(word, 0) + 1.0
    count = 1 * len(wordList) if len(wordList) > 1 else 1
    for word in hmap:
        hmap[word] = float(hmap.get(word,0)) / float(count)
    return hmap


def createTermFrequencyVector(tag, entity, odir):
    entityFilePath = os.path.join(odir, "corpus", tag, entity + ".txt")
    pattern = re.compile(r"(?i)\[\[{0} \| {1}\]\]".format(entity, tag))
    wordList = []
    try:
        with open(entityFilePath) as entityFile:
            entityFileLine = entityFile.readline()
            if entityFileLine != "<doc>" and entityFileLine != "</doc>" :
                tempList = re.split(pattern, entityFileLine)
                for temp in tempList:
                    partialWordList = removeStopWords(removeUPunctuations(unicode(temp.strip()))).split()
                    wordList = wordList + [x.lower() for x in partialWordList]
        return createCountMap(wordList)
    except IOError, e:
        return None
