from collections import defaultdict
import json
import jsonpickle

class term_data():
    '''Object definition for a term_data object.  Contains data members to keep track of information for search terms'''

    def __init__(self, str_url=None, str_tf_idf=0.0, str_term_frequency=0):

        '''url holds the URL that pairs with the document ID'''
        self.url = str_url

        '''tf_idf is the tf-idf score for the term/document pair.'''
        self.tf_idf = str_tf_idf

        '''frequency is the term frequency within the specified document (not currently used)'''
        self.term_frequency = str_term_frequency




if __name__ == "__main__":
    test = dict(dict())

    data = {'0': term_data('test1', 1.1, 5)}
    data2 = {'1': term_data('test2', 2.1, 10)}
    test['term'] = data
    test['term2'] = data2


    print jsonpickle.encode(test, unpicklable=False)

    f = open('pickle_test.json', 'w')
    f.write(jsonpickle.encode(test))


