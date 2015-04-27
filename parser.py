#!/usr/bin/env python2

import sys, re
try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.stderr.write("{0} depends on python {1} module. Run 'pip install {1}' from a shell.\n".format(sys.argv[0], "BeautifulSoup"))
    exit(1)

try:
    import urllib2
except ImportError:
    sys.stderr.write("{0} depends on python {1} module. Run 'pip install {1}' from a shell.\n".format(sys.argv[0], "urllib"))
    exit(1)

def http_download(url):
    # max file size 100MB
    maxFileSize = 1024*1024*100
    try:
        request = urllib2.urlopen(url)
        data = request.read(maxFileSize)
        # if file too large
        if request.read(1) != '':
            return None
        else:
            return data
    except urllib2.HTTPError, e:
        print("urllib2.HttpError")
        exit()
    except urllib2.URLError, e:
        print("urllib2.URLError")
        exit()


def extract_tags(text):
    tag_regex = re.compile("\[\[([^:\[\]]*:?)*\]\]")
    return [ str(tag).strip("[]") for tag in
        tag_regex.findall(text) if not str(tag).strip("[]").startswith(":")]


def main():
    dico = {}
    for arg in sys.argv[1:]:
        try:
            with open(arg) as myfile:
                soup = BeautifulSoup(myfile)
                for tag in extract_tags(soup.text):
                    dico[tag] = True
                for tag in dico.keys():
                    print tag
        except IOError, e:
            sys.stderr.write("{0}\n".format(e))


if __name__ == "__main__":
    main()
