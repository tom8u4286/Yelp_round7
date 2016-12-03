import json, sys, uuid, os

class DishScore:

    def __init__(self):

        self.vec200_src = "../data/line-data/vectors/200dim/restaurant_1_vector200.txt"
        self.rest_dic_src ="../data/coreProcess_word2vec/restaurant_dict_list.json"
        self.lex_pos = "../data/lexicon/stanfer/positive.txt"
        self.lex_neg = "../data/lexicon/stanfer/negative.txt"

        self.rest_dic = {}

    def calculate(self):
        """get the 200dim vectors of words trained by line."""
        vectors = []
        f = open(self.vec200_src)
        next(f)
        vectors = [line.split(" ")[:-1] for line in f]
        words = [word[0] for word in vectors]

        """load the restaurant dic list"""
        rest_dic = json.load(open(self.rest_dic_src))

        """get the number of restaurant"""
        rest_num = int(self.vec200_src.split("/")[5].split("_")[1])
        print "rest_num: ", rest_num

        """get the menu of restaurant"""
        dic = {}
        for rest in rest_dic:
            if rest['index'] == rest_num:
                dic = rest
                break
            else:
                dic = None

        """get the lexicon"""
        pos_words = [line for line in open(self.lex_pos)]
        neg_words = [line for line in open(self.lex_neg)]

        """caculate the dish score"""
        for dish in dic["menu"]:
            cos_avg_score = -2
            """get the index of words."""
            index = words.index(dish["name_ar"])


if __name__ == "__main__":
    dishScore = DishScore()
    dishScore.calculate()
