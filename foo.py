#!/usr/bin/env python2

import os, sys, re
import cPickle as pickle

INPUT_DATA_DIR = "./corpus_data"
OUTPUT_DATA_DIR = "./foo"

# TODO: write wrapper function: pass in the path to a directory, dictionary is made
# TODO: convince Ronak that his idea of passing in a single tag to associate_tags is bad, pointless and unoptimized

def extract_sentences(filepath):
    try:
        with open(filepath) as myfile:
            file_contents = myfile.readlines()
    except IOError, e:
        sys.stderr.write(e + '\n')
        exit(1)
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
        for tag in tags:
            if tag in sentence:
                dico[tag] = dico.get(tag, []).append(sentence)
    return dico


def print_dict_to_files(mydict):
    if not os.path.isdir(OUTPUT_DATA_DIR):
        if os.path.exists(OUTPUT_DATA_DIR):
            sys.stderr.write("Error: file exists\n")
            exit(1)
        else:
            os.makedirs(OUTPUT_DATA_DIR)
    for disambiguated_form in mydict.keys():
        with open(os.path.join(OUTPUT_DATA_DIR, disambiguated_form), "w") as f:
            pickle.dump(mydict[disambiguated_form], f)


def main():
    sentences = []
    for arg in sys.argv[1:]:
        sentences.extend(extract_sentences(arg))
    print associate_tags(["english", "Coming"], sentences) 

if __name__ == "__main__":
    main()
