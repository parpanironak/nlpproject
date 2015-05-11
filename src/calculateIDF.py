#!/usr/bin/env python2

import os, sys
import xml.etree.cElementTree as ET
import getopt, codecs, logging
import re, string, math, unicodedata

TEST_FILE = '/home/rap450/nlp/shellscripts'

try:
    import utils, config
except ImportError:
    sys.stderr.write("Error: missing file utils.py, config.py\n")
    exit(1)

cachedStopWords = utils.stopwords
table = string.maketrans("","")

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

def removeUPunctuations(text):
    return text.translate(tbl)


def removeStopWords(text):
    return ' '.join([stemmer.stem(word) for word in text.split() if stemmer.stem(word) not in cachedStopWords])


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
                    if flag and (re.match(r'<doc.*>', line) is not None):
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


def extract_sentences(rawText):
    try:
        nltk.data.find('tokenizers/punkt/english.pickle')
    except LookupError:
        nltk.download('punkt', download_dir = config.NLTK_DATA_DIR)
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
        if i.endswith(".xml"):
            totalFiles += 1
            absFilePath = os.path.join(ipDirectory, str(i))
            rawXMLText = getRawTextFromXMLDocTag(absFilePath)
            docWordSet = documentWordSet(extract_sentences(unicode(rawXMLText)))
            for docWord in docWordSet:
                hmap[docWord] = hmap.get(docWord, 0) + 1
    return hmap, totalFiles


def normalizeIDF(hmap, totalFiles):
    max = 1.0;
    totalFiles = 1.0*totalFiles
    for docWord in hmap.keys():
        hmap[docWord] = math.log(totalFiles/(hmap.get(docWord, 1)))/math.log(10.0)
        if(max < hmap[docWord]):
            max = hmap[docWord]
    for docWord in hmap.keys():
        hmap[docWord] = hmap[docWord]/max
    return hmap


def usage():
    sys.stderr.write('createRawCorpus.py -i <inputdirectory> -o <outputdirectory>\n')


def writeToFile(hmap, odir):
    outputFilePath = os.path.join(odir, "idf", "wordIDF.txt")
    dir_path = os.path.dirname(outputFilePath)
    utils.ensure_dir(dir_path)
    try:
        outputFile = codecs.open(outputFilePath, "w", "utf-8")
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
        exit(1)

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
        exit(1)


if __name__ == "__main__":
   main()
