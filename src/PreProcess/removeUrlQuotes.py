#!/usr/bin/env python2

import sys
import urllib as ul

def main():
    original_filepath = "./Combined_articles"
    newfile_path = "./Combined_art_2"
    newfile = open(newfile_path,'w')
    
    with open(original_filepath) as myfile:
        for line in myfile:
            newline = ul.unquote(line)
            newfile.write(newline)


if __name__ == '__main__':
    main()
