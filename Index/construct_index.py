import re
from nltk.stem.snowball import SnowballStemmer
import os
from bs4 import BeautifulSoup
from bs4.element import Comment

class index():
    index = dict()

    def __init__(self):
        print "init"

    '''Function tag_visible sourced from https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text'''
    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    '''Function text_from_html sourced from https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text'''
    def text_from_html(self, body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def build_index(self):
        '''Build the index'''
        '''root = "..\\WEBPAGES_RAW"
        Loop through all the dirs, extract content in each file.
        for path, subdirs, files in os.walk(root):
            for current_file in files:
                print current_file'''

        html_source = open("C:\\Users\\resca\\Documents\\test.html").read()
        print self.text_from_html(html_source)





    def tokenize(self, raw_input):
        '''Function takes a string and splits it into a list of individual words, mutated to lowercase'''

        '''tokenize the input, creates a list of strings'''

        token_list = re.sub("[^\w]", " ", raw_input.lower()).split()
        return token_list

    def stem(self, token_list):
        '''Function takes a list of strings and stems each string'''
        '''create a stemmer object'''
        stemmer = SnowballStemmer('english', ignore_stopwords=True)
        stemmed_list = []
        for item in token_list:
            stemmed_list.append(stemmer.stem(item))
        #print, for testing only.   ==== REMOVE ====
        print stemmed_list



if __name__ == "__main__":
    test = index()

    #test.stem(test.tokenize("Hello my name is Bob.  I'm awesome, and I'm not married.  Glory be to the gods.  Words, tokenization, glorification"))
    test.build_index()