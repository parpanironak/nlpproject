#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string

table = string.maketrans("","")

def removePunctuations(s):
    return s.translate(table, string.punctuation)

def createCountMap(wordList):
    hmap = {};
    if not isinstance(word , list):
        return None
        ema
    for word in wordList:
        hmap[word] = hmap.get(word, 0) + 1
    return hmap

def methodd(tag, entity, odir):
    termFrequencyVector = {}
    pattern = re.compile(r"(?i)\[\[{0} \\| {1}\]\]".format(entity, tag))
    entityFilePath = odir + "/corpus/" + tag + "/" + entity + ".txt"

    if(os.path.isfile(entityFilePath)):
        wordList = []
        with open(entityFilePath) as entityFile:
            entityFileLine = entityFile.readline()
            if entityFileLine == "<doc>" or entityFileLine == "</doc>" :
                tempList = pattern.split(entityFileLine)
                for temp in tempList:
                    partialWordList = removePunctuations(temp.strip()).split()
                    wordList = wordList + [x.lower() for x in partialWordList]
