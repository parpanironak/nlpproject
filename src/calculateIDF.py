#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string
import math
import unicodedata
import logging

TEST_FILE = '/home/rap450/nlp/shellscripts'

try:
    import utils
except ImportError:
    sys.stderr.write("Error: missing file utils.py\n")
    exit(1)

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

def removeUPunctuations(text):
    return text.translate(tbl)

table = string.maketrans("","")

#def removePunctuations(s):
#    return s.translate(table, string.punctuation)


def removeStopWords(text):
    return ' '.join([word for word in text.split() if word not in utils.stopwords])


def getRawTextFromXMLDocTag(absFilePath):
    logging.getLogger('main')
    logging.basicConfig(level = logging.DEBUG, filename = './errors.txt')

    if os.path.isfile(absFilePath):
        xmldoc = u'';
        flag = True
        try:
            with codecs.open(absFilePath ,'r', encoding='utf-8',errors='replace') as document:
                for line in document:
                    line = line.strip()
                    if flag and (re.match(r'<doc.*?>', line) is not None):
                        flag = False
                    elif not flag:
                        if line != "</doc>":
                            xmldoc += u'\n'
                            xmldoc += line
                        else:
                            flag = True;
            return xmldoc
        except IOError, e:
            logging.error(str(absFilePath) + '\n' + str(e) + '\n')
    else:
        sys.stderr.write("doesnotexit\n")
    try:
        e = ET.parse(absFilePath).getroot()
        if e.tag == "doc":
            return e.text
        else:
            sys.stderr.write("No doc tag\n")
            return None
    except OSError, e:
        sys.stderr.write(str(e) + '\n')
        return None


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
        absFilePath = os.path.join(ipDirectory, str(i))
        rawXMLText = getRawTextFromXMLDocTag(absFilePath)
        docWordSet = documentWordSet(utils.extract_sentences(unicode(rawXMLText)))
        for docWord in docWordSet:
            hmap[docWord] = hmap.get(docWord, 0) + 1
    return hmap, totalFiles


def normalizeIDF(hmap, totalFiles):
    for docWord in hmap:
        hmap[docWord] = math.log(float(totalFiles)/float(hmap.get(docWord, 1.0)))
    return hmap


def usage():
    sys.stderr.write('createRawCorpus.py -i <inputdirectory> -o <outputdirectory>\n')


def processIDF(hmap, totalFiles):
    for docWord in hmap.keys():
        hmap[docWord] = math.log(float(totalFiles)/float(hmap.get(docWord, 1.0)))
    return hmap


def writeToFile(hmap, odir):
    outputFilePath = os.path.join(odir, "idf", "wordIDF.txt")
    dir_path = os.path.dirname(outputFilePath)
    utils.ensure_dir(dir_path)
    try:
        outputFile = open(outputFilePath, "w")
        for k, v in hmap.items():
            outputFile.write("{0}\t{1}\n".format(str(k), str(v)))
        outputFile.close()
    except IOError, e:
        sys.stderr.write(str(e) + '\n')
        exit(1)


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

