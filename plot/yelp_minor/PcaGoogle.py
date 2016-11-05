import json
import numpy as np
from sklearn import decomposition


class PcaGoogle:

    def __init__(self):
        self.src = "./GoogleNews-vectors-negative300.txt"
        self.dst_vec2 = "./GoogleNews-vectors-negative2.txt"

    def get_vectors300(self):

        vectors300 = []
        uniquewords = []
        failed = []
        with open(self.src) as f:
            for line in f:
                line = line.replace('"',"")
                line = line.replace( ' ' , '",' ,1)
                line = line.replace( ' ' , ',' )
                line = '["' + line + ']'

                try:
                    tmp = json.loads( line )
                    print tmp[0]
                    uniquewords.append( tmp.pop(0) )
                    vectors300.append( tmp )
                except:
                    failed.append( tmp.pop(0) )
        vectors300.pop(0)

        print "failed list:"
        print failed

        return vectors300

    def get_reduction(self):

        source = self.get_vectors300()

        print "performing reduction by pca"
        pca = decomposition.PCA(n_components=2)
        pca.fit(source)
        vectors2 = pca.transform(source).tolist()

        return vectors2

    def render(self):

        vectors2 = self.get_reduction()

        print "Writing data to:", self.dst_vec2

        f = open(self.dst_vec2, 'w+')
        for vector in vectors2:
            f.write( str(vector) + '\n')

if __name__ == '__main__':
    pca = PcaGoogle()
    pca.render()
