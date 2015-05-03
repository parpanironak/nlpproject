#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string

NLTK_DATA_DIR = "./nltk_data"
TEST_FILE = '/home/rap450/nlp/shellscripts'

try:
    os.environ['NLTK_DATA'] = NLTK_DATA_DIR
    import nltk.data
    try:
        nltk.data.find('corpora/stopwords/english')
    except LookupError:
        nltk.download('stopwords', download_dir = NLTK_DATA_DIR)
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


def extract_sentences(rawText):
    try:
        nltk.data.find('tokenizers/punkt/english.pickle')
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
        partialWordList = removeStopWords(removePunctuations(tempLine.strip())).split()
        wordList = wordList | set([x.lower() for x in partialWordList])
    return wordList


def calculateIDF(ipDirectory):
    hmap = {}
    totalFiles = 0
    for i in os.listdir(ipDirectory):
        if i.endswith(".xml"):
            totalFiles += 1
            absFilePath = os.path.join(ipDirectory, str(i))
            rawXMLText = getRawTextFromXMLDocTag(absFilePath)
            docWordSet = documentWordSet(extract_sentences(str(rawXMLText)))
            for docWord in docWordSet:
                hmap[docWord] = hmap.get(docWord, 0) + 1
    return hmap

def processIDF(hmap, totalFiles):
    for docWord in hmap.keys():
        hmap[docWord] = math.log(totalFiles/(hmap.get(docWord, 0)))
    return hmap


def writeToFile(hmap, odir):
    outputFilePath = os.path.join(odir, "idf/wordIDF.txt")
    dirpath = os.path.dirname(outputFilePath)
    try:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        outputFile = open(outputFilePath, "w")
    except (IOError, OSError), e:
        sys.stderr.write(str(e) + '\n')
        exit(1)

    for k, v in hmap.items():
        outputFile.write("{0}\t{1}\n".format(str(k), str(v)))

    outputFile.close()


def main():
    hmap = { "ronak": 200, "parpani": 300 }
    writeToFile(hmap, "/home/rap450/nlp/check")

if __name__ == '__main__':
    main()
