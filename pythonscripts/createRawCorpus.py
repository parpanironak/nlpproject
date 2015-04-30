#!/usr/bin/python
 
import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
 
def extractSentencesWithLinks(tag, filePath):
    return {"fish": (4,["r","o","n","a"]), "city":(3,["r","o","n","a","k"])}
 
def extractSentencesWithLinks2(tag, filePath):
    if(not os.path.isfile(filePath)):
        return {}
 
 
 
def extract(inputfile, tag, odir):
 
        entityCountMap = {};
        with open(inputfile) as f:
            filePath = f.readline()
            hmap = extractSentencesWithLinks(tag, filePath)
            for entity in hmap:
                hmapValue = hmap[entity]
                sentList = hmapValue[1]
                if(entityCountMap.has_key(entity)):
                    old = entityCountMap[entity]
                    entityCountMap[entity] = (old[0] + hmapValue[0], old[1] + len(sentList))
                else:
                    entityCountMap[entity] = (hmapValue[0], len(sentList))
                outputFilePath = odir + "/corpus/" + tag + "/" + entity + ".txt"
                dir = os.path.dirname(outputFilePath)
                if not os.path.exists(dir):
                    os.makedirs(dir)
 
                outPutFile = open(outputFilePath, "a")
                outPutFile.write("<doc>\n")
                for sent in sentList:
                    outPutFile.write(sent)
                    outPutFile.write("\n")
                outPutFile.write("</doc>\n")
                outPutFile.close()
 
        outputFilePath = odir + "/tags/" + tag + ".txt"
        dir = os.path.dirname(outputFilePath)
        if not os.path.exists(dir):
            os.makedirs(dir)
        outPutFile = open(outputFilePath, "w")
 
        for entity in entityCountMap:
            counts = entityCountMap[entity];
            outPutFile.write(entity + "\t" + str(counts[0]) + "\t" + str(counts[1]) + "\n")
        outPutFile.close()
 
        for entity in entityCountMap:
            outputFilePath = odir + "/entities/" + entity + ".txt"
            dir = os.path.dirname(outputFilePath)
            if not os.path.exists(dir):
                os.makedirs(dir)
            outPutFile = open(outputFilePath, "a")
            outPutFile.write(tag + "\n")
 
def main(argv):
   print "start"
   inputfile = ''
   tag = ''
   outputdir = ''
   try:
      opts, args = getopt.getopt(argv,"i:t:o:",["ifile=","tag=","odir="])
 
   except getopt.GetoptError:
      print 'createRawCorpus.py -i <inputfile> -o <outputdirectory> -t <tag>'
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
        print 'createRawCorpus.py -i <inputfile> -o <outputdirectory> -t <tag>'
        sys.exit(2)
 
if __name__ == "__main__":
   main(sys.argv[1:])
