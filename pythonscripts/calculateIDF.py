#!/usr/bin/env python2

import sys, getopt
import xml.etree.cElementTree as ET
import codecs
import os.path
import re
import string




def calculateIDF(ipDirectory):
	for i in os.listdir(ipDirectory):
		if i.endswith(".xml"): 
			filePath = os.path.abspath(i)			
			continue
		else:
			continue



calculateIDF("/home/rap450/nlp/nlpproject")
