#!/usr/bin/env python2
import codecs
import os, sys
from bs4 import BeautifulSoup
try:
    import config
except ImportError:
    sys.stderr.write("Error: missing file utils.py\n")
    exit(1)

try:
    os.environ['NLTK_DATA'] = config.NLTK_DATA_DIR
    import nltk.data
    try:
        nltk.data.find('corpora/stopwords/english')
    except LookupError:
        nltk.download('stopwords', download_dir = config.NLTK_DATA_DIR)
    from nltk.corpus import stopwords
except ImportError:
    sys.stderr.write("{0} depends on python {1} module. Run 'pip install {1}' from a shell.\n".format(sys.argv[0], "nltk"))
    exit(1)

stopwords = stopwords.words('english')

class Entity:
    """Entity class.
    str self.tag_name: tag associated to entity.
    int self.count: number of times entity appears.
    str[] self.sentences: list of sentences in which entity appears."""

    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.count = 0
        self.sentences = []

    def increment(self, value = 1):
        self.count += value
    def __str__(self):
        return "{0}: {1}|{2}".format(self.tag_name, self.count, self.sentences)


def extract_sentences(filepath):
    """Uses NLTK module to segment text from file into english sentences.
        Segmentation is only as good as what is provided by NLTK.
        Text is also split along double-newlines to provide for titles/lists/other.
        Returns empty list in case of error reading file.
        
        str[] extract_sentences(str filepath)
        str filepath: path to file to process.
        return value: list of sentences in processed file.
        
        IMPORTS: sys, nltk, config
        GLOBAL CONSTANTS: config.NLTK_DATA_DIR"""
    
    try:
        nltk.data.find('tokenizers/punkt/english.pickle')
    except LookupError:
        nltk.download('punkt', download_dir = config.NLTK_DATA_DIR)
    #    xmldoc = []
    #    flag = True
    #    open_doc_tag = re.compile(r'<doc[^>]*>')
    try:
        with codecs.open(filepath,'r', encoding='utf-8', errors='replace') as document:
            xmldoc = BeautifulSoup(document).text
    #            for line in document:
#                line = line.strip()
#                if flag and (open_doc_tag.match(line) is not None):
#                    flag = False
#                elif not flag:
#                    if line != "</doc>":
#                        xmldoc.append(line)
#                    else:
#                        flag = True;
    except IOError, e:
        sys.stderr.write(str(e) + '\n')
        return []
    file_contents = "".join(xmldoc)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    tokenized_text = tokenizer.tokenize(file_contents)
    sentences = []
    for textblob in tokenized_text:
        sentences.extend(textblob.split('\n\n'))
    return sentences


