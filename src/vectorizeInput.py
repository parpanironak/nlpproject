#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, getopt
import os
import re
import nltk
import unicodedata
import string
import math
import operator
from nltk.stem import PorterStemmer
hmap2 = {}

stemmer = PorterStemmer()

NLTK_DATA_DIR = "./nltk_data"

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

tags = ["Barcelona", "Chinese", "Dutch", "Finnish", "Greek", "Italian", "Latin", "Milan", "PST", "Public", "Scottish", "Swedish", "Turkish" ]
#tags = ["French","English","Tokyo","Japanese"]

cachedStopWords = stopwords.words("english")

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

table = string.maketrans("","")
def removePunctuations(s):
    return s.translate(table, string.punctuation)

def removeUPunctuations(text):
    print tbl
    return text.translate(tbl)


def loadIDF(filePath):
    hmap = {}
    with open(filePath, 'r') as f:
        for line in f:
            word, idf = line.split()
            idf = float(idf)
            hmap[word] = idf
    return hmap

def removeStopWordsStem(text):
    return ' '.join([stemmer.stem(word.lower()) for word in text.split() if stemmer.stem(word.lower()) not in cachedStopWords])

def removeStopWords(text):
    return ' '.join([word.lower() for word in text.split() if word.lower() not in cachedStopWords])

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
    return re.sub(r'\[\[\s*([^\[\]|]+)\s*\|\s*([^\[\]|]+)\s*\]\]', r'\1 \2', text)

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
    text = removeStopWordsStem(text)
    return createCountMap(text.split())

def compare(entityMap, entityCountMap ,sentvec, idf):
    hmap = {}
    totalEntityCount = len(entityMap)
    maxval = 1.0
    for dim in sentvec:
        count = 0.0
        for entity in entityMap:
            if dim in entityMap[entity]:
                count = count + entityMap[entity][dim]
        if count > 0:
            hmap[dim] = math.log(1.0*totalEntityCount/count)
            maxval = hmap[dim] if hmap[dim] > maxval else maxval
        else:
            hmap[dim] = 1.0
    for dim in sentvec:
        hmap[dim] = 1.0 + hmap[dim] / maxval

    score = 0.0
    entitScoreMap = {}
    maxentity = None

    for entity in entityMap:
        score = 0.0
        d1 = 0.0
        d2 = 0.0
        for dim in sentvec:
            if dim in entityMap[entity]:
                score = score + (hmap[dim]**2)*entityMap[entity][dim]*sentvec[dim]*((idf.get(dim,0.0))**2)
                d1 = d1 + (hmap[dim]*entityMap[entity][dim]*(idf.get(dim,0.0)))**2.0
                d2 = d2 + (hmap[dim]*sentvec[dim]*(idf.get(dim,0.0)))**2.0
        d1 = (1+d1)**0.5
        d2 = (1+d2)**0.5

        entitScoreMap[entity] = score/(d1*d2)

    x = entitScoreMap
    sorted_x = sorted(x.items(), key=lambda x:x[1])
    sorted_x.reverse()
    #if len(sorted_x) > 0:
    #    max = sorted_x[0][0]
    #    maxcount =
    #    for x in sorted_x:

    if len(sorted_x) == 0:
        return []

    maxval = sorted_x[0][1];
    retlist = [sorted_x[0][0]]

    for i in range(1, len(sorted_x)):
        if sorted_x[i][1] == maxval:
            retlist.append(sorted_x[i][0])
        else:
            break

    return retlist

def disambiguate(inputfilepath, entitymap, hmap2 , odir):
    idfFilePath = odir + "/idf/wordIDF2.txt"
    idfMap = loadIDF(idfFilePath)
    outputfile = open(odir+"/ans.txt","w")
    with open(inputfilepath, "r") as f:
    for line in f:
            #print line
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
                            sorted_x = compare(entitymap[tag], hmap2[tag], sentvec, idfMap)
                            #print line[0 : end + m1.start()] + m1.group(0).replace("@@",ent)+ line[end + m1.end() :];
                #for x in sorted_x:
                            #    print x
                            maxv = sorted_x[0]
                            if len(sorted_x) > 1:
                                for fg in sorted_x:
                                    if hmap2[tag][fg] > hmap2[tag][maxv]:
                                        maxv = fg
                            #print re.sub(r"\s*\|\s", r"|", m1.group(0).replace("@@",maxv))
                            outputfile.write( re.sub(r"\s*\|\s", r"|", m1.group(0).replace("@@",maxv)))
                            outputfile.write("\n")
                        end = m1.end()
                #else:
                    #print ""
            #print line
            #print "No tags to disambiguate"
            #print "========================================="
            #else:
            #    print line
    outputfile.close()

def loadEntiyVector(entity, tag, odir):

    fpath = odir + "/vectors/" + tag + "/" + entity.strip() + ".txt"
    hmap = {}
    with open(fpath, "r") as f:
        for line in f:
            word, score = line.rsplit("\t", 2)
            score = float(score)
            hmap[word] = score

    return hmap

def loadVectors(odir):

    hmap = {}
    hmap2 = {}
    for tag in tags:
        fpath = odir + "/tags/" + tag + ".txt"
        innerhmap = {}
        innerhmap2 = {}
        with open(fpath, "r") as f:
            for line in f:
                entity, acount, bcount = line.rsplit("\t",3)
                if float(acount) > 0:
                    innerhmap[entity] = loadEntiyVector(entity.strip(), tag ,odir)
                    innerhmap2[entity] = acount
        hmap[tag] = innerhmap
        hmap2[tag] = innerhmap2
    return hmap, hmap2

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
            directory = arg

    if inputfile != '' and directory != "":
        hmap, hmap2 = loadVectors(directory)
        disambiguate(inputfile, hmap, hmap2, directory)

if __name__ == "__main__":
    main(sys.argv[1:])

