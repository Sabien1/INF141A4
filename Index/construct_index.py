import re
from nltk.stem.snowball import SnowballStemmer
import os
from bs4 import BeautifulSoup
from bs4.element import Comment
import string
import unicodedata
from nltk.corpus import stopwords

class index():
    index = dict()
    stop_words = set(stopwords.words('english'))
    documents = 0
    unique_words = 0
    index_size = 0
    def __init__(self):
        print "init"

    '''Function tag_visible sourced from https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text'''
    def tag_visible(self, element):
        '''Detects visible content on page, returns true if it is visible'''
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    '''Function text_from_html sourced from https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text'''
    def text_from_html(self, body):
        '''extract all visible text from html document'''
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def build_index(self):
        '''Build the index.  Loops through all files, passes to helper functions to parse html and tokenize/stem'''
        root = "..\\WEBPAGES_RAW\\"
        '''Loop through all the dirs, extract content in each file.'''
        for path, subdirs, files in os.walk(root):
            for current_file in files:
                current_path = path + "\\" + current_file
                html_source = open(current_path).read()
                #print self.text_from_html(html_source)
                tokens = self.tokenize(self.text_from_html(html_source))
                tokens = self.stem(tokens)
                #print tokens
                #print "Removing number strings"
                tokens = self.remove_number_tokens(tokens)
                #print tokens
                self.add_to_index(tokens)
                #print self.index
        self.print_report()


        '''====Left off here, take tokens list and insert into dict, count frequencies, print to file.'''


    def tokenize(self, raw_input):
        '''Function takes a string and splits it into a list of individual words, mutated to lowercase'''

        '''tokenize the input, creates a list of strings'''

        token_list = re.sub("[^\w]", " ", raw_input.lower()).split()
        filtered_list = []
        for word in token_list:
            if word not in self.stop_words:
                filtered_list.append(word)
        return filtered_list

    def stem(self, token_list):
        '''Function takes a list of strings and stems each string'''
        '''create a stemmer object'''
        stemmer = SnowballStemmer('english', ignore_stopwords=True)
        stemmed_list = []
        for item in token_list:
            normal_string = stemmer.stem(item)
            normal_string = self.normalize_unicode(normal_string)
            stemmed_list.append(normal_string)
        #print stemmed_list
        #print "exiting stemmed function."
        return stemmed_list

    def remove_number_tokens(self, token_list):
        '''parse the list and remove all tokens that are numbers only.'''
        for item in token_list:
            if item.isdigit():
                token_list.remove(item)
        return token_list

    def normalize_unicode(self, string):
        '''convert any string of unicode into ascii'''
        string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
        return string

    def add_to_index(self, token_list):
        '''Parses list of tokens and adds to the index if they don't exist yet'''
        for token in token_list:
            if token in self.index:
                self.index[token] = self.index[token] + 1
            else:
                self.index[token] = 1
                self.unique_words = self.unique_words + 1

    def print_report(self):
        '''print data required for report.'''
        print "Unique words: " + str(self.unique_words + self.stop_words.__len__())
        f = open('index.txt', 'w')
        sorted(self.index.items(), key=lambda x: x[1], reverse=True)
        for key, value in self.index:
            f.write(str(key) + ": " + str(value) + "\n")
        f.close()

if __name__ == "__main__":
    test = index()
    test.build_index()