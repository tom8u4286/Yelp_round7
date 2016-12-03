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
        """the first line of vec200 file is the number of unique words count."""
        num = int(f.readline().split(" ")[0])
        print "word num:", num

        "putting words into word_list from vec200 words"
        print "putting words into word_list..."
        for line in f :
            lst = line.split(" ")
            self.word_list.append(lst[0])

        print "lenght of word_list(line rendered):", len(self.word_list)

        self.matrix = np.zeros([num,num])

        "matching"
        print "matching..."
        self.file_num = re.search("[0-9]+", self.vec200.split("/")[5])
        f_cooccur = open("../data/line-data/cooccurrence/restaurant_%s_cooccur.txt"%self.file_num.group(0))

        #test_list = []
        #for line in f_cooccur:
        #    lst = line.split(" ")
        #    if lst[0] not in test_list:
        #        test_list.append(lst[0])
        #    if lst[1] not in test_list:
        #        test_list.append(lst[1])
        #print "the length of restaurant_1_cooccur.txt unique words(I counted): ",len(test_list)

        length = 1406266
        index_cnt = 0
        word = []
        for line in f_cooccur:
            index_cnt += 1
            lst = line.split(" ")
            try:
                index1 = self.word_list.index(lst[0])
                index2 = self.word_list.index(lst[1])
                #print type(lst[2])
                print "index1: ", index1, " index2: ", index2
                self.matrix[index1][index2] = lst[2]
                #self.matrix[index2][index1] = lst[2]
            except:
                word.append(lst[0])
                word.append(lst[1])
            #sys.stdout.write("Status: %s / %s"%(index_cnt, length))
            #sys.stdout.flush()

        print word

    def file_length(self, f):
        print "Counting file length..."
        for i, l in enumerate(f):
            pass
        return i + 1

    def render(self):
        f = open("../data/line-data/cooccurrence_matrix/restaurant_%s_cooccur_matrix.txt"%self.file_num.group(0), "w+")
        tmp = self.matrix.tolist()
        lst = []
        print len(tmp[0])
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

