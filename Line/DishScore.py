import json, sys, uuid, os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import OrderedDict

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

    def rank(self, dish_list):
        dish_list = sorted(dish_list, key=lambda k: k['max_cos'], reverse=True)
        for i in range( 0, len(dish_list)):
            dish_list[i]["rank_by_max"] = i+1

        dish_list = sorted(dish_list, key=lambda k: k['avg_cos'], reverse=True)
        for i in range( 0, len(dish_list)):
            dish_list[i]["rank_by_avg"] = i+1

        """Indention problem"""
        #dish_list = [ NoIndent(item) for item in dish_list ]
        ordered_dict_list = []
        for item in dish_list:
            ordered_dict = OrderedDict()
            ordered_dict["dish"] = item["dish"]
            ordered_dict["rank_by_avg"] = item["rank_by_avg"]
            ordered_dict["rank_by_max"] = item["rank_by_max"]
            ordered_dict["avg_cos"] = item["avg_cos"]
            ordered_dict["max_cos"] = item["max_cos"]
            ordered_dict["max_word"] = item["max_word"]
            ordered_dict_list.append(ordered_dict)

        return ordered_dict_list

    def render(self, dish_list):
        f = open("../data/line-data/dish_senti_cos/restaurant_%s_sortByAvg.json"%self.rest_num,"w+")
        f.write(json.dumps(dish_list ,indent = 4))
        f.close()


class NoIndent(object):
    def __init__(self, value):
        self.value = value

class NoIndentEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(NoIndentEncoder, self).__init__(*args, **kwargs)
        self.kwargs = dict(kwargs)
        del self.kwargs['indent']
        self._replacement_map = {}

    def default(self, o):
        if isinstance(o, NoIndent):
            key = uuid.uuid4().hex
            self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
            return "@@%s@@" % (key,)
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)
        for k, v in self._replacement_map.iteritems():
            result = result.replace('"@@%s@@"' % (k,), v)
        return result

if __name__ == "__main__":
    dishScore = DishScore()
    dish_list = dishScore.calculate()
    rank_by_avg = dishScore.rank(dish_list)
    dishScore.render(rank_by_avg)
