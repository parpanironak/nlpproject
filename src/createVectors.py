#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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


from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

table = string.maketrans("","")

TEST_FILE = '/home/rap450/nlp/shellscripts'

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                    if unicodedata.category(unichr(i)).startswith('P'))


def removeUPunctuations(text):
    return text.translate(tbl)


def removePunctuations(s):
    return s.translate(table, string.punctuation)


def removeStopWords(text):
    return ' '.join([stemmer.stem(word.lower()) for word in text.split() if stemmer.stem(word.lower()) not in cachedStopWords])

def createCountMap(wordList):
    hmap = {};
    if not isinstance(wordList, list):
        return None
    maxcount = 1.0
    for word in wordList:
        hmap[word] = hmap.get(word, 0) + 1.0
        if maxcount < hmap[word]:
            maxcount = hmap[word]
    count = float(len(wordList)) if len(wordList) > 1 else 1.0
    for word in hmap:
        hmap[word] = float(hmap.get(word,0)) / float(count)
    return hmap


def createTermFrequencyVector(tag, entity, odir):
    entityFilePath = os.path.join(odir, "corpus", tag, entity + ".txt")
    pattern = re.compile(r"(?i)\[\[{0} \| {1}\]\]".format(entity, tag))
    wordList = []
    try:
        with open(entityFilePath) as entityFile:
            for entityFileLine in entityFile:
                if entityFileLine != "<doc>" and entityFileLine != "</doc>" :
                    tempList = re.split(pattern, entityFileLine)
                    for temp in tempList:
                        partialWordList = removeStopWords(removeUPunctuations(unicode(temp.strip()))).split()
                        wordList = wordList + [x for x in partialWordList]
        return createCountMap(wordList)
    except IOError, e:
        print "None One"
        print tag
        print entity
        print odir
        return None



def loadIDF(filePath):
    hmap = {}
    with open(filePath, 'r') as f:
        for line in f:
            word, idf = line.split()
            idf = float(idf)
            hmap[word] = idf
    return hmap

def tfIdf(idfMap, vector):
    for word in vector:
        #vector[word] = vector[word] * idfMap.get(word, 0)
        vector[word] = vector[word]
    return vector


def mainMethod(odir):
    tags = ["Barcelona", "Chinese", "Dutch", "Finnish", "Greek", "Italian", "Latin", "Milan", "PST", "Public", "Scottish", "Swedish", "Turkish" ]
    #tags = ["English","Tokyo","Japanese","French"]
    idfFilePath = odir + "/idf/wordIDF.txt"
    idfMap = loadIDF(idfFilePath)
    for tag in tags:
        ipfile = odir + "/tags/" + tag + ".txt"
        with open(ipfile, 'r') as f:
            for line in f:
                #print line
                tokens = line.rsplit("\t", 3)
                entity = tokens[0]
                acount = int(tokens[1])
                bcount = int(tokens[2])
                if(bcount >= 0):
                    vec = createTermFrequencyVector(tag, entity, odir)
                    tfidf = tfIdf(idfMap, vec)
                    opfile = odir + "/vectors/" + tag + "/" + entity.strip() + ".txt"
                    dir = os.path.dirname(opfile)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    fx = open(opfile, "w")
                    for key in tfidf:
                        fx.write(key)
                        fx.write('\t')
                        fx.write(unicode(tfidf[key]))
                        fx.write('\n')
                    fx.close()


def usage():
    sys.stderr.write('createRawCorpus.py -i <inputdirectory>\n')


def main():
    print "start"
    inputdir = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"i:",["idir="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--idir"):
            inputdir = arg


    if inputdir != "":
        mainMethod(inputdir)
    else:
        usage()
        sys.exit(2)


if __name__ == "__main__":
   main()
