# -*- coding: utf-8 -*-

import sys, getopt
import wikipedia
import threading
from time import sleep
import requests
import random


API_URL = 'http://%s.wikipedia.org/api/rest_v1/page/random/summary'
SPECIAL = '\\!\"/()[]{}=?\'<>,;.:-—_+*@#«»'


class WikipediaWordList:

    def __init__(self,
        pages = 100,
        lang = 'en',
        special_chars = SPECIAL,
        min_length = 1,
        max_length = 0,
        threads = 1,
        timeout = 30
    ):
        self.pages = pages
        self.lang = lang
        self.special_chars = special_chars
        self.min_length = min_length
        self.max_length = max_length
        self.threads = threads
        self.timeout = timeout

    def get_random_title(self):
        # return wikipedia.random(self.pages)   # Not sure this is random
        response = requests.get(API_URL % self.lang)
        return response.json()['title']

    def get_page_content(self, title):
        page = wikipedia.page(title)
        return page.content

    def valid_length(self, word):
        m = self.min_length
        M = self.max_length
        l = len(word)
        return (M == 0 or l <= M) and l >= m

    def format_line(self, line):
        wordlist = []
        for char in self.special_chars:
            line = line.replace(char, ' ')
        for word in line.split(' '):
            if self.valid_length(word):
                wordlist.append(word.lower())
        return wordlist

    def format_page(self, page_content):
        wordlist = []
        for line in page_content.split('\n'):
            if line != '' and line[0] != '=':   # Header lines look like '== Header =='
                wordlist += self.format_line(line)
        return wordlist

    def retrieve_words(self, i, wordlist):
        try:
            title = self.get_random_title()
            print('Page #%d > %s' % (i + 1, title))
            page_content = self.get_page_content(title)
            words = self.format_page(page_content)
            print('Page #%d > Retrieved %d words' % (i + 1, len(words)))
            wordlist += words
        except:
            print('Page #%d > Something went wrong' % (i + 1))

    def wait_for_responses(self):
        i = 0
        T = self.timeout
        while threading.active_count() > 1 and (T == 0 or i < T):
            sleep(1)
            i += 1

    def generate_wordlist(self):
        wikipedia.set_lang(self.lang)
        wordlist = []
        for i in range(self.pages):
            while threading.active_count() > self.threads:
                sleep(1)
            threading.Thread(
                target = self.retrieve_words,
                args = (i, wordlist)
            ).start()
        self.wait_for_responses()
        return wordlist

    def sort_wordlist(self, word_count):
        print('Sorting %d unique words by frequency...' % len(word_count))
        sorted_wordlist = []
        for word, count in word_count.items():
            sorted_wordlist.append((count, word))
        sorted_wordlist.sort(reverse = True)
        return sorted_wordlist

    def generate_sorted_wordlist(self):
        wordlist = self.generate_wordlist()
        word_count = {}
        for word in wordlist:
            if not word in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1
        return self.sort_wordlist(word_count)

    def save_sorted_wordlist(self, filename, n = 0):
        sorted_wordlist = self.generate_sorted_wordlist()
        words = len(sorted_wordlist)
        max = words if n == 0 or n > words else n
        print('Saving %d unique words...' % words)
        f = open(filename, 'w', encoding = 'utf-8')
        for i in range(max):
            word_freq = sorted_wordlist[i]
            f.write(word_freq[1] + '\n')
        f.close()


if __name__ == '__main__':

    help = '''

        Usage:          wwl.py [OPTIONS]


        Description:    Creates a list of words from Wikipedia's random pages,
                        and saves them sorted by their frequency.


        Options:        -h, --help
                        Shows this message.

                        -p, --pages (NUMBER)
                        Sets the number of pages to process (default 100).

                        -l, --lang (ISO-CODE)
                        Sets the language of the pages to retrieve (default "en").

                        -s, --special (STRING)
                        Sets the special chars to use as splitters (the space is always used, default "\\\\!\\"/()[]{}=?\\'<>,;.:-—_+*@#«»").

                        -m, --min (NUMBER)
                        Sets the minimum length of the words to process (default 1).

                        -M, --max (NUMBER)
                        Sets the maximum length of the words to process (0 for infinity, default 0).

                        -t, --threads (NUMBER)
                        Sets the maximum amount of threads working simultanously to retrieve pages (default 1).

                        -T, --timeout (NUMBER)
                        Sets the maximum time (in seconds) to wait for the threads to retrieve the pages once the last thread started (0 for infinity, default 30).

                        -o, --output (FILENAME)
                        Specifies the output file (default "output.txt").

                        -w, --words (NUMBER)
                        Specifies the maximum number of words to save (0 for infinity, default 0).


        Example:        wwl.py -p 1000 -l it -m 8 -t 50 -w 100
                        Saves 100 most common words of 8 or more characters out of 1000 italian pages, using 50 threads.

    '''

    # Default parameters
    pages = 100
    lang = 'en'
    special_chars = SPECIAL
    min_length = 1
    max_length = 0
    threads = 1
    timeout = 30
    output = 'output.txt'
    words = 0

    # Get user arguments
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            'hp:l:s:m:M:t:T:o:w:',
            [
                'help',
                'pages=',
                'lang=',
                'special=',
                'min=',
                'max=',
                'threads=',
                'timeout=',
                'output=',
                'words='
            ]
        )
    except getopt.GetoptError:
        print(help)
        sys.exit()
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print(help)
            sys.exit()
        elif opt in ['-p', '--pages']:
            pages = int(arg)
        elif opt in ['-l', '--lang']:
            lang = arg
        elif opt in ['-s', '--special']:
            special_chars = arg
        elif opt in ['-m', '--min']:
            min_length = int(arg)
        elif opt in ['-M', '--max']:
            max_length = int(arg)
        elif opt in ['-t', '--threads']:
            threads = int(arg)
        elif opt in ['-T', '--timeout']:
            timeout = int(arg)
        elif opt in ['-o', '--output']:
            output = arg
        elif opt in ['-w', '--words']:
            words = int(arg)

    # Create wwl object
    wwl = WikipediaWordList(
        pages,
        lang,
        special_chars,
        min_length,
        max_length,
        threads,
        timeout
    )

    # Run wwl and save the result
    wwl.save_sorted_wordlist(output, words)
    print('DONE!')
