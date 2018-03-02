import re
from nltk.stem.snowball import SnowballStemmer
import os
from bs4 import BeautifulSoup
from bs4.element import Comment
import unicodedata
from nltk.corpus import stopwords
from collections import defaultdict
import math

class index():
    '''Calculate an inverse index of a corpus'''

    '''term_unique_count is dictionary to keep track of total unique occurrances of each term in entire corpus'''
    term_unique_count = dict()

    '''term_frequency is the number of times a term appears in a given document'''
    term_frequency = defaultdict(int)

    '''document_index is the mapping of terms to their doc_id (record of which documents a term appeared in)'''
    document_index = defaultdict(list)

    '''tf_idf_score keeps track of the tf-idf score of each term'''
    tf_idf_weight = defaultdict(float)

    '''doc_term_count is the number of times a key term appeared in a specific document.'''
    doc_term_count = defaultdict(lambda: defaultdict(int))

    stop_words = set(stopwords.words('english'))
    documents = 0
    unique_words = 0
    index_size = 0
    def __init__(self):
        '''Count directories in root dir, for idf calculation'''
        print "init"
        root = "..\\WEBPAGES_RAW\\"
        for root, dirs, files in os.walk(root):
            self.documents += len(files)
        #print str(self.documents) + " files exist."

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

    def calculate_idf(self, df):
        idf = math.log((self.documents / df), 10)
        return idf

    def calculate_tf(selfself, tf):
        wtf = 1 + math.log(tf, 10)
        return wtf

    def build_index(self):
        '''Build the index.  Loops through all files, passes to helper functions to parse html and tokenize/stem'''
        root = "..\\WEBPAGES_RAW\\"
        '''Loop through all the dirs, extract content in each file.'''
        for path, subdirs, files in os.walk(root):
            for current_file in files:
                self.term_frequency.clear()
                #print "Path: " + str(path)
                #print "Subidrs is " + str(subdirs)
                #print "File: " + str(files)
                #print "Current file: " + str(current_file)
                parent_directory = path.split(os.path.sep)[-1]

                doc_ID = str(parent_directory + "\\" + current_file)
                #print doc_ID

                #print "Parent:  " + str(parent_directory)
                current_path = path + "\\" + current_file
                html_source = open(current_path).read()
                #print self.text_from_html(html_source)
                tokens = self.tokenize(self.text_from_html(html_source))
                tokens = self.stem(tokens)
                #print "Removing number strings"
                tokens = self.remove_number_tokens(tokens)
                for token in tokens:
                    if token in self.term_unique_count:
                        self.term_unique_count[token] += 1
                    else:
                        self.term_unique_count[token] = 1
                        self.unique_words = self.unique_words + 1
                    self.document_index[token].append(doc_ID)
                    self.term_frequency[token] += 1

                for token2 in tokens:
                    self.doc_term_count[token2][doc_ID] = self.term_frequency[token2]

                print self.doc_term_count


                    #print self.doc_term_count
                #print self.doc_term_count
                #print self.term_unique_count
                #print self.document_index
                #print tokens
                ##self.add_to_index(tokens)
                #print self.index
        for token3 in

        for key in self.document_index:
            df = len(self.document_index[key])
            print self.calculate_idf(df)
        self.print_report()

        return
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
        return stemmed_list

    def remove_number_tokens(self, token_list):
        '''parse the list and remove all tokens that are numbers only.'''
        length = token_list.__len__()
        i = 0
        while i < length:
            if self.is_number(token_list[i]):
                del token_list[i]
                length -= 1
            else:
                i += 1
        return token_list

    def normalize_unicode(self, string):
        '''convert any string of unicode into ascii'''
        string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
        return string

    '''function is depricated'''
    #def add_to_index(self, token_list):
        #'''Parses list of tokens and adds to the index if they don't exist yet'''
        #for token in token_list:
            #if token in self.index:
                #self.index[token] = self.index[token] + 1
           # else:
                #self.index[token] = 1
               # self.unique_words = self.unique_words + 1

    '''is_number function sourced from https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/'''
    def is_number(self, s):
        '''determine if the string s is a digit.'''
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False


    def print_report(self):
        '''print data required for report.'''
        print "Unique words: " + str(self.unique_words + self.stop_words.__len__())
        f = open('index.txt', 'w')
        sorted(self.index.items(), key=lambda x: x[1], reverse=True)
        for key in self.index:
            f.write(str(key) + ": " + str(self.index[key]) + "\n")
        f.close()
        print "I work hard every fucking day."



if __name__ == "__main__":
    test = index()
    test.build_index()