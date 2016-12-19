import json, sys, uuid, os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re

class DishScore:

    def __init__(self):

        """sys.argv[0] ../data/line-data/vectors/200dim/restaurant_1_vector200.txt"""
        self.vec200_src = sys.argv[1]
        self.rest_num = int(re.search("_([0-9]+)_", sys.argv[1].split("/")[5]).group(1))
        self.rest_dic_src ="../data/coreProcess_word2vec/restaurant_dict_list.json"
        self.rest_dic = {}

    def get_words_and_vectors(self):
        words = []
        vectors = []
        f_vec200 = open(self.vec200_src)
        length = int(next(f_vec200).split(" ")[0])
        for line in f_vec200:
            word_vec = line.split(" ")
            words.append(word_vec[0])
            vec = [float(num) for num in word_vec[1:-1]]
            vectors.append(vec)
        return words, vectors

    def get_rest_name(self):
        f_res_dic = open(self.rest_dic_src)
        rest_dic = json.load(f_res_dic)
        rest_name = ""
        for rest in rest_dic:
            if rest["index"] == self.rest_num:
                rest_name = rest["restaurant_name"]
        return rest_name

    def get_indices(self, words, vectors):
        senti_indices = []
        dish_indices = []
        rest_name = self.get_rest_name().lower().replace(" ","-")
        print "rest name:",rest_name
        for idx, word in enumerate(words):
            if "_senti" in word:
                senti_indices.append(idx)
            elif rest_name in word:
                dish_indices.append(idx)

        return senti_indices, dish_indices

    def calculate(self):
        """2017/12/18 Tom"""
        """Render the cosine matrix."""
        words, vectors = self.get_words_and_vectors()
        senti_indices, dish_indices = self.get_indices(words, vectors)
        A = np.array(vectors)
        cos_matrix = cosine_similarity(A)

        dish_list = []
        for dish_index in dish_indices:
            dic = {}
            dic["dish"] = words[dish_index]
            avg_cos = sum( [cos_matrix[dish_index][senti_index] for senti_index in senti_indices] )/len(senti_indices)
            max_cos = max( [cos_matrix[dish_index][senti_index] for senti_index in senti_indices] )
            max_word = words[ list(cos_matrix[dish_index]).index(max_cos) ]
            dic["avg_cos"] = avg_cos
            dic["max_cos"] = max_cos
            dic["max_word"] = max_word
            dish_list.append(dic)

        return dish_list

    def render(self,dish_list):
        f = open("../data/line-data/dish_senti_cos/restaurant_%s.json"%self.rest_num,"w+")
        f.write(json.dumps(dish_list ,indent = 4))
        f.close()

if __name__ == "__main__":
    dishScore = DishScore()
    dish_list = dishScore.calculate()
    dishScore.render(dish_list)
