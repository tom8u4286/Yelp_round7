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

        """self.switch"""
        """0:calculate origin matrix, 1:calculate without zero"""
        self.switch = int(sys.argv[1])

    def get_dir_list(self):
        self.dir_list_cos = os.listdir(self.cos_path)
        self.dir_list_dot = os.listdir(self.dot_path)
        self.dir_list_cor = os.listdir(self.coo_path)
        #print self.dir_list_dot

    def calculate(self):
        coo_matrix = []
        cos_matrix = []
        dot_matrix = []

        for fi in [1]:
            #num = re.search("[0-9]+", fi)

            """Load the matrix..."""
            #f1 = open("../data/line-data/cooccurrence_matrix/restaurant_*_cooccur_matrix.json")
            f1 = open("../data/line-data/cooccurrence_matrix/restaurant_1_cooccur_matrix.txt")
            coo_matrix = json.loads(f1.read())
            #print "length of coo_matrix:",len(coo_matrix)
            #print coo_matrix[0]
            coo_matrix = np.array(coo_matrix)
            #print "Size of coo_matrix:",coo_matrix.size
            #print "coo_matrix OK"

            """Load the cosine matrix..."""
            #f = open("../data/line-data/cosine_matrix/restaruant_%s_cosine.json"%num.group(0))
            """restaurant_1"""
            f2 = open("../data/line-data/cosine_matrix/restaruant_1_cosine.json")
            cos_matrix = json.loads(f2.read())
            #print "length of cos_matrix:",len(cos_matrix)
            cos_matrix = np.array(cos_matrix)
            #print "Size of cos_matrix:",cos_matrix.size
            #print "cos_matrix OK"

            """Load the dot matrix..."""
            #f = open("../data/line-data/cosine_matrix/restaruant_%s_cosine.json"%num.group(0))
            """restaurant_1"""
            f3 = open("../data/line-data/dot_matrix/restaruant_1_dot.json")
            dot_matrix = np.array(json.loads(f3.read()))
            #print "dot_matrix:", dot_matrix.size
            #print "dot_matrix OK"

            print self.switch
            if self.switch == 2:
                np.fill_diagonal(coo_matrix, 0)
                coo_matrix = coo_matrix.flatten()
                cos_matrix = cos_matrix.flatten()
                dot_matrix = dot_matrix.flatten()
                indices = np.nonzero(coo_matrix)
                new_coo_matrix = [coo_matrix[index] for index in indices]
                new_cos_matrix = [cos_matrix[index] for index in indices]
                new_dot_matrix = [dot_matrix[index] for index in indices]
                print "------------without zero and diagonal------------"
                print "coo and cos: ", np.corrcoef(new_coo_matrix,new_cos_matrix)[0][1]
                print "coo and dot: ", np.corrcoef(new_coo_matrix,new_dot_matrix)[0][1]


            if self.switch == 1:
                coo_matrix = coo_matrix.flatten()
                cos_matrix = cos_matrix.flatten()
                dot_matrix = dot_matrix.flatten()
                indices = np.nonzero(coo_matrix)
                new_coo_matrix = [coo_matrix[index] for index in indices]
                new_cos_matrix = [cos_matrix[index] for index in indices]
                new_dot_matrix = [dot_matrix[index] for index in indices]
                print "------------------without zero-------------------"
                print "coo and cos: ", np.corrcoef(new_coo_matrix,new_cos_matrix)[0][1]
                print "coo and dot: ", np.corrcoef(new_coo_matrix,new_dot_matrix)[0][1]


            if self.switch == 0:
                coo_matrix = coo_matrix.flatten()
                cos_matrix = cos_matrix.flatten()
                dot_matrix = dot_matrix.flatten()
                print "------------------origin matrix------------------"
                print "coo and cos: ", np.corrcoef(coo_matrix, cos_matrix)[0][1]
                print "coo and cos: ", np.corrcoef(coo_matrix, dot_matrix)[0][1]

if __name__ == '__main__':
    cor = Correlations()
    cor.get_dir_list()
    cor.calculate()
