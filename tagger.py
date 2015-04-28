#!/usr/bin/env python2

import os, sys, re
import cPickle as pickle

INPUT_DATA_DIR = "./corpus_data"
OUTPUT_DATA_DIR = "./tagger_data"

# TODO: write wrapper function: pass in the path to a directory, dictionary is made
# TODO: convince Ronak that his idea of passing in a single tag to associate_tags is bad, pointless and unoptimized

class Tag:
    def __init__(self, tagname, surface_forms = [], phrases = []):
        self.tagname = tagname
        self.surface_forms = surface_forms
        self.phrases = phrases
    def append(self, string):
        self.phrases.append(string)


def extract_sentences(filepath):
    try:
        with open(filepath) as myfile:
            file_contents = myfile.readlines()
    except IOError, e:
        sys.stderr.write(str(e) + '\n')
        return []
    file_contents = "".join(file_contents)
    # TODO: properly segment into phrases. Use nltk?
    sentences = file_contents.split(".?!")
    return sentences
 

# TODO: debug me
# TODO: properly process tags: get rid of brackets and extract surface form/disambiguated form
# TODO: store file offsets in memory as opposed to entire phrase (save some mem).
#    Provide associated wrapper functions
# TODO: discuss previous TODO. Is it strictly necessary? Sure it's more optimized,
#    but it comes at the cost of a lot of extra work, and the resulting
#    optimizations may not be worth it
def associate_tags(tags, sentences):
    dico = {}
    for sentence in sentences:
        print sentence
        for tag in tags:
            if tag in sentence:
                dico[tag] = dico.get(tag, Tag(tag)).append(sentence)
    return dico


def print_dict_to_files(mydict, out_dir = OUTPUT_DATA_DIR):
    if not os.path.isdir(out_dir):
        if os.path.exists(out_dir):
            sys.stderr.write("Error: file exists\n")
            exit(1)
        else:
            try:
                os.makedirs(out_dir)
            except OSError:
                sys.stderr.write("Error creating directory\n")
                exit(1)
    for disambiguated_form in mydict.keys():
        try:
            with open(os.path.join(out_dir, disambiguated_form), "w") as f:
                pickle.dump(mydict[disambiguated_form], f)
        except IOError, e:
            sys.stderr.write("Error creating file\n")
            exit(1)


def main():
    sentences = []
    for arg in sys.argv[1:]:
        sentences.extend(extract_sentences(arg))
    print associate_tags(["english", "Coming"], sentences) 

if __name__ == "__main__":
    main()
