import json, sys, uuid, math, glob, scipy, os
import numpy as np
from scipy.spatial import distance
from json import dumps, loads, JSONEncoder, JSONDecoder
from operator import itemgetter
from collections import OrderedDict

class PostProcess:

    def render(self):
        tmp = np.array([[0.0,0.0,0.0,0.0],[1.1,1.1,1.1,1.1],[2.2,2.2,2.2,2.2],[3.3,3.3,3.3,3.3]])
        tmp.tolist()
        lst = []
        for vector in tmp:
            lst.append(NoIndent(vector))

        f = open("test.json", "w+")
        f.write(json.dumps(lst, indent=4, cls=NoIndentEncoder))
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
    postProcess = PostProcess()
    postProcess.render()
