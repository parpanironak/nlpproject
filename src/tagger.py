#!/usr/bin/env python2

import os, sys, re

INPUT_DATA_DIR = "./corpus_data"
OUTPUT_DATA_DIR = "./tagger_data"
NLTK_DATA_DIR = "./nltk_data"

try:
    os.environ['NLTK_DATA'] = NLTK_DATA_DIR
    import nltk.data
except ImportError:
    sys.stderr.write("{0} depends on python {1} module. Run 'pip install {1}' from a shell.\n".format(sys.argv[0], "nltk"))
    exit(1)



class Entity:
    def __init__(self, entity_name, count = 0, sentences = []):
        self.entity_name = entity_name
        self.count = count
        self.sentences = sentences
    def append(self, string):
        self.sentences.append(string)
    def increment(value = 1):
        self.count += value


def create_dict(taglist, corpus_path = INPUT_DATA_DIR):
    dico = {}
    testfunc = lambda x: map(lambda filepath: sys.stdout.write("{0}\n".format(os.path.join(x[0], filepath))), x[2])
    map(testfunc, os.walk(corpus_path))
    return dico


def extract_sentences_with_links(tag, filepath):
    sentences = extract_sentences(filepath)
    return associate_tags([tag], sentences)

# compatibility with Ronak's existing code
extractSentencesWithLinks = extract_sentences_with_links


def extract_sentences(filepath):
    try:
        nltk.data.find('tokenizers/punkt.zip')
    except LookupError:
        nltk.download('punkt', download_dir = NLTK_DATA_DIR)
    try:
        with open(filepath) as myfile:
            file_contents = myfile.readlines()
    except IOError, e:
        sys.stderr.write(str(e) + '\n')
        return []
    file_contents = "".join(file_contents)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    tokenized_text = tokenizer.tokenize(file_contents)
    sentences = []
    for textblob in tokenized_text:
        sentences.extend(textblob.split('\n\n'))
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
    for tag in tags:
        for sentence in sentences:
            print sentence
            if tag in sentence:
                dico[tag] = dico.get(tag, Entity(tag)).append(sentence)
    return dico


def print_dict_to_files(mydict, out_dir = OUTPUT_DATA_DIR, use_pickle = False):
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
    if use_pickle:
        import cPickle as pickle
        for disambiguated_form in mydict.keys():
            try:
                with open(os.path.join(out_dir, disambiguated_form), "w") as f:
                    pickle.dump(mydict[disambiguated_form], f)
            except IOError, e:
                sys.stderr.write("Error creating file\n")
                exit(1)


def main():
    # test code to check if correct splitting on sentences
    for sentence in extract_sentences(sys.argv[1]):
        print sentence
        print "******************************************"
    exit(0)
    sentences = []
    create_dict([], sys.argv[1])
    #for arg in sys.argv[1:]:
    #    sentences.extend(extract_sentences(arg))
    #print associate_tags(["english", "Coming"], sentences) 


if __name__ == "__main__":
    main()
