#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path

try:
    import utils
    from utils import Entity
    from tagger import extract_sentences_with_links
except ImportError:
    sys.stderr.write("Error: missing files utils.py\n")
    exit(1)


def extract(inputfile, tag, odir):
    entityCountMap = {};
    try:
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
                    outputFilePath = os.path.join(odir, "corpus", tag, entity + ".txt")
                    dir_path = os.path.dirname(outputFilePath)
                    utils.ensure_dir(dir_path)
                    try:
                        outPutFile = codecs.open(outputFilePath,'a', encoding='utf-8', errors='replace')
                        outPutFile.write(u"<doc>\n")
                        for sent in sentList:
                            outPutFile.write(unicode(sent) + u'\n')
                        outPutFile.write(u"</doc>\n")
                        outPutFile.close()
                    except IOError,e:
                        sys.stderr.write(str(e) + '\n')
                        exit(1)
    except IOError, e:
        sys.stderr.write(str(e) + '\n')
        exit(1)

    outputFilePath = os.path.join(odir, "tags", tag + ".txt")
    dir_path = os.path.dirname(outputFilePath)
    utils.ensure_dir(dir_path)

    try:
        outPutFile = open(outputFilePath, "w")
        for entity in entityCountMap:
            counts = entityCountMap[entity];
            outPutFile.write(entity + "\t" + str(counts[0]) + "\t" + str(counts[1]) + "\n")
        outPutFile.close()
    except IOError, e:
        sys.stderr.write(str(e) + '\n')
        exit(1)

    for entity in entityCountMap:
        outputFilePath = os.path.join(odir, "entities", entity + ".txt")
        dir_path = os.path.dirname(outputFilePath)
        utils.ensure_dir(dir_path)
        try:
            outPutFile = open(outputFilePath, "a")
            outPutFile.write(tag + "\n")
            outPutFile.close()
        except IOError, e:
            sys.stderr.write(str(e) + '\n')
            exit(1)


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

