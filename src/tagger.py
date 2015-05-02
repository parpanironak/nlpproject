#!/usr/bin/env python2

import os, sys, re

"Default directory for corpus"
INPUT_DATA_DIR = "./corpus_data"

"Default directory for writing files"
OUTPUT_DATA_DIR = "./tagger_data"

"Default directory for data downloaded by python nltk module"
NLTK_DATA_DIR = "./nltk_data"

"Tags to process"
TAGS = ["Daisy", "autumn|fall"]

try:
    os.environ['NLTK_DATA'] = NLTK_DATA_DIR
    import nltk.data
except ImportError:
    sys.stderr.write("{0} depends on python {1} module. Run 'pip install {1}' from a shell.\n".format(sys.argv[0], "nltk"))
    exit(1)


class Entity:
    """Entity class.
    str self.tag_name: tag associated to entity
    int self.count: number of times entity appears
    str[] self.sentences: list of sentences in which entity appears"""

    def __init__(self, tag_name, count = 0, sentences = []):
        self.tag_name = tag_name
        self.count = count
        self.sentences = sentences
    def increment(self, value = 1):
        self.count += value
    def __str__(self):
        return "{0}: {1}".format(self.tag_name, self.count)

class TagMatcher:
    """Tag matching class
    str self.tag_name: tag
    re.pattern self.pattern: compiled pattern of tag of the form [[.*|TAG]]"""

    def __init__(self, tag_name, pattern):
        self.tag_name = tag_name
        self.pattern = pattern


def merge_dicts(dict1, dict2):
    """Merges 2 dicts of Entity s

    dict merge_dict(dict dict1, dict dict2)"""
    for key in dict1.keys():
        my_entity = dict2.get(key, Entity(dict1[key].tag_name))
        if isinstance(dict1[key], list):
            has_matched = False
	    for entity in dict1[key]:
                if entity.tag_name == my_entity.tag_name:
                    has_matched = True
                    entity.increment(my_entity.count)
                    entity.sentences.extend(my_entity.sentences)
            if not has_matched:
                sys.stderr.write("CONFLICT FOR ENTITY {0}\n".format(key))
                dict1[k].append(my_entity)
        else:
            if my_entity.tag_name != dict1[key].tag_name:
                sys.stderr.write("CONFLICT FOR ENTITY {0}\n".format(key))
                dict1[key] = [dict1[key], my_entity]
            else:
                dict1[key].increment(my_entity.count)
                dict1[key].sentences.extend(my_entity.sentences)
    for key in dict2.keys():
        if not dict1.has_key(key):
            dict1[key] = dict2[key]


def create_dict(tag_list, corpus_path = INPUT_DATA_DIR):
    """Builds dictionary of Entity s from all files located under corpus_path
    directory.

    dict create_dict(str[] tag_list, str corpus_path)
    str[] tag_list: list of tags to search for in corpus
    str corpus_path: path to corpus root directory. Defaults to value of global
    variable INPUT_DATA_DIR
    return value: dict of all Entity s encountered in corpus. Keys are entities
    as strings, values are Entity classes or lists of Entity classes in case of
    conflict.

    IMPORTS: os
    GLOBAL CONSTANTS: INPUT_DATA_DIR"""

    corpus_dict = {}
    def apply_to_file(filepath):
        sentences = extract_sentences(filepath)
        merge_dicts(corpus_dict, associate_tags(tag_list, sentences))
    apply_to_dir = lambda x: map(apply_to_file,
            [ os.path.join(x[0], filepath) for filename in x[2]])
    map(apply_to_dir, os.walk(corpus_path))
    return corpus_dict


def extract_sentences_with_links(tag, filepath):
    """Build a dict of Entity s from a single file

    dict extract_sentences_with_links(str tag, str filepath)
    str tag: name of tag to search for
    str filepath: path to file to process
    return value: dictionary of Entity s encountered in processed file. Keys are
    entities as strings, values are Entity classes or lists of Entity classes in
    case of conflict."""

    sentences = extract_sentences(filepath)
    return associate_tags([tag], sentences)


def extract_sentences(filepath):
    """Uses NLTK module to segment text from file into english sentences.
    Segmentation is only as good as what is provided by NLTK.
    Text is also split along double-newlines to provide for titles/lists/other.
    Returns empty list in case of error reading file.

    str[] extract_sentences(str filepath)
    str filepath: path to file to process.
    return value: list of sentences in processed file.

    IMPORTS: sys, nltk
    GLOBAL CONSTANTS: NLTK_DATA_DIR"""

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


# TODO: !!!!! DEBUG !!!!!
# TODO: store file offsets in memory as opposed to entire phrase (save some mem).
#    Provide associated wrapper functions
# TODO: discuss previous TODO. Is it strictly necessary? Sure it's more optimized,
#    but it comes at the cost of a lot of extra work, and the resulting
#    optimizations may not be worth it
def associate_tags(tags, sentences):
    """Search for presence of tags in sentences, extract entities
    and build dictionary of Entity s with obtained information.

    dict associate_tags(str[] tags, str[] sentences)
    str[] tags: list of tags to search for in sentences
    str[] sentences: list of sentences in which to search for tags
    return value: dictionary of Entity s encountered in corpus. Keys are
    entities as strings, values are Entity classes or lists of Entity classes in
    case of conflict.

    IMPORTS: re"""
    sentence_dict = {}
    tag_patterns = [ TagMatcher(tag, re.compile(r"\[\[\s*([^\[\]|]+)\s*\|\s*{0}\s*\]\]".format(re.escape(tag))))
                     for tag in tags ]
    for sentence in sentences:
        for tag_pattern in tag_patterns:
            match_obj = tag_pattern.pattern.search(sentence, re.I)
            if match_obj is not None:
                entities = match_obj.groups()
                entity = entities[0].strip()
                sentence_dict[entity] = sentence_dict.get(entity, Entity(tag_pattern.tag_name))
                sentence_dict[entity].sentences.append(sentence)
                sentence_dict[entity].increment(len(entities))
    return sentence_dict


def print_dict_to_files(mydict, out_dir = OUTPUT_DATA_DIR, use_pickle = False):
    """Dump data to disk. In the event of any error, print an error message and
    call exit().
    If using pickle, dump the complete dict. If dumping plaintext, only dump the
    sentences associated with each Entity.
    Files are created under directory out_dir. File names are generated as
    follows:
    entity + '|' + tag

    void print_dict_to_files(dict mydict, str out_dir, bool use_pickle)
    dict mydict: dictionary of Entity s.
    str out_dir: path to directory in which to create the files. Defaults to
    value of global variable OUTPUT_DATA_DIR
    bool use_pickle: indicates whether to use pickle or to dump plaintext.
    Defaults to False (dump plaintext)

    IMPORTS: os, sys
        NOTE: There is no need to manually import pickle, as the function takes care
        of doing so if needed.
        WARNING: when using this function in python3, 'import cPickle as pickle'
        will fail. Replace by 'import pickle'
    GLOBAL CONSTANTS: OUTPUT_DATA_DIR"""

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
        for entity in mydict.keys():
            if isinstance(mydict[entity], list):
                for ent in mydict[entity]:
                    filename = entity + '|' + ent.tag_name
                    filepath = os.path.join(out_dir, filename)
                    try:
                        with open(filepath, "w") as f:
                            pickle.dump(mydict[entity], f)
                    except IOError, e:
                        sys.stderr.write("Error creating file\n")
                        exit(1)
            else:
                filename = entity + '|' + mydict[entity].tag_name
                filepath = os.path.join(out_dir, filename)
                try:
                    with open(filepath, "w") as f:
                        pickle.dump(mydict[entity], f)
                except IOError, e:
                    sys.stderr.write("Error creating file\n")
                    exit(1)
    else:
        for entity in mydict.keys():
            if isinstance(mydict[entity], list):
                for ent in mydict[entity]:
                    filename = entity + '|' + ent.tag_name
                    filepath = os.path.join(out_dir, filename)
                    try:
                        with open(filepath, "w") as f:
                            for sentence in ent.sentences:
                                f.write(sentence + '\n')
                    except IOError, e:
                        sys.stderr.write("Error creating file\n")
                        exit(1)
            else:
                filename = entity + '|' + mydict[entity].tag_name
                filepath = os.path.join(out_dir, filename)
                try:
                    with open(filepath, "w") as f:
                        for sentence in mydict[entity].sentences:
                            f.write(sentence + '\n')
                except IOError, e:
                    sys.stderr.write("Error creating file\n")
                    exit(1)


def main():
    tags = TAGS

    my_dict = associate_tags(tags, extract_sentences("./testfile"))
    for stuff in my_dict.keys():
        print stuff, "|", my_dict[stuff]
    exit(0)

    #####
    sentences = []
    my_dict = {}
    for arg in sys.argv:
        if os.path.isdir:
            merge_dicts(my_dict, create_dict([], argv))
        else:
            file_dict = associate_tags(tags, extract_sentences(arg))
            merge_dicts(my_dict, file_dict)


if __name__ == "__main__":
    main()
