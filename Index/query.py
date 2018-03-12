import json
from nltk.stem.snowball import SnowballStemmer
import operator

class Query:


    json_data = "index.json"
    file = open(json_data)
    f = json.load(file)
    def __init__(self):
        print "Query Object Created"
        print "Loading Index File " + self.json_data


    # def query(self, query_terms):
    #     index_json = json.load(open(".\\json_test.json"))
    #     for i in query_terms:
    #         print "Queried for " + str(i)
    #         print "Found in file: "
    #         print index_json[i]

    def stem(self, search_term):
        """Function takes a list of strings and stems each string"""
        '''create a stemmer object'''
        stemmer = SnowballStemmer('english', ignore_stopwords=True)
        normal_string = stemmer.stem(search_term)
        #//Not implemented:  normal_string = self.normalize_unicode(normal_string)
        return normal_string

    def retrieve_data(self, term):

        stemmed = self.stem(term)
        ranking = dict()
        for doc in self.f[stemmed]:
            ranking[doc] = (self.f[stemmed][doc]["tf_idf"], self.f[stemmed][doc]["url"])
            #print ranking
        sorted_list = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
        ranked_urls = list()
        print sorted_list
        i = 0
        for v in sorted_list:
            ranked_urls.append(sorted_list[i][1][1])
        print ranked_urls
        return sorted_list


if __name__ == "__main__":
    test = Query()
    test.retrieve_data("research")
