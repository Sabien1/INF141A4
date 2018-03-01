import re
from nltk.stem.snowball import SnowballStemmer

class index():

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

    test.stem(test.tokenize("Hello my name is Bob.  I'm awesome, and I'm not married.  Glory be to the gods.  Words, tokenization, glorification"))