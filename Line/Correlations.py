"""This program aims to caculate the correlation between two matrix, cooccur matrix and cosine matrix or dot matrix."""
import os, sys
import re
import json
import numpy as np
from numpy import corrcoef

class Correlations:
    def __init__(self):
        #self.src = sys.argv[1]
        self.dir_list_cos = []
        self.cos_path = "../data/line-data/cosine_matrix/"
        self.dir_list_dot = []
        self.dot_path = "../data/line-data/dot_matrix/"
        self.dir_list_cor = []
        self.coo_path = "../data/line-data/cooccurrence_matrix/"
    def get_dir_list(self):
        self.dir_list_cos = os.listdir(self.cos_path)
        self.dir_list_dot = os.listdir(self.dot_path)
        self.dir_list_cor = os.listdir(self.coo_path)
        #print self.dir_list_dot

    def caculate(self):
        coo_matrix = []
        cos_matrix = []
        dot_matrix = []

        for fi in [1]:
            #num = re.search("[0-9]+", fi)

            """Load the matrix..."""
            #f1 = open("../data/line-data/cooccurrence_matrix/restaurant_*_cooccur_matrix.json")
            f1 = open("../data/line-data/cooccurrence_matrix/restaurant_1_cooccur_matrix.txt")
            coo_matrix = np.array(json.loads(f1.read()))
            #coo_matrix = coo_matrix.flatten()
            print coo_matrix.size
            print "coo_matrix OK"

            """Load the cosine matrix..."""
            #f = open("../data/line-data/cosine_matrix/restaruant_%s_cosine.json"%num.group(0))
            """restaurant_1"""
            f2 = open("../data/line-data/cosine_matrix/restaruant_1_cosine.json")
            cos_matrix = np.array(json.loads(f2.read()))
            #cos_matrix = cos_matrix.flatten()
            print cos_matrix.size
            print "cos_matrix OK"

            """Load the dot matrix..."""
            #f = open("../data/line-data/cosine_matrix/restaruant_%s_cosine.json"%num.group(0))
            """restaurant_1"""
            f3 = open("../data/line-data/dot_matrix/restaruant_1_dot.json")
            dot_matrix = np.array(json.loads(f3.read()))
            #dot_matrix = dot_matrix.flatten()
            print dot_matrix.size
            print "dot_matrix OK"




if __name__ == '__main__':
    cor = Correlations()
    cor.get_dir_list()
    cor.caculate()
