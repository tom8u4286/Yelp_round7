import json
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine

class FindNearestSentiment:

    def __init__(self):
        self.w = "../../data/coreProcess_word2vec_stars/unique_words_word2vec.txt"
        self.vec = "../../data/coreProcess_word2vec_stars/vectors300_word2vec.txt"
        self.lexicon = "../../data/sentiment_statistics/total.json"

        self.sentiment_list = []

        self.testing = 1

    def get_sentiment_list(self):
        "This function aims to find the sentiment words which appears more than 100 times."

        f = open(self.lexicon)
        lexicon = json.load(f)

        for word in lexicon:
            if word["count"] >= 100:
                self.sentiment_list.append(word["word"])

        if self.testing == 1:
            print "Type of lexicon: "+ type(lexicon)
            print "Length of lexicon list:"+ len(self.sentiment_list)

    def caculate(self):
        "This function aims to caculate the cosine similarity of stars and sentiment words."

        star_dic = {}
        unique_words = [line.rstrip('\n') for line in open(self.w)]
        print "start putting vecs..."
        vec = [json.loads(line) for line in open(self.vec)]

        #one = unique_words.index("1star")
        #two = unique_words.index("2star")
        #three = unique_words.index("3star")
        #four = unique_words.index("4star")
        #five = unique_words.index("5star")

        starlist = ["1star", "2star", "3star", "4star", "5star"]
        index_of_star_word = [unique_words.index(star) for star in starlist]

        A = np.array(vec)
        cos_array = 1-pairwise_distances(A, metric="cosine")

        print "start caculate np-array and finding nearest..."
        word_lists = []
        for index in index_of_star_word:
            """Caculate the array of cosine distance of every unique word using np-array"""

            """find the vector of cosine distance of '1star' from the caculated array """
            distance_vector = cos_array[index].tolist()
            """Sort the vector of cosine distance of '1star' and find the index of nearest 10 words.(largest cosine similarity)"""
            sorted_index = sorted(range(len(distance_vector)), key=lambda k:distance_vector[k])[::-1][:30]

            word_list = [unique_words[word] for word in sorted_index]
            word_lists.append(word_list)

        dic_list = []
        for i in range(len(starlist)):
            dic = {}
            dic["word"] = starlist[i]
            dic["nearest"] = word_lists[i]
            dic_list.append(dic)

        f = open('Nearest_word.json','w+')
        f.write(json.dumps(dic_list, indent=4))

        print "FindNearestSentiment.py is done."

if __name__ == '__main__':
    findNearest = FindNearestSentiment()
    findNearest.caculate()
