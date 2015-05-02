#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os
import re

def extract(ip):
    fileNames = codecs.open('FileNames','w',encoding='utf-8',errors='replace')
    print "extract start"
    if(not os.path.isfile(ip)):
        print "no target file"
        sys.exit(0);

    lineno = long(0);
    docs = long(0);
    with codecs.open(ip ,'r', encoding='utf-8',errors='replace') as wikifile:
        title = u'';
        flag = True;
        xmldoc = u'';
        for line in wikifile:
            if flag and (re.match(r'<doc.*?>',line.strip()) is not None): #check if line matches <doc .... > tag
                flag = False
                xmldoc += line
                xmldoc += u'\n'
                matchObj = re.search(r'title=\".*?\"',line.strip())
                fileNames.write(str(docs)+" "+matchObj.group(0)+"\n")
                #title = extractTitle(matchObj.group(0))
            elif not flag and not line.strip() == "</doc>":
                xmldoc += u'\n'
                xmldoc += line
            elif not flag and line.strip() == "</doc>":
                xmldoc += line
                xmldoc += u'\n'
                flag = True;
                name = os.path.dirname(os.path.abspath(ip)) + "/Articles/" + str(docs) + u".xml"
                try:
                    fileObj = codecs.open(name, encoding='utf-8', errors='replace', mode="w")
                    fileObj.write(xmldoc)
                    xmldoc = u'';
                except:
                    print "Unexpected error:", sys.exc_info()
                    print "Line:"+str(lineno) + "\n" +"Cannot write file" + name
                docs = docs + 1;
                lineno = lineno + 1;
                # if docs >= 10:
                #    sys.exit(0);


# def extractTitle(title):
#    SplitResultList = title.split('"');
#    SplitResult = re.sub('[^\d\s\w]','SC',SplitResultList[1])
#    return SplitResult

def main(argv):
    print "start"
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"i:",["ifile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg

    if inputfile != '':
        directory = os.path.dirname(os.path.abspath(inputfile)) + "/Articles/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        extract(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
