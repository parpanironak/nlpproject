#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string
import unicodedata
reload(sys)
sys.setdefaultencoding('utf8')




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
table = string.maketrans("","")

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

def removeUPunctuations(text):
    return text.translate(tbl)

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
	entityFilePath = odir + "corpus/" + tag + "/" + entity.strip() + ".txt"
	print entityFilePath
	if(os.path.isfile(entityFilePath)):
		
		pattern = re.compile(r"(?i)\[\[{0} \| {1}\]\]".format(entity, tag))
		wordList = []
		with open(entityFilePath) as entityFile:
			for entityFileLine in entityFile:
				if entityFileLine.strip() != "<doc>" and entityFileLine.strip() != "</doc>" :
					tempList = re.split(pattern, entityFileLine)
					for temp in tempList:
						partialWordList = removeStopWords(removeUPunctuations(unicode(temp.strip()))).split()
						wordList = wordList + [x.lower() for x in partialWordList]
		return createCountMap(wordList)

	else:
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
		vector[word] = vector[word] * idfMap.get(word, 0)
	return vector


def mainMethod(odir):
    #  tags = ["Barcelona", "Chinese" "Dutch", "Finnish", "Greek", "Italian", "Latin", "Milan", "PST", "Public", "Scottish", "Swedish", "Turkish" ]
    tags = ["Barcelona"]
    idfFilePath = odir + "idf/wordIDF.txt"
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
