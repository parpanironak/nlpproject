#!/usr/local/bin/python

import sys
import urllib as ul

original_filepath = "Combined_articles"
newfile_path = "Combined_art_2"
newfile = open(newfile_path,'w')

with open(original_filepath) as myfile:
    for line in myfile:
        newline = ul.unquote(line)
        newfile.write(newline)
