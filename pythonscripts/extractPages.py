#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path


def extract(ip):
	print "extract start"
	if(not os.path.isfile(ip)):
		print "no target file" 
		sys.exit(0);

	lineno = long(0);
	docs = long(0);
	with codecs.open(ip ,'r', encoding="utf8") as wikifile:
	    flag = True;
	    xmldoc = u'';
	    for line in wikifile:
		if flag and line.strip() == "<page>":
		    flag = False;
		    xmldoc += line
		    xmldoc += u'\n'
		elif not flag and not line.strip() == "</page>":   
		    xmldoc += line
		    xmldoc += u'\n'
		elif not flag and line.strip() == "</page>":   
		    xmldoc += line
		    xmldoc += u'\n'
		    flag = True;
		    elem = ET.fromstring(xmldoc.encode('utf-8', 'replace'))
		    xmldoc = u'';
		    tree = ET.ElementTree(elem)
		    name = os.path.dirname(os.path.abspath(ip)) + "/pages1/" + tree.find(u'title').text.replace("/", "") + u".xml"

		    try:    
		    	tree.write(name, "utf-8")
		    except:
			print "Unexpected error:", sys.exc_info()
		        print "Line:"+str(lineno) + "\n" +"Cannot write file " + name
			docs = docs + 1;
		    
		lineno = lineno + 1;
		if docs >= 10:
			sys.exit(0);


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
	extract(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
