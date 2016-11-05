###This program aims to find the dishes in the highest cosAvg list but both in the least eucAvg list.###


import json
import uuid

class ScoreTest:

    def __init__(self):
        self.src = "../../data/postProcess_word2vec/processed_restaurant_dict_list.json"
        self.dst = "./dishes_list.json"

    def get_data(self):
        f = open(self.src)
        rest_dict = json.load(f)

        all_rest = []
        for rest in rest_dict:
            problem_dishes = {}
            problem_dishes['restaurant_name'] = rest['restaurant_name']
            problem_dishes['menu_length'] = rest['menu_length']
            problem_dishes['problem_list'] = []

            percent25 = int( rest['menu_length'] * 0.25 )
            percent75 = int( rest['menu_length'] * 0.75 )

            cosAvg_less25 = sorted(rest['menu'], key=lambda k: k['cosine_avg_score'])[:percent25]
            #print 'cosAvg_less25:',len(cosAvg_less25)
            eucAvg_more75 = sorted(rest['menu'], key=lambda k: k['euclidean_avg_score'])[percent75:]
            #print 'eucAvg_less75:',len(eucAvg_more75)

            problem_dishes['cosAvg_less25'] = sorted([dish['name'] for dish in cosAvg_less25])
            problem_dishes['eucAvg_more75'] = sorted([dish['name'] for dish in eucAvg_more75])

            rank = 1
            for dish in cosAvg_less25:
                dish['rank'] = rank
                rank+=1

            rank = 1
            for dish in eucAvg_more75:
                dish['rank'] = rank
                rank+=1

            for dish_cos in cosAvg_less25:
                for dish_euc in eucAvg_more75:
                    if dish_cos['index'] == dish_euc['index']:
                        problem_dish = { 'dish' : dish_euc['name'],
                                'dish_cos_index': dish_cos['rank'],
                                'dish_euc_index': dish_euc['rank'] }
                        problem_dishes['problem_list'].append(problem_dish)
            all_rest.append(problem_dishes)

        for rest in all_rest:
            rest['eucAvg_more75'] = NoIndent(rest['eucAvg_more75'])
            rest['cosAvg_less25'] = NoIndent(rest['cosAvg_less25'])

        with open(self.dst,'w+') as f:
            f.write( json.dumps( all_rest, indent = 4, cls=NoIndentEncoder))

class NoIndent(object):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        if not isinstance(self.value, list):
            return repr(self.value)
        else:  # the sort the representation of any dicts in the list
            reps = ('{{{}}}'.format(', '.join(('{!r}:{}'.format(k, v) for k, v in sorted(v.items()))))
                if isinstance(v, dict) else repr(v) for v in self.value)
            return '[' + ', '.join(reps) + ']'

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
            return super( NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super( NoIndentEncoder, self).encode(o)
        for k, v in self._replacement_map.iteritems():
            result = result.replace('"@@%s@@"' % (k,), v)
        return result

if __name__ == '__main__':
    test = ScoreTestPlot()
    test.get_data()
