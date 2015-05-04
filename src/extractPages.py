#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os
import re

try:
    import utils
except ImportError:
    sys.stderr.write("Error: missing file utils.py\n")
    exit(1)

def extract(ip):
    fileNames = codecs.open('FileNames','w',encoding='utf-8',errors='replace')
    print "extract start"
    if(not os.path.isfile(ip)):
        print "no target file"
        sys.exit(1);

    lineno = long(0);
    docs = long(0);
    with codecs.open(ip ,'r', encoding='utf-8',errors='replace') as wikifile:
        title = u'';
        flag = True;
        xmldoc = u'';
        for line in wikifile:
            if flag and (re.match(r'<doc.*>',line.strip()) is not None): #check if line matches <doc .... > tag
                flag = False
                xmldoc += line
                xmldoc += u'\n'
                matchObj = re.search(r'title=\".*\"',line.strip())
                fileNames.write(str(docs)+" "+matchObj.group(0)+"\n")
                #title = extractTitle(matchObj.group(0))
            elif not flag:
                if line.strip() != "</doc>":
                    xmldoc += u'\n'
                    xmldoc += line
                else:
                    xmldoc += line
                    xmldoc += u'\n'
                    flag = True;
                    name = os.path.join(os.path.dirname(os.path.abspath(ip)), "Articles", str(docs) + u'.xml')
                    utils.ensure_dir(dirname(name))
                    try:
                        fileObj = codecs.open(name, encoding='utf-8', errors='replace', mode="w")
                        fileObj.write(xmldoc)
                        fileObj.close()
                        xmldoc = u'';
                    except IOError, e:
                        sys.stderr.write(str(e) + '\n')
                        sys.stderr.write("Line:" + str(lineno) + "\n")
                    docs += 1;
                    lineno += 1;
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
        dir_path = os.path.join(os.path.dirname(os.path.abspath(inputfile)), "Articles")
        utils.ensure_dir(dir_path)
        extract(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
