import json
import os
from collections import OrderedDict


class ReviewClassifierWithStars:
    """This program aims to
            1.filter out redundant reviews
            2.classify the reviews of the matched restaurants
        The difference between the previous ReviewClassifier.py wroten by Denffer is this one also take the stars rating of the reviews.
        The purpose of this program is to train the representation of stars."""

    def __init__(self):
        self.src_b = "../../data/business_list.json"
        self.src_r = "../../data/review_list.json"

    def get_business_list(self):

        print "Loading data from:", self.src_b
        with open(self.src_b) as f:
            business_list = json.load(f)

        return business_list

    def get_review_list(self):

        print "Loading data from:", self.src_r
        with open( self.src_r) as f:
            review_list = json.load(f)

        return review_list

    def create_folder(self):
        """ create directory if not found """
        directory = os.path.dirname("../../data/reviews_each_with_stars")
        if not os.path.exists(directory):
            os.makedirs(directory)

    def classify(self):

        self.create_folder()
        review_list = self.get_review_list()
        business_list = self.get_business_list()

        length = len(business_list)
        #fi = open("../../data/business_list.json","r")

        cnt = 0
        for business in business_list:

            f = open("../../data/reviews_each_with_stars/restaurant_%s.json"%(cnt+1), "w+")
            print "Status,", cnt, "/", length, "Sorting reviews in that match business_id",  business["business_id"], "into:", business["business_name"]

            reviews_list = []
            review_count = 0
            for review in review_list:
                if business["business_id"] == review["business_id"]:
                    reviews_list.append({
                        "review_stars" : review["review_stars"],
                        "text" : review["text"]
                        })

            ordered_dict = OrderedDict()
            ordered_dict["index"] = cnt
            ordered_dict["business_id"] = business["business_id"]
            ordered_dict["business_name"] = business["business_name"]
            ordered_dict["reviews"] = review_list

            f.write(json.dumps(ordered_dict, indent=4))
            f.close()
        print "Done"

if __name__ == '__main__':
    classifier = ReviewClassifierWithStars()
    classifier.classify()

