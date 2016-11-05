import matplotlib
import matplotlib.pyplot as plt
import json
#import numpy as np


class Plot:

    def __init__(self):
        self.w = "../../data/coreProcess_word2vec/unique_words_word2vec.txt"
        self.vec2 = "../../data/coreProcess_word2vec/vectors2_word2vec.txt"

    def get_vec2(self, senti):
        word = open(self.w)
        #vec2 = open( self.vec2 )

        cnt = 1
        for line in word:
            if senti+"\n" in line:
                print line
                print "line number:", cnt
                break
            cnt += 1

        with open(self.vec2) as f:
            for i, line in enumerate(f):
                if i+1 == cnt:
                    vec = line.replace("\n","")
                    print "vector:", vec
                    return json.loads(vec)

    def render(self):
        testing_list = ["great","good", "better", "best", "bad", "worse", "worst", "nice", "nicer", "nicest", ]
        testing_list2 = [ "astonished", "astonishing", "astonishingly", "awesome", "awesomely", "awesomeness",
                "beauty", "beautiful", "beautifully","flexibility", "flexible",
                "abundance" ,"abundant",
                "acceptable", "acceptance",
                "admire", "admirer"]

        matplotlib.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        ax.set_xlim( -1, 1)
        ax.set_ylim( -1, 1)

        for item in testing_list:
            vec = self.get_vec2(item)
            ax.plot( vec[0], vec[1], 'go')
            plt.text( vec[0]+0.01, vec[1] +0.01, item)

        for item in testing_list2:
            print "item:",item
            vec = self.get_vec2(item)
            if vec != "None":
                ax.plot( vec[0], vec[1], 'bo')
                plt.text( vec[0]+0.01, vec[1]+0.01, item)

        ax.set_title('sentiment words(Google pretrained + yelp corpus)')
        plt.savefig('sentiment_words(Google_pretrained_and_yelp_corpus)')

if __name__ == '__main__':
    plot = Plot()
    plot.render()
