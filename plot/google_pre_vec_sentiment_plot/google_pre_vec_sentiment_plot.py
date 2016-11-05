import matplotlib
import matplotlib.pyplot as plt
import json
#import numpy as np


class Plot:

    def __init__(self):
        self.w = "../yelp_minor/unique_words.txt"
        self.vec2 = "../yelp_minor/GoogleNews-vectors-negative2.txt"
        self.psw = '../../data/lexicon/lexicon.json'
        self.ngw = '../../data/lexicon/lexicon-negative.json'

    def get_vec2(self, senti):
        word = open(self.w)

        cnt = 1
        for line in word:
            if senti.encode('utf-8')+'\n' in line:
                break
            cnt +=1

        with open(self.vec2) as f:
            for i,line in enumerate(f):
                if i+1 == cnt:
                    vec = line.replace('\n','')
                    print 'vector:', vec
                    return json.loads(vec)


    def get_lexicon_list(self):
        pos_list = []
        neg_list = []
        with open(self.psw) as f:
            data = json.load(f)
            pos_list = [word['word'] for word in data][:100]
        print pos_list
        with open(self.ngw) as f:
            data = json.load(f)
            neg_list = [word['word'] for word in data][:100]

        return pos_list, neg_list

    def render(self):
        #testing_list = ["great","good", "better", "best", "bad", "worse", "worst", "nice", "nicer", "nicest", ]
        #testing_list2 = [ "astonished", "astonishing", "astonishingly", "awesome", "awesomely", "awesomeness",
        #        "beauty", "beautiful", "beautifully","flexibility", "flexible",
        #        "abundance" ,"abundant",
        #        "acceptable", "acceptance",
        #        "admire", "admirer"]

        testing_list, testing_list2 = self.get_lexicon_list()

        matplotlib.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        ax.set_xlim( -2.0, 1.1)
        ax.set_ylim( -1.5, 1.5)

        for item in testing_list:
            vec = self.get_vec2(item)
            try:
                ax.plot( vec[0], vec[1], 'go')
                plt.text( vec[0]+0.01, vec[1] +0.01, item, fontsize=8)
            except:
                print 'error word:',item

        for item in testing_list2:
            print "item:",item
            vec = self.get_vec2(item)
            try:
                ax.plot( vec[0], vec[1], 'bo')
                plt.text( vec[0]+0.01, vec[1]+0.01, item, fontsize=8)
            except:
                print 'error word:', item
        ax.set_title('sentiment words test')
        plt.savefig('google_pre_sentiment.png')

if __name__ == '__main__':
    plot = Plot()
    plot.render()

