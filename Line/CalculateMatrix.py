from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import numpy as np
import sys
import json
import uuid
import re

class CalculateMatrix:

    def __init__(self):
        self.src = sys.argv[1]
        self.source = open(self.src)
        self.dim200 = []
        self.cosine_matrix = []
        self.dot_matrix = []

    def cosineMatrix(self):
        f = self.source

        "the first line of file is the unique word number and the dimenstion number. use the next() to skip it."
        next(f)

        for line in f:
            vector200 = [float(num) for num in line.split(" ")[1:-1]]
            self.dim200.append(vector200)

        A = np.array(self.dim200)
        similarities = cosine_similarity(A)
        self.cosine_matrix = similarities.tolist()
        print "length of matrix: ",len(self.cosine_matrix), ", ", len(self.cosine_matrix[0])
        self.cosine_matrix = [NoIndent(vector) for vector in self.cosine_matrix]

        self.dot_matrix = A.dot(A.T).tolist()
        self.dot_matrix = [NoIndent(vector) for vector in self.dot_matrix]

    def render(self):
        filename = sys.argv[1].split("/")
        num = re.search("[0-9]+", filename[5])
        f1 = open( "../data/line-data/cosine_matrix/restaurant_%s_cosine.json"%num.group(0), "w+")
        f1.write(json.dumps( self.cosine_matrix, indent = 4, cls=NoIndentEncoder))
        f1.close()

        f2 = open( "../data/line-data/dot_matrix/restaurant_%s_dot.json"%num.group(0), "w+")
        f2.write(json.dumps( self.dot_matrix, indent=4, cls=NoIndentEncoder))
        f2.close()

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
    matrix = CalculateMatrix()
    matrix.cosineMatrix()
    matrix.render()
