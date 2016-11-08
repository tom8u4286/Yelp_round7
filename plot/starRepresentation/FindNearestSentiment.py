import json


class FindNearestSentiment:

    def __init__(self):
        self.w = "../../data/coreProcess_word2vec_stars/unique_words_word2vec.txt"
        self.vec2 = "../../data/coreProcess_word2vec_stars/"
        self.lexicon = "../../data/sentiment_statistics/total.json"


    def Caculate(self):

