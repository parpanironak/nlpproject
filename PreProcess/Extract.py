import xml.etree.cElementTree as ET
import sys
import codecs

with codecs.open('../data/simplewiki.xml' ,'r', encoding="utf8") as wikifile:
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
            elem = ET.fromstring(xmldoc.encode('utf-8',errors="replace"))
            xmldoc = u'';
            tree = ET.ElementTree(elem)
            name = "../data/wikidocs/" + tree.find(u'title').text.replace("/", "") + u".xml"
            try:
                print name
            except:
                print "Error"
            try:    
                tree.write(name, "utf-8", method="xml")
            except:
                print "Error"    