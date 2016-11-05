import json
import matplotlib
import matplotlib.pyplot as plt

class RestaurantTest:

    def __init__(self):
        print "start"
        self.src = "../data/website_word2vec/frontend_restaurant_dict_list.json"
        self.vec2 = "../data/coreProcess_word2vec/vector2_word2vec.txt"
        self.w = "../data/coreProcess_word2vec/unique_words_word2vec.txt"

    def render(self):

        with open(self.src) as f:
            rest_dict_list = json.load(f)

        matplotlib.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        #ax.set_xlim( -1, 1)
        #ax.set_ylim( -1, 1)

        for rest in rest_dict_list:
            if rest["index"] == 1:
                print "restaurant:",rest["restaurant_name"]
                ax.set_title( rest["restaurant_name"])
                for dish in rest["top5_euclidean_min"]:
                    ax.plot(dish["x"], dish["y"] , "bo")

                    plt.text(dish["x"], dish["y"], dish["name"])

        plt.show()


if __name__ == "__main__":
    rest = RestaurantTest()
    rest.render()
