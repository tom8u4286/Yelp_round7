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
        print "start putting vecs"
        vec = [json.loads(line) for line in open(self.vec)]

        one = unique_words.index("1star")
        two = unique_words.index("2star")
        three = unique_words.index("3star")
        four = unique_words.index("4star")
        five = unique_words.index("5star")

        print "start caculate np-array"
        A = np.array(vec)
        cos_array = 1-pairwise_distances(A, metric="cosine")

        one_array = cos_array[one].tolist()
        one_sorted_index = sorted(range(len(one_array)), key=lambda k:one_array[k])[::-1][:10]

        for index in one_sorted_index:
            print unique_words[index]

        #for index in one_sorted_index:
        #    print unique_words[index]

        #two_array = cos_array[two]
        #three_array = cos_array[three]
        #four_array = cos_array[four]
        #five_array = cos_array[five]
        #print one_array

        #print np.argmax(one_array)
        #print np.sort(one_array[10:])
        #print np.amax(one_array)


if __name__ == '__main__':
    findNearest = FindNearestSentiment()
    findNearest.caculate()
