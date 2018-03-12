import re
from nltk.stem.snowball import SnowballStemmer
import os
from bs4 import BeautifulSoup
from bs4.element import Comment
import unicodedata
from nltk.corpus import stopwords
from collections import defaultdict
from term_data import term_data
import math
import winsound
import json
import jsonpickle


class Index:
    """Calculate an inverse index of a corpus"""

    '''term_unique_count is dictionary to keep track of total unique occurrances of each term in entire corpus'''
    term_unique_count = dict()

    '''term_frequency is the number of times a term appears in a given document'''
    term_frequency = defaultdict(int)

    '''document_index is the mapping of terms to their doc_id (record of which documents a term appeared in)
        (AKA posting list)'''
    document_index = defaultdict(list)

    '''doc_term_count is the number of times a key term appeared in a specific document.'''
    doc_term_count = dict(dict())

    '''loaded_dict is a dictionary to compile all required info into a single data structure, 
        so it can be printed to a JSON file'''
    loaded_dict = dict(list(defaultdict(float)))

    stop_words = set(stopwords.words('english'))
    documents = 0
    unique_words = 0
    index_size = 0

    def __init__(self):
        """Count directories in root dir, for idf calculation"""
        root = "..\\WEBPAGES_RAW\\4"
        for root, dirs, files in os.walk(root):
            self.documents += len(files)

    '''Function tag_visible sourced from 
        https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text'''
    def tag_visible(self, element):
        '''Detects visible content on page, returns true if it is visible'''
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    '''Function text_from_html sourced from 
        https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text'''
    def text_from_html(self, body):
        '''extract all visible text from html document'''
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def calculate_idf(self, df):
        if df == 0:
            return 0
        else:
            idf = math.log10((float(self.documents) / float(df)))
        return idf

    def calculate_tf(self, tf):
        wtf = 1 + math.log10(float(tf))
        return wtf

    def build_index(self):
        """Build the index.  Loops through all files, passes to helper functions to parse html and tokenize/stem"""

        root = "..\\WEBPAGES_RAW\\4"
        '''Loop through all the dirs, extract content in each file.'''

        bookkeeper = json.load(open("..\\WEBPAGES_RAW\\bookkeeping.json"))
        print bookkeeper
        for path, subdirs, files in os.walk(root):
            for current_file in files:
                '''clear term_frequency for next HTML file'''
                self.term_frequency.clear()
                '''Get the parent directory, used to map terms to "doc_id"'''
                parent_directory = path.split(os.path.sep)[-1]
                '''Create the doc_id using parent directory and the current file.'''
                doc_id = str(parent_directory + "\\" + current_file)
                print doc_id
                current_path = path + "\\" + current_file
                html_source = open(current_path).read()
                tokens = self.tokenize(self.text_from_html(html_source))
                tokens = self.stem(tokens)
                tokens = self.remove_number_tokens(tokens)
                for token in tokens:
                    if token in self.term_unique_count:
                        self.term_unique_count[token] += 1
                    else:
                        self.term_unique_count[token] = 1
                        self.unique_words = self.unique_words + 1
                    self.document_index[token].append(doc_id)
                    self.term_frequency[token] += 1
                '''At this time, 'tokens' holds a list of every token in the current document.
                    doc_id is the current document.  document_index '''
                for token2 in tokens:
                    self.doc_term_count[token2] = dict()
                    print bookkeeper[str(doc_id)]
                    #self.doc_term_count[token2][doc_id] = term_data(bookkeeper[doc_id], 0.0, )

        for token5 in self.doc_term_count:
            for doc5 in self.doc_term_count[token5]:
                print self.doc_term_count[token5][doc5]
        #self.print_report()
        return

    def tokenize(self, raw_input):
        """Function takes a string and splits it into a list of individual words, mutated to lowercase"""

        '''tokenize the input, creates a list of strings'''

        token_list = re.sub("[^\w]", " ", raw_input.lower()).split()
        filtered_list = []
        for word in token_list:
            if word not in self.stop_words:
                filtered_list.append(word)
        return filtered_list

    def stem(self, token_list):
        """Function takes a list of strings and stems each string"""
        '''create a stemmer object'''
        stemmer = SnowballStemmer('english', ignore_stopwords=True)
        stemmed_list = []
        for item in token_list:
            normal_string = stemmer.stem(item)
            normal_string = self.normalize_unicode(normal_string)
            stemmed_list.append(normal_string)
        return stemmed_list

    def remove_number_tokens(self, token_list):
        """parse the list and remove all tokens that are numbers only."""
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
        """convert any string of unicode into ascii"""
        string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
        return string

    '''is_number function sourced from https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/'''
    def is_number(self, s):
        """determine if the string s is a digit."""
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
        """print data required for report."""

        '''Read the JSON file into memory'''
        urls = json.load(open('..\\WEBPAGES_RAW\\bookkeeping.json'))


        f = open('index.json', 'w')
        print "Unique words: " + str(self.unique_words + self.stop_words.__len__())
        #f.write("Unique words: " + str(self.unique_words + self.stop_words.__len__()))
        print "Total documents: " + str(self.documents)
        #f.write("\nTotal documents: " + str(self.documents) + "\n")
        #f.write("{")

        for token3 in self.doc_term_count:
            #f.write("Term: " + str(token3))
            for doc in self.doc_term_count[token3]:
                tf = self.calculate_tf(self.doc_term_count[token3][doc].term_frequency)
                idf = self.calculate_idf(len(self.document_index[token3]))
                tf_idf_score = tf * idf
                self.doc_term_count[token3][doc].tf_idf = tf_idf_score
                #print "\t" + str(doc) + ": " + str(tf_idf)
                #f.write("\n\t" + str(doc) + ": " + str(tf_idf))
        #f.write("}")
        for token4 in self.doc_term_count:
            for doc2 in self.doc_term_count[token4]:
                print token4
                print self.doc_term_count[token4][doc2].tf_idf
                print ""

        f.close()



if __name__ == "__main__":
    test = Index()
    test.build_index()
    duration = 1000  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)