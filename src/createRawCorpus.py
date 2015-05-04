#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
from tagger import Entity
from tagger import extract_sentences_with_links


def extract(inputfile, tag, odir):
    entityCountMap = {};
    with open(inputfile) as f:
		for line in f:
			filePath = line.strip()
			hmap = extract_sentences_with_links(tag, filePath)
			for entity in hmap:
				hmapValue = hmap[entity]
				
				count = hmapValue.count
				sentList = hmapValue.sentences
				old = entityCountMap.get(entity, (0, 0))
				print old
				entityCountMap[entity] = (old[0] + count, old[1] + len(sentList))
				outputFilePath = odir + "/corpus/" + tag + "/" + entity + ".txt"
				dir = os.path.dirname(outputFilePath)
				if not os.path.exists(dir):
					os.makedirs(dir)				
				outPutFile = codecs.open(outputFilePath,'a', encoding='utf-8',errors='replace')
				outPutFile.write(u"<doc>\n")
				for sent in sentList:
					outPutFile.write(unicode(sent))
					outPutFile.write(u"\n")
				outPutFile.write(u"</doc>\n")
				outPutFile.close()

    outputFilePath = odir + "/tags/" + tag + ".txt"
    dir = os.path.dirname(outputFilePath)
    if not os.path.exists(dir):
        os.makedirs(dir)
    outPutFile = codecs.open(outputFilePath,'w', encoding='utf-8',errors='replace')

    for entity in entityCountMap:
        counts = entityCountMap[entity];
        outPutFile.write(entity + "\t" + str(counts[0]) + "\t" + str(counts[1]) + "\n")
    outPutFile.close()

    for entity in entityCountMap:
        outputFilePath = odir + "/entities/" + entity + ".txt"
        dir = os.path.dirname(outputFilePath)
        if not os.path.exists(dir):
            os.makedirs(dir)
        outPutFile = codecs.open(outputFilePath,'a', encoding='utf-8',errors='replace')
        outPutFile.write(tag + "\n")
        outPutFile.close()


def usage():
    sys.stderr.write('createRawCorpus.py -i <inputfile> -o <outputdirectory> -t <tag>\n')


def main():
    print "start"
    inputfile = ''
    tag = ''
    outputdir = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"i:t:o:",["ifile=","tag=","odir="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        if opt in ("-t", "--tag"):
           tag = arg
        if opt in ("-o", "--odir"):
           outputdir = arg

    if inputfile != "" and tag != "" and outputdir != "":
        extract(inputfile, tag, outputdir)
    else:
        usage()
        sys.exit(2)


if __name__ == "__main__":
   main()


