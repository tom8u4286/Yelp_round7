import sys, re
import time
from nltk.stem.snowball import SnowballStemmer

start_time = time.time()

"""load the review file. backend_reviews/restaurant_1.txt"""
review_f = open(sys.argv[1])
review_list = [review for review in review_f]
review_list_length = len(review_list)

"""load the lexiconfile. lexicon/stanfer/positive.txt"""
pos_f = open("../data/lexicon/stanfer/positive.txt")

pos_list = [word.strip("\n") for word in pos_f]

words_length = len(pos_list)
matched_cnt = 0
review_cnt = 0
new_reviews_list = []
for review in review_list:
    review_cnt += 1
    new_review = review
    word_cnt = 0
    for word in pos_list:
        word_cnt += 1
        word_senti = " "+word+"_senti "
        if "_" in word:
            word = word.replace("_", " ")
            word = " "+ word+ " "
        elif "-" in word:
            word = word.replace("-", " ")
            word = " "+ word+ " "
        else:
            word = " "+ word+ " "

        if word in review:
            new_review = new_review.replace( word, word_senti)
            matched_cnt += 1
        sys.stdout.write("\rtotally matched: %s, reviews: %s / %s, uni_words: %s / %s  "%(matched_cnt, review_cnt, review_list_length, word_cnt, words_length))
    new_reviews_list.append(new_review)


print "\nmatched count: %s"%matched_cnt

"""Write the new list to file."""
print "Start writing file..."
rest_num = re.search('[0-9]+',sys.argv[1]).group(0)
new_f = open("../data/backend_reviews_senti_stemmed/restaurant_%s_senti_stemmed.txt"%rest_num, 'w+')
for item in new_reviews_list:
    new_f.write("%s"%item)
new_f.close()

print "Total time: %s"%(time.time()- start_time)
print "Done."


