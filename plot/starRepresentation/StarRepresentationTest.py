# -*- coding: utf-8 -*-
import sys, re, json, os, uuid, itertools
from operator import itemgetter
from collections import OrderedDict
#import SpellingChecker #self defined
import unicodedata

class StarRepresentationTest:

    def __init__(self):
        print "Processing", sys.argv[1]
        self.src = sys.argv[1]  # E.g. data/reviews/restaurant_3.json

        "menu is in business_list.json"
        self.src_b = '../../data/business_list.json'

        self.backend_reviews = []
        self.frontend_reviews = []
        self.clean_reviews = []

        self.switch = 0

    def get_review_dict(self):
        #print "Loading data from", self.src
        with open(self.src) as f:
            review_dic = json.load(f)

        return review_dic

    def get_business(self):
        """ match business_id in review_dict with business_list.json """
        review_dic = self.get_review_dict()
        with open(self.src_b) as f:
            business_list = json.load(f)

        for business in business_list:
            if business["business_id"] == review_dic["business_id"]:
                matched_business = business

        return matched_business

    def get_lexicon(self):
        """ return p_list containing dictionaries of positive words """

        positive_list = []
        with open('data/lexicon/lexicon.json') as f:
            lexicon = json.load(f)
            for word_dict in lexicon:
                positive_list.append(word_dict["word"])

        #print positive_list
        return positive_list

    def get_clean_menu(self):
        """ get menu from business_list and return a clean menu"""
        menu = self.get_business()["menu"]
        clean_menu = []

        for dish in menu:
            dish = re.sub("\(.*\)", "", dish)
            dish = dish.replace("(","").replace(")","")
            dish = dish.replace("&", "and").replace("\'", "").replace("*","").replace("-"," ")
            dish = re.sub("(\s)+", " ", dish)
            dish = dish.strip()
            dish = re.sub("(!|@|#|\$|%|\^|\*\:|\;|\.|\,|\"|\'|\\|\/)", r'', dish)

            clean_menu.append(dish)

        #print clean_menu
        return clean_menu

    def get_dishes_regex(self):
        """ dishes_regex is the regular expression for every dish in the dish_list # about to be changed """
        dishes_regex = self.get_clean_menu()

        for i in xrange(len(dishes_regex)):

            dishes_regex[i] = dishes_regex[i].lower()
            dishes_regex[i] = dishes_regex[i].split()
            dishes_regex[i][0]= "(" + dishes_regex[i][0] # adding '(' before the first word

            for word in xrange(len(dishes_regex[i])-1):
                dishes_regex[i][word] += "\\s*"

            for word in xrange(len(dishes_regex[i])-2):
                dishes_regex[i][word] += "|"

            dishes_regex[i][len(dishes_regex[i])-2] = dishes_regex[i][len(dishes_regex[i])-2] + ")+"
            dishes_regex[i] = "".join(dishes_regex[i])[:-1]
            dishes_regex[i] += "[a-z]+(s|es|ies)?"

        #print dishes_regex
        return dishes_regex

    def get_dishes_ar(self):
        """ dishes_ar is the dish_list with every dish 'a'ppending 'r'estaurant_name E.g. dish_restaurant """
        #dishes_ar = self.get_business()['menu']
        dishes_ar = self.get_clean_menu()
        restaurant_name = self.get_business()['business_name']

        for i in xrange(len(dishes_ar)):
            dishes_ar[i] = dishes_ar[i].replace(" ", "-") + "_" + restaurant_name.replace(" ", "-")
            dishes_ar[i] = re.sub("(\s)+", r" ", dishes_ar[i])
            dishes_ar[i] = dishes_ar[i].lower().replace("&", "and").replace("\'", "").replace(".", "").replace(",","")

        #print dishes_ar
        return dishes_ar

    def get_marked_dishes(self):
        """ match the dishes in the reviews and mark the dish"""
        menu = self.get_clean_menu()
        #dishes = self.get_business()["menu"]
        marked_dishes = []

        if self.switch:
            print "\n" + "-"*70
            print "Marking dishes"

        cnt = 0
        length = len(menu)
        for dish in menu:
            cnt += 1
            #dish = re.sub("(!|@|#|\$|%|\^|\&|\*\:|\;|\.|\,|\"|\')", r'', dish)
            dish = dish.lower().replace("&","and").replace("'","").replace(" ","-")
            marked_dishes.append(" <mark>" + dish + "</mark> ")

            if self.switch:
                sys.stdout.write("\rStatus: %s / %s"%(cnt, length))
                sys.stdout.flush()

        return marked_dishes

    def get_clean_reviews(self):
        """ clean reviews """
        raw_reviews = self.get_review_dict()

        if self.switch:
            print "Cleaning reviews"
        cnt = 0
        length = len(raw_reviews)
        clean_reviews = []
        for review in raw_reviews["reviews"]:
            cnt += 1

            text = review["text"]

            text = re.sub(r'https?:\/\/.*[\r\n]*', ' ', text, flags=re.MULTILINE)

            text = text.replace("!"," ! ").replace("@"," @ ").replace("#"," # ").replace("$"," $ ").replace("%"," % ")
            text = text.replace("^"," ^ ").replace("&"," & ").replace("*"," * ").replace("("," ( ").replace(")"," ) ")
            text = text.replace(":"," : ").replace(";"," ; ").replace("."," . ").replace(","," , ").replace("=", " = ")
            text = text.replace("+"," + ").replace("-"," - ").replace("|"," | ").replace("\\"," \ ").replace("/"," / ")
            text = text.replace("~"," ~ ").replace("_", "").replace(">"," > ").replace("<", " < ").replace("?", " ? ")
            text = text.replace("\""," ").replace("[","").replace("]","").replace("{","").replace("}","")

            #text = re.sub("(!|@|#|\$|%|\^|\&|\*|\(|\)|\:|\;|\.|\,|\?|\")", r' \1 ', text)

            text = re.sub(r"'m", " am", text)
            text = re.sub(r"'re", " are", text)
            text = re.sub(r"'s", " is", text)
            text = re.sub(r"'ve", " have", text)
            text = re.sub(r"'d", " would", text)
            text = re.sub(r"n't", " not", text)
            text = re.sub(r"'ll", " will", text)

            text = text.replace("\'"," ")

            #Remove accents
            text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')

            #porterStemmer # but may lose information

            text = re.sub("(\\n)+", r" ", text)
            text = re.sub("(\s)+", r" ", text)

            text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text)) # sooo happppppy -> so happy
            #text = ' '.join(SpellingChecker.correction(word) for word in text.split())
            review["text"] = text
            clean_reviews.append(review)

            if self.switch:
                sys.stdout.write("\rStatus: %s / %s"%(cnt, length))
                sys.stdout.flush()

        return clean_reviews

    def get_frontend_review_dict_list(self):

        frontend_reviews = list(self.clean_reviews)
        dishes = self.get_clean_menu()
        dishes_regex = self.get_dishes_regex()
        marked_dishes = self.get_marked_dishes()

        if self.switch:
            print "\n" + "-"*70
            print "Processing frontend reviews"

        frontend_review_dict_list = []
        length1 = len(marked_dishes)
        for i in xrange(len(marked_dishes)):
            length2 = len(frontend_reviews)
            for j in xrange(len(frontend_reviews)):
                frontend_reviews[j] = frontend_reviews[j]
                frontend_reviews[j] = re.sub("\\n+", r" ", frontend_reviews[j])

                """ Replacing | E.g. I love country pate. -> I love <mark>housemade country pate</mark>. """
                frontend_reviews[j] = re.sub(dishes_regex[i], marked_dishes[i], frontend_reviews[j], flags = re.IGNORECASE)

                if self.switch:
                    sys.stdout.write("\rStatus: %s / %s | %s / %s"%(i+1, length1, j+1, length2))
                    sys.stdout.flush()

            reviews = []
            for k in xrange(len(frontend_reviews)):
                if marked_dishes[i] in frontend_reviews[k]:
                    frontend_reviews[k] = frontend_reviews[k].replace("-"," ")

                    frontend_reviews[k] = frontend_reviews[k].replace(" ! ","! ").replace(" @ ","@ ").replace(" # ","# ").replace(" $ ","$ ").replace(" % ","% ")
                    frontend_reviews[k] = frontend_reviews[k].replace(" ^ ","^ ").replace(" & ","& ").replace(" * ","* ").replace(" ( ","( ").replace(" ) ",") ")
                    frontend_reviews[k] = frontend_reviews[k].replace(" : ",": ").replace(" ; ","; ").replace(" . ",". ").replace(" , ",", ").replace(" = ", "= ")
                    frontend_reviews[k] = frontend_reviews[k].replace(" + ","+ ").replace(" - ","- ").replace(" | ","| ")
                    frontend_reviews[k] = frontend_reviews[k].replace(" ~ ","~ ").replace(" > ","> ").replace(" < ", "< ").replace(" ? ", "? ")
                    frontend_reviews[k] = re.sub("(\s)+", r" ", frontend_reviews[k])

                    reviews.append(frontend_reviews[k])

                if self.switch:
                    sys.stdout.write("\rStatus: %s / %s | %s / %s"%(i+1, length1, k+1, length2))
                    sys.stdout.flush()

            frontend_review_dict_list.append({"dish_name": dishes[i], "reviews": reviews})

        return frontend_review_dict_list

    def get_backend_reviews(self):
        """ match the dishes in the reviews with dishes_regex and replace them with the dishes in dishes_ar  """

        backend_reviews = list(self.clean_reviews)
        dishes_regex = self.get_dishes_regex()
        dishes_ar = self.get_dishes_ar()

        if self.switch:
            print "\n" + "-"*70
            print "Processing backend_reviews"

        length1 = len(backend_reviews)
        for i in xrange(len(backend_reviews)):
            length2 = len(dishes_regex)
            for j in xrange(len(dishes_regex)):
                backend_reviews[i]["text"] = backend_reviews[i]["text"].lower()
                """ Replacement | E.g. I love country pate. -> I love housemade-country-pate_mon-ami-gabi. """
                backend_reviews[i]["text"] = re.sub(dishes_regex[j], str(backend_reviews[i]["review_stars"])+"stars", backend_reviews[i]["text"], flags = re.IGNORECASE)
                backend_reviews[i]["text"] = re.sub("(\s)+", r" ", backend_reviews[i]["text"])

                if self.switch:
                    sys.stdout.write("\rStatus: %s / %s | %s / %s"%(i+1, length1, j+1, length2))
                    sys.stdout.flush()

        return backend_reviews

    def get_restaurant_dict(self):
        """ match backend_review_list with dish_ar count the frequnecy of every dish"""

        business = self.get_business()
        #backend_reviews = self.get_backend_reviews()
        dishes_ar = self.get_dishes_ar()

        if self.switch:
            print "\n" + "-"*70
            print "Processing restaurant_dict"

        count_list = []
        count = 0
        """ counting the frequencies of dish in reviews"""
        cnt = 0
        length = len(dishes_ar)
        for dish in dishes_ar:
            cnt += 1
            for review in self.backend_reviews:
                count += review["text"].count(dish)
            count_list.append(count)
            count = 0

            if self.switch:
                sys.stdout.write("\rStatus: %s / %s"%(cnt, length))
                sys.stdout.flush()

        menu = self.get_clean_menu()
        """ sorted by count """
        i = 0
        dish_dict_list = []
        for i in xrange(len(menu)):
            dish_dict = {"count": count_list[i], "name": menu[i], "name_ar": dishes_ar[i]}
            i += 1
            dish_dict_list.append(dish_dict)
        dish_dict_list = sorted(dish_dict_list, key=itemgetter('count'), reverse = True)

        index = 0
        processed_menu = []
        for dish_dict in dish_dict_list:
            index += 1
            orderedDict = OrderedDict()
            orderedDict["index"] = index
            orderedDict["count"] = dish_dict["count"]
            orderedDict["name"] = dish_dict["name"]
            orderedDict["name_ar"] = dish_dict["name_ar"]
            orderedDict["x"] = 0
            orderedDict["y"] = 0

            processed_menu.append(NoIndent(orderedDict))

        business["menu"] = processed_menu
        restaurant_dict = business

        return restaurant_dict

    def get_statistics(self):
        """ count the sentiment word in reviews """
        #backend_reviews = self.get_backend_reviews()
        positive_list = self.get_lexicon()

        if self.switch:
            print "\n" + "-"*70
            print "Processing statistics"

        statistics = []
        index_cnt = 0
        length = len(positive_list)

        for word in positive_list:
            index_cnt += 1
            dish_count = 0
            for review in self.backend_reviews:
                dish_count += review.count(" " + word + " ")
            orderedDict = OrderedDict()
            orderedDict["index"] = index_cnt
            orderedDict["word"] = word
            orderedDict["count"] = dish_count
            statistics.append(NoIndent(orderedDict))

            if self.switch:
                sys.stdout.write("\rStatus: %s / %s"%(index_cnt, length))
                sys.stdout.flush()

        return statistics

    def create_dirs(self):
        """ create the directory if not exist"""
        dir1= os.path.dirname("../../data/backend_reviews_dish_change_to_stars/")

        if not os.path.exists(dir1):
            print "creating dir"
            os.makedirs(dir1)

    def render(self):
        """ render backend_reviews_dish_change_to_stars"""

        business = self.get_business()
        self.clean_reviews = self.get_clean_reviews()
        self.backend_reviews = self.get_backend_reviews()
        restaurant_dict = self.get_restaurant_dict()

        self.create_dirs()

        if self.switch:
            print "\n" + "-"*70
            print "Rendering"

        filename = sys.argv[1][46]
        if sys.argv[1][47] != ".":
            filename = filename + sys.argv[1][47]
            if sys.argv[1][48] != ".":
                filename = filename + sys.argv[1][48]

        total_review_count = len(self.clean_reviews)

        """ render restaurant_*.json in ./backend_reviews_dish_change_to_stars """
        backend_txt = open("../../data/backend_reviews_dish_change_to_stars/restaurant_%s.txt"%(filename), "w+")
        for review in self.backend_reviews:
            backend_txt.write(review["text"].encode("utf-8") + '\n')
        backend_txt.close()

        print sys.argv[1], "'s backend json is completed"



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

if  __name__ == '__main__':
    parser = StarRepresentationTest()
    parser.render()
