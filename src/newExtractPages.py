#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path

from wikiExtractor import replaceExternalLinks
from wikiExtractor import dropNested
from wikiExtractor import replaceInternalLinks
from wikiExtractor import magicWordsRE
from wikiExtractor import syntaxhighlight
from wikiExtractor import unescape

bold_italic = re.compile(r"'''''(.*?)'''''")
bold = re.compile(r"'''(.*?)'''")
italic_quote = re.compile(r"''\"([^\"]*?)\"''")
italic = re.compile(r"''(.*?)''")
quote_quote = re.compile(r'""([^"]*?)""')
comment = re.compile(r'<!--.*?-->', re.DOTALL)

selfClosingTags = [ 'br', 'hr', 'nobr', 'ref', 'references', 'nowiki' ]

# These tags are dropped, keeping their content.
# handle 'a' separately, depending on keepLinks
ignoredTags = [
    'abbr', 'b', 'big', 'blockquote', 'center', 'cite', 'div', 'em',
    'font', 'h1', 'h2', 'h3', 'h4', 'hiero', 'i', 'kbd', 'nowiki',
    'p', 'plaintext', 's', 'span', 'strike', 'strong',
    'sub', 'sup', 'tt', 'u', 'var'
]
ignored_tag_patterns = []

def ignoreTag(tag):
    left = re.compile(r'<%s\b[^>/]*>' % tag, re.IGNORECASE) # both <ref> and <reference>
    right = re.compile(r'</\s*%s>' % tag, re.IGNORECASE)
    ignored_tag_patterns.append((left, right))

for tag in ignoredTags:
    ignoreTag(tag)



selfClosing_tag_patterns = [
    re.compile(r'<\s*%s\b[^>]*/\s*>' % tag, re.DOTALL | re.IGNORECASE) for tag in selfClosingTags
]

placeholder_tags = {'math':'formula', 'code':'codice'}

placeholder_tag_patterns = [
    (re.compile(r'<\s*%s(\s*| [^>]+?)>.*?<\s*/\s*%s\s*>' % (tag, tag), re.DOTALL | re.IGNORECASE),
     repl) for tag, repl in placeholder_tags.items()
]

# Matches space
spaces = re.compile(r' {2,}')

# Matches dots
dots = re.compile(r'\.{4,}')

def clean(text):
    """
    Transforms wiki markup.
    @see https://www.mediawiki.org/wiki/Help:Formatting
    """

    # Drop transclusions (template, parser functions)
    text = dropNested(text, r'{{', r'}}')

    # Drop tables
    text = dropNested(text, r'{\|', r'\|}')

    # replace external links
    text = replaceExternalLinks(text)

    # replace internal links
    text = replaceInternalLinks(text)

    # drop MagicWords behavioral switches
    text = magicWordsRE.sub('', text)

    ################ Process HTML ###############

    # turn into HTML, except for the content of <syntaxhighlight>
    res = ''
    cur = 0
    for m in syntaxhighlight.finditer(text):
        end = m.end()
        res += unescape(text[cur:m.start()]) + m.group(1)
        cur = end
    text = res + unescape(text[cur:])


    text = bold_italic.sub(r'\1', text)
    text = bold.sub(r'\1', text)
    text = italic_quote.sub(r'"\1"', text)
    text = italic.sub(r'"\1"', text)
    text = quote_quote.sub(r'"\1"', text)
    # residuals of unbalanced quotes
    text = text.replace("'''", '').replace("''", '"')

    # Collect spans

    spans = []
    # Drop HTML comments
    for m in comment.finditer(text):
            spans.append((m.start(), m.end()))

    # Drop self-closing tags
    for pattern in selfClosing_tag_patterns:
        for m in pattern.finditer(text):
            spans.append((m.start(), m.end()))

    # Drop ignored tags
    for left, right in ignored_tag_patterns:
        for m in left.finditer(text):
            spans.append((m.start(), m.end()))
        for m in right.finditer(text):
            spans.append((m.start(), m.end()))

    # Bulk remove all spans
    text = dropSpans(spans, text)

    # Drop discarded elements
    for tag in discardElements:
        text = dropNested(text, r'<\s*%s\b[^>/]*>' % tag, r'<\s*/\s*%s>' % tag)

    text = unescape(text)

    # Expand placeholders
    for pattern, placeholder in placeholder_tag_patterns:
        index = 1
        for match in pattern.finditer(text):
            text = text.replace(match.group(), '%s_%d' % (placeholder, index))
            index += 1

    text = text.replace('<<', u'«').replace('>>', u'»')

    #############################################

    # Cleanup text
    text = text.replace('\t', ' ')
    text = spaces.sub(' ', text)
    text = dots.sub('...', text)
    text = re.sub(u' (,:\.\)\]»)', r'\1', text)
    text = re.sub(u'(\[\(«) ', r'\1', text)
    text = re.sub(r'\n\W+?\n', '\n', text) # lines with only punctuations
    text = text.replace(',,', ',').replace(',.', '.')

    return text


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
		    name = os.path.dirname(os.path.abspath(ip)) + "/pages/" + tree.find(u'title').text.replace("/", "") + u".xml"		    	
			header = '<doc title="%s">\n' % (tree.find(u'title').text.replace("/", ""))
			footer = "\n</doc>\n"
		    
		    try:    
		    	rawtext = tree.find(u'text').text
		    	cleantext = clean(rawtext)
		    	f = codecs.open(name,'a', encoding='utf-8',errors='replace')
		    	f.write(header + cleantext + footer)
		    	f.close();
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
      print 'test.py -i <inputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         inputfile = arg
 
   if inputfile != '': 
	extract(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
