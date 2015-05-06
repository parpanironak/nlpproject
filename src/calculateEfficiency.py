#!usr/local/bin/python

import re
import sys
import os
import codecs
import getopt

pattern = re.compile(r'\[\[.*?\]\]')
tags = ["English","Japanese","Tokyo","French"]

def createTagList(inputfile):
    count = 0
    answertaglist = []
    with open(inputfile,'r') as myfile:
        for line in myfile:
            if line != "=========================================" and line != "+++++++++++++++++++++++++++++++++++++++++":
                if re.search(pattern,line) is not None:
                    for tag in tags:
                        if tag in re.search(pattern,line).group(0):
                            tagfromline = re.search(pattern,line).group(0)
                            answertaglist.append(tagfromline.split('|')[0].split('[')[2].strip())
    return answertaglist

def calculateEfficiency(predictedTagList, correctTagList):
    correctMatchCount = 0.0
    if len(predictedTagList) != len(correctTagList):
        print "Tags in both files not equal"
        exit(0)
    else:
        for ptag,ctag in itertools.izip(predictedTagList,correctTagList):
            if ptag == ctag:
                correctMatchCount +=1
    efficiency = (correctMatchCount/len(predictedTags))*100
    print "efficiency is" + efficiency


def main():

   print "start"
   predictedTagsFile = ''
   correctTagsFile = ''
   try:
       opts, args = getopt.getopt(sys.argv[1:],"p:c:",["ptags=","ctags="])
   except getopt.GetoptError:
       usage()
       sys.exit(2)

   for opt, arg in opts:
       if opt in ("-p", "--ptags"):
           predictedTagsFile = arg
       if opt in ("-c", "--ctags"):
           correctTagsFile = arg

   if predictedTagsFile != "" and correctTagsFile != "":
       print "getting tags from prediction file"
       predictedTagList = createTagList(predictedTagsFile)
       print "getting tags from correct tags file"
       correctTagList = createTagList(correctTagsFile)
       print "Calculating efficiency"
       calculateEfficiency(predictedTagList,correctTagList)
   else:
       usage()
       sys.exit(2)


if __name__ == "__main__":
    main()
