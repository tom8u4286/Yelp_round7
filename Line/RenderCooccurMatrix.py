import numpy as np
import json
import sys
import re
import uuid

class RenderCooccurMatrix:

    def __init__(self):
        self.vec200 = sys.argv[1]
        self.word_list = []
        self.matrix = []
        self.file_num = ""

    def match_and_put(self):

        f = open(self.vec200)
        num = int(f.readline().split(" ")[0])-1
        print "word num:",num

        "putting words into word_list"
        print "putting words into word_list..."
        for line in f :
            lst = line.split(" ")
            self.word_list.append(lst[0])

        self.matrix = np.zeros([num,num])

        "matching"
        print "matching..."
        self.file_num = re.search("[0-9]+", self.vec200.split("/")[5])
        f_cooccur = open("../data/line-data/cooccurrence/restaurant_%s_cooccur.txt"%self.file_num.group(0))
        for line in f_cooccur:
            lst = line.split(" ")
            index1 = self.word_list.index(lst[0])
            index2 = self.word_list.index(lst[1])
            #print type(lst[2])
            self.matrix[index1][index2] = lst[2]
            self.matrix[index2][index1] = lst[2]

    def render(self):
        f = open("../data/line-data/cooccurrence_matrix/restaurant_%s_cooccur_matrix.txt"%self.file_num.group(0), "w+")
        tmp = self.matrix.tolist()
        lst = []
        for vector in tmp:
            lst.append(NoIndent(vector))
        f.write(json.dumps( lst, indent = 4, cls=NoIndentEncoder))
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

if __name__ == '__main__':
    renderCooccur = RenderCooccurMatrix()
    renderCooccur.match_and_put()
    renderCooccur.render()

