#!/usr/bin/env python2

import sys
try:
    from bs4 import BeautifulSoup
except ImportError:
	sys.stderr.write("{0} depends on python {1} module. Run 'pip install {1}' from a shell.\n".format(sys.argv[0], "beautifulsoup"))
	exit(1)

def main():
    print "Hello World!"


if __name__ == "__main__":
        main()
